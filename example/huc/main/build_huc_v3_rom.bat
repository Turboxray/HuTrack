rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt
del S_log.txt
del *.s

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\pce
set PATH=%PATH%;c:\huc\bin

huc.exe  -v -s huc_example.c -T > C_log.txt

pceas.exe huc_example.s -l 3 -S -m > S_log.txt
type C_log.txt
type S_log.txt
pause