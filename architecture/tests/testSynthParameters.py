import random

from matplotlib import gridspec

from architecture.components.motorCommandGenerator import MotorCommandGenerator
from architecture.components.soundSynthesizer import SoundSynthesizer
from architecture.synth.dat2wav import Dat2Wav
import matplotlib.pyplot as plt
from scikits.audiolab import wavread
import numpy as np

if __name__ == "__main__":

    def r(scaling):
        return random.random() * scaling - (scaling / 2)


    patterns = [
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.25],
        [2, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0.25],
        [0.1, 0.1, 0.1, 0.1, 100, -10, 0.1, 0.1, 0.1, 100, 0.25],
        [10, 10, 10, 10, 10, -10, 10, 10, 10, 10, 0.25],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25],
        [1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 0.25],
        [0.0001, 0.0001, 0.0001, 0.0001, 0.0001, -0.0001, 0.0001, 0.0001, 0.0001, 0.0001, 0.25],
        [r(2), r(2), r(2), r(2), r(2), r(2)-2, r(2), r(2), r(2), r(2), 0.25],
        [r(4), r(4), r(4), r(4), r(4), r(4)-4, r(4), r(4), r(4), r(4), 0.25],
        [r(10), r(10), r(10), r(10), r(10), r(10)-10, r(10), r(10), r(10), r(10), 0.25],
        [r(10), r(10), r(10), r(10), r(10), r(10)-10, r(10), r(10), r(10), r(10), 0.25]
    ]

    mcg = MotorCommandGenerator(frequency=44100)

    splitPos = len(patterns) / 2

    f = plt.figure()
    gs0 = gridspec.GridSpec(1, 2) # figure with 1 row, 2 column
    gs00 = gridspec.GridSpecFromSubplotSpec(splitPos, 2, subplot_spec=gs0[0], width_ratios=[3,1], hspace=0.6)
    gs01 = gridspec.GridSpecFromSubplotSpec(splitPos, 2, subplot_spec=gs0[1], width_ratios=[3,1], hspace=0.6)

    for j in range(len(patterns)):

        print "start synthing pattern " + str(j)
        alphaBetaList = mcg.getList(patterns[j])
        i = 0


        def inputStream():
            global i
            if i < len(alphaBetaList):
                i += 1
                return alphaBetaList[i - 1]
            else:
                return (False, False)


        output = []


        def outputStream(content):
            global output
            output.append(content)


        ss = SoundSynthesizer(inputStream, outputStream)
        ss.synthesize()

        d2w = Dat2Wav
        sound = d2w.convert(output)
        fileName = "testpattern-" + str(j) + ".wav"
        d2w.writeWAV(sound, fileName, 44100)

        print "done synthing pattern " + str(j)

        data, sample_freq, encoding = wavread(fileName)

        timeArray = np.arange(0.0, len(data), 1)
        timeArray = timeArray / sample_freq
        timeArray = timeArray * 1000  # scale to milliseconds


        index = j
        column = gs00
        if j >= splitPos:
            index = j - splitPos
            column = gs01

        patternAsString = [str(round(param,4)) for param in patterns[j]]

        params = ",".join(patternAsString[:len(patternAsString)/2]) + "\n" + \
            ",".join(patternAsString[len(patternAsString)/2:])

        ax1 = plt.Subplot(f, column[index, 0])
        ax1.set_title("parameters: " + params)
        ax1.specgram(data, Fs=sample_freq)
        f.add_subplot(ax1)

        ax2 = plt.Subplot(f, column[index, 1])

        ax2.plot(alphaBetaList)
        f.add_subplot(ax2)
    plt.suptitle("blue: air pressure, green: tension")
    plt.show()
