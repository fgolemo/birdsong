import librosa
import os


class Hearing:
    def __init__(self, tutorsong):
        self.tutorsong = False
        self.mfcc = False
        if tutorsong != None and tutorsong != False:
            self.tutorsong = tutorsong

    def calcMfcc(self, soundFile):
        if self.tutorsong != False:
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
        self.mfcc = mfcc[1:4, :]
        return self.mfcc


if __name__ == "__main__":
    h = Hearing(tutorsong=False)

    testFile = "../../sebastian-analysis/audio-samples/b1592.d91.t65217093.flac"

    mfcc = h.calcMfcc(testFile)

    import matplotlib.pyplot as plt

    librosa.display.specshow(mfcc, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()
