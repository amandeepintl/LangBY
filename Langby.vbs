' Langby - Silent Launcher
' Double-click this to start Langby with zero visible windows
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "launcher.bat", 0, False
Set WshShell = Nothing
