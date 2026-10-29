# Readme

Are you sick and tired of having to write down your last known position in a Moksha queue? Annoyed that you have 10 different pages you need to refresh to see if you've moved? There's got to be a better way!

The creatively named moksha_checker script looks at these webpages for you and returns only the information you care about (i.e your position in line, and how long you've been waiting compared to the average wait time). If you use the script more than once, it "remembers" your position, and will report if you've moved up, and by how many spots. If the status has changed (like a rejection or acceptance), it returns this instead of your number in line.

It's set up so that it'll work if you have multiple submissions at the same market (both at the same time, and over time). If you no longer want a submission to be checked (like if it's no longer under consideration), simply delete its URL from the URL file.

As Moksha has recently implemented the Anubis web app firewall, it has since been updated to include bypassing it.

## How it works

Simply: you put your submission status URL into a file and run the script (exactly how depends on your OS). The script goes through the URLs one at a time, opens the web page, looks for specific information, and then prints it to the terminal. It also writes this information to an output file, so it can know if you've moved up in line.

This also looks in your /home/$USER/Downloads folder for a Moksha cookie file. I chose that because I'm lazy and that's where it downloads to. It works on duplicates that are numbered, so it only pulls the freshest cookie. This is how you get past the WAF.

## How to use

The core script is Python, so you need it installed on your computer for it to run. You can download it [straight from the source](https://www.python.org/downloads/) or from your favorite software source (apt homebrew Windows store etc.). It only uses standard modules, so you won't need to install anything else.

The code is set up that the url and output files are within the same folder, so either keep all three files in a dedicated folder, or update the code to include their new locations.

Before you run the script, you need to download your cookies from Moksha. This *only* needs your Anubis-based cookies, and not sessions from being logged in.
1. Navigate to any Moksha.io webpage
2. Wait the 1-2 seconds for your browser to pass the challenge
3. Wait for the anime girl to dissappear and a Moksha page to load
4. Use an extension or tool to export your cookies. I used `Get cookies.txt LOCALLY`. The code is currently set to look for it in the ~\Downloads directory, but if it's somewhere else (like you're a Windows user), then you'll need to update the code to where it downloads.

The cookie is good for <1 hour for me...except when it's just the 7 day long cookie. If it can't find a cookie or it's expired, the script will display a corresponding error and close. I'm currently working on a way to do this more automatically, so stay tuned!

You will also need a file called `moksha_URLS`. Place your submission status URLs (these are the ones you see in the confirmation emails) into the file, one per line. If your OS requires you to use extensions (like .txt), edit the code to change the file name.

I've designed the output to be pretty self-evident, but here's some example output:

```
Cookie status:
techaro.lol-anubis-auth-XXXX is GOOD. It expires in 6 days, 19 hours.

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

0. Cookie status - Whether your cookie(s) are currently "fresh"/valid. If they are expired, it will say so and exit the script. This is only printed to the terminal.
1. Timestamp - For your convenience. Only written to output file, as I assume your terminal has timestamps.
2. Market - The name of the magazine/podcast/journal/etc. May not reflect the specific submission window ("special novella call) and probably won't be perfectly formatted. If the name is too long, it'll be shortened.
3. Position - Your number in line, or status. Some markets don't show numbers, just that it's still "In Progress," which would be showed instead. If the submission has been rejected (or accepted, or withdrawn), that will be shown instead.
4. Days - The number of days the submission has been open. Not all markets show this number.
5. Avg. Days - The market-reported average time submissions are open before they get a response. This is then followed by how above/below the average you are. 
6. ID - Each submission has a unique UID, which allows users to have multiple submissions to the same market but have different URLs. This is captured by the script and saved to the output file to ensure that checks are for the same submission. This is obfuscated in the terminal printout (and I obfuscated my own here with Xs, but you would see your own)
7. Change - The difference between your last recorded position and your current position. This will only show up if there's been a difference (theoretically, if you've moved *backwards*, this number would be a negative...but idk if that's even possible)


## Troubleshooting

#### The URLs aren't being read!

You need to be connected to the internet, of course, but the most likely culprit is the URL file isn't properly formatted. You should ONLY have the URLs in the file, separated by hitting enter so there's one per line. No comments or notes to yourself or etc. The URL needs to be the page where you can look at your submission status. This is what's emailed to you by Moksha when you make a submission.

It's also possible that you're not a Linux(/MacOS?) user. So your "downloads" folder where the cookie is being is probably somewhere other than /home/$USER/Downloads. But if you're technical enough to run a Python script, I trust you're technical enough to open it with a text editor and change that line. You're free to change it to something else, if you download stuff to another directory.

#### It's not saying I'm moving up in line?

The script compares the number to the last time you ran it (which is recorded in the output file). If you moved, renamed, or deleted the output file (or have never run the script before), it won't be able to find it. If there has been no change between the last check and the one you just ran, it won't print out a 0, just report the number in line.

#### What if I want this to run automatically? What if I want email alerts?

You can set that up yourself! Each OS has different built-in tools to run scripts automatically, as well as sending yourself emails for alerts. But, since Moksha already emails you when a decision has been made, the only benefit would be to alert you if you've moved up in line (or if their emails have a habit of not getting to your inbox).

#### How often should I run this?

Whenever you want, honestly. But probably no more than once a day, because markets don't move *that* fast, and after you've made a submission, to record where you started.

#### Wouldn't Moksha not like this?

What this script is doing is functionally no different than you opening a browser session and loading your 10 saved Moksha tabs at the same time. Since this script is running locally on *your* machine through *your* internet connection (and not a single central location hitting it a ton of times), it doesn't look weird. I have had 0 issues, even with testing this lots of times, so you using it once or twice a day shouldn't cause any issues.

Of course, if you run this, like, every minute or check hundreds/thousands of URLs at once, then you might annoy Moksha and get blocked. But that's what VPNs are for. This script is meant for individuals to use for their own subs, which isn't enough web page openings to look suspicious. If anything, this will allow you to open Moksha *less often*!

#### What are you doing with my data? What can you see?

I can't see anything! You are saving and running this script on your own machine, looking at URLs and outputs that are only on your machine. The only data being sent "out" of your computer is the cookie, which is exactly what your web browser does. It's only taking "in" the content of the Moksha webpages and looking at it locally.

Because anyone with a Moksha URL can withdraw that submission, it's not safe to hand that URL over to random people. Which is why this has been designed to only be a local script you run yourself.

If you wanted to share the output with others, I recommend that you either copy/screenshot the terminal output or use the file with the IDs removed. I don't *think* someone can cause problems with only the UID (as submissions also have a normal ID, but with my testing I've noticed that they're not always unique per submission), but I want to be extra sure your subs are safe :3

#### The output is formatted weird?

It's possible that the columns won't nicely line up for edge cases, like you're 1,000+ in line (or moved up 1,000 spaces), the average wait time is over 1,000 days (or the difference between your time and the average is 1,000). Mostly anything with 4 digits lol.

The names might not be exact, but that's based on my hacky way of making the HTML regex-able. Like it should be `PodCastle`, not `Pod Castle`, but I'm not going to lose sleep over it, nor should you. You know what it means.A very long name (like `Cosmic Horror Monthly LLC`) will be truncated, but you should be able to tell what it is still.

These statuses have been formatted to print nicely: rejected, accepted, revision requested, withdrawn, in progress. I *think* these are all the statuses that a writer is exposed to, but it's entirely possible that others exist (like archived, or file error) and it might not look nice. If that happens, please let me know! Then I can tweak the code so it'll look nice again.

Finally, it's possible that your terminal/text editor is too narrow. The output is 75 characters wide, which *should* fit most default terminal sizes nicely. Stretch it horizontally and it should look better.

#### I installed Python, but it's not working?

I know it's kinda naughty but I hardcoded it for python3. But it's 2026 you should be using python3 (especially if you're installing it for the first time for this script). What's most likely the issue is your cookies.

#### What's this about cookies?

This is a brand new "feature", becaus Moksha has changed! I'm sure you've seen webpages that make you click a Cloudflare captcha to prove you're human. Anubis is similar to that, only it's free. The only thing it does to make a computer "prove" it's "human" is to do some "proof of work". If you remember cryptocurrency, those do a really hard math problem to earn a coin. What Anubis is having your web browser do is solve a much less difficult math problem for a cookie.

A cookie is a small file saved on your computer that can be shown to a website to prove who you are. Mostly, this is to say "yes, I'm chasejxyz, and I'm signed in to my bluesky account, see?" For Anubis, the cookie is proof that you solved the math problem and should be let through. In order for this script to get "around" Anubis, it needs to show the cookie, which is the exact same one you'd use in your web browser. The script is cutting out the "middle man" of your web browser to pull the web page data, which is why it's faster than opening a bunch of tabs yourself.

Cookies, when issued, are given an expiration date. Some can be for years, while others are much shorter. The Anubis cookie lives either one week or less than an hour. Don't ask me why.

#### Why do *I* have to get the cookie?

Because grabbing a cookie out of your web browser and flashing it to the security guard should be difficult! Otherwise a program could steal your bluesky cookie and be logged in to your account. I'm currently working on a way to do the math problem outside of a web browser, but it would probably require another program that is *not* in Python, which will be more complicated for you. You manually downloading the cookie is a good stopgap, especially if you don't run this super often.

#### Your code sucks!

Yeah I know!!! But it works, okay? If you want to update it to make it run better, feel free. This a'int anything groundbreaking so change it however you want.
