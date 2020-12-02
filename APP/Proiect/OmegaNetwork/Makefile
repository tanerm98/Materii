#!/bin/bash

build:
	gcc serial.c -o serial -lm
	gcc-9 openmp.c -o openmp -fopenmp -fdump-tree-all -lm
	gcc pthreads.c -o pthreads -lm -lpthread
	mpicc -o mpi mpi.c -lm
	mpicc -o hybrid hybrid.c -fopenmp -fdump-tree-all -lm

run_all_tests:
	make run_all P=1
	make run_all P=2
	make run_all P=4
	make run_all P=8
	make run_all P=16

run_all:
	make run_serial
	make run_openmp
	make run_pthreads
	make run_mpi
	make run_hybrid

run_serial:
	time ./serial input > output_serial

run_openmp:
	time ./openmp input $(P) > output_openmp_$(P)

run_pthreads:
	time ./pthreads input $(P) > output_pthreads_$(P)

run_mpi:
	time mpirun -np $(P) ./mpi input > output_mpi_$(P)

run_hybrid:
	time mpirun -np $(P) ./hybrid input > output_hybrid_$(P)

clean:
	rm serial openmp pthreads mpi hybrid || echo "Continuing..."
	rm output_serial* output_openmp* output_pthreads* output_mpi* output_hybrid* || echo "Continuing..."
	rm openmp.c.* hybrid.c.* || echo "Continuing..."
