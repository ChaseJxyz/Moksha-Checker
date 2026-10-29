#!/usr/bin/env python3
import os
import re
import glob
import time
import datetime
import subprocess
import shutil
from html import unescape

# =====================================================================
# 1. Get the latest cookie file in the Downloads folder
# =====================================================================
downloads_dir = os.path.expanduser("~/Downloads")
cookie_files = glob.glob(os.path.join(downloads_dir, "moksha.io_cookies*.txt"))

if not cookie_files:
    print("No cookie found. You need a cookie to bypass Anubis.")
    exit(0)

# Sort by creation time (newest first)
cookie_file = max(cookie_files, key=os.path.getctime)
file_name = os.path.basename(cookie_file)
#print(f"File name: {file_name}")

# =====================================================================
# 2. Check Expiration & Build Raw Cookie Header
# =====================================================================
current_time = int(time.time())
cookie_str_parts = []

print("Cookie status:")
with open(cookie_file, "r") as f:
    for line in f:
        line = line.strip()
        # Handle HttpOnly prefixes which curl ignores sometimes
        if line.startswith("#HttpOnly_"):
            line = line[10:]
            
        if not line or line.startswith("#"):
            continue
        
        parts = line.split("\t")
        if len(parts) >= 7:
            name = parts[5]
            value = parts[6].strip()
            cookie_str_parts.append(f"{name}={value}")
            
            try:
                expiration = int(parts[4])
            except ValueError:
                continue
            
            if expiration == 0:
                print(f"Cookie '{name}' is NOT EXPIRED (Session cookie).")
                continue
            
            if expiration < current_time:
                print(f"{name} has EXPIRED.")
                exit(0)
            else:
                diff = expiration - current_time
                days = diff // 86400
                hours = (diff % 86400) // 3600
                print(f"{name} is GOOD. It expires in {days} days, {hours} hours.")

# This manually aggregates all cookies to bypass strict domain rules in curl
raw_cookie_header = "; ".join(cookie_str_parts)

# =====================================================================
# 3. moksha_checker.py logic
# =====================================================================
table_width = 75
separator = "-" * table_width
header = ["Market", "Position", "Days", "Avg. Days", "ID"]

# opens file with 1 moksha url per line + converts into array
try:
    f = open("moksha_URLS")
    raw_urls = f.read()
    f.close()
    url_array = raw_urls.split()
except FileNotFoundError:
    print(
        "Please make a URL file! Otherwise this has nothing to do :)\n1. Open up notepad and paste in your Moksha URLs (one per line)\n2. Save it as `moksha_URLS` (in the same folder as this script)\n3. If your OS forces you to have a file extension, open up *this* file (the .py) in your text editor, ctrl + F `moksha_URLS`and add the extension to the try in this code block (and save the .py, of course!)\n4. Rerun this script, and it should work!"
    )
    quit()

# regex for finding vars of interest
queue_pattern = r"(?<=QueuePosition<\/th><td>)\d+"
market_pattern = r"(?<=SubmissionStatus-)(.*?)\|"
status_pattern = r"(?<=<th>Status<\/th><td>)\w+"
days_pattern = r"(?<=DaysUnderReview<\/th><td>)\d+"
avg_pattern = r"(?<=<th>ResponseTimeAverage<\/th><td>)\d+"
uid_pattern = r"(?<=uid\=)\S+"

# dict for prettifying results
results = {
    "rejected": "Rejected",
    "accepted": "🎉Accepted🎉",
    "revisionrequested": "Revision Requested",
    "withdrawn": "Withdrawn",
    "inprogress": "In Progress",
}

def delister(lst):
    return "".join(lst)

def despacer(name):
    return re.sub(r"(?<=[a-z])([A-Z])", r" \1", name)

try:
    o = open(file="moksha_output", mode="r")
    previous_entries = o.readlines()
    o.close()
    history = True
except FileNotFoundError:
    print("No history found")
    previous_entries = []
    history = False

last_checked_index = 0
last_checked_markets = []
prev_dict = {}

if history:
    for index, element in reversed(list(enumerate(previous_entries))):
        if element[0:3] == "---":
            last_checked_index = index + 3
            break
    for element in range(last_checked_index, len(previous_entries)):
        temp = previous_entries[element]
        temp = temp.strip("\n")
        temp = re.split(r'[" "]{2,}', temp)
        if temp[0] == "":
            continue
        elif temp[0] == "Change:":
            continue
        else:
            try:
                if temp[1][1] in [0 - 9]:
                    temp[1] = int(temp[1])
                last_checked_markets.append(temp)
            except IndexError:
                continue
    for x in range(0, len(last_checked_markets)):
        prev_dict[last_checked_markets[x][0]] = [
            last_checked_markets[x][1],
            last_checked_markets[x][-1],
        ]

