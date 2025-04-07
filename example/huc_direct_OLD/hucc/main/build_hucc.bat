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

hucc.exe -v -v -gL -msmall -fno-recursive hucc_example.c > C_log.txt

type C_log.txt

pause