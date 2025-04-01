rem ***************************************************************************

setlocal

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\hucc
set PATH=%PATH%;c:\huc\bin

hucc.exe  
pause