o = open(file="moksha_output", mode="a+")
o.write(f"{datetime.datetime.now()}\n{separator}\n")
o.write(
    "%-24s %-14s %-9s %-9s %-14s\n"
    % (header[0], header[1], header[2], header[3], header[4])
)
o.write(f"{'.' * table_width}\n")

print("")
print(
    "%-24s %-14s %-9s %-9s %-14s"
    % (header[0], header[1], header[2], header[3], header[4])
)
print(f"{'.' * table_width}")

i = 0
x = 0
market = ""
sub_status = ""
pos_difference = 0
sub_uid = ""

for i in range(len(url_array)):
    pos_difference = 0
    x = 0
    
    # Passing BOTH -H and -b ensures cookies are sent even if domains mismatch (like techaro.lol vs moksha.io)
    # Added --compressed so curl decompresses gzip bytes into readable HTML text
    try:
        result = subprocess.run([
            "/usr/local/bin/curl-impersonate-ff", "-s", "-L", "--compressed", "--location-trusted",
            url_array[i],
            "-H", f"Cookie: {raw_cookie_header}",
            "-b", cookie_file
        ], capture_output=True, check=True)
        html_str = result.stdout.decode('utf-8', errors='ignore')
    except subprocess.CalledProcessError as e:
        print(f"{'Curl Error':<25}{'-':<15}{'-':<10}{'-':<3} {'-':<7}{13 * '*'}")
        continue

    html_str = html_str.strip()
    html_str = html_str.replace(" ", "")
    html_str = html_str.replace("\t", "")
    html_str = html_str.replace("\n", "")
    html_str = html_str.replace("\r", "")
    
    market = re.findall(market_pattern, html_str)
    
    # Graceful error catching if HTML structure is broken or blocked
    if not market:
        if "ThiswebsiteisrunningAnubisversion" in html_str:
            print(f"{'Blocked by Anubis':<25}{'-':<15}{'-':<10}{'-':<3} {'-':<7}{13 * '*'}")
        elif "login" in html_str.lower():
            print(f"{'Blocked by Login':<25}{'-':<15}{'-':<10}{'-':<3} {'-':<7}{13 * '*'}")
        elif not html_str:
            print(f"{'Empty Response':<25}{'-':<15}{'-':<10}{'-':<3} {'-':<7}{13 * '*'}")
        else:
            print(f"{'Parse Error':<25}{'-':<15}{'-':<10}{'-':<3} {'-':<7}{13 * '*'}")
        continue

    market = delister(market)
    if "&" in market:
        market = unescape(market)
    market = despacer(market)
    if len(market) > 24:
        market = f"{market[0:21]}..."
        
    sub_status = re.findall(queue_pattern, html_str)
    if sub_status == []:
        sub_status = re.findall(status_pattern, html_str)
        sub_status = delister(sub_status)
        if sub_status in results:
            sub_status = results[sub_status]
    else:
        sub_status = delister(sub_status)
        if sub_status and ord(sub_status[0]) in range(48, 60):
            sub_status = int(sub_status)
            
    sub_uid = re.findall(uid_pattern, url_array[i])
    sub_uid = delister(sub_uid)
    sub_uid = sub_uid + " "
    
    if market in prev_dict and prev_dict[market][1] == sub_uid:
        if isinstance(sub_status, int):
            try:
                pos_difference = int(prev_dict[market][0]) - int(sub_status)
            except ValueError:
                pos_difference = 0
                
    length = re.findall(days_pattern, html_str)
    length = delister(length)
    if length == "":
        length = "-"
    avg_length = re.findall(avg_pattern, html_str)
    avg_length = delister(avg_length)
    if avg_length == "":
        avg_length = "-"
        
    try:
        day_diff = -1 * (int(avg_length) - int(length))
        if day_diff > 0:
            day_diff = f"(+{day_diff})"
        else:
            day_diff = f"({day_diff})"
    except ValueError:
        day_diff = " - "
        
    print(
        f"{market:<25}{sub_status:<15}{length:<10}{avg_length:<3} {day_diff:<7}{13 * '*'}"
    )
    if pos_difference != 0:
        print(f"Change: {(pos_difference):>19}")
        
    o.write(
        f"{market:<25}{sub_status:<15}{length:<10}{avg_length:<3} {day_diff:<7}{sub_uid:<14}\n"
    )
    if pos_difference != 0:
        o.write(f"Change: {(pos_difference):>19}\n")

o.write("\n")
o.close()
