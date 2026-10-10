@echo off
setlocal
cd /d "%~dp0"

rem Override HUC_HOME to select a matching 4.x compiler, assembler and headers.
if not defined HUC_HOME set "HUC_HOME=C:\huc"
set "PATH=%HUC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUC_HOME%\include\huc"
set "PCE_BINPATH=%HUC_HOME%\bin"
set "PCE_PCEAS=%HUC_HOME%\bin\pceas.exe"

"%HUC_HOME%\bin\huc.exe" -v -v -msmall -fno-recursive -s -AHUTRACK_BENCHMARK=1 huc_example.c -T > C_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type C_log.txt
if not "%BUILD_RESULT%"=="0" exit /b %BUILD_RESULT%

"%PCE_PCEAS%" huc_example.s -l 3 -S -m > S_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type S_log.txt
exit /b %BUILD_RESULT%
