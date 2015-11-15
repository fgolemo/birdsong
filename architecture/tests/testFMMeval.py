import os, sys, inspect
from time import time

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
parentparentdir = os.path.dirname(parentdir)
sys.path.insert(0, parentdir)
sys.path.insert(0, parentparentdir)

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

    print inputs.shape
    print outputs.shape

    print "loaded data, now training the model"
    gp = gaussian_process.GaussianProcess(theta0=1000000)
    print "created model, now fitting"


    # gp.fit(inputs, outputs)
    # print "fitted model, now predicting"


    # tests = np.atleast_2d([
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 0],
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 1],
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 2],
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 8],
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 9],
    #     [1, 1, 1, 1, 1, 2, -1, -2, 1, 1, 0.25, 10],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 0],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 1],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 2],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 8],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 9],
    #     [10, 10, 10, 10, 10, -10, -10, -10, -10, -10, 0.25, 10]
    # ]).T
    #
    # y_pred, sigma2_pred = gp.predict(tests, eval_MSE=True)
    #
    # print y_pred
    # print sigma2_pred

    # Utility function to report best scores
    def report(grid_scores, n_top=5):
        top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
        for i, score in enumerate(top_scores):
            print("Model with rank: {0}".format(i + 1))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                score.mean_validation_score,
                np.std(score.cv_validation_scores)))
            print("Parameters: {0}".format(score.parameters))
            print("")


    # corr='cubic', theta0=1e-2, thetaL=1e-4, thetaU=1e-1,
    #                      random_start=100

    def getTheta0():
        theta0 = np.random.randint(low=1, high=int(1e+8), size=13)
        return [theta0]


    param_dist = {
        "regr": ['constant'],
        "corr": ['absolute_exponential'],
        "theta0": [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6],
        # "thetaL": sp_randint(1, 100000000),
        # "thetaU": sp_randint(1, 100000000),
        "normalize": [True],
        "optimizer": ['fmin_cobyla', 'Welch']
    }

    # run randomized search
    n_iter_search = 14
    random_search = RandomizedSearchCV(gp, param_distributions=param_dist, n_iter=n_iter_search, error_score=-1000, verbose=3)

    start = time()
    random_search.fit(inputs, outputs)
    print("RandomizedSearchCV took %.2f seconds for %d candidates"
          " parameter settings." % ((time() - start), n_iter_search))
    report(random_search.grid_scores_)
