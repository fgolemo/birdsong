from ..synth.alphabeta2dat import AlphaBeta2Dat
from .motorCommandGenerator import MotorCommandGenerator


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



    def outputStream(content):
        print content


    ss = SoundSynthesizer(inputStream, outputStream)
    ss.synthesize()
