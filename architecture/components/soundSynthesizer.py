from scipy.io import wavfile
import numpy as np

from ..synth.alphabeta2dat import AlphaBeta2Dat
from .motorCommandGenerator import MotorCommandGenerator
from ..synth.dat2wav import Dat2Wav


class SoundSynthesizer():
    """ TODO: doc
    """

    def __init__(self, inputStream, outputStream):
        self.inputStream = inputStream
        self.outputStream = outputStream
        self.ab2d = AlphaBeta2Dat(inputStream, outputStream)

    def synthesize(self):
        self.ab2d.mainLoop()


if __name__ == "__main__":
    mcg = MotorCommandGenerator(frequency=44100)
    params = [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25]

    alphaBetaList = mcg.getList(params)
    i = 0


    def inputStream():
        global i
        if i < len(alphaBetaList):
            i += 1
            return alphaBetaList[i-1]
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
    d2w.writeWAV(sound, "testsound2.wav", 44100)
