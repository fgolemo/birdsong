# We'll need numpy for some mathematical operations
import numpy as np

# Librosa for audio
import librosa

# matplotlib for displaying the output
import matplotlib.pyplot as plt
# %matplotlib inline
# And seaborn to make it look nice
import seaborn

seaborn.set(style='ticks')

# audio_path = "./testsong-featureextraction-jazz.flac"
# audio_path = "../b1136.d94.t282148.flac"
audio_path = "../b1592.d54.t66047281.flac"
y, sr = librosa.load(audio_path)
print 'HAS_SAMPLERATE: ', librosa.core.audio._HAS_SAMPLERATE

S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128)
log_S = librosa.logamplitude(S, ref_power=np.max)


plt.figure(figsize=(12, 10))


plt.subplot(4, 1, 1)
librosa.display.specshow(log_S, sr=sr, x_axis='time', y_axis='mel')
plt.title('mel power spectrogram')
plt.colorbar(format='%+02.0f dB')


C = librosa.feature.chroma_cqt(y=y, sr=sr)
plt.subplot(4, 1, 2)
librosa.display.specshow(C, sr=sr, x_axis='time', y_axis='chroma', vmin=0, vmax=1)
plt.title('Chromagram')
plt.colorbar()


mfcc = librosa.feature.mfcc(S=log_S, n_mfcc=13)
delta_mfcc = librosa.feature.delta(mfcc)
delta2_mfcc = librosa.feature.delta(mfcc, order=2)
plt.subplot(4, 1, 3)
librosa.display.specshow(mfcc)
plt.ylabel('MFCC')
plt.colorbar()

plt.subplot(4, 1, 4)
librosa.display.specshow(delta_mfcc)
plt.ylabel('MFCC-$\Delta$')
plt.colorbar()

plt.tight_layout()


plt.show()
