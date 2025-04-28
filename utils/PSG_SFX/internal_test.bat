del lot.txt

del /Q .\internal_test\test1
del /Q .\internal_test\swiss
del /Q .\internal_test\smb3
del /Q .\internal_test\l1
del /Q .\internal_test\chan3_slow
del /Q .\internal_test\FF3_smeared_graffiti

del /Q .\internal_test\smb3_overworld
del /Q .\internal_test\Night_Slave_-_Bottom_Sweep_V2
del /Q .\internal_test\smb3_overworld_comp

del /Q .\internal_test\Sonic2_ChemicalPlantZone01g
del /Q .\internal_test\SOR2GoStraight_NormalMix_01w

del /Q .\internal_test\SCV4_SimonTheme

del /Q .\internal_test\jazzy0
del /Q .\internal_test\title_screen



del .\internal_test\main.wf.inc
copy .\internal_test\main.wf .\internal_test\main.wf.inc

md .\internal_test\test1
md .\internal_test\swiss
md .\internal_test\smb3
md .\internal_test\l1
md .\internal_test\chan3_slow

md .\internal_test\smb3_overworld
md .\internal_test\Night_Slave_-_Bottom_Sweep_V2
md .\internal_test\smb3_overworld_comp
md .\internal_test\FF3_smeared_graffiti

md .\internal_test\Sonic2_ChemicalPlantZone01g
md .\internal_test\SOR2GoStraight_NormalMix_01w

md .\internal_test\SCV4_SimonTheme

md .\internal_test\jazzy0
md .\internal_test\title_screen


@REM python VGM2SFX.py --filein internal_test/test1.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/test1 --chanproc 2 --debugBin
@REM python VGM2SFX.py --filein internal_test/swiss.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/swiss --chanproc 0 --debugBin
@REM python VGM2SFX.py --filein internal_test/smb3_sfx.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/smb3 --sfxname smb3_sfx --debugBin
@REM python VGM2SFX.py --filein internal_test/light_1.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/l1 --chanproc 0 --debugBin
@REM python VGM2SFX.py --filein internal_test/chan3_slow.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/chan3_slow --chanproc 0 1 2 3 4 5 --debugBin

@REM python VGM2SFX.py --filein internal_test/Night_Slave_-_Bottom_Sweep_V2.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/Night_Slave_-_Bottom_Sweep_V2 --chanproc 0 1 2 3 4 5 --debugBin
@REM python VGM2SFX.py --filein internal_test/smb3_overworld.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/smb3_overworld --chanproc 0 1 2 3 4 5 --debugBin

@REM python VGM2SFX.py --filein internal_test/FF3_smeared_graffiti.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/FF3_smeared_graffiti --chanproc 0 1 2 3 4 5 --debugBin

@REM python VGM2SFX.py --filein internal_test/Sonic2_ChemicalPlantZone01g.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/Sonic2_ChemicalPlantZone01g --chanproc 0 1 2 3 4 5 --debugBin
@REM python VGM2SFX.py --filein internal_test/SOR2GoStraight_NormalMix_01w.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/SOR2GoStraight_NormalMix_01w --chanproc 0 1 2 3 4 5 --debugBin

python VGM2SFX.py --filein internal_test/SCV4_SimonTheme.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/SCV4_SimonTheme --chanproc 0 1 2 3 4 5 --debugBin

@REM python VGM2SFX.py --filein internal_test/jazzy0.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/jazzy0 --chanproc 0 1 2 3 4 5 --debugBin

@REM python VGM2SFX.py --filein internal_test/title_screen.vgm --debugLog --waveformlist internal_test/main.wf.inc --destfolder internal_test/title_screen --chanproc 0 1 2 3 4 5 --debugBin

pause