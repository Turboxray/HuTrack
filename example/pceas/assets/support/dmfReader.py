
import argparse
import json
import numpy
import os
import pprint
import resampy
import sys
import zlib

from support.huTrackBase import HuTrackContainer, RATE_TABLE, RATE_VAL, PITCH_VAL

HEXbase = 16
DECbase = 10
INT_MAX = 2**32 - 1
INT_MIN = (INT_MAX) / -2 - 1

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

    def getByte(self):
        return self.contents[self.index]

    def setIndex(self, val):
        self.index = val

    def getIndex(self):
        return self.index



class ConvertDeflemask():

    def __init__(self, runOptions=None):
        self.params     = runOptions
        self.songInfo   = ''
        self.AuthorInfo = ''
        self.dmf     = DMFcontainer(0)
        self.huTrack = None

    def process(self, runOptions=None):

        self.params = (self.params, runOptions)[runOptions is not None]

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

        self.dmf.setIndex(SONG_INFO_IDX)
        self.initHutrackModule(*self.getSongInfo())

        return True

    def initHutrackModule(self, songname, author):

        # skip over 'highlight' bytes A and B. I think they're editor related.
        skip = self.getNextByte()
        skip = self.getNextByte()

        timebase  = self.getNextByte()
        timetick1 = self.getNextByte()
        timetick2 = self.getNextByte()
        mode      = self.getNextByte()
        customHZ  = self.getNextByte()
        # We're not supporting custom Hz mode, so skip over its operands
        skip = self.getNextByte()
        skip = self.getNextByte()
        skip = self.getNextByte()

        rowLen     = self.getNextByteFromDword()
        PatternLen = self.getNextByte()

        # a pattern matrix for each channel..
        patternMatrix = [ [self.getNextByte() for i in range(PatternLen) ]  for i in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS)]

        instrumentsLen = self.getNextByte()
        self.huTrack = HuTrackContainer(PatternLen, instrumentsLen, rowLen)

        self.huTrack.authorName = author
        self.huTrack.songName   = songname
        self.huTrack.timeBase   = timebase + 1
        self.huTrack.tickTime1  = timetick1 * self.huTrack.timeBase
        self.huTrack.tickTime2  = timetick2 * self.huTrack.timeBase
        self.huTrack.frameMode  = mode
        self.huTrack.customMode = customHZ
        self.huTrack.PatternMatrix = patternMatrix

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
                continue

            # volume
            volEnvSize = self.getNextByte()
            volEnvLoop = 0xff
            volEnv = [ self.getNextByteFromDword() for i in range(volEnvSize) ]
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
            arpEnv = [ self.getNextDword() for i in range(arpEnvSize) ]
            if arpEnvSize > 0:
                arpEnvLoop = self.getNextByte()
            newInstr.arpeggioEnvLength = arpEnvSize
            newInstr.arpeggioEnvLoopPosition = arpEnvLoop
            newInstr.arpeggioEnvMode = self.getNextByte()
            arpEnv = [ (signed_int - 12, signed_int)[newInstr.arpeggioEnvMode] & 0xff for signed_int in arpEnv ]
            newInstr.arpeggioEnv = arpEnv

            if arpEnvLoop >= arpEnvSize and arpEnvLoop != 255:
                print(f' - Error in file: Instrument #{i} arpeggio envelope loop position {arpEnvLoop} outside of size {arpEnvSize}. Changing loop {arpEnvLoop} to {arpEnvSize -1}')
                newInstr.arpeggioEnvLoopPosition = arpEnvSize - 1


            # noise. NOTE: This actually isn't used on the PCE format, but we still need to read past it. Maybe it's beta?
            noiseEnvSize = self.getNextByte()
            noiseEnvLoop = 0xff
            noiseEnv = [ self.getNextByteFromDword() for i in range(noiseEnvSize) ]
            if noiseEnvSize > 0:
                noiseEnvLoop = self.getNextByte()
            newInstr.noiseEnv       = noiseEnv
            newInstr.noiseEnvLength = noiseEnvSize
            newInstr.noiseEnvLoopPosition = noiseEnvLoop

            #wavetable
            waveEnvSize = self.getNextByte()
            waveEnvLoop = 0xff
            waveEnv = [ self.getNextByteFromDword() for i in range(waveEnvSize) ]
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


    def getPatternData(self):
        self.huTrack.patternData       = []
        self.huTrack.uncompPatternData = []
        for channel in range(HuTrackContainer.SYSTEM_TOTAL_CHANNELS):
            self.huTrack.patternData.append([])
            self.huTrack.uncompPatternData.append([])
            self.huTrack.PatternMatrixCompressed[channel] = []
            numFX = self.getNextByte()
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
                    rawRowEntry.append(octave)
                    octave = octaveDelta + octave
                    rowEntry.append(octave)
                    skip = self.getNextByte()

                    # volume
                    volume = self.getNextWord()
                    rowEntry.append(volume)
                    rawRowEntry.append(volume)

                    for fx in range(numFX):
                        # FX code
                        fxEntry = self.getNextByte()
                        fxEntry |= self.getNextByte() << 8
                        rowEntry.append(fxEntry)
                        rawRowEntry.append(fxEntry)

                        # FX arg
                        fxArg = self.getNextByte()
                        fxArg |= self.getNextByte() << 8
                        rawRowEntry.append(fxArg)
                        if (fxEntry == 0x09 or fxEntry == 0x0f) and fxArg != 0xffff:
                            fxArg *= self.huTrack.timeBase
                            if self.huTrack.timeBase != 1:
                                print(f' - Converting: fx {fxEntry} : arg {fxArg}')

                        if fxEntry == 0x08 and fxArg == 0xffff:
                            fxArg = 0xff
                            print(f' - Error. Found empty pan FX. Forcing to 0xFF.')
                            # continue

                        rowEntry.append(fxArg)

                    # instr
                    rowEntry.append(self.getNextWord())
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

        wavetableEntries = self.getNextByte()
        for i in range(wavetableEntries):
            wavetableDataSize = self.getNextByteFromDword()
            self.huTrack.wavetableData.append( [self.getNextByteFromDword() for i in range(wavetableDataSize)] )
        self.huTrack.wavetableLen = wavetableEntries


    def getPCMdata(self):

        samplesLen = self.getNextByte()
        self.huTrack.samplesLen = samplesLen
        for sampleNum in range(samplesLen):

            newSample = HuTrackContainer.Sample()
            newSample.sampleSize   = self.getNextDword()
            sampleNameLen          = self.getNextByte()
            newSample.sampleName   = ''.join([chr(self.getNextByte()) for i in range(sampleNameLen)])
            newSample.sampleRate   = self.getNextByte()
            newSample.samplePitch  = self.getNextByte()
            newSample.sampleAmp    = self.getNextByte()
            newSample.sampleDepth  = self.getNextByte()
            newSample.sampleData   = [self.getNextWord() for i in range(newSample.sampleSize)]
            newSample.samplePCE    = None
            newSample.sampleFilter  = self.params['resampleFilter']
            newSample.samplePCERate = self.params['playback']
            newSample.sampleNum     = sampleNum

            self.convertPCMData(newSample)

            self.huTrack.samples.append(newSample)


    def getSongInfo(self):

        len = self.getNextByte()
        songName = ''.join([chr(self.getNextByte()) for i in range(len)])
        songName = songName.replace('\"', '\'')
        len = self.getNextByte()
        songAuthor = ''.join([chr(self.getNextByte()) for i in range(len)])
        songAuthor = songAuthor.replace('\"', '\'')

        return (songName, songAuthor)


    def convertPCMData(self, sampleObj):
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
            data = [ (sample - 128) * 256 for sample in data ]
        else:
            print('error unknown bit depth')
            sampleObj.sampleName = 'ERROR: Unknown sample format'
            sampleObj.sampleData = []
            sampleObj.samplePCE  = []
            return

        # Update with corrected values.
        sampleObj.sampleData = data[::]

        data = [sample * 1.5 for sample in data]
        data = [ (sample, -32767)[sample < -32767] for sample in data]
        data = [ (sample, 32767)[sample > 32767] for sample in data]

        # use resampy to resample down to target frequency
        orgData = numpy.array(data)
        sr_orig = RATE_VAL[sampleRate] * PITCH_VAL[samplePitch]
        newSampleData = resampy.resample(orgData, sr_orig, int(self.params['playback']), filter=self.params['resampleFilter'])

        # numpy arrays are great and all, but let's convert this base to a python list
        newSampleData = [ int(sample) for sample in newSampleData ]

        # need to clamp the samples because.. well.. you know.. filters.
        newSampleData = [ (sample, -32767)[sample < -32767] for sample in newSampleData]
        newSampleData = [ (sample, 32767)[sample > 32767] for sample in newSampleData]

        # DEBUG
        # if sampleDepth == 8:
        #     eightbitSampleData = [ ((sample + 32767) >> 8)   for sample in newSampleData ]
            # with open(f'{sampleData.sampleName}.pre.bin','wb') as fout:
            #     fout.write(bytearray(eightbitSampleData))

        if self.params['debug']:
            filename = os.path.join(f'{self.params["subFolder"]}',f'{self.params["songName"]}.{sampleNum}.8bit.bin').replace("\\","/")
            with open(os.path.join(runOptions['destinationPath'],filename),'wb') as fout:
                eightbitSampleData = [ ((sample + 32767) >> 8)   for sample in newSampleData ]
                fout.write(bytearray(eightbitSampleData))

        # Convert the data to PCE 5bit format
        newSampleData = [ (sample + 32767) >> 11 for sample in newSampleData ]

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
        except:
            dmf = None
            print(f"\n\nException - {os.path.split(self.params['filein'])[-1]} is not a zlib or dmf file, or is damaged/missing.",end="")

        return dmf is not None and len(dmf) != 0


    def checkPlatform(self):
        return self.dmf.contents[PLATFORM_IDX] == PCE_VER

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

    def getNextByteFromDword(self):
        return self.getNextDword() & 0xff

    def getNextByteFromWord(self):
        return self.getNextWord() & 0xff

    def getNextWord(self):
        val = self.getNextByte()
        val |= self.getNextByte() << 8
        return val

    def getNextByte(self):
        self.dmf.index += 1
        return int(self.dmf.contents[self.dmf.index-1])


