' start_server_hidden.vbs
Option Explicit
Dim shell, fso, scriptDir, pyScript, py, cmd, i
Set shell = CreateObject("WScript.Shell")
Set fso   = CreateObject("Scripting.FileSystemObject")

scriptDir = fso.GetParentFolderName(WScript.ScriptFullName)
pyScript  = fso.BuildPath(scriptDir, "server_clipboard.py")

If Not fso.FileExists(pyScript) Then
  MsgBox "Can't find server_clipboard.py at:" & vbCrLf & pyScript, vbCritical, "Startup error"
  WScript.Quit 1
End If

Dim candidates
candidates = Array( _
  "pyw.exe", _
  "pythonw.exe", _
  "%LocalAppData%\Programs\Python\Python313\pythonw.exe", _
  "%LocalAppData%\Programs\Python\Python312\pythonw.exe", _
  "%LocalAppData%\Programs\Python\Python311\pythonw.exe", _
  "%ProgramFiles%\Python313\pythonw.exe", _
  "%ProgramFiles%\Python312\pythonw.exe", _
  "%ProgramFiles%\Python311\pythonw.exe", _
  "%UserProfile%\AppData\Local\Microsoft\WindowsApps\pythonw.exe" _
)

py = ""
For i = 0 To UBound(candidates)
  Dim p
  p = shell.ExpandEnvironmentStrings(candidates(i))
  If InStr(p, "\") = 0 Then
    py = p   ' let PATH resolve bare name
    Exit For
  ElseIf fso.FileExists(p) Then
    py = """" & p & """"
    Exit For
  End If
Next

If py = "" Then
  MsgBox "Couldn't find Python (pyw.exe/pythonw.exe). Install Python and ensure the launcher is on PATH.", vbCritical, "Startup error"
  WScript.Quit 1
End If

cmd = py & " " & """" & pyScript & """"
shell.Run cmd, 0, False   ' hidden, do not wait
