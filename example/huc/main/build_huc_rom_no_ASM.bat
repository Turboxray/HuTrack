rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt
del S_log.txt

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\huc
set PATH=%PATH%;c:\huc\bin

huc.exe  -v -v -s -msmall -fno-recursive huc_example.c -T > C_log.txt

type C_log.txt

pause