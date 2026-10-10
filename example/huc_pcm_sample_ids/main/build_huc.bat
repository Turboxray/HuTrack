@echo off
rem Run this project's HuC build from any working directory.
setlocal
cd /d "%~dp0"
if not defined HUC_HOME set "HUC_HOME=C:\huc"
set "PATH=%HUC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUC_HOME%\include\huc"
set "PCE_BINPATH=%HUC_HOME%\bin"
set "PCE_PCEAS=%HUC_HOME%\bin\pceas.exe"
"%HUC_HOME%\bin\huc.exe" -v -v -msmall -fno-recursive pcm_sample_ids.c -T > C_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type C_log.txt
exit /b %BUILD_RESULT%
