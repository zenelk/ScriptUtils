#SingleInstance force
; Play or Pause the currently playing media when "Ctrl+Win+Alt+S" is pressed
^#!s::
Send, {Media_Play_Pause}
return

; Turn the volume up when the 'Alt+Page Up' is pressed
!PgUp::
Send, {Volume_Up}
return

; Turn the volume down when the "Alt+Page Down" key is pressed
!PgDn::
Send, {Volume_Down}
return