@echo off
setlocal
cd /d "%~dp0"

rem Override HUC_HOME to select a matching 4.x compiler, assembler and headers.
if not defined HUC_HOME set "HUC_HOME=C:\huc"
set "PATH=%HUC_HOME%\bin;%PATH%"
set "PCE_INCLUDE=%CD%\..\..\..\lib;%HUC_HOME%\include\huc"
set "PCE_BINPATH=%HUC_HOME%\bin"
set "PCE_PCEAS=%HUC_HOME%\bin\pceas.exe"

"%HUC_HOME%\bin\huc.exe"
exit /b %ERRORLEVEL%
