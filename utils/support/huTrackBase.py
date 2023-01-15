

RATE_TABLE = ['???','8000hz','11025hz','16000hz','22050hz','32000hz']
RATE_VAL   = [1,8000,11025,16000,22050,32000]
PITCH_VAL  = [1/6, 1/5, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5]

class HuTrackContainer():

    NTSC = 1
    PAL  = 0
    NTSC_PAL_MODE = 0
    SYSTEM_TOTAL_CHANNELS = 6
    CHANNEL_LIST = [i for i in range(SYSTEM_TOTAL_CHANNELS)]

    class Sample():
        def __init__(self):
            self.sampleSize  = 0
            self.sampleName  = ''
            self.sampleRate  = 0
            self.samplePitch = 0
            self.sampleAmp   = 0
            self.sampleDepth = 0
            self.sampleData  = []
            self.samplePCE   = []
            self.sampleFilter  = None
            self.samplePCERate = None
            self.sampleNum     = -1

    class Instrument():
        def __init__(self):
            self.name = ''
            self.mode = 0

            self.volumeEnvLength = 0
            self.volumeEnv = [128]
            self.volumeEnvLoopPosition = -1

            self.arpeggioEnvLength = 0
            self.arpeggioEnv = [128]
            self.arpeggioEnvLoopPosition = -1
            self.arpeggioEnvMode = 0

            self.noiseEnvLength = 0
            self.noiseEnv = [128]
            self.noiseEnvLoopPosition = -1

            self.wavetableEnvLength = 0
            self.wavetableEnv = [128]
            self.wavetableEnvLoopPosition = -1

    class Pattern():
        def __init__(self):
            self.fxLen   = 11
            self.rowLen  = 64
            self.patternData = []
            self.compressedRowLen = 0

        def compare(self, other):
            result = True

            if self.rowLen != other.rowLen:
                result = False
            elif self.fxLen != other.fxLen:
                result = False
            else:
                for i in range(len(other.patternData)):
                    if self.patternData[i] != other.patternData[i]:
                        result = False
                        break

            return result

    class PatternEntry():
        def __init__(self):
            self.note   = 0
            self.octave = 0
            self.volume = 0
            self.instrument = 0

            self.fx0     = 0
            self.fxData0 = 0
            self.fx1     = 0
            self.fxData1 = 0
            self.fx2     = 0
            self.fxData2 = 0
            self.fx3     = 0
            self.fxData3 = 0


    def __init__(self, totalPatterns, totalInstruments, totalRows):
        self.songName   = ''
        self.authorName = ''
        self.timeBase   = 0
        self.tickTime1  = 0
        self.tickTime2  = 0
        self.frameMode  = self.NTSC
        self.customMode = self.NTSC_PAL_MODE
        self.rowsPerPattern          = totalRows
        self.PatternMatrixLen        = totalPatterns
        self.PatternMatrix           = []
        self.compressedPatternMatrix = []
        self.instrumentsLen = totalInstruments
        self.instrumentData = []
        self.patternData             = self.CHANNEL_LIST
        self.uncompPatternData       = self.CHANNEL_LIST
        self.PatternListUnique       = self.CHANNEL_LIST
        self.PatternMatrixCompressed = self.CHANNEL_LIST
        self.wavetableLen   = 0
        self.wavetableData  = []
        self.samples        = []
        self.samplesLen     = 0
