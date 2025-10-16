; hotkey.ahk  (AutoHotkey v2)
; Ctrl+Alt+Shift+Home -> create .clip.trigger in the same folder as this script

; Get directory where this .ahk file is located
scriptDir := A_ScriptDir
triggerPath := scriptDir "\.clip.trigger"

; ^ = Ctrl, ! = Alt, + = Shift
^!+Home::
{
    try FileDelete(triggerPath)
    catch
    FileAppend("", triggerPath, "UTF-8")
}
