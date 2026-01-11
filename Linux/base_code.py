#!/usr/bin/env python3

import re
import urllib.request
import datetime
from html import unescape

# nice formatting for output
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
    # i only have rejected/accepted urls to test so idk if
    # the others work yet
    "rejected": "Rejected",
    "accepted": "🎉Accepted🎉",
    "revisionrequested": "Revision Requested",
    "withdrawn": "Withdrawn",
    "inprogress": "In Progress",
}

"""
Additional moksha statuses (that are probably backend-only, but storing
here in case they might be of use later):
Open, Closed, Archived, Claimed, File Error, Needs Second Opinion,
Not recommended, Recommended, Unclaimed
"""


# turns array into string
def delister(list):
    return "".join(list)


# puts whitespaces back into market name
# it a'int perfect but it's close
def despacer(name):
    return re.sub(r"(?<=[a-z])([A-Z])", r" \1", name)


# read all old entries and turn into array
try:
    o = open(file="moksha_output", mode="r")
    previous_entries = o.readlines()
    o.close()
    history = True
except FileNotFoundError:
    print("No history found")
    previous_entries = []
    history = False


# finds last instance script ran + saves results into list
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
    # converts list into dict cause i couldnt get it to work otherwise
    x = 0
    for x in range(0, len(last_checked_markets)):
        prev_dict[last_checked_markets[x][0]] = [
            last_checked_markets[x][1],
            last_checked_markets[x][-1],
        ]


# opens/creates output file for results w/timestamp
o = open(file="moksha_output", mode="a+")
o.write(f"{datetime.datetime.now()}\n{separator}\n")
o.write(
    "%-24s %-14s %-9s %-9s %-14s\n"
    % (header[0], header[1], header[2], header[3], header[4])
)
o.write(f"{'.' * table_width}\n")

# prints header for terminal
print(
    "%-24s %-14s %-9s %-9s %-14s"
    % (header[0], header[1], header[2], header[3], header[4])
)
print(f"{'.' * table_width}")

# inits for the core loop
i = 0
x = 0
market = ""
sub_status = ""
pos_difference = 0
sub_uid = ""

for i in range(len(url_array)):
    pos_difference = 0
    x = 0
    # opens/closes URL and saves as string
    fp = urllib.request.urlopen(url_array[i])
    my_bytes = fp.read()
    html_str = my_bytes.decode("utf8")
    fp.close()
    # strips out whitespace from webpage
    html_str = html_str.strip()
    html_str = html_str.replace(" ", "")
    html_str = html_str.replace("\t", "")
    html_str = html_str.replace("\n", "")
    # find/save/format market name
    market = re.findall(market_pattern, html_str)
    market = delister(market)
    if "&" in market:
        market = unescape(market)
    market = despacer(market)
    if len(market) > 24:
        market = f"{market[0:21]}..."
    # looks for queue position
    sub_status = re.findall(queue_pattern, html_str)
    # runs if no digits (i.e. closed sub or market doesn't share positions)
    # find/save/format sub status
    if sub_status == []:
        sub_status = object = re.findall(status_pattern, html_str)
        sub_status = delister(sub_status)
        sub_status = results[sub_status]
    else:
        sub_status = delister(sub_status)
        if ord(sub_status[0]) in range(48, 60):
            sub_status = int(sub_status)
    # find/save uid
    sub_uid = re.findall(uid_pattern, url_array[i])
    sub_uid = delister((sub_uid))
    sub_uid = sub_uid + " "
    # find in prev outputs and find position movement
    if market in prev_dict and prev_dict[market][1] == sub_uid:
        if isinstance(sub_status, int):
            try:
                pos_difference = int(prev_dict[market][0]) - int(sub_status)
            except ValueError:
                pos_difference = 0
    # find/save length and avg length
    length = re.findall(days_pattern, html_str)
    length = delister(length)
    if length == "":
        length = "-"
    avg_length = re.findall(avg_pattern, html_str)
    avg_length = delister(avg_length)
    if avg_length == "":
        avg_length = "-"
    # var for difference from average
    try:
        day_diff = -1 * (int(avg_length) - int(length))
        if day_diff > 0:
            day_diff = f"(+{day_diff})"
        else:
            day_diff = f"({day_diff})"
    except ValueError:
        day_diff = " - "
    # print results to terminal
    print(
        f"{market:<25}{sub_status:<15}{length:<10}{avg_length:<3} {day_diff:<7}{13 * '*'}"
    )
    if pos_difference != 0:
        print(f"Change: {(pos_difference):>19}")
    # writes results to output file
    o.write(
        f"{market:<25}{sub_status:<15}{length:<10}{avg_length:<3} {day_diff:<7}{sub_uid:<14}\n"
    )
    if pos_difference != 0:
        o.write(f"Change: {(pos_difference):>19}\n")

# closes output file
o.write("\n")
o.close()
