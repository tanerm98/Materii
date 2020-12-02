#include "header.h"
#include <omp.h>

int P = 1;

void check_possibility_openmp(int *version, int io_pair, int *found_result) {
	int shuffled_value;

	int *input_values = (int*) malloc (N * sizeof(int));
	int *shuffled_values = (int*) malloc (N * sizeof(int));
	int *output_values;

	memcpy(input_values, INPUT[io_pair], N * sizeof(int));

	for (int level = 0; level < m; level++) {
		for (int i = 0; i < N; i++) {
			shuffled_value = shuffle(i);
			shuffled_values[shuffled_value] = input_values[i];
		}
		free(input_values);

		output_values = go_through_level(level * N / 2, shuffled_values, version);
        input_values = output_values;
	}

	if (memcmp(output_values, OUTPUT[io_pair], N * sizeof(int)) == 0) {
		(*found_result) = 1;
		print_output(version, io_pair);
	}

	free(shuffled_values);
	free(output_values);
}

void generate_possibilities_openmp(int *version, int io_pair, int *found_result) {
	if (!(*found_result)) {
        for (int i = 2; i < nr_of_blocks; i++) {
	        if (version[i] == EMPTY) {
	            for (int j = 0; j < BLOCK_TYPES_NR; j++) {
	                version[i] = BLOCK_TYPES[j];
	                if (i == nr_of_blocks - 1) {
	                    if (!(*found_result)) {
                            check_possibility_openmp(version, io_pair, found_result);
	                    }
	                } else {
	                    generate_possibilities_openmp(version, io_pair, found_result);
	                }
	            }
	            version[i] = EMPTY;
	            return;
	        }
	    }
    }
}

void generate_parallel_possibilities(int io_pair, int *found_result) {
	if (nr_of_blocks == 1) {
        int version[1];
        for (int i = 0; i < BLOCK_TYPES_NR; i++) {
            if (!(*found_result)) {
                version[0] = BLOCK_TYPES[i];
                check_possibility_openmp(version, io_pair, found_result);
            }
        }
        return;
    }

	int v[16][2];
	int count = 0;

    for (int i = 0; i < BLOCK_TYPES_NR; i++) {
        for (int j = 0; j < BLOCK_TYPES_NR; j++) {
			v[count][0] = BLOCK_TYPES[i];
			v[count][1] = BLOCK_TYPES[j];
			count++;
        }
    }

    #pragma omp parallel for shared(found_result) num_threads(P)
    for (int i = 0; i < count; i++) {
        int *version = (int*) malloc (nr_of_blocks * sizeof(int));
        memset (version, EMPTY, nr_of_blocks * sizeof(int));
        memcpy (version, v[i], 2 * sizeof(int));

        if (!(*found_result)) {
            generate_possibilities_openmp(version, io_pair, found_result);
        }

        free(version);
    }
}

int main (int argc, char *argv[]) {
	clock_t begin = clock();

	if (argc == 3) {
        P = atoi(argv[2]);
        printf("Number of processors requested: %d\n\n", P);
    } else {
        printf("Using default number of processors: 1!\n\n");
    }

	open_input(argc, argv);
	get_input();
	compute_network_properties();

	for (int io_pair = 0; io_pair < n; io_pair++) {
		found_result = 0;
		generate_parallel_possibilities(io_pair, &found_result);
		if (!found_result) {
			printf("Invalid INPUT/OUTPUT pair! No OMEGA network possible!\n");
		}
	}

	clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Total execution time = [%lf]\n", time_spent);

	return 0;
}