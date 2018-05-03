#SingleInstance force

!`::
if WinExist("ahk_class mintty")
{
	if WinActive("ahk_class mintty") {
		WinMinimize
	}
	else {
		WinActivate
	}
}
else {
	Run, C:\cygwin64\bin\mintty.exe -i /Cygwin-Terminal.ico /bin/zsh --login
}