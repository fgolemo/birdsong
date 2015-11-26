import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, parentparentdir)
from time import time

from architecture.components.esn import ESN

from numpy import genfromtxt
import numpy as np
from sklearn.gaussian_process import gaussian_process
from scipy.stats import randint as sp_randint
from sklearn.grid_search import RandomizedSearchCV
from operator import itemgetter

""" Scipt tests a given machine learning algorithm to map the demo input data (patterns) to the output (mfccs)
"""

if __name__ == "__main__":

    outFileNamePrefix = "fmmTrainingData"
    if len(sys.argv) >= 2:
        outFileNamePrefix = sys.argv[1]

    filehandleInputs = outFileNamePrefix + ".inputs.csv"
    filehandleOutputs = outFileNamePrefix + ".outputs.csv"

    inputs = genfromtxt(filehandleInputs, delimiter=',')
    outputs = genfromtxt(filehandleOutputs, delimiter=',')

    # print inputs.shape
    # print outputs.shape
    # print inputs[1,:]
    # print outputs[1,:]

    print "loaded data, now reshaping the data"

    inputsNew = []
    outputsNew = []
    lineIn = []
    lineOut = []
    for i_in in range(len(inputs[:,1])):
        # print inputs[i_in,:]
        if inputs[i_in,0] == 0:
            if len(lineIn) > 0 and len(lineOut) > 1:
                inputsNew.append(lineIn)
                outputsNew.append(lineOut)
            lineIn = inputs[i_in,1:]
            lineOut = [outputs[i_in,:]]
            continue
        lineOut.append(outputs[i_in,:])

    # print len(inputsNew)
    # print len(outputsNew)
    # print inputsNew[0]
    # print outputsNew[0]

    # lens = []
    # for i in outputsNew:
    #     lens.append(len(i))
    # print max(lens)
    # print min(lens)

    print "done reshaping the data, now training ESN"

    esn = ESN(reservoir_size=100,
                 inputs=11,
                 outputs=3,
                 generate_time_sequence=True,
                 reservoir_connectivity=10,
                 simulation_steps=10,
                 echo_decay=0.5)
    esn.createNetwork()

    esn.train(inputsNew, outputsNew)

    print "done training, now predicting"

    prediction =  esn.predict(inputsNew[:10], steps=11)
    print len(prediction)
    print prediction.shape
    print prediction

    predErr = prediction - outputsNew[:10]
    print predErr



