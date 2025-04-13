del lot.txt

del /Q .\examples\test1
del /Q .\examples\swiss
del /Q .\examples\smb3
del /Q .\examples\l1

del .\examples\main.wf.inc
copy .\examples\main.wf .\examples\main.wf.inc

md .\examples\test1
md .\examples\swiss
md .\examples\smb3
md .\examples\l1

python VGM2SFX.py --filein examples/test1.vgm --debugLog --waveformlist examples/main.wf.inc --destfolder examples/test1 --chanproc 2
python VGM2SFX.py --filein examples/swiss.vgm --debugLog --waveformlist examples/main.wf.inc --destfolder examples/swiss --chanproc 0
python VGM2SFX.py --filein examples/smb3_sfx.vgm --debugLog --waveformlist examples/main.wf.inc --destfolder examples/smb3 --sfxname smb3_sfx
python VGM2SFX.py --filein examples/light_1.vgm --debugLog --waveformlist examples/main.wf.inc --destfolder examples/l1 --chanproc 0

pause