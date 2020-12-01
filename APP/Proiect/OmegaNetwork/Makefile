#!/bin/bash

build:
	gcc serial.c -o serial -lm
	gcc-9 openmp.c -o openmp -fopenmp -fdump-tree-all -lm
	gcc pthreads.c -o pthreads -lm -lpthread

run_serial:
	time ./serial input > serial_output
	cat serial_output

run_openmp:
	time ./openmp input $(P) > openmp_output
	cat openmp_output

run_pthreads:
	time ./pthreads input $(P) > pthreads_output
	cat pthreads_output

clean:
	rm serial openmp pthreads || echo "Continuing..."
	rm serial_output openmp_output pthreads_output || echo "Continuing..."
	rm openmp.c.* || echo "Continuing..."
