rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt
del S_log.txt
del *.sym
del *.lst
del *.s

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\huc
set PATH=%PATH%;c:\huc\bin

huc.exe  -v -v -msmall -fno-recursive huc_example.c -T > C_log.txt

type C_log.txt

pause