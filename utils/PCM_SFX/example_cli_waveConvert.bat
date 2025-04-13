del /Q output\emergency
rmdir /Q output\emergency
md output\emergency

python waveConvert.py --noGui --filein examples\emergency.wav --destinationPath output\emergency --debug
pause