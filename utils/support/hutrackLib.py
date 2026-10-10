
import os

from support.huTrackBase import HuTrackContainer, RATE_TABLE
from support.dmfReader import ConvertDeflemask
from support.outputBundle import OutputBundle


class HuTrackLib():

    def __init__(self, hutrack=None, params=None):
        self.huTrack = hutrack
        self.params  = params

    def importDmf(self):
        print("\n\n import params",self.params,"\n")
        convertDeflemask = ConvertDeflemask(self.params)
        result, hutrack = convertDeflemask.process()
        return result, hutrack

    def exportHuTrackTextFile(self):
        pceModule = HuTrackExportPCE(hutrack=self.huTrack, params=self.params)
        print("\n\n export params", self.params,"\n")
        pceModule.process()
        del pceModule
        return True

    def exportPceHuTrackFile(self):


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

    def __indentDec(self):
        self.indentMod -= (0,4)[self.indentMod > 0]

    def __indentReset(self):
        self.indentMod = 0

    def __insYaml(self, text, _indent=None):
        #pre indent
        if _indent == '+':
            self.__indentInc()
        elif _indent == '-':
            self.__indentDec()

        indent = ('',' '*self.indentMod)[text != '']
        self.hutrackMod.append(indent + text + '\n')

        #post indent
        if _indent == '++':
            self.__indentInc()
        elif _indent == '--':
            self.__indentDec()




