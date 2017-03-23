cd backupDriverFiles
cd Android
:CheckOS
IF EXIST "%PROGRAMFILES(X86)%" (GOTO 64BIT) ELSE (GOTO 32BIT)

:64BIT
echo 64-bit...
msiexec.exe /i node-v0.12.4-x64.msi 
GOTO END

:32BIT
echo 32-bit...
msiexec.exe /i node-v0.12.5-x86.msi 
GOTO END

:END
appium-installer.exe
curl.exe

