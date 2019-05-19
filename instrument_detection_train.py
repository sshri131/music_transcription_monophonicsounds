from python_speech_features import mfcc
from python_speech_features import logfbank
from python_speech_features import base
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.model_selection import train_test_split
import pickle
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import struct
import wave


def featuresplot(sig,rate,typo):
    m = mfcc(sig,rate)
    fbank_feat = logfbank(sig,rate)

    mlst = []
    for i in range(0, len(m)):
        l = m[0:4]
        mlst.append(m[i][2])
    m=[]
    m.append(np.mean(mlst))
    clst=[]
    for i in range(0, len(fbank_feat)):
        l = m[0:4]
        clst.append(np.mean(fbank_feat[i]))
    c=[]
    c.append(np.mean(clst))
    plt.plot(m,c, typo)
    return  m[0],c[0]





with open ('sample_data.pkl','rb') as pickle_file:
    dataset = pickle.load(pickle_file)

dataset = np.array(dataset)
le = LabelEncoder()
data = pd.DataFrame(dataset)
X, Y = data.iloc[:,1:], dataset[:,0]
Y = le.fit_transform(Y)
#print le.classes_
#print Y[:5]
#print (X.shape, Y.shape)
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state = 42)
#print (X_train.shape, y_train.shape)
clf = svm.SVC(kernel = 'linear', C = 2.0)
clf.fit(X_train, y_train)
acc = clf.score(X_test, y_test)
#print str(acc*100)+"% accuracy"

lst = ['flute','piano','trumpet','violin']

file= 'piano/sample_'+'10'+'.wav'
audio_file = wave.open(file)
length = audio_file.getnframes()
signal = np.zeros(length)
for i in range (0,length):
    data = audio_file.readframes(1)
    data = struct.unpack("<h", data)
    signal[i] = int(data[0])
rate = audio_file.getframerate()
signal = np.divide(signal, float(2**15))
typo = '.g'
m,c = featuresplot(signal, rate, typo)
print m,c
instrument = clf.predict([[m , c]])
print lst[instrument[0]]