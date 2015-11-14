import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0,parentdir)
sys.path.insert(0,parentparentdir)

from numpy import genfromtxt
import numpy as np
from sklearn.gaussian_process import gaussian_process

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

    print inputs.shape
    print outputs.shape

    print "loaded data, now training the model"
    gp = gaussian_process.GaussianProcess(theta0=100000)
    print "created model, now fitting"
    gp.fit(inputs, outputs)
    print "fitted model, now predicting"
    tests = np.atleast_2d([
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 0],
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 1],
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 2],
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 8],
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 9],
        [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 10],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 0],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 1],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 2],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 8],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 9],
        [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 10]
    ]).T

    y_pred, sigma2_pred = gp.predict(tests, eval_MSE=True)

    print y_pred
    print sigma2_pred



