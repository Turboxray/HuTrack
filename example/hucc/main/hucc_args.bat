@echo off
setlocal
cd /d "%~dp0"

rem Override HUCC_HOME to select a matching 4.x compiler, assembler and headers.
if not defined HUCC_HOME set "HUCC_HOME=C:\huc"
set "PATH=%HUCC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUCC_HOME%\include\hucc"
set "PCE_BINPATH=%HUCC_HOME%\bin"
set "PCE_PCEAS=%HUCC_HOME%\bin\pceas.exe"

"%HUCC_HOME%\bin\hucc.exe"
exit /b %ERRORLEVEL%
