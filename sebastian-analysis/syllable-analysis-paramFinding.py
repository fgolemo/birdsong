from __future__ import division
import numpy as np
import matplotlib as mpl
# mpl.use('Agg')
import matplotlib.pyplot as plt
import sys
from scipy import fft, ifft
from scikits.audiolab import flacread, Format, Sndfile
from parameters import parameters

__author__ = 'Florian'

zero_val = parameters['zero_val']  # the value that wave data gets set to if it's not a syllable

# Params for bird 112 - whole motif
# amp_threshold = 1.5e-08
# freq_threshold = 9
# smoothing = 5
# Params for bird 112 - single syllables
# amp_threshold = 1.5e-08
# freq_threshold = 5
# smoothing = 3

# Params for bird 1136 - whole motif
# amp_threshold = 1e-09
# freq_threshold = 8
# smoothing = 12
# Params for bird 1136 - single syllables
# amp_threshold = 1e-08
# freq_threshold = 4
# smoothing = 4

# Params for bird 1233 - whole motif
# amp_threshold = 1e-08
# freq_threshold = 7
# smoothing = 4
# Params for bird 1233 - single syllables
# amp_threshold = 7e-09
# freq_threshold = 3
# smoothing = 4

# Params for bird 1592 - whole motif
# amp_threshold = 4.1e-08
# freq_threshold = 2
# smoothing = 12
# Params for bird 1592 - single syllables
# amp_threshold = 1e-09
# freq_threshold = 5
# smoothing = 2


pBird = '1592' # bird number as string
pType = 'syllable' # ['motif'|'syllable]

amp_threshold = parameters[pBird][pType][0]  # if the amp of any freq is higher than this, it will be counted as good
freq_threshold = parameters[pBird][pType][1]  # if the number of good freqs (see prev line) is higher than this, it's probably birdsong
smoothing = parameters[pBird][pType][2]  # HAS TO BE >1, also keep the bins N to the left and right of good segments



if smoothing <= 1:
    quit("smoothing has to be >1")

if len(sys.argv) == 2:
    inFile = sys.argv[1]
else:
    if len(sys.argv) > 2:
        quit("only one optional argument: path to wav file that is to be analyzed")
    else:
        # inFile = 'audio-samples/b112.d54.t481481.flac'
        # inFile = 'audio-samples/b112.d92.t5639583333.flac'
        # inFile = 'audio-samples/b1136.d94.t282148.flac'
        # inFile = 'audio-samples/b1136.d94.t24981322.flac'
        # inFile = 'audio-samples/b1233.d48.t4839703.flac'
        # inFile = 'audio-samples/b1233.d92.t44511791.flac'
        # inFile = 'audio-samples/b1592.d54.t66047281.flac'
        inFile = 'audio-samples/b1592.d91.t65217093.flac'

data, sample_freq, encoding = flacread(inFile)

timeArray = np.arange(0.0, len(data), 1)
timeArray = timeArray / sample_freq
timeArray = timeArray * 1000  # scale to milliseconds

NFFT = 1000  # the length of the windowing segments

fft = fft(data)  # FFT
bp = fft[:]  # copy for manipulating //currently not needed
ibp = ifft(bp)  # inverse FFT for spectrogram

ax1 = plt.subplot(4, 1, 1)
plt.plot(timeArray, data)
plt.subplot(4, 1, 2)
Pxx, freqs, bins, im = plt.specgram(data, Fs=sample_freq)


def loudBits(slice):
    return [1 if slice[i] > amp_threshold else 0 for i in range(len(slice))]


dataMod = data[:]

goodSegmentCount = 0

i = 0
prevGood = False
while i < len(bins):
    step = 1
    goodSegmentsInThere = False
    for j in range(smoothing):
        if i + j == len(bins):
            break
        lb = loudBits(Pxx[:, i + j])
        if sum(lb) > freq_threshold:
            goodSegmentsInThere = True
            step = j + 1
            prevGood = True
            break
    if not goodSegmentsInThere:
        if prevGood:
            step = smoothing - 1
        else:
            for k in range(128):
                dataMod[i * 128 + k] = zero_val
        prevGood = False

    i += step

plt.subplot(4, 1, 3)
plt.plot(timeArray, dataMod)
plt.subplot(4, 1, 4)
Pxx2, freqs2, bins2, im2 = plt.specgram(dataMod, Fs=sample_freq)


class AudioWriter:
    syllableIndex = 0
    baseFilename = "syllable"
    fileOpen = False
    format = Format('flac', 'pcm24')
    f = None
    filecount = 0

    def open(self):
        self.f = Sndfile(self.baseFilename + "." + str(self.syllableIndex) + '.flac', 'w', self.format, 1, 44100)
        self.fileOpen = True

    def close(self):
        if self.fileOpen:
            self.f.close()
            self.syllableIndex += 1
            self.fileOpen = False

    def write(self, data):
        if not self.fileOpen:
            self.open()
        self.f.write_frames(data)

    def parseData(self, data):
        buffer = []
        for i in range(len(data) - 1):
            if i == len(data) - 2 or (data[i] == zero_val and data[i + 1] == zero_val):
                if len(buffer) > 0:
                    self.write(np.array(buffer))
                    self.filecount += 1
                    buffer = []
                self.close()
            else:
                buffer.append(data[i])
                # print self.filecount


# aud = AudioWriter()
# aud.parseData(dataMod)

plt.show()
