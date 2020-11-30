#include "header.h"
#include <omp.h>

int P = 1;  // default number of processes

void generate_possibilities(int *version, int io_pair) {
	if (!found_result) {
        for (int i = 1; i < nr_of_blocks; i++) {
	        if (version[i] == EMPTY) {
	            for (int j = 0; j < BLOCK_TYPES_NR; j++) {
	                version[i] = BLOCK_TYPES[j];
	                if (i == nr_of_blocks - 1) {
	                    if (!found_result) {
                            check_possibility(version, io_pair);
	                    }
	                } else {
	                    generate_possibilities(version, io_pair);
	                }
	            }
	            version[i] = EMPTY;
	            return;
	        }
	    }
    }
}

void generate_parallel_possibilities(int io_pair) {

    #pragma omp parallel for shared(found_result) num_threads(P)
    for (int j = 0; j < BLOCK_TYPES_NR; j++) {

        int tid = omp_get_thread_num();
		printf("Computing network with first block %s from thread %d...\n", BLOCK_NAMES[j], tid);

        int *version = (int*) malloc (nr_of_blocks * sizeof(int));
        memset (version, EMPTY, nr_of_blocks * sizeof(int));
        version[0] = BLOCK_TYPES[j];

        if (0 == nr_of_blocks - 1) {
            if (!found_result) {
                check_possibility(version, io_pair);
            }
        } else {
            if (!found_result) {
                generate_possibilities(version, io_pair);
            }
        }

        free(version);
    }
}

int main (int argc, char *argv[]) {

	if (argc == 3) {
		P = atoi(argv[2]);
		printf("Number of processors: %d\n\n", P);
	} else {
		printf("Using default number of processors: 1!\n\n");
	}

	open_input(argc, argv);
	get_input();
	compute_network_properties();

	for (int io_pair = 0; io_pair < n; io_pair++) {
		found_result = 0;
		generate_parallel_possibilities(io_pair);
		if (!found_result) {
			printf("Invalid INPUT/OUTPUT pair! No OMEGA network possible!\n");
		}
	}

	return 0;
}