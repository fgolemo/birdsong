import os, sys, inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
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

    print "loaded data"

    esn = ESN(reservoir_size=50,
              inputs=12,
              outputs=3,
              generate_time_sequence=False,
              input_connectivity=10,
              reservoir_connectivity=10,
              feedback_connectivity=0,
              simulation_steps=2,
              echo_decay=0.8,
              reset_each_step=False,
              disconnect_inputs=False)
    esn.createNetwork()

    esn.train(inputs, outputs)

    print "done training, now predicting"

    errors = []

    for i in range(100):
        pred = esn.predict([inputs[i]])
        predErr = pred-outputs[i]
        err = np.square(predErr).sum()
        errors.append(err)

    print "total error:",round(sum(errors)/100000,2)

    print "avg activation",esn.getAvgResActivation()

