from __future__ import division
# from pylab import *
import numpy as np
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import sys
import os
from scipy import fft, ifft
from scikits.audiolab import flacread, Format, Sndfile
from parameters import parameters


""" On the cluster separate a given birdsong recording into it's component syllables or motifs.
"""

if __name__ == "__main__":

    __author__ = 'Florian'

    zero_val = parameters['zero_val']  # the value that wave data gets set to if it's not a syllable

    birdDataDir = "/argile/golemo/birddata-flac/"
    outDir = "/argile/golemo/birddata-syllables/"

    outDir = os.path.expanduser(outDir)

    if not os.path.exists(outDir):
        os.makedirs(outDir)

    inData = sys.argv[1].split(",")  # [0] = #bird, [1] = day, [2] = hour, [3] = min, [4] = sec, [5] = filename
    inFile = os.path.expanduser(birdDataDir) + inData[0] + '/' + inData[1] + '/' + inData[5]

    pBird = str(inData[0])
    pType = 'syllable' # ['motif'|'syllable]

    amp_threshold = parameters[pBird][pType][0]
    freq_threshold = parameters[pBird][pType][1]
    smoothing = parameters[pBird][pType][2]

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

        def __init__(self, outDir, inData):
            self.outDir = outDir
            self.inData = inData

        def open(self):
            filename = inData[0] + "-" + inData[1] + "-" + inData[2] + "-" + inData[3] + "-" + inData[4]
            self.f = Sndfile(self.outDir + filename + ".syllable-" + str(self.syllableIndex) + '.flac', 'w',
                             self.format, 1, 44100)
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


    aud = AudioWriter(outDir, inData)
    aud.parseData(dataMod)

