cd backupDriverFiles
cd Android
:CheckOS
IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
echo 64-bit...
msiexec.exe /i node-v6.10.3-x64.msi 
GOTO END

:32BIT
echo 32-bit...
msiexec.exe /i node-v6.10.3-x86.msi 
GOTO END

:END
curl.exe

