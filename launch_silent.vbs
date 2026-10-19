' Silent launcher — no CMD window
Option Explicit
Dim sh, fso, here, pyw, main, candidates, i, p
Set sh = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")
here = fso.GetParentFolderName(WScript.ScriptFullName)
main = here & "\main.py"
sh.CurrentDirectory = here

candidates = Array( _
  sh.ExpandEnvironmentStrings("%LocalAppData%\Python\pythoncore-3.14-64\pythonw.exe"), _
  sh.ExpandEnvironmentStrings("%LocalAppData%\Python\pythoncore-3.13-64\pythonw.exe"), _
  sh.ExpandEnvironmentStrings("%LocalAppData%\Python\bin\pythonw.exe"), _
  sh.ExpandEnvironmentStrings("%LocalAppData%\Programs\Python\Python314\pythonw.exe"), _
  sh.ExpandEnvironmentStrings("%LocalAppData%\Programs\Python\Python313\pythonw.exe") _
)

pyw = ""
For i = 0 To UBound(candidates)
  p = candidates(i)
  If fso.FileExists(p) Then
    pyw = p
    Exit For
  End If
Next

If pyw = "" Then
  ' Last resort: hope pythonw is on PATH
  pyw = "pythonw.exe"
End If

' 0 = hidden window
sh.Run """" & pyw & """ """ & main & """", 0, False
