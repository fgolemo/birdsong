from architecture.components.hearing import Hearing
import numpy as np
from sklearn.decomposition import PCA


if __name__ == "__main__":
    # testfiles = [
    #     "./testSong1Original.wav",
    #     "./testSong2Synth.wav"
    # ]
    testfiles = []
    for i in range(12):
        testfiles.append("./testpattern-{i}.wav".format(i=i))
    h = Hearing(channels=12)
    dataTmp = []
    for f in testfiles:
        mfcc = h.calcMfcc(f)
        dataTmp.append(mfcc.T)

    data = np.concatenate(dataTmp)
    print "data shape:",data.shape


    pca = PCA(n_components=12)
    pca.fit(data)
    print(pca.explained_variance_ratio_)




