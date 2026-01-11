## INSTRUCTIONS

0. Install python3. You can download it from Python.org, the Windows store, or through cmd.exe/powershell. Which, if you don't know how to do that, don't. Don't download/install random exes this way it's not a good idea. But if you trust me (or just like to gamble), you can do `winget install 9NQ7512CXL7T`
0.5. You might need to install PowerShell, too, which is the modern Windows terminal. You have a couple of options, and you can find them all [here](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows?view=powershell-7.5).
1. Put your moksha status URLs into moksha_URLS.txt using your Notepad.exe and save the file (make sure to delete the comments!).
2. Right-click the background of this folder and select "open in terminal" (or navigate there yourself, if you're already familiar with PowerShell)
3. Type `py .\moksha_checker.py`
4. If you ever want to look at the output file, you can open it with your favorite text editor (or Notepad.exe).
5. The next time you want to run this, you can just hit the up arrow key to cycle back through your history to `py .\moksha_checker.py`. Which, if this is the only thing you use PowerShell for, should just be only going up the once.

## TROUBLESHOOTING:

### Why doesn't this have a nice script like Linux?

Because I am not a PowerShell guy and couldn't make it work. I know a ~~dog~~ guy I can ask him to write one for me but for now this is the best I got.