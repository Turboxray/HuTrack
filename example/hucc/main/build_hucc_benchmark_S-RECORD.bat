@echo off
setlocal
cd /d "%~dp0"

rem Override HUCC_HOME to select a matching 4.x compiler, assembler and headers.
if not defined HUCC_HOME set "HUCC_HOME=C:\huc"
set "PATH=%HUCC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUCC_HOME%\include\hucc"
set "PCE_BINPATH=%HUCC_HOME%\bin"
set "PCE_PCEAS=%HUCC_HOME%\bin\pceas.exe"

"%HUCC_HOME%\bin\hucc.exe" -v -v -msmall -fno-recursive -gL -s -AHUTRACK_BENCHMARK=1 hucc_example.c > C_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type C_log.txt
if not "%BUILD_RESULT%"=="0" exit /b %BUILD_RESULT%

"%PCE_PCEAS%" --hucc hucc_example.s -l 3 -S -m > S_log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type S_log.txt
exit /b %BUILD_RESULT%
