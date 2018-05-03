#SingleInstance force
; Makes it so the "Insert" key does not toggle "Insert Mode",
; But instead "Alt+Insert" toggles "Insert Mode"
$Insert::return

!Insert::Send, {Insert}