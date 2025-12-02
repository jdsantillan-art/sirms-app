Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)

' Kill any stuck Python processes
WshShell.Run "taskkill /F /IM python.exe", 0, True
WScript.Sleep 2000

' Run git commands
WshShell.Run "cmd /c git add . && git commit -m ""Fix: Behavior concerns schedule + indentation + template"" && git push origin main && echo Deployment pushed! && pause", 1, False

MsgBox "Deployment started! Check the command window for progress.", vbInformation, "SIRMS Deployment"
