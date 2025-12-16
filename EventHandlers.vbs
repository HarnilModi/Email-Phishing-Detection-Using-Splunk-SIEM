Option Explicit

Dim SAVE_FOLDER
SAVE_FOLDER = "C:\email_logs\inbound_eml\"

Sub AppendLine(path, text)
  On Error Resume Next
  Dim fso, tf
  Set fso = CreateObject("Scripting.FileSystemObject")
  Set tf = fso.OpenTextFile(path, 8, True)
  tf.WriteLine text
  tf.Close
End Sub

Function MakeFilename()
  MakeFilename = SAVE_FOLDER & _
    Year(Now) & "-" & Right("0" & Month(Now),2) & "-" & Right("0" & Day(Now),2) & "_" & _
    Right("0" & Hour(Now),2) & "-" & Right("0" & Minute(Now),2) & "-" & Right("0" & Second(Now),2) & ".eml"
End Function

Sub OnDeliverMessage(oMessage)
  On Error Resume Next

  Dim fso, outFile, tf
  outFile = MakeFilename()

  Set fso = CreateObject("Scripting.FileSystemObject")
  Set tf = fso.CreateTextFile(outFile, True)

  ' Write headers
  tf.WriteLine oMessage.Header

  tf.WriteLine ""
  tf.WriteLine "----- BODY -----"
  tf.WriteLine oMessage.Body

  tf.Close

  AppendLine SAVE_FOLDER & "saved_messages.log", _
    Now() & " SAVED EMAIL: " & outFile & _
    " FROM=" & oMessage.FromAddress & _
    " TO=" & oMessage.To
End Sub
