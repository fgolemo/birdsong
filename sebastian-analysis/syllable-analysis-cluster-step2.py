import os
import cPickle as pickle
import subprocess
import sys

__author__ = 'Florian'

jobsPerWorker = 50

os.chdir(os.path.dirname(sys.argv[0]))

# This script takes the list from step one and for each N lines it submits a job to the cluster

bird = 112
if len(sys.argv) == 2:
    bird = int(sys.argv[1])

for folder in ["./pool", "./logs"]:
    if not os.path.exists(folder):
        os.makedirs(folder)

songsPerDay = pickle.load(open('todo-cluster.pickle', "rb"))
todos = songsPerDay[str(bird)]

workers = [todos[x:x + jobsPerWorker] for x in range(0, len(todos), jobsPerWorker)]

print "found "+str(len(workers))+" jobs to submit"

#print workers
#quit()
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
        print "submitted {jobs} jobs with job number: {job}".format(jobs=len(worker), job=output)
        i += 1
