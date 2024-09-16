
import argparse
import json
import numpy
import os
import pprint
import resampy
import sys
import zlib

from support.huTrackBase import HuTrackContainer, RATE_TABLE, RATE_VAL
from support.dmfReader import ConvertDeflemask


class HuTrackLib():

    def __init__(self, hutrack=None, params=None):
        self.huTrack = hutrack
        self.params  = params

    def importDmf(self):
        print("\n params",self.params)
        convertDeflemask = ConvertDeflemask(self.params)
        result, hutrack = convertDeflemask.process()
        return result, hutrack

    def importHutrackFile(self):
        pass

    def exportHuTrackTextFile(self):
        pceModule = HuTrackExportPCE(hutrack=self.huTrack, params=self.params)
        print("\n\n params", self.params,"\n\n params")
        pceModule.process()
        del pceModule
        return True

    def exportPceHuTrackFile(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.HuTrack').replace("\\","/")

        self.indentMod  = 0
        self.hutrackMod = []
        # Header

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Song Info                                                                        .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('SongInfo:', '++')
        self.__insYaml('')
        self.__insYaml(f'songname: {self.huTrack.songName}')
        self.__insYaml(f'authorName: {self.huTrack.authorName}')
        self.__insYaml(f'timeBase: {self.huTrack.timeBase}')
        self.__insYaml(f'frameMode: {self.huTrack.frameMode}')
        self.__insYaml(f'customMode: {self.huTrack.customMode}')
        self.__insYaml(f'tickTime1: {self.huTrack.tickTime1}')
        self.__insYaml(f'tickTime2: {self.huTrack.tickTime2}')
        self.__insYaml(f'rowsPerPattern: {self.huTrack.rowsPerPattern}')
        self.__insYaml(f'PatternMatrixLen: {self.huTrack.PatternMatrixLen}')
        self.__insYaml(f'instrumentsLen: {self.huTrack.instrumentsLen}')
        self.__insYaml(f'wavetableLen: {self.huTrack.wavetableLen}')
        self.__insYaml(f'samplesLen: {self.huTrack.samplesLen}')
        self.__indentReset()
        self.__insYaml('')
        self.__insYaml('')

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Pattern List                                                                     .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('PatternList:','++')
        self.__insYaml('')
        for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
            self.__insYaml(f'#....................................................')
            self.__insYaml(f'# Channel {channel}')
            self.__insYaml(f'{channel}:','++')
            self.__insYaml(f'{self.huTrack.PatternMatrixCompressed[channel]}')
            self.__insYaml('','-')


        self.__indentReset()
        self.__insYaml('')
        self.__insYaml('')

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Pattern Data                                                                     .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('PatternData:','++')
        self.__insYaml('')
        for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
            self.__insYaml(f'#########################################################################')
            self.__insYaml(f'#........................................................................')
            self.__insYaml(f'# Channel {channel}')
            self.__insYaml(f'{channel}:','++')

            noteLut = [' C','C#',' D','D#',' E',' F','F#',' G','G#',' A','A#',' B']

            # Pattern data
            for pattern in set(self.huTrack.PatternMatrixCompressed[channel]):
                self.__insYaml(f'#...........................................')
                self.__insYaml(f'#...........................................')
                self.__insYaml(f'#...........................................')
                self.__insYaml(f'# Pattern {pattern}   (channel {channel})   P{pattern}:{channel}')
                self.__insYaml(f'{pattern}:','++')
                self.__insYaml(f'# Note  Vol  Ins  FX1  arg  FX2  arg  FX3  arg  FX4  arg')
                for idx,row in enumerate(self.huTrack.uncompPatternData[channel][pattern].patternData):
                    row = [(item,'')[item == 0xffff] for item in row]
                    row = (row, ['']+row[2:])[row[0] == 0]

                    if row[0] != '' and row[0] != 100:
                        note = noteLut[row[0] % 12] + '-' + str(row[1])
                        row = [note] + row[2:]
                    elif row[0] == 100:
                        row = [' OFF'] + row[2:]

                    row = row + ['' for i in range(11 - len(row))]
                    entry = '[ '

                    for item in row:
                        if item == '':
                            entry += "  \'\',"
                        elif type(item) != str:
                            val    = hex(item)[2:].upper()
                            entry += '  ' + (val,'0'+val)[len(val) < 2] + ','
                        else:
                            entry += item + ','

                    entry = entry[:-1] + ' ]'


                    self.__insYaml(f'{entry}  # row {idx}')
                self.__insYaml('','-')

            self.__insYaml('','-')

        self.__indentReset()
        self.__insYaml('')
        self.__insYaml('')

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Instruments                                                                      .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('Instrument:','++')
        self.__insYaml('')

        for instrument in range(self.huTrack.instrumentsLen):
            self.__insYaml(f'#########################################################################')
            self.__insYaml(f'#........................................................................')
            self.__insYaml(f'# Instrument {instrument}')
            self.__insYaml(f'{instrument}:','++')
            self.__insYaml('')


            self.__insYaml(f'#...........................................')
            self.__insYaml(f'# Volume Envelope')
            self.__insYaml('')
            self.__insYaml(f'volEnvSize:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].volumeEnvLength}','--')
            self.__insYaml(f'volEnvLoop:','++')
            loop = self.huTrack.instrumentData[instrument].volumeEnvLoopPosition
            loop = (loop,-1)[loop == 255]
            self.__insYaml(f'{loop}','--')
            self.__insYaml(f'volEnvData:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].volumeEnv}','--')
            self.__insYaml('')

            self.__insYaml(f'#...........................................')
            self.__insYaml(f'# Arpeggio Envelope')
            self.__insYaml('')
            self.__insYaml(f'arpEnvMode:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].arpeggioEnvMode}','--')
            self.__insYaml(f'arpEnvSize:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].arpeggioEnvLength}','--')
            self.__insYaml(f'arpEnvLoop:','++')
            loop = self.huTrack.instrumentData[instrument].arpeggioEnvLoopPosition
            loop = (loop,-1)[loop == 255]
            self.__insYaml(f'{loop}','--')
            self.__insYaml(f'arpEnvData:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].arpeggioEnv}','--')
            self.__insYaml('')

            self.__insYaml(f'#...........................................')
            self.__insYaml(f'# Waveform Envelope')
            self.__insYaml('')
            self.__insYaml(f'waveFormEnvSize:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].wavetableEnvLength}','--')
            self.__insYaml(f'waveFormEnvLoop:','++')
            loop = self.huTrack.instrumentData[instrument].wavetableEnvLoopPosition
            loop = (loop,-1)[loop == 255]
            self.__insYaml(f'{loop}','--')
            self.__insYaml(f'waveFormEnvData:','++')
            self.__insYaml(f'{self.huTrack.instrumentData[instrument].wavetableEnv}','--')
            self.__insYaml('','--')



        self.__indentReset()
        self.__insYaml('')
        self.__insYaml('')

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Waveform Data                                                                    .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('WaveformData:','++')
        self.__insYaml('')
        for wavetableNum in range(self.huTrack.wavetableLen):
            self.__insYaml(f'#.....................................................')
            self.__insYaml(f'# Waveform Data {wavetableNum}')
            self.__insYaml(f'{wavetableNum}:','++')
            self.__insYaml(f'{self.huTrack.wavetableData[wavetableNum]}','--')
            self.__insYaml('')


        self.__indentReset()
        self.__insYaml('')
        self.__insYaml('')

        self.__insYaml(f'##***********************************************************************************##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml(f'## Sample Data                                                                      .##')
        self.__insYaml(f'##...................................................................................##')
        self.__insYaml('')

        self.__insYaml('SampleData:','++')
        self.__insYaml('')

        for sample in range(self.huTrack.samplesLen):
            self.__insYaml(f'#.....................................................')
            self.__insYaml(f'# PCM {sample}')
            self.__insYaml(f'{sample}:','++')
            self.__insYaml(f'name: {self.huTrack.samples[sample].sampleName}')
            self.__insYaml(f'size: {self.huTrack.samples[sample].sampleSize}')
            self.__insYaml(f'rate: {RATE_TABLE[self.huTrack.samples[sample].sampleRate]}')
            self.__insYaml(f'pitch: {self.huTrack.samples[sample].samplePitch}')
            self.__insYaml(f'amp: {self.huTrack.samples[sample].sampleAmp}')
            self.__insYaml(f'depth: {self.huTrack.samples[sample].sampleDepth}')
            self.__insYaml(f'pceRate: {self.params["playback"]}')
            self.__insYaml(f'filter: {self.params["resampleFilter"]}')
            self.__insYaml('')

            self.__insYaml(f'pceData:','++')
            self.__insYaml(f'{self.huTrack.samples[sample].samplePCE}','--')
            self.__insYaml(f'rawData:','++')
            self.__insYaml(f'{self.huTrack.samples[sample].sampleData}','--')
            self.__insYaml('','--')

        return self.hutrackMod

    def __indentInc(self):
        self.indentMod += 4

    def __indentInc(self):
        self.indentMod -= (0,4)[self.indentMod > 0]

    def __indentReset(self):
        self.indentMod = 0

    def __indentSet(self, indent):
        self.indentMod = indent*4

    def __insYaml(self, text, _indent=None):
        #pre indent
        if _indent == '+':
            self.__indentInc()
        elif _indent == '-':
            self.__indentInc()

        indent = ('',' '*self.indentMod)[text != '']
        self.hutrackMod.append(indent + text + '\n')

        #post indent
        if _indent == '++':
            self.__indentInc()
        elif _indent == '--':
            self.__indentInc()




class HuTrackExportPCE():


    def __init__(self, hutrack, params):
        self.huTrack = hutrack
        self.params  = params

    def process(self, hutrack=None, params=None):
        self.huTrack = (self.huTrack, hutrack)[hutrack is not None]
        self.params  = (self.params, params)[params is not None]
        self.writeHutrackFiles()
        return True

    def writeSongHeader(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.header.inc').replace("\\","/")
        self.songHeader = filename

        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            hu_out.write(f'\n\n\n')
            hu_out.write(f'.song\n')
            hu_out.write(f'  .dw .song.tables\n')
            hu_out.write(f'  .dw .song.tables.bank\n')

            hu_out.write(f'.songname\n')
            hu_out.write(f'  .db "{self.huTrack.songName}",0\n')
            hu_out.write(f'.author\n')
            hu_out.write(f'  .db "{self.huTrack.authorName}",0\n')
            hu_out.write(f'\n\n')

            hu_out.write(f'.song.tables\n')
            hu_out.write(f'  .dw .attributes\n')
            hu_out.write(f'  .dw .patternList.table\n')
            hu_out.write(f'  .dw .instrument.table\n')
            hu_out.write(f'  .dw .waveform.table\n')
            hu_out.write(f'  .dw .pattern.table\n')
            hu_out.write(f'  .dw .samples.table\n')
            hu_out.write(f'\n')
            hu_out.write(f'.song.tables.bank\n')
            hu_out.write(f'  .db bank(.attributes)\n')
            hu_out.write(f'  .db bank(.patternList.table)\n')
            hu_out.write(f'  .db bank(.instrument.table)\n')
            hu_out.write(f'  .db bank(.waveform.table)\n')
            hu_out.write(f'  .db bank(.pattern.table)\n')
            hu_out.write(f'  .db bank(.samples.table)\n')


            hu_out.write(f'\n\n')

            hu_out.write(f'.attributes\n\n')

            hu_out.write(f' ;NOTE: time base =  {self.huTrack.timeBase}\n')
            hu_out.write(f' ;NOTE: frame mode =  {self.huTrack.frameMode}\n')
            hu_out.write(f' ;NOTE: custom mode =  {self.huTrack.customMode}\n')
            hu_out.write(f'\n')

            hu_out.write(f'.attributes.tick1\n')
            hu_out.write(f'  .db {self.huTrack.tickTime1}\n')
            hu_out.write(f'.attributes.tick2\n')
            hu_out.write(f'  .db {self.huTrack.tickTime2}\n')
            hu_out.write(f'.attributes.rowLength\n')
            hu_out.write(f'  .db {self.huTrack.rowsPerPattern}\n')
            hu_out.write(f'.attributes.patternListLen\n')
            hu_out.write(f'  .db {self.huTrack.PatternMatrixLen}\n')
            hu_out.write(f'.attributes.instrumentLen\n')
            hu_out.write(f'  .db {self.huTrack.instrumentsLen}\n')
            hu_out.write(f'.attributes.waveformsLen\n')
            hu_out.write(f'  .db {self.huTrack.wavetableLen}\n')
            hu_out.write(f'.attributes.samplesLen\n')
            hu_out.write(f'  .db {self.huTrack.samplesLen}\n')
            hu_out.write(f'\n\n')



    def writeInstruments(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.instrMatrix.inc').replace("\\","/")
        self.instrMatrix = filename

        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'.instrument.table\n')
            for instrument in range(self.huTrack.instrumentsLen):
                hu_out.write(f'  .dw .instrument.{str(instrument)}\n')
            hu_out.write(f'\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.instrData.inc').replace("\\","/")
        self.instrData = filename

        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            for instrument in range(self.huTrack.instrumentsLen):
                hu_out.write(f'\n\n')
                hu_out.write(f';###########################################################################\n')
                hu_out.write(f'.instrument.{str(instrument)}\n')
                hu_out.write(f'; name {self.huTrack.instrumentData[instrument].name}\n')
                hu_out.write(f'; mode {self.huTrack.instrumentData[instrument].mode}\n')
                hu_out.write(f'\n')
                hu_out.write(f'.instrument.{str(instrument)}.table\n')
                hu_out.write(f'  .dw .instrument.{str(instrument)}.volEnv\n')
                hu_out.write(f'  .dw .instrument.{str(instrument)}.arpEnv\n')
                hu_out.write(f'  .dw .instrument.{str(instrument)}.waveFormEnv\n')


                hu_out.write(f'\n')
                hu_out.write(f';........................\n')
                hu_out.write(f'.instrument.{str(instrument)}.volEnv\n')
                hu_out.write(f'\n')
                hu_out.write(f'.instrument.{str(instrument)}.volEnv.size\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].volumeEnvLength)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.volEnv.loop\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].volumeEnvLoopPosition)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.volEnv.data\n')
                self.writeArrayAs_DB_fourInRow(hu_out, self.huTrack.instrumentData[instrument].volumeEnv)
                hu_out.write(f'\n')

                hu_out.write(f'\n')
                hu_out.write(f';........................\n')
                hu_out.write(f'.instrument.{str(instrument)}.arpEnv\n')
                hu_out.write(f'\n')
                hu_out.write(f'.instrument.{str(instrument)}.arpEnv.mode\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].arpeggioEnvMode)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.arpEnv.size\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].arpeggioEnvLength)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.arpEnv.loop\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].arpeggioEnvLoopPosition)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.arpEnv.data\n')
                self.writeArrayAs_DB_fourInRow(hu_out, self.huTrack.instrumentData[instrument].arpeggioEnv)
                hu_out.write(f'\n')


                hu_out.write(f'\n')
                hu_out.write(f';........................\n')
                hu_out.write(f'.instrument.{str(instrument)}.waveFormEnv\n')
                hu_out.write(f'\n')
                hu_out.write(f'.instrument.{str(instrument)}.waveFormEnv.size\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].wavetableEnvLength)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.waveFormEnv.loop\n')
                hu_out.write(f'  .db {str(self.huTrack.instrumentData[instrument].wavetableEnvLoopPosition)}\n')
                hu_out.write(f'.instrument.{str(instrument)}.waveFormEnv.data\n')
                self.writeArrayAs_DB_fourInRow(hu_out, self.huTrack.instrumentData[instrument].wavetableEnv)
                hu_out.write(f'\n')

            hu_out.write(f'\n\n')

    def writePatterns(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.patternMatrix.inc').replace("\\","/")
        self.patternMatrix = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'.patternList.table\n')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f'  .dw .patternList.chan{str(channel)}\n')
            hu_out.write(f'\n')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f'.patternList.chan{str(channel)}\n')
                for patternNum in range(self.huTrack.PatternMatrixLen):
                    hu_out.write(f'  .db {self.huTrack.PatternMatrixCompressed[channel][patternNum]}\n')

            hu_out.write(f'\n\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.patternData.inc').replace("\\","/")
        self.patternData = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Pattern tables
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'.pattern.table\n')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f'  .dw .pattern.table.chan{channel}\n')
            hu_out.write(f'\n\n')

            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f'  .db bank(.pattern.table.chan{channel})\n')
            hu_out.write(f'\n\n')

            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f';.....................................................\n')
                hu_out.write(f'.pattern.table.chan{channel}\n')
                for pattern in set(self.huTrack.PatternMatrixCompressed[channel]):
                    hu_out.write(f'  .dw .pattern.table.chan{channel}.pattern{pattern}\n')
                hu_out.write(f'\n\n')
                hu_out.write(f';###########################################################################\n')
                hu_out.write(f'\n\n')

            # Pattern data
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f';........................................................................\n')
                hu_out.write(f';........................................................................\n')
                hu_out.write(f'\n')
                for pattern in set(self.huTrack.PatternMatrixCompressed[channel]):
                    hu_out.write(f';......................................\n')
                    hu_out.write(f'.pattern.table.chan{channel}.pattern{pattern}\n')
                    hu_out.write(f'\n')
                    for row in self.huTrack.patternData[channel][pattern].patternData:

                        byteNum = 0
                        for byte in row:
                            if byteNum == 0:
                                hu_out.write(f'  .db ${hex(byte).split("0x")[1]}')
                            else:
                                hu_out.write(f', ${hex(byte).split("0x")[1]}')
                            byteNum += 1
                        hu_out.write(f'\n')
                    hu_out.write(f'\n\n')
            hu_out.write(f'\n\n')


    def writeWaveforms(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.wfMatrix.inc').replace("\\","/")
        self.wfMatrix = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            # waveform table
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'.waveform.table\n')
            hu_out.write(f'\n')
            for wavetableNum in range(self.huTrack.wavetableLen):
                hu_out.write(f'  .dw .waveform.{str(wavetableNum)}\n')
            hu_out.write(f'\n\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.wfData.inc').replace("\\","/")
        self.wfData = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            # waveform data
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            for wavetableNum in range(self.huTrack.wavetableLen):
                hu_out.write(f';.....................................................\n')
                hu_out.write(f'.waveform.{str(wavetableNum)}\n')
                self.writeArrayAs_DB_fourInRow(hu_out, self.huTrack.wavetableData[wavetableNum])
                hu_out.write(f'\n')
            hu_out.write(f'\n\n')

    def writePCMs(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.pcmMatrix.inc').replace("\\","/")
        self.pcmMatrix = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Sample table
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'\n')
            hu_out.write(f'.samples.table\n\n')
            hu_out.write(f'  ; offset to sample bank table.\n')
            hu_out.write(f'  .dw ${hex(self.huTrack.samplesLen*2).split("0x")[1]}\n')
            hu_out.write(f'\n')
            hu_out.write(f';.........................\n\n')
            for sample in range(self.huTrack.samplesLen):
                hu_out.write(f'  .dw .sample{sample}\n')
            hu_out.write(f'\n')
            hu_out.write(f';.........................\n\n')
            for sample in range(self.huTrack.samplesLen):
                hu_out.write(f'  .db bank(.sample{sample})\n')
            hu_out.write(f'\n\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.pcmData.inc').replace("\\","/")
        self.pcmData = filename
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Sample data
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'\n')
            for sample in range(self.huTrack.samplesLen):
                if sample > 0:
                    hu_out.write(f'  .bank (bank(.sample{sample-1}.end))\n')
                    hu_out.write(f'  .org $4000 + (* & $1fff)\n')
                hu_out.write(f'.sample{sample}\n')
                hu_out.write(f'  ; name = {self.huTrack.samples[sample].sampleName}\n')
                hu_out.write(f'  ; size = {self.huTrack.samples[sample].sampleSize}\n')
                hu_out.write(f'  ; rate = {RATE_TABLE[self.huTrack.samples[sample].sampleRate]}\n')
                hu_out.write(f'  ; pitch = {self.huTrack.samples[sample].samplePitch}\n')
                hu_out.write(f'  ; amp = {self.huTrack.samples[sample].sampleAmp}\n')
                hu_out.write(f'  ; depth = {self.huTrack.samples[sample].sampleDepth}\n')
                hu_out.write(f'\n')
                self.writePCMData(hu_out, self.huTrack.samples[sample], base=16)
                hu_out.write(f'\n')
                hu_out.write(f'  .db $80\n\n')
                hu_out.write(f'.sample{sample}.end\n')


            hu_out.write(f'\n\n')

    def writeHutrackFiles(self):

        os.makedirs(os.path.join(self.params['destinationPath'],f'{self.params["subFolder"]}'), exist_ok=True)

        self.writeSongHeader()
        self.writeInstruments()
        self.writePatterns()
        self.writeWaveforms()
        self.writePCMs()


        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.song.inc')
        includePath = ("",self.params["includePath"]+"/")[self.params["includePath"] != ""]
        with open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
          hu_out.write(f'  .include "{includePath}{self.songHeader}"\n')
          hu_out.write(f'  .include "{includePath}{self.instrMatrix}"\n')
          hu_out.write(f'  .include "{includePath}{self.instrData}"\n')
          hu_out.write(f'  .include "{includePath}{self.patternMatrix}"\n')
          hu_out.write(f'  .include "{includePath}{self.patternData}"\n')
          hu_out.write(f'  .include "{includePath}{self.wfMatrix}"\n')
          hu_out.write(f'  .include "{includePath}{self.wfData}"\n')
          hu_out.write(f'  .include "{includePath}{self.pcmMatrix}"\n')
          hu_out.write(f'  .include "{includePath}{self.pcmData}"\n')

        # Write the raw data out.. for debug purposes
        if self.params['debug']:
            dmf = self.dmf.getDMF()
            with open(os.path.join(self.params['destinationPath'],f'{self.params["subFolder"]}',f'{self.params["songName"]}.debug.txt'), 'w') as fileout:
                column = 0
                for i in range(len(dmf)):
                    outByte = hex(dmf[i]).split("0x")[1]
                    outByte = f'{("","0")[len(outByte)==1]}{outByte}'
                    fileout.write(f'{outByte}')
                    column += 1
                    fileout.write(('','\n')[column % 16 == 0 and column > 0])

            with open(os.path.join(self.params['destinationPath'],f'{self.params["subFolder"]}',f'{self.params["songName"]}.debug.bin'), 'wb') as fileout:
                fileout.write(bytearray(dmf))

        return True


    def writePCMData(self, hu_out, sampleObj, base=10):

        if self.params['debug']:
            filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.{sampleObj.sampleNum}.5bit.bin').replace("\\","/")
            with open(os.path.join(self.params['destinationPath'],filename),'wb') as fout:
                fout.write(bytearray(sampleObj.samplePCE))

        hu_out.write(f'  ; size\n')
        hu_out.write(f'  .dw {len(sampleObj.samplePCE)}\n')
        hu_out.write(f'\n')
        hu_out.write(f'  ; data\n')

        self.writeArrayAs_DB_fourInRow(hu_out, sampleObj.samplePCE, base=base)


    def writeArrayAs_DB_fourInRow(self, hu_out, array, base=10):
        rowCounter = 0
        newLine = '\n'
        for i in range(len(array)):
            hu_out.write( (f'  .db ',', ')[rowCounter != 0])
            digit_str = ('$'+hex(array[i]).split('0x')[1], str(array[i]))[base == 10]
            hu_out.write(f"{digit_str}{('',newLine)[rowCounter == 3]}")
            rowCounter = (rowCounter + 1) % 4
        hu_out.write( (f'\n', '')[rowCounter == 3])

