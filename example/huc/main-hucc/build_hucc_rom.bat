rem ***************************************************************************

setlocal

cd /d "%~dp0"

pushd

del C_log.txt

set HUCC_HOME=D:\retrogamedev\src\huc\huc\

set PCE_INCLUDE=%CD%\..\..\..\lib;%HUCC_HOME%\include\hucc
set PATH=%HUCC_HOME%\bin;%PATH%

hucc.exe -v -O2 -gC huc_example.c > C_log.txt

type C_log.txt
pause
