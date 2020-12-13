#!/bin/bash

qsub -q all.q -cwd ./run.sh
qstat

#qsub -q all-8.q -pe openmpi 45 -cwd ./run.sh
#qstat