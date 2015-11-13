import os
import cPickle as pickle
import subprocess
import sys

__author__ = 'Florian'

""" TODO: document
"""

if __name__ == "__main__":
    os.chdir(os.path.dirname(sys.argv[0]))

    # This script takes a directory as parameter that has pool files
    # (where each pool file contains several lines with a file to a syllable file path each)

    pool = "./pool"
    if len(sys.argv) == 2:
        pool = sys.argv[1]

    if len(sys.argv) > 2:
        quit("only 1 parameter allowed: path to pool directory (default: './pool')")

    for folder in ["./logs"]:
        if not os.path.exists(folder):
            os.makedirs(folder)

    # for CSV output
    if not os.path.isdir("/argile/golemo/birddata-syllables-csv/"):
        os.makedirs("/argile/golemo/birddata-syllables-csv/")

    workers = [poolfile for poolfile in os.listdir(pool) if poolfile[-5:]==".pool"]

    print "found "+str(len(workers))+" jobs to submit"

    # print workers
    # quit()
    i = 1

    for worker in workers:
        cmd = 'qsub development-worker.sh -v pool=' + worker
        output = subprocess.Popen(cmd,
                                  stderr=open("./logs/submit." + str(i) + ".stderr.log", "w"),
                                  stdin=open(os.devnull),
                                  shell=True,
                                  stdout=subprocess.PIPE).communicate()[0]
        print "submitted {jobs} jobs with job number: {job}".format(jobs=len(worker), job=output)
        i += 1
