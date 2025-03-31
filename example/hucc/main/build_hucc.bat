rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt
del S_log.txt

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\hucc
set PATH=%PATH%;c:\huc\bin

hucc.exe -s -v -v -msmall -fno-recursive huc_example.c -T > C_log.txt
@REM hucc.exe huc_example.c > C_log.txt
@REM pceas  -S -l 3 -o hucc_example.pce --raw --hucc huc_example.s > S_log.txt

type C_log.txt
@REM type S_log.txt

pause