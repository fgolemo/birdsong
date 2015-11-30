#!/bin/bash
#PBS -N birdsong_job
#PBS -o birdsong_job.out
#PBS -b birdsong_job.err
#PBS -m abe
#PBS -M fgolemo@gmail.com
#PBS -l walltime=00:59:59
#PBS -l ncpus=16

# Execute up to 16 jobs in parallel on the cluster,
# where a job is executing the python script syllable-analysis-cluster-worker.py
# to find syllables in birdsong recordings. Read the file names from the provided pool file


export PATH=$PATH:$HOME/libsndfile/bin/
export PYTHONPATH=$PYTHONPATH:$HOME/pylib/lib/python2.7/site-packages/

cd $HOME/birdsong/sebastian-analysis

nb_concurrent_processes=16
j=0
while read line; do
    python syllable-analysis-cluster-worker.py ${line} &
    ((++j == nb_concurrent_processes)) && { j=0; wait; }
done < ${pool}

wait
echo "done"
