#SingleInstance force
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Manipulate Entire Line
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Map "Alt+Left" to "Home"
!Left::Send, {Home}

; Map "Alt+Right" to "End"
!Right::Send, {End}

; Map "Shift+Alt+Left" to "Shift+Home"
+!Left::Send, +{Home}

; Map "Shift+Alt+Right" to "Shift+End"
+!Right::Send, +{End}

; Map "Alt+BS" to "Delete To Beginning"
!BS::Send, +{Home}{BS}

; Map "Control+Alt+BS" to "Delete To End"
^!BS::Send, +{End}{BS}

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Manipulate Word
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Map "Modifier+Left" to "Control+Left", Disabling "Control+Left"
$^Left::return
#Left::Send, ^{Left}
return

; Map "Modifier+Right" to "Control+Right", Disabling "Control+Right"
$^Right::return
#Right::Send, ^{Right}
return

; Map "Modifier+Shift+Right" to "Control+Shift+Right", Disabling "Control+Shift+Right" 
$^+Right::return
#+Right::Send, ^+{Right}
return

; Map "Modifier+Shift+Left" to "Control+Shift+Left", Disabling "Control+Shift+Left" 
$^+Left::return
#+Left::Send, ^+{Left}
return

; Map "Modifier+BS" to "Control+BS", Disabling "Control+BS"
$^BS::return
#BS::Send, ^{BS}
return

; Map "Modifier+Control+BS" to "Control+Del", Disabling "Control+Del"
$^Del::return
#^BS::Send, ^{Del}

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Remap Missing Window Shortcuts
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; Map "Modifier+Alt+Left" to "Modifier+Left"
#!Left::Send, #{Left}

; Map "Modifier+Alt+Right" to "Modifier+Right"
#!Right::Send, #{Right}

; Map "Modifier+Alt+Up" to "Modifier+Up"
#!Up::Send, #{Up}

; Map "Modifier+Alt+Down" to "Modifier+Down"
#!Down::Send, #{Down}

; Disable "Modifier+Down" for consistency
$#Down::return

; Disable "Modifier+Up" for consistency
$#Up::return