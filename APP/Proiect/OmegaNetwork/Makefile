#!/bin/bash

build:
	gcc serial.c -o serial -lm
	gcc-9 openmp.c -o openmp -fopenmp -fdump-tree-all -lm

run_serial:
	time ./serial input > serial_output
	cat serial_output

run_openmp:
	time ./openmp input $(P) > openmp_output
	cat openmp_output

clean:
	rm serial openmp || echo "Continuing..."
	rm serial_output openmp_output || echo "Continuing..."
	rm openmp.c.* || echo "Continuing..."
