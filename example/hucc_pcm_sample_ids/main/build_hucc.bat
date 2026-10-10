@echo off
rem Run this project's HuCC build from any working directory.
setlocal
cd /d "%~dp0"
if not defined HUCC_HOME set "HUCC_HOME=C:\huc"
set "PATH=%HUCC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUCC_HOME%\include\hucc"
set "PCE_BINPATH=%HUCC_HOME%\bin"
set "PCE_PCEAS=%HUCC_HOME%\bin\pceas.exe"
"%HUCC_HOME%\bin\hucc.exe" -v -v -msmall -fno-recursive -gL pcm_sample_ids.c > C_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type C_log.txt
exit /b %BUILD_RESULT%
