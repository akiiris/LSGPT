; hotkey.ahk  (AutoHotkey v2)
; Ctrl+Alt+Shift+Home -> create .clip.trigger in the same folder as this script

; Get directory where this .ahk file is located
scriptDir := A_ScriptDir
triggerPath := scriptDir "\.clip.trigger"

; ^ = Ctrl, ! = Alt, + = Shift
; ('g' for generate)
^!+g::
{
    try FileDelete(triggerPath)
    catch
    FileAppend("", triggerPath, "UTF-8")
}
