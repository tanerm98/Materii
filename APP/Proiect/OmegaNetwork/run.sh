#!/bin/bash

time ./serial input

time ./openmp input 1
time ./openmp input 2
time ./openmp input 4
time ./openmp input 8
time ./openmp input 16

time ./pthreads input 1
time ./pthreads input 2
time ./pthreads input 4
time ./pthreads input 8
time ./pthreads input 16

time mpirun -np 1 ./mpi input
time mpirun -np 2 ./mpi input
time mpirun -np 4 ./mpi input
time mpirun -np 8 ./mpi input
time mpirun -np 16 ./mpi input

time mpirun -np 1 ./hybrid input
time mpirun -np 2 ./hybrid input
time mpirun -np 4 ./hybrid input
time mpirun -np 8 ./hybrid input
time mpirun -np 16 ./hybrid input