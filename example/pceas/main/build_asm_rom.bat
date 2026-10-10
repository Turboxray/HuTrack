@echo off
setlocal
cd /d "%~dp0"

rem Use the installed 4.x assembler instead of the bundled historical executable.
if not defined HUC_HOME set "HUC_HOME=C:\huc"
set "PCE_INCLUDE=%CD%\..\lib;%CD%\..\..\..\lib"
"%HUC_HOME%\bin\pceas.exe" -raw pceas_example.asm -l 2 -S > log.txt 2>&1
set "BUILD_RESULT=%ERRORLEVEL%"
type log.txt
exit /b %BUILD_RESULT%
