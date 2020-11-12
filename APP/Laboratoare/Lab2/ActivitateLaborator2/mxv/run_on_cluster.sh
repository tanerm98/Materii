#!/bin/bash

./mxv_base
./mxv_par
./mxv_omp

# qsub -q all.q -cwd ./run_on_cluster.sh