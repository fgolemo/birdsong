import os
import cPickle as pickle
import subprocess

__author__ = 'Florian'

jobsPerWorker = 5

# This script takes the list from step one and for each N lines it submits a job to the cluster

for folder in ["./pool", "./logs"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

songsPerDay = pickle.load(open('todo-cluster.pickle', "rb"))

workers = [songsPerDay[x:x + jobsPerWorker] for x in range(0, len(songsPerDay), jobsPerWorker)]

i = 1
for worker in workers:
    poolfile = './pool/worker-' + str(i) + '.txt'
    with open(poolfile, 'w') as outfile:
        for line in worker:
            outfile.write(",".join(line) + '\n')
        cmd = 'qsub syllable-worker.sh -v pool=' + poolfile
        output = subprocess.Popen(cmd,
                                  stderr=open("./logs/submit." + str(i) + ".stderr.log", "w"),
                                  stdin=open(os.devnull),
                                  shell=True,
                                  stdout=subprocess.PIPE).communicate()[0]
        i += 1
