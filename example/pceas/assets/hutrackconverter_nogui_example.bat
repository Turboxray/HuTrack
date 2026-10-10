@echo off
setlocal
cd /d "%~dp0"
python HuTrackConverter.py --no_gui --filein test_1.dmf --songname test --subfolder song/test --includePath ../assets --no_songname --no_author
exit /b %ERRORLEVEL%
