#!/bin/bash

build:
	gcc -g serial.c -o serial -lm
	gcc -g openmp.c -o openmp -fopenmp -fdump-tree-all -lm
	gcc -g pthreads.c -o pthreads -lm -lpthread
	mpicc -g -o mpi mpi.c -lm
	mpicc -g -o hybrid hybrid.c -fopenmp -fdump-tree-all -lm
	mpicc -g -o hybrid2 hybrid2.c -lm -lpthread
	mkdir OUTPUT

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
	make run_hybrid2

run_serial:
	time ./serial input > OUTPUT/output_serial

run_openmp:
	time ./openmp input $(P) > OUTPUT/output_openmp_$(P)

run_pthreads:
	time ./pthreads input $(P) > OUTPUT/output_pthreads_$(P)

run_mpi:
	time mpirun -np $(P) ./mpi input > OUTPUT/output_mpi_$(P)

run_hybrid:
	time mpirun -np $(P) ./hybrid input > OUTPUT/output_hybrid_$(P)

run_hybrid2:
	time mpirun -np $(P) ./hybrid2 input > OUTPUT/output_hybrid2_$(P)

clean:
	rm serial openmp pthreads mpi hybrid hybrid2 || echo "Continuing..."
	rm -r OUTPUT || echo "Continuing..."
	rm openmp.c.* hybrid.c.* || echo "Continuing..."
