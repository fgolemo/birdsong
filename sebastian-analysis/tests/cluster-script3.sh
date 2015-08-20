#!/bin/bash
#PBS -N test_job 
#PBS -o test_job.out
#PBS -b test_job.err
#PBS -m abe
#PBS -M fgolemo@gmail.com
#PBS -l walltime=00:59:59
#PBS -l ncpus=16
export PATH=$PATH:$HOME/libsndfile/bin/
export PYTHONPATH=$PYTHONPATH:$HOME/pylib/lib/python2.7/site-packages/
cd $HOME/pytest
date
nb_concurrent_processes=16
j=0
for i in {1..500}
do
        python syllalysis-cluster.py $i &
        ((++j == nb_concurrent_processes)) && { j=0; wait; }
done
date
