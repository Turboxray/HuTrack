@echo off

rem ***************************************************************************


setlocal

cd /d "%~dp0"

pushd

del log.txt

set PCE_INCLUDE=%CD%\..\lib;%CD%\..\..\..\lib

pceas -raw pceas_example.asm -l 2 -S > log.txt
type log.txt
pause
