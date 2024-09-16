rem ***************************************************************************

setlocal

set PCE_INCLUDE=%CD%\..\..\..\lib;C:\huc\include\huc
set PATH=%PATH%;c:\huc\bin

huc.exe  
pause