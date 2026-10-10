@echo off
setlocal
if not defined HUC_HOME set "HUC_HOME=C:\huc"
"%HUC_HOME%\bin\pceas.exe"
exit /b %ERRORLEVEL%
