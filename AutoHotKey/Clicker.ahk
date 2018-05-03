SetTitleMatchMode 2
DetectHiddenWindows, On
sendMode Input
SetDefaultMouseSpeed, 0
SetMouseDelay, -1
SetKeyDelay, -1
SetWinDelay, -1
SetBatchLines, -1
SetControlDelay -1

^esc::ExitApp

~$*LButton::
  ; On LButton (* wildcards[ctrl/alt]) (~ native not blocked) ($ uses send)
  Loop
  {
    ; Get state of caps lock (on/off), if off, leave loop
    GetKeyState, CapsState, CapsLock, T
    if CapsState = U
      break

    ; Since our 'break' state doesn't trigger, send LButton
    send {LButton}

    ; Back to beginning of loop after 10 ms.
    sleep, 40
  }
  ; This is necessary
  return