# Intro

Are you sick and tired of having to write down your last known position in a moksha queue? Annoyed that you have 10 different pages you need to refresh to see if you've moved? There's got to be a better way!

The creatively named moksha_checker script looks at these webpages for you and returns only the information you care about (i.e your position in line, and how long you've been waiting compared to the average wait time). If you use the script more than once, it "remembers" your position, and will report if you've moved up, and by how many spots. If the status has changed (like a rejection or acceptance), it returns this instead of your number in line.

It's set up so that it'll work if you have multiple submissions at the same market (both at the same time, and over time). If you no longer want a submission to be checked (like if it's no longer under consideration), simply delete its URL from the URL file.

This has only been tested/set up for (Ubuntu-based) Linux, Windows 10/11, and ~~MacOS~~ (eventually). If you're running something else (iOS, Android, RedStar) idk what to tell you you'll have to figure it out yourself. But it should *probably* work for all the other Linux distro families, older versions of Windows, etc.

# How it works

Simply: you put your submission status URL into a file and run the script (exactly how depends on your OS). The script goes through the URLs one at a time, opens the web page, looks for specific information, and then prints it to the terminal. It also writes this information to an output file, so it can know if you've moved up in line.

For more specifics: It opens the URL file and saves each in an array (or returns an error code if it's not found). It does the same for the history file (which, if found, then saves them into a dictionary). The output file is opened (or made, if it doesn't exist), and it receives (mostly) the same information that gets printed to the terminal.

For each entry in the URL array, the webpage at the URL is saved to the heap and a regex search looks for the market name, submission status, the length it's been open, and the average length. The sub's UID is read from the URL itself. Some basic math is done to compare this new data to the historic data, as well as the two length values, and this is output for the user. Everything closes nicely once it's finished.

# How to use

Specifics are within each folder, for each major OS. The easiest thing you can do is download the zip file within the folder for your OS, unzip it, and then follow the instructions inside.

The core script is in Python, so you need it installed on your computer for it to run. You can download it [straight from the source](https://www.python.org/downloads/) or from your favorite software source (apt homebrew Windows store etc.). It only uses standard modules, so you won't need to install anything else.

You can either run the python script itself (in your IDE of choice or etc.) or run the nice moksha_checker script (by double clicking, probably). The code is set up that all the files are within the same folder, so *please* do not move the individual files around (but you can move the parent folder wherever you please).

I've designed the output to be pretty self-evident, but here's some example output (from the file), and an explanation:

```
2026-01-09 14:12:11.232686
---------------------------------------------------------------------------
Market                   Position       Days      Avg. Days ID            
...........................................................................
Bourbon Penn             In Progress    0         30  (-30)  XXXXXXXXXXXXX 
Castof Wonders           Rejected       -         -    -     XXXXXXXXXXXXX 
Tales&Feathers Magazine  26             160       111 (+49)  XXXXXXXXXXXXX 
Change:                   1
Pod Castle               139            25        25  (0)    XXXXXXXXXXXXX 
Cosmic Horror Monthly... 106            7         10  (-3)   XXXXXXXXXXXXX 
Pod Castle               298            7         25  (-18)  XXXXXXXXXXXXX 
Change:                  24
```

1. Timestamp - For your convenience. Only written to output file.
2. Market - The name of the magazine/podcast/journal/etc. May not reflect the specific submission window ("special novella call) and probably won't be perfectly formatted. If the name is too long, it'll be shortened (so all the output is formatted nicely)
3. Position - Your number in line, or status. Some markets don't show numbers, just that it's still "In Progress," which would be showed instead. If the submission has been rejected (or accepted, or withdrawn), that will be shown instead.
4. Days - The number of days the submission has been open.
5. Avg. Days - The market-reported average time submissions are open before they get a response. This is then followed by how above/below the average you are.
6. ID - Each submission has a unique UID, which allows users to have multiple submissions to the same market but have different URLs. This is captured by the script and saved to the output file to ensure that checks are for the same submission. This is obfuscated in the terminal printout (and I obfuscated my own here with Xs, but you would see your own)
7. Change - The difference between your last recorded position and your current position. This will only show up if there's been a difference (theoretically, if you've moved *backwards*, this number would be a negative...but idk if that's even possible)


# Troubleshooting

### The URLs aren't being read!

You need to be connected to the internet, of course, but the most likely culprit is the URL file isn't properly formatted. You should ONLY have the URLs in the file, separated by hitting enter so there's one per line. No comments or notes to yourself or etc. The URL needs to be the page where you can look at your submission status. This is what's emailed to you by moksha when you make a submission.

### It's not saying I'm moving up in line?

The script compares the number to the last time you ran it (which is recorded in the output file). If you moved, renamed, or deleted the output file (or have never run the script before), it won't be able to find it. If there has been no change between the last check and the one you just ran, it won't print out a 0, just report the number in line.

### What if I want this to run automatically? What if I want email alerts?

You can set that up yourself! Each OS has different built-in tools to run scripts automatically, as well as sending yourself emails for alerts. But, since moksha already emails you when a decision has been made, the only benefit would be to alert you if you've moved up in line.

### How often should I run this?

Whenever you want, honestly. But probably no more than once a day, because markets don't move *that* fast.

### Wouldn't moksha not like this?

What this script is doing is no different than you opening a browser session and loading your 10 saved moksha tabs at the same time. Since this script is running locally on *your* machine through *your* internet connection (and not a single central location hitting it a ton of times), it doesn't look weird. I have had 0 issues, even with testing this lots of times, so you using it once or twice a day shouldn't cause any issues.

Of course, if you run this, like, every minute or check hundreds/thousands of URLs at once, then you might annoy moksha or cloudflare or something. But this script is meant for individuals to use for their own subs, which isn't enough web page openings to look suspicious. If anything, this will allow you to open moksha *less often*!

### What are you doing with my data? What can you see?

I can't see anything! You are saving and running this script on your own machine, looking at URLs and outputs that are only on your machine, and no data is being sent "out" of your computer. It's only taking "in" the content of the moksha webpages and looking at it locally.

Because anyone with a moksha URL can withdraw that submission, it's not safe to hand that URL over to random people. Which is why this has been designed to only be a local script you run yourself.

If you wanted to share the output with others, I recommend that you either copy/screenshot the terminal output or use the file with the IDs removed. I don't *think* someone can cause problems with only the UID (as submissions also have a normal ID, but with my testing I've noticed that they're not always unique per submission), but I want to be extra sure your subs are safe :3

### The output is formatted weird?

It's possible that the columns won't nicely line up for edge cases, like you're 1,000+ in line (or moved up 1,000 spaces), the average wait time is over 1,000 days (or the difference between your time and the average is 1,000). Mostly anything with 4 digits lol.

The names might not be exact, but that's based on my hacky way of making the HTML regex-able. Like it should be `PodCastle`, not `Pod Castle`, but I'm not going to lose sleep over it, nor should you. You know what it means.A very long name (like `Cosmic Horror Monthly LLC`) will be truncated, but you should be able to tell what it is still.

These statuses have been formatted to print nicely: rejected, accepted, revision requested, withdrawn, in progress. I *think* these are all the statuses that a writer is exposed to, but it's entirely possible that others exist (like archived, or file error) and it might not look nice. If that happens, please let me know! Then I can tweak the code so it'll look nice again.

Finally, it's possible that your terminal/text editor is too narrow. The output is 75 characters wide, which *should* fit most default terminal sizes nicely. Stretch it horizontally and it should look better.

### I installed python, but it's not working?

I know it's kinda naughty but I hardcoded it for python3. But it's 2026 you should be using python3 (especially if you're installing it for the first time for this script).

### Your code sucks!

Yeah I know!!! But it works, okay? If you want to update it to make it run better, feel free. This a'int anything groundbreaking so change it however you want.