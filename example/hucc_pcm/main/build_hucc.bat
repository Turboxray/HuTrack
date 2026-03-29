rem ***************************************************************************
@echo off
set HUCC_HOME=C:\PCEngine\huc
set HUTRACK_HOME=C:\PCEngine\HuTrack

set PATH=%HUCC_HOME%\bin;%PATH%
set PCE_INCLUDE=%HUCC_HOME%\include\hucc;%HUTRACK_HOME%\lib\

@cls

hucc hucc_pcm_example.c -gC

pause
