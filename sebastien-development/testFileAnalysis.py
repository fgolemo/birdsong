import os
import re
import pyaudio
from numpy import mean
from numpy.fft import fft
from scikits.audiolab import flacread
from scipy.stats import gmean
import pymir
import pymir.SpectralFlux

dirpath = "./audio-samples"
regexFilePattern = re.compile(
    r"([0-9]{3,4})-([0-9]{1,3})-([0-9]{1,2})-([0-9]{1,2})-([0-9]{1,2})\.syllable-([0-9]{1,3})\.flac")

print "bird," \
      "day," \
      "hour," \
      "minute," \
      "second," \
      "syllable," \
      "spectralFlatness," \
      "energyMin," \
      "energyMax," \
      "energyMean," \
      "amplitudeMin," \
      "amplitudeMax," \
      "amplitudeMean," \
      "zeroCrossingRateMin," \
      "zeroCrossingRateMax," \
      "zeroCrossingRateMean," \
      "spectralCentroidMin," \
      "spectralCentroidMax," \
      "spectralCentroidMean," \
      "spectralCrestFactorMin," \
      "spectralCrestFactorMax," \
      "spectralCrestFactorMean," \
      "spectralKurtosisMin," \
      "spectralKurtosisMax," \
      "spectralKurtosisMean," \
      "spectralMeanMin," \
      "spectralMeanMax," \
      "spectralMeanMean," \
      "spectralRolloffMin," \
      "spectralRolloffMax," \
      "spectralRolloffMean," \
      "spectralSkewnessMin," \
      "spectralSkewnessMax," \
      "spectralSkewnessMean," \
      "spectralSpreadMin," \
      "spectralSpreadMax," \
      "spectralSpreadMean," \
      "spectralVarianceMin," \
      "spectralVarianceMax," \
      "spectralVarianceMean" \
      "spectralFluxMin," \
      "spectralFluxMax," \
      "spectralFluxMean"

import time

start = time.time()

goodfiles = 0
for filename in os.listdir(dirpath):
    nameMatch = regexFilePattern.match(filename)
    if nameMatch is None:
        continue

    goodfiles += 1

    # get file info
    bird = nameMatch.group(1)
    day = nameMatch.group(2)
    hour = nameMatch.group(3)
    minute = nameMatch.group(4)
    sec = nameMatch.group(5)
    syllable = nameMatch.group(6)

    # extract data from flac
    audioData = pymir.AudioFile.open(dirpath + os.path.sep + filename)

    # calculate features (wiener entropy aka spectral flatness)
    spectrum = abs(fft(audioData))
    spectral_flatness = gmean(spectrum ** 2) / mean(spectrum ** 2)

    # other features
    fixedFrames = audioData.frames(1024)
    spectra = [f.spectrum() for f in fixedFrames]

    energy = []
    amplitude = []
    zeroCrossingRate = []
    centroid = []
    crestFactor = []
    kurtosis = []
    smean = []
    rolloff = []
    skewness = []
    spread = []
    variance = []
    for i in range(len(fixedFrames)):
        energy.append(mean(fixedFrames[i].energy(windowSize=256)))
        amplitude.append(fixedFrames[i].rms())
        zeroCrossingRate.append(fixedFrames[i].zcr())

        centroid.append(spectra[i].centroid())  # Spectral Centroid
        crestFactor.append(spectra[i].crest())  # Spectral Crest Factor
        kurtosis.append(spectra[i].kurtosis())  # Spectral Kurtosis
        smean.append(spectra[i].mean())  # Spectral Mean
        rolloff.append(spectra[i].rolloff())  # Spectral Rolloff
        skewness.append(spectra[i].skewness())  # Spectral Skewness
        spread.append(spectra[i].spread())  # Spectral Spread
        variance.append(spectra[i].variance())  # Spectral Variance

    # Compute the spectral flux
    flux = pymir.SpectralFlux.spectralFlux(spectra, rectify=True)

    output = [
        bird,
        day,
        hour,
        minute,
        sec,
        syllable,
        spectral_flatness,

        min(energy),
        max(energy),
        mean(energy),

        min(amplitude),
        max(amplitude),
        mean(amplitude),

        min(zeroCrossingRate),
        max(zeroCrossingRate),
        mean(zeroCrossingRate),

        min(centroid),
        max(centroid),
        mean(centroid),

        min(crestFactor),
        max(crestFactor),
        mean(crestFactor),

        min(kurtosis),
        max(kurtosis),
        mean(kurtosis),

        min(smean),
        max(smean),
        mean(smean),

        min(rolloff),
        max(rolloff),
        mean(rolloff),

        min(skewness),
        max(skewness),
        mean(skewness),

        min(spread),
        max(spread),
        mean(spread),

        min(variance),
        max(variance),
        mean(variance),

        min(flux),
        max(flux),
        mean(flux)
    ]

    stringifiedOutput = [str(o) for o in output]

    print ",".join(stringifiedOutput)

end = time.time()
diff = end - start
print diff
perFileTime =  diff / goodfiles
print perFileTime
print (perFileTime * 5600000)/60/60
