@echo off
setlocal
cd /d "%~dp0"

rem Override HUCC_HOME if your HuC/HuCC installation is elsewhere.
if not defined HUCC_HOME set "HUCC_HOME=C:\huc"
set "PATH=%HUCC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUCC_HOME%\include\hucc"
set "PCE_BINPATH=%HUCC_HOME%\bin"
set "PCE_PCEAS=%HUCC_HOME%\bin\pceas.exe"

"%HUCC_HOME%\bin\hucc.exe" -v -v -gL -msmall -fno-recursive hucc_pcm_example.c > C_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type C_log.txt
exit /b %BUILD_RESULT%
