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
	Run, "C:\Program Files\Git\git-bash.exe" --cd-to-home
}