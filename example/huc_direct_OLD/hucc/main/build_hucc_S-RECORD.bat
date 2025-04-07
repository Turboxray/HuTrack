rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt
del S_log.txt
del *.sym
del *.lst
del *.s

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\hucc
set PATH=%PATH%;c:\huc\bin

hucc.exe -s -v -v -msmall -gL -fno-recursive -s hucc_example.c > C_log.txt

pceas.exe --hucc hucc_example.s -l 3 -S -m > S_log.txt
type C_log.txt
type S_log.txt
pause