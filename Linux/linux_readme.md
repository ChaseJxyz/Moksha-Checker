## INSTRUCTIONS

0. Install python3, if it isn't already installed. Type `which python` in terminal, it should let you tab autocomplete to python3 if it's installed (and then also tell you its path). Use apt or yum or whatever to install python3 if needed.
1. Put your moksha status URLs into moksha_URLS using your favorite text editor and save the file (make sure to delete the comments!).
2. Run moksha_checker.sh (double click it, run it in terminal, etc). If you're given options, choose "Run in terminal" or similar. Close the terminal window when you're done.
3. If you ever want to look at the output file, you can open it with your favorite text editor.

## TROUBLESHOOTING:

### I can't run the sh script!

Ensure that you have permissions to execute it. You can change this in properties (right click the file > properties > permissions > check "Allow executing file as program")(language may be different depending on your distro ) or run `umod u+x moksha_checker.sh`

If you want to launch this from the terminal, make sure it's "in" the same folder as this script (you can right click the interior of the folder and launch "Open in terminal" or similar)(or `cd` into wherever you saved this) and run `./moksha_checker.sh`.