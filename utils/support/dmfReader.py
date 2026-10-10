
import numpy
import os
import resampy
import zlib

from support.huTrackBase import HuTrackContainer, RATE_VAL, PITCH_VAL


PCE_VER       = 0x05
VER_IDX       = 16
PLATFORM_IDX  = 17
SONG_INFO_IDX = 18


class DMFcontainer():

    def __init__(self, val):
        self.index = val
        self.contents = None

    def setDMF(self, dmf):
        self.contents = dmf

    def getDMF(self):
        return self.contents

    def setIndex(self, val):
        self.index = val



class ConvertDeflemask():

    def __init__(self, runOptions=None):
        self.params     = runOptions
        self.songInfo   = ''
        self.AuthorInfo = ''
        self.dmf     = DMFcontainer(0)
        self.huTrack = None
        self.warnings = []

    def process(self, runOptions=None):
        try:
            return self._process(runOptions)
        except ValueError as error:
            print(f'\nError: {error}\n')
            self.huTrack = None
            return False, None

    def _process(self, runOptions=None):

        self.params = (self.params, runOptions)[runOptions is not None]
        self.huTrack = None
        self.warnings = []

        result = True

        # Gonna need a separate function to check params more in depth
        if not self.params or self.params == []:
            print(f'\nError: cannot process dmf conversion without valid params.\n\n')
            result = False
        elif not self.readDMF():
            print(f'\nError: cannot access file {self.params["filein"]} contents.\n\n')
            result = False
        elif not self.checkHeaderString():
            print(f'\nError: file {self.params["filein"]} does not match deflemask signature string.\n\n')
            result = False
        elif not self.checkPlatform():
            print(f'\nError: deflemask platform is not PC-Engine.\n\n')
            result = False
        elif not self.decodeDMF():
            print(f'\nError: internal issue decoding dmf file.\n\n')
            result = False
        else:
            print(f'Successfully converted [ {self.params["filein"]} ] to hutrack song [ {self.params["songName"]} ].\n')

        return result, self.huTrack

    def decodeDMF(self):
        if len(self.dmf.contents) <= PLATFORM_IDX:
            raise ValueError('Truncated DMF header')
        self.version = int(self.dmf.contents[VER_IDX])
        if not 11 <= self.version <= 27:
            raise ValueError(f'Unsupported legacy DMF revision {self.version}; use Furnace to resave it')
        self.dmf.setIndex(SONG_INFO_IDX)
        self.initHutrackModule(*self.getSongInfo())
        self.huTrack.rawDMF = list(self.dmf.getDMF())
        if self.dmf.index != len(self.dmf.contents):
            # Bundled original DMFs include a zero padding byte after samples.
            # Furnace tolerates trailing data; retain strict nonzero rejection
            # so a genuinely misaligned intermediate layout is still visible.
            if any(self.dmf.contents[self.dmf.index:]):
                raise ValueError(f'Trailing or misaligned DMF data at byte {self.dmf.index}')
            self.warn('Ignoring zero padding after the DMF sample section')
            self.dmf.index = len(self.dmf.contents)

        return True

    def initHutrackModule(self, songname, author):

        # skip over 'highlight' bytes A and B. I think they're editor related.
        if self.version > 12:
            self.getNextByte()
            self.getNextByte()

        timebase  = self.getNextByte()
        timetick1 = self.getNextByte()
        timetick2 = self.getNextByte()
        mode      = self.getNextByte()
        customHZ  = self.getNextByte()
        # We're not supporting custom Hz mode, so skip over its operands
        skip = self.getNextByte()
        skip = self.getNextByte()
        skip = self.getNextByte()

        rowLen = self.getNextDword() if self.version >= 24 else self.getNextByte()
        if not 1 <= rowLen <= 256:
            raise ValueError(f'Unsupported DMF pattern length: {rowLen} (expected 1..256)')
        PatternLen = self.getNextByte()
        if not 1 <= PatternLen <= 127:
            raise ValueError(f'Unsupported DMF order count: {PatternLen} (expected 1..127)')

        arp_speed = self.getNextByte() if self.version < 20 else 1
        patternMatrix = []
        for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
            orders = []
            for order in range(PatternLen):
                pattern = self.getNextByte()
                if pattern > 127:
                    raise ValueError(f'Invalid pattern number {pattern} on channel {channel}')
                orders.append(pattern)
                if self.version > 24:
                    self.getString()  # editor pattern name
            patternMatrix.append(orders)

        instrumentsLen = self.getNextByte()
        if instrumentsLen > 128:
            raise ValueError("HuTrack instrument pointer tables support at most 128 instruments")
        self.huTrack = HuTrackContainer(PatternLen, instrumentsLen, rowLen)

        self.huTrack.authorName = author
        self.huTrack.songName   = songname
        self.huTrack.timeBase   = timebase + 1
        self.huTrack.tickTime1  = timetick1 * self.huTrack.timeBase
        self.huTrack.tickTime2  = timetick2 * self.huTrack.timeBase
        self.huTrack.frameMode  = mode
        self.huTrack.customMode = customHZ
        self.huTrack.PatternMatrix = patternMatrix
        self.huTrack.legacyArpSpeed = max(1, arp_speed)
        self.huTrack.dmfVersion = self.version
        if customHZ:
            self.warn('Custom Hz requires the application to call HuTrack at that tick rate; the VBlank hook does not retime itself')
        elif mode == 0:
            self.warn('PAL DMF requires 50 Hz music calls; the application must supply the matching tick rate')
        if not (1 <= self.huTrack.tickTime1 <= 255 and 1 <= self.huTrack.tickTime2 <= 255):
            raise ValueError('HuTrack row speeds must fit in 1..255 ticks')

        self.getInstrumentData()
        self.getWavetableData()
        self.getPatternData()
        self.getPCMdata()

        if self.huTrack.timeBase > 1:
            print(f" - Warning: time base {self.huTrack.timeBase} is not set to 1. Re-adjusting speed timings.")

    def getInstrumentData(self):

        for i in range(self.huTrack.instrumentsLen):
            newInstr = HuTrackContainer.Instrument()

            # name and mode
            strLen = self.getNextByte()
            newInstr.name = ''.join([chr(self.getNextByte()) for i in range(strLen)])
            newInstr.mode = self.getNextByte()

            # Currently, only supporting standard mode of 0
            if newInstr.mode != 0:
                raise ValueError(f'Instrument {i}: FM instruments are not supported by the PCE converter')

            # volume
            volEnvSize = self.getNextByte()
            volEnvLoop = 0xff
            volEnv = [self.getMacroValue() for _ in range(volEnvSize)]
            if any(value > 31 for value in volEnv):
                raise ValueError(f'Instrument {i}: PCE volume envelope values must be 0..31')
            if volEnvSize > 0:
                volEnvLoop = self.getNextByte()
            newInstr.volumeEnv       = volEnv
            newInstr.volumeEnvLength = volEnvSize
            newInstr.volumeEnvLoopPosition = volEnvLoop
            if volEnvLoop >= volEnvSize and volEnvLoop != 255:
                print(f' - Error in file: Instrument #{i} volume envelope loop position {volEnvLoop} outside of size {volEnvSize}. Changing loop {volEnvLoop} to {volEnvSize -1}')
                newInstr.volumeEnvLoopPosition = volEnvSize - 1

            # arpeggio
            arpEnvSize = self.getNextByte()
            arpEnvLoop = 0xff
            # Arp envelope data is actually signed for normal mode, so we need the whole dword. It's also offset by 12 in normal mode. So correct for that.
            arpEnv = [ self.getMacroValue() for i in range(arpEnvSize) ]
            if arpEnvSize > 0:
                arpEnvLoop = self.getNextByte()
            newInstr.arpeggioEnvLength = arpEnvSize
            newInstr.arpeggioEnvLoopPosition = arpEnvLoop
            newInstr.arpeggioEnvMode = self.getNextByte() if self.version > 15 else 0
            if newInstr.arpeggioEnvMode not in (0, 1):
                raise ValueError(f'Instrument {i}: invalid arpeggio mode')
            arpEnv = [value - 0x100000000 if value >= 0x80000000 else value for value in arpEnv]
            if newInstr.arpeggioEnvMode == 0:
                arpEnv = [value - 12 for value in arpEnv]
                if any(not -128 <= value <= 127 for value in arpEnv):
                    raise ValueError(f'Instrument {i}: relative arpeggios must fit signed bytes')
            elif any(not 0 <= value <= 195 for value in arpEnv):
                raise ValueError(f'Instrument {i}: fixed arpeggio notes must be 0..195')
            newInstr.arpeggioEnv = [value & 255 for value in arpEnv]

            if arpEnvLoop >= arpEnvSize and arpEnvLoop != 255:
                print(f' - Error in file: Instrument #{i} arpeggio envelope loop position {arpEnvLoop} outside of size {arpEnvSize}. Changing loop {arpEnvLoop} to {arpEnvSize -1}')
                newInstr.arpeggioEnvLoopPosition = arpEnvSize - 1


            # An intermediate legacy layout included this field without a
            # version increment. Consume it even though PCE playback ignores it.
            noiseEnvSize = self.getNextByte()
            noiseEnvLoop = 0xff
            noiseEnv = [ self.getMacroValue() & 255 for i in range(noiseEnvSize) ]
            if noiseEnvSize > 0:
                noiseEnvLoop = self.getNextByte()
            newInstr.noiseEnv       = noiseEnv
            newInstr.noiseEnvLength = noiseEnvSize
            newInstr.noiseEnvLoopPosition = noiseEnvLoop

            #wavetable
            waveEnvSize = self.getNextByte()
            waveEnvLoop = 0xff
            waveEnv = [self.getMacroValue() for _ in range(waveEnvSize)]
            if waveEnvSize > 0:
                waveEnvLoop = self.getNextByte()
            newInstr.wavetableEnv       = waveEnv
            newInstr.wavetableEnvLength = waveEnvSize
            newInstr.wavetableEnvLoopPosition = waveEnvLoop
            if waveEnvLoop >= waveEnvSize and waveEnvLoop != 255:
                print(f' - Error in file: Instrument #{i} waveform envelope loop position {waveEnvLoop} outside of size {waveEnvSize}. Changing loop {waveEnvLoop} to {waveEnvSize -1}')
                newInstr.wavetableEnvLoopPosition = waveEnvSize - 1

            # Add new instrument to list
            self.huTrack.instrumentData.append(newInstr)

        if not self.huTrack.instrumentData:
            # A note without an instrument uses an empty instrument in Furnace.
            # The assembly engine still needs a valid instrument-zero pointer.
            empty = HuTrackContainer.Instrument()
            for field in ('volume', 'arpeggio', 'noise', 'wavetable'):
                setattr(empty, field + 'Env', [])
                setattr(empty, field + 'EnvLoopPosition', 255)
            self.huTrack.instrumentData.append(empty)
            self.huTrack.instrumentsLen = 1


    def getPatternData(self):
        self.huTrack.patternData       = []
        self.huTrack.uncompPatternData = []
        for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
            self.huTrack.patternData.append([])
            self.huTrack.uncompPatternData.append([])
            self.huTrack.PatternMatrixCompressed[channel] = []
            numFX = self.getNextByte()
            if not 1 <= numFX <= 4:
                raise ValueError(f'Channel {channel}: expected 1..4 effect columns, got {numFX}')
            uniquePattern = 0
            for pattern in range(self.huTrack.PatternMatrixLen):
                newPattern    = HuTrackContainer.Pattern()
                rawNewPattern = HuTrackContainer.Pattern()
                newPattern.fxLen    = numFX
                rawNewPattern.fxLen = numFX
                #                   note + octave + vol + FX's + instr
                newPattern.rowLen    = 1 + 1 + 1 + (numFX * 2) + 1
                rawNewPattern.rowLen = 1 + 1 + 1 + (numFX * 2) + 1
                checkEmptyRow = 0
                for row in range(self.huTrack.rowsPerPattern):
                    rowEntry    = []
                    rawRowEntry = []

                    # NOTE: 'C' or note 12 is a special case; it needs the octave increased
                    # note
                    octaveDelta = 0
                    note = self.getNextByte()
                    rawRowEntry.append(note)
                    note = (note, note + 1)[note > 0 and note < 13]
                    octaveDelta = (0,1)[note == 13]
                    note = (note, 1)[note == 13]
                    rowEntry.append(note)
                    skip = self.getNextByte()

                    # octave
                    octave = self.getNextByte()
                    if octave >= 128:
                        octave -= 256
                    rawRowEntry.append(octave)
                    octave = octaveDelta + octave
                    if note == 0 and octave != 0:
                        note = 1
                        rowEntry[0] = note
                    rowEntry.append(octave)
                    skip = self.getNextByte()

                    # volume
                    volume = self.getNextWord()
                    if volume != 0xffff and not 0 <= volume <= 31:
                        raise ValueError(f'Channel {channel}, row {row}: PCE volume must be 0..31')
                    rowEntry.append(volume)
                    rawRowEntry.append(volume)

                    for fx in range(numFX):
                        # FX code
                        fxEntry = self.getNextByte()
                        fxEntry |= self.getNextByte() << 8
                        supported = set(range(0x0e)) | {0x0f,0x10,0x11,0x12,0x13,0x17} | set(range(0xe0,0xf0))
                        if fxEntry != 0xffff and fxEntry not in supported:
                            self.warn(f'Effect {fxEntry:02X} is unsupported and will be ignored')
                        if fxEntry != 0xffff and fxEntry > 255:
                            raise ValueError(f'Channel {channel}, row {row}: effect code exceeds one byte')
                        rowEntry.append(fxEntry)
                        rawRowEntry.append(fxEntry)

                        # FX arg
                        fxArg = self.getNextByte()
                        fxArg |= self.getNextByte() << 8
                        rawRowEntry.append(fxArg)
                        if fxEntry == 0xe5 and fxArg != 0xffff and self.version < 20:
                            fxArg = 128 + int((fxArg - 128) / 4)
                        if (fxEntry == 0x09 or fxEntry == 0x0f) and fxArg != 0xffff:
                            fxArg *= self.huTrack.timeBase
                            if self.huTrack.timeBase != 1:
                                print(f' - Converting: fx {fxEntry} : arg {fxArg}')

                        if fxArg != 0xffff and not 0 <= fxArg <= 255:
                            raise ValueError(f'Channel {channel}, row {row}: effect argument exceeds one byte')
                        if fxEntry == 0x10 and fxArg != 0xffff and fxArg >= self.huTrack.wavetableLen:
                            raise ValueError(f'Channel {channel}, row {row}: invalid waveform {fxArg}')

                        rowEntry.append(fxArg)

                    # instr
                    instrument = self.getNextWord()
                    if instrument != 0xffff and not 0 <= instrument < self.huTrack.instrumentsLen:
                        raise ValueError(f'Channel {channel}, row {row}: invalid instrument {instrument}')
                    rowEntry.append(instrument)
                    rawRowEntry = rawRowEntry[:3] + [rowEntry[-1]] + rawRowEntry[3:]

                    #raw entry complete.. store it.
                    rawNewPattern.patternData.append(rawRowEntry)

                    if rowEntry[0] == 0 and rowEntry[1] == 0 and all(rowEntry[entry] == 0xffff for entry in range(2,len(rowEntry))):
                        checkEmptyRow += 1
                        if checkEmptyRow == 30:
                            newPattern.patternData.append([checkEmptyRow + 224])
                            checkEmptyRow = 0
                        elif checkEmptyRow > 0 and row+1 >= self.huTrack.rowsPerPattern:
                            newPattern.patternData.append([checkEmptyRow + 224])
                            checkEmptyRow = 0
                    else:
                        if checkEmptyRow > 0:
                            newPattern.patternData.append([checkEmptyRow + 224])
                            checkEmptyRow = 0

                        #compress data
                        mask = 0
                        mask |= (0,1)[rowEntry[0] > 0 or rowEntry[1] > 0] << 0
                        mask |= (0,1)[rowEntry[-1] != 0xffff ] << 2
                        mask |= (0,1)[rowEntry[2] != 0xffff ] << 3
                        mask |= (0,1)[rowEntry[3] != 0xffff ] << 4
                        mask |= (0,1)[rowEntry[4] != 0xffff ] << 5
                        mask |= (0,1)[ rowEntry[5:-1] != [] and any(fx != 0xffff for fx in rowEntry[5:-1]) ] << 6

                        compressedNote = (rowEntry[0] - 1) + (rowEntry[1]*12)
                        if rowEntry[0] != 100 and (mask & 1) and not 0 <= compressedNote < 84:
                            raise ValueError(f'Channel {channel}, row {row}: note outside compressed C0..B6 range')
                        compressedNote = (compressedNote, compressedNote + 128)[mask <= 1 and rowEntry[0] != 0]
                        compressedNote = (compressedNote, 224)[rowEntry[0] == 100]  # note cut
                        oldEntry = rowEntry[::]
                        rowEntry = []
                        if mask == 1:
                            # If only note, note+octave, or notecut in entry
                            rowEntry += [compressedNote]
                        else:
                            rowEntry += [mask]
                            if (mask & 0x01) > 0:
                                rowEntry += [compressedNote]
                            if (mask & 0x04) > 0:
                                rowEntry += [oldEntry[-1] & 0xff]
                            if (mask & 0x08) > 0:
                                rowEntry += [oldEntry[2] & 0xff]
                            if (mask & 0x10) > 0:
                                rowEntry += [oldEntry[3] & 0xff]
                            if (mask & 0x20) > 0:
                                rowEntry += [oldEntry[4] & 0xff]
                            if (mask & 0x40) > 0:
                                mask_extFX = 0
                                extFX_arry = []
                                for i in range(len(oldEntry[5:-1])):
                                    mask_extFX |= (0, 1 << i)[oldEntry[5:-1][i] != 0xffff]
                                    extFX_arry += ([], [oldEntry[5:-1][i]])[oldEntry[5:-1][i] != 0xffff]
                                rowEntry += [mask_extFX]
                                rowEntry += extFX_arry

                        newPattern.patternData.append(rowEntry)


                patternMatch = 0
                for prevPattern in self.huTrack.patternData[channel]:
                    if newPattern.compare(prevPattern):
                        break
                    patternMatch += 1

                if patternMatch >= len(self.huTrack.patternData[channel]):
                    self.huTrack.PatternMatrixCompressed[channel].append(uniquePattern)
                    self.huTrack.patternData[channel].append(newPattern)
                    self.huTrack.uncompPatternData[channel].append(rawNewPattern)
                    uniquePattern += 1
                else:
                    self.huTrack.PatternMatrixCompressed[channel].append(patternMatch)


    def getWavetableData(self):
        wavetableEntries = self.getNextByte() if self.version > 11 else 0
        if wavetableEntries > 128:
            raise ValueError('HuTrack waveform pointer tables support at most 128 waveforms')
        for i in range(wavetableEntries):
            wavetableDataSize = self.getNextDword()
            if wavetableEntries == 1 and wavetableDataSize == 0:
                break  # Furnace treats this historical empty-wave placeholder as no waves.
            if wavetableDataSize != 32:
                raise ValueError(f'PCE waveform {i} has {wavetableDataSize} values; expected 32')
            self.huTrack.wavetableData.append( [self.getMacroValue() & 31 for i in range(wavetableDataSize)] )
        if not self.huTrack.wavetableData:
            self.huTrack.wavetableData.append([15] * 32)  # Furnace's DMF null wave
        self.huTrack.wavetableLen = len(self.huTrack.wavetableData)
        for i, instrument in enumerate(self.huTrack.instrumentData):
            if any(not 0 <= value < self.huTrack.wavetableLen for value in instrument.wavetableEnv):
                raise ValueError(f'Instrument {i}: waveform envelope references a missing waveform')


    def getPCMdata(self):

        samplesLen = self.getNextByte()
        if samplesLen > 128:
            raise ValueError('HuTrack sample pointer tables support at most 128 samples')
        self.huTrack.samplesLen = samplesLen
        for sampleNum in range(samplesLen):

            newSample = HuTrackContainer.Sample()
            newSample.sampleSize   = self.getNextDword()
            newSample.sampleName   = self.getString() if self.version > 22 else ''
            newSample.sampleRate   = self.getNextByte()
            newSample.samplePitch  = self.getNextByte()
            newSample.sampleAmp    = self.getNextByte()
            newSample.sampleDepth  = self.getNextByte() if self.version > 21 else 16
            if newSample.sampleDepth not in (8, 16):
                newSample.sampleDepth = 16
            if not 1 <= newSample.sampleRate < len(RATE_VAL):
                raise ValueError(f'Sample {sampleNum}: invalid rate index')
            if not 0 <= newSample.samplePitch < len(PITCH_VAL):
                newSample.samplePitch = 5
            if newSample.sampleSize > (len(self.dmf.contents)-self.dmf.index)//2:
                raise ValueError(f'Sample {sampleNum}: truncated PCM data')
            if self.version >= 27:
                newSample.cutStart = self.getNextDword()
                newSample.cutEnd = self.getNextDword()
            newSample.sampleData   = [self.getNextWord() for i in range(newSample.sampleSize)]
            newSample.samplePCE    = None
            newSample.sampleFilter  = self.params['resampleFilter']
            newSample.samplePCERate = self.params['playback']
            newSample.sampleNum     = sampleNum

            self.convertPCMData(newSample)

            self.huTrack.samples.append(newSample)


    def warn(self, message):
        if message not in self.warnings:
            self.warnings.append(message)
            print(' - Warning: ' + message)

    def getSongInfo(self):

        len = self.getNextByte()
        songName = ''.join([chr(self.getNextByte()) for i in range(len)])
        songName = songName.replace('\"', '\'')
        len = self.getNextByte()
        songAuthor = ''.join([chr(self.getNextByte()) for i in range(len)])
        songAuthor = songAuthor.replace('\"', '\'')

        return (songName, songAuthor)


    def convertPCMData(self, sampleObj):
        # Import is read-only. Keep diagnostic PCM with the decoded sample so
        # the exporter installs it in the same transaction as the song.
        sampleObj.sample8bit = b''
        sampleDepth = sampleObj.sampleDepth
        data        = sampleObj.sampleData
        sampleRate  = sampleObj.sampleRate
        samplePitch = sampleObj.samplePitch
        sampleNum   = sampleObj.sampleNum

        # promote all sample data to signed 16bit
        if sampleDepth == 16:
            # need to convert any originally signed data back to signed data. Shouldn't affect 8bit samples stored as 16bit data
            data = [ (sample, sample - 0x10000)[sample > 0x7fff] for sample in data ]
        elif sampleDepth == 8:
            data = [ sample - 128 for sample in data ]
        else:
            print('error unknown bit depth')
            sampleObj.sampleName = 'ERROR: Unknown sample format'
            sampleObj.sampleData = []
            sampleObj.samplePCE  = []
            return

        # Legacy DMF pitch is a nearest-neighbour resample in Furnace's importer.
        # Apply cuts in that intermediate sample domain, before PCE resampling.
        # Furnace uses float gain and incrementing double source positions.
        # Keep its truncated 8-bit scaling before promotion to signed 16-bit.
        gain = numpy.float32(sampleObj.sampleAmp) / numpy.float32(50)
        limit = 128 if sampleDepth == 8 else 32768
        scaled_len = int(numpy.ceil(len(data) / PITCH_VAL[samplePitch]))
        pitched = []
        position = 0.0
        while position < len(data) and len(pitched) < scaled_len:
            value = int(max(-limit, min(limit-1, numpy.float32(data[int(position)]) * gain)))
            pitched.append(value * (256 if sampleDepth == 8 else 1))
            position += PITCH_VAL[samplePitch]
        pitched.extend([0] * (scaled_len-len(pitched)))
        if hasattr(sampleObj, 'cutStart'):
            if not 0 <= sampleObj.cutStart <= sampleObj.cutEnd <= len(pitched):
                raise ValueError(f'Sample {sampleNum}: invalid legacy sample cuts')
            pitched = pitched[sampleObj.cutStart:sampleObj.cutEnd]
        data = pitched
        if not data:
            sampleObj.samplePCE = []
            return

        # use resampy to resample down to target frequency
        orgData = numpy.array(data)
        sr_orig = RATE_VAL[sampleRate]
        newSampleData = resampy.resample(orgData, sr_orig, int(self.params['playback']), filter=self.params['resampleFilter'])

        # numpy arrays are great and all, but let's convert this base to a python list
        newSampleData = [ int(sample) for sample in newSampleData ]

        # need to clamp the samples because.. well.. you know.. filters.
        newSampleData = [ (sample, -32768)[sample < -32768] for sample in newSampleData]
        newSampleData = [ (sample, 32767)[sample > 32767] for sample in newSampleData]

        sampleObj.sample8bit = bytes((sample + 32768) >> 8 for sample in newSampleData)

        # Convert the data to PCE 5bit format
        newSampleData = [ (sample + 32768) >> 11 for sample in newSampleData ]

        sampleObj.samplePCE = newSampleData[::]


    def readDMF(self):

        dmf = None
        try:
            with open(self.params['filein'], 'rb') as compressed_data:
                dmf = zlib.decompress(compressed_data.read())

            # Attempted to use numpy arrays to make things faster.. there's still a performance bottle neck somewhere.
            dmf = list(dmf)
            dmf = numpy.asarray(dmf)

            self.dmf.setDMF(dmf)
        except (OSError, zlib.error):
            dmf = None
            print(f"\n\nException - {os.path.split(self.params['filein'])[-1]} is not a zlib or dmf file, or is damaged/missing.",end="")

        return dmf is not None and len(dmf) != 0


    def checkPlatform(self):
        return len(self.dmf.contents) > PLATFORM_IDX and self.dmf.contents[PLATFORM_IDX] == PCE_VER

    def checkHeaderString(self):
        return '.DelekDefleMask.' in "".join([chr(i) for i in self.dmf.contents[:VER_IDX]])

    # Helper functions
    #....................................................................................

    def getNextDword(self):
        val = self.getNextByte()
        val |= self.getNextByte() << 8
        val |= self.getNextByte() << 16
        val |= self.getNextByte() << 24

        return val

    def getMacroValue(self):
        return self.getNextByte() if self.version < 14 else self.getNextDword()

    def getString(self):
        return ''.join(chr(self.getNextByte()) for _ in range(self.getNextByte()))

    def getNextWord(self):
        val = self.getNextByte()
        val |= self.getNextByte() << 8
        return val

    def getNextByte(self):
        if self.dmf.index >= len(self.dmf.contents):
            raise ValueError(f'Truncated DMF at byte {self.dmf.index}')
        self.dmf.index += 1
        return int(self.dmf.contents[self.dmf.index-1])