class HuTrackExportPCE():


    def __init__(self, hutrack, params):
        self.huTrack = hutrack
        self.params  = params

    def process(self, hutrack=None, params=None):
        self.huTrack = (self.huTrack, hutrack)[hutrack is not None]
        self.params  = (self.params, params)[params is not None]
        if self.params.get('bitpackPCM') or self.params.get('alignPCM256') or self.params.get('bitDepth','5bit')!='5bit':
            raise ValueError('HuTrack exports unpacked 5-bit PCM; packing, alignment and other bit depths are not implemented')
        self.writeHutrackFiles()
        return True

    def writeLocation(self, output, label):
        # Rebase CPU addresses without changing the physical output position.
        # Every independently addressed music object fits a two-bank window.
        if self.banked:
            output.write('  .page 2\n')
        output.write(label + '\n')

    def writePointer(self, output, label):
        output.write(f'  .dw {label}\n')
        if self.banked:
            output.write(f'  .db bank({label})\n')

    def writeSongHeader(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.header.inc').replace("\\","/")
        self.songHeader = filename

        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            hu_out.write(f'\n\n\n')
            self.writeLocation(hu_out, '.song')
            if self.banked:
                hu_out.write('  .dw 0 ; banked-format marker\n  .db 1 ; format revision\n')
                self.writePointer(hu_out, '.song.tables')
            else:
                hu_out.write('  .dw .song.tables\n  .dw .song.tables.bank\n')

            songname = (self.huTrack.songName,'')[ self.params['no_songname'] ]
            authorname = (self.huTrack.authorName,'')[ self.params['no_author'] ]
            for label, text in (('songname',songname),('author',authorname)):
                hu_out.write(f'.{label}\n')
                # Runtime/C buffers hold 47 text bytes and one terminator.
                # DMF fields are length-prefixed: an embedded NUL must also
                # discard the suffix, or it becomes the next field at runtime.
                data = bytes(ord(c) & 255 for c in text).split(b'\0', 1)[0]
                if len(data) > 47:
                    print(f' - Warning: {label} truncated to 47 bytes for HuTrack metadata')
                data = list(data[:47]) + [0]
                for start in range(0,len(data),32):
                    hu_out.write('  .db ' + ','.join(str(value) for value in data[start:start+32]) + '\n')

            hu_out.write(f'\n\n')
            self.writeLocation(hu_out, '.song.tables')
            for label in ('.attributes','.patternList.table','.instrument.table','.waveform.table','.pattern.table','.samples.table'):
                self.writePointer(hu_out,label)
            hu_out.write(f'\n')
            if not self.banked:
                hu_out.write(f'.song.tables.bank\n')
                hu_out.write(f'  .db bank(.attributes)\n')
                hu_out.write(f'  .db bank(.patternList.table)\n')
                hu_out.write(f'  .db bank(.instrument.table)\n')
                hu_out.write(f'  .db bank(.waveform.table)\n')
                hu_out.write(f'  .db bank(.pattern.table)\n')
                hu_out.write(f'  .db bank(.samples.table)\n')


            hu_out.write(f'\n\n')

            self.writeLocation(hu_out, '.attributes')
            hu_out.write('  ; Extended attributes: marker, initial arp ticks, legacy volume slides\n')
            hu_out.write(f'  .db 0,{getattr(self.huTrack, "legacyArpSpeed", 1)},{int(getattr(self.huTrack, "dmfVersion", 24) <= 24)}\n')

            hu_out.write(f' ;NOTE: time base =  {self.huTrack.timeBase}\n')
            hu_out.write(f' ;NOTE: frame mode =  {self.huTrack.frameMode}\n')
            hu_out.write(f' ;NOTE: custom mode =  {self.huTrack.customMode}\n')
            hu_out.write(f'\n')

            hu_out.write(f'.attributes.tick1\n')
            hu_out.write(f'  .db {self.huTrack.tickTime1}\n')
            hu_out.write(f'.attributes.tick2\n')
            hu_out.write(f'  .db {self.huTrack.tickTime2}\n')
            hu_out.write(f'.attributes.rowLength\n')
            hu_out.write(f'  .db {self.huTrack.rowsPerPattern & 255}\n')
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

        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            self.writeLocation(hu_out, '.instrument.table')
            for instrument in range(self.huTrack.instrumentsLen):
                self.writePointer(hu_out,f'.instrument.{instrument}')
            hu_out.write(f'\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.instrData.inc').replace("\\","/")
        self.instrData = filename

        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            for instrument in range(self.huTrack.instrumentsLen):
                hu_out.write(f'\n\n')
                hu_out.write(f';###########################################################################\n')
                self.writeLocation(hu_out,f'.instrument.{instrument}')
                name = ''.join(c if c.isprintable() else ' ' for c in self.huTrack.instrumentData[instrument].name)
                hu_out.write(f'; name {name}\n')
                hu_out.write(f'; mode {self.huTrack.instrumentData[instrument].mode}\n')
                hu_out.write(f'\n')
                hu_out.write(f'.instrument.{str(instrument)}.table\n')
                for kind in ('volEnv','arpEnv','waveFormEnv'):
                    self.writePointer(hu_out,f'.instrument.{instrument}.{kind}')


                hu_out.write(f'\n')
                hu_out.write(f';........................\n')
                self.writeLocation(hu_out,f'.instrument.{instrument}.volEnv')
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
                self.writeLocation(hu_out,f'.instrument.{instrument}.arpEnv')
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
                self.writeLocation(hu_out,f'.instrument.{instrument}.waveFormEnv')
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
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            self.writeLocation(hu_out,'.patternList.table')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                self.writePointer(hu_out,f'.patternList.chan{channel}')
            hu_out.write(f'\n')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                self.writeLocation(hu_out,f'.patternList.chan{channel}')
                for patternNum in range(self.huTrack.PatternMatrixLen):
                    hu_out.write(f'  .db {self.huTrack.PatternMatrixCompressed[channel][patternNum]}\n')

            hu_out.write(f'\n\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.patternData.inc').replace("\\","/")
        self.patternData = filename
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Pattern tables
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            self.writeLocation(hu_out,'.pattern.table')
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                self.writePointer(hu_out,f'.pattern.table.chan{channel}')
            hu_out.write(f'\n\n')

            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f'  .db bank(.pattern.table.chan{channel})\n')
            hu_out.write(f'\n\n')

            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f';.....................................................\n')
                self.writeLocation(hu_out,f'.pattern.table.chan{channel}')
                for pattern in sorted(set(self.huTrack.PatternMatrixCompressed[channel])):
                    self.writePointer(hu_out,f'.pattern.table.chan{channel}.pattern{pattern}')
                hu_out.write(f'\n\n')
                hu_out.write(f';###########################################################################\n')
                hu_out.write(f'\n\n')

            # Pattern data
            totalSongdataBinsize = 0
            for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
                hu_out.write(f';........................................................................\n')
                hu_out.write(f';........................................................................\n')
                hu_out.write(f'\n')
                chanSongdataBinsize = 0
                for pattern in sorted(set(self.huTrack.PatternMatrixCompressed[channel])):
                    hu_out.write(f';......................................\n')
                    self.writeLocation(hu_out,f'.pattern.table.chan{channel}.pattern{pattern}')
                    hu_out.write(f'\n')
                    for row in self.huTrack.patternData[channel][pattern].patternData:
                        byteNum = 0
                        chanSongdataBinsize += len(row)
                        for byte in row:
                            if byteNum == 0:
                                hu_out.write(f'  .db ${hex(byte).split("0x")[1]}')
                            else:
                                hu_out.write(f', ${hex(byte).split("0x")[1]}')
                            byteNum += 1
                        hu_out.write(f'\n')
                    hu_out.write(f'\n\n')
                print(f'  - Chan {channel} song data in binary size: {chanSongdataBinsize}')
                totalSongdataBinsize += chanSongdataBinsize
            hu_out.write(f'\n\n')
            print(f'  - Total channel song data in binary size: {totalSongdataBinsize}')


    def writeWaveforms(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.wfMatrix.inc').replace("\\","/")
        self.wfMatrix = filename
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            # waveform table
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            self.writeLocation(hu_out,'.waveform.table')
            hu_out.write(f'\n')
            for wavetableNum in range(self.huTrack.wavetableLen):
                self.writePointer(hu_out,f'.waveform.{wavetableNum}')
            hu_out.write(f'\n\n')

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.wfData.inc').replace("\\","/")
        self.wfData = filename
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
            # waveform data
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            for wavetableNum in range(self.huTrack.wavetableLen):
                hu_out.write(f';.....................................................\n')
                self.writeLocation(hu_out,f'.waveform.{wavetableNum}')
                self.writeArrayAs_DB_fourInRow(hu_out, self.huTrack.wavetableData[wavetableNum])
                hu_out.write(f'\n')
            hu_out.write(f'\n\n')

    def writePCMs(self):

        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.pcmMatrix.inc').replace("\\","/")
        self.pcmMatrix = filename
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Sample table
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'\n')
            self.writeLocation(hu_out,'.samples.table')
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
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:

            # Sample data
            hu_out.write(f'\n\n')
            hu_out.write(f';###########################################################################\n')
            hu_out.write(f'\n')
            for sample in range(self.huTrack.samplesLen):
                if sample > 0 and not self.banked:
                    hu_out.write(f'  .bank (bank(.sample{sample-1}.end))\n')
                    hu_out.write(f'  .org $4000 + (* & $1fff)\n')
                self.writeLocation(hu_out,f'.sample{sample}')
                safeName=self.huTrack.samples[sample].sampleName.replace('\r',' ').replace('\n',' ')
                hu_out.write(f'  ; name = {safeName}\n')
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
        self.outputs = OutputBundle()
        self._writeHutrackFiles()
        self.outputs.commit()
        return True

    def _writeHutrackFiles(self):

        # These strings become assembler include paths. Reject unusable names
        # before creating the output directory or leaving partial song files.
        name = self.params['songName']
        if not name or name in ('.', '..') or any(c in name for c in '/\\\r\n"'):
            raise ValueError('Song name must be a file name without directories, quotes or line breaks')
        for key in ('subFolder', 'includePath'):
            if any(c in self.params[key] for c in '\r\n"'):
                raise ValueError(f'Invalid assembly include path in {key}')
        self.banked = not self.params.get('legacy_format',False)

        self.writeSongHeader()
        self.writeInstruments()
        self.writePatterns()
        self.writeWaveforms()
        self.writePCMs()


        filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.song.inc')
        includePath = ("",self.params["includePath"]+"/")[self.params["includePath"] != ""]
        with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'w') as hu_out:
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
            dmf = getattr(self.huTrack, 'rawDMF', [])
            with self.outputs.open(os.path.join(self.params['destinationPath'],f'{self.params["subFolder"]}',f'{self.params["songName"]}.debug.txt'), 'w') as fileout:
                column = 0
                for i in range(len(dmf)):
                    outByte = hex(dmf[i]).split("0x")[1]
                    outByte = f'{("","0")[len(outByte)==1]}{outByte}'
                    fileout.write(f'{outByte}')
                    column += 1
                    fileout.write(('','\n')[column % 16 == 0 and column > 0])

            with self.outputs.open(os.path.join(self.params['destinationPath'],f'{self.params["subFolder"]}',f'{self.params["songName"]}.debug.bin'), 'wb') as fileout:
                fileout.write(bytearray(dmf))

        return True


    def writePCMData(self, hu_out, sampleObj, base=10):

        if self.params['debug']:
            if hasattr(sampleObj, 'sample8bit'):
                filename = os.path.join(self.params['subFolder'], f'{self.params["songName"]}.{sampleObj.sampleNum}.8bit.bin')
                with self.outputs.open(os.path.join(self.params['destinationPath'], filename), 'wb') as fout:
                    fout.write(sampleObj.sample8bit)
            filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.{sampleObj.sampleNum}.5bit.bin').replace("\\","/")
            with self.outputs.open(os.path.join(self.params['destinationPath'],filename),'wb') as fout:
                fout.write(bytearray(sampleObj.samplePCE))

        # The driver skips this historical word and reads until the control
        # marker. Keep its low 16 bits for old readers; streams may exceed 64KB.
        hu_out.write(f'  ; size {len(sampleObj.samplePCE)} (informational low 16 bits)\n')
        hu_out.write(f'  .dw {len(sampleObj.samplePCE) & 65535}\n')
        hu_out.write(f'\n')
        hu_out.write(f'  ; data\n')

        if self.banked:
            # A single PCM stream may span many banks. Rebase each small chunk
            # so PCEAS never wraps its CPU address from $ffff to $0000.
            for start in range(0,len(sampleObj.samplePCE),4096):
                hu_out.write('  .page 2\n')
                self.writeArrayAs_DB_fourInRow(hu_out,sampleObj.samplePCE[start:start+4096],base=base)
        else:
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

