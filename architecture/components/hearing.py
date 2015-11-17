import librosa
import os


class Hearing:
    def __init__(self, tutorsong=None, channels=3):
        self.mfcc = False
        self.channels = int(channels)
        self.tutorsong = tutorsong
        if self.channels < 1 or self.channels > 12:
            raise AttributeError("channels parameter must be an integer between (including) 1 and 12")

    def calcMfcc(self, soundFile):
        if self.tutorsong != False and self.tutorsong != None:
            soundFile = self.tutorsong
            if self.mfcc != False:
                return self.mfcc

        if not os.path.isfile(soundFile):
            print "ERR: sound file couldn't be found:" + str(soundFile)
            return False
        data, sr = librosa.load(soundFile)

        # Compute MFCC features from the raw signal, 13 channels is a reasonable resolution,
        # mappable onto the chromatic spectrum
        mfcc = librosa.feature.mfcc(y=data, sr=sr, n_mfcc=13)

        # discard the first row (amplitude) and evey row higher than 4, because they are mostly noise & artefacts
        self.mfcc = mfcc[1:self.channels+1, :]
        return self.mfcc


if __name__ == "__main__":
    h = Hearing()

    testFile = "../../sebastian-analysis/audio-samples/b1592.d91.t65217093.flac"

    mfcc = h.calcMfcc(testFile)

    import matplotlib.pyplot as plt

    librosa.display.specshow(mfcc, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()
