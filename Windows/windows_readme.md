## INSTRUCTIONS

0. Install python3. You can download it from Python.org, the Windows store, or through cmd.exe/powershell. Which, if you don't know how to do that, don't. Don't download/install random exes this way it's not a good idea. But if you trust me (or just like to gamble), you can do `winget install 9NQ7512CXL7T`
0.5. You might need to install PowerShell, too, which is the modern Windows terminal. If hitting the Windows key and typing "powershell" doesn't turn up `Windows PowerShell` the app, it's not installed. You have a couple of options to get it, and you can find them all [here](https://learn.microsoft.com/en-us/powershell/scripting/install/install-powershell-on-windows?view=powershell-7.5).
1. Put your moksha status URLs into moksha_URLS.txt using Notepad.exe and save the file (make sure to delete the comments!).
2. Double-click `moksha_checker.ps1`. If Windows is weird and asks what program to open it with, choose PowerShell. You can also right-click it and choose "Run with PowerShell". Close the terminal window when you're done.
3. If you ever want to look at the output file, you can open it with your favorite text editor (or Notepad.exe).


## TROUBLESHOOTING:

### I hate right-clicking I only want to double click ☹️

You must right-click once more, but choose open with > Choose Another app. If PowerShell is one of the options it shows, select it, check "AAlways use this app to open .ps1 files", and click okay. If it's *not* an option, click "more apps." If it's still not there, click "Look for another app on this PC," and paste `C:\Windows\System32\WindowsPowershell\v1.0\` into the address bar on explorer (or manually go to that folder). If your OS isn't on the C drive, change it to the proper letter.

### Windows is being mean/doesn't like it

Windows is weird and can ask you if you want to allow an app to make changes to your computer for lots of things. You can say yes if it does, as this script doesn't send "out" any information or otherwise have security concerns. You shouldn't *need* to run PowerShell as an admin for this to work, but I can't really say, since there's so many configurations out there and updates that might break this.