#include "header.h"

void generate_possibilities(int *version, int io_pair) {
	if (!found_result) {
        for (int i = 0; i < nr_of_blocks; i++) {
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

void check_possibility(int *version, int io_pair) {
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
		found_result = 1;
		print_output(version, io_pair);
	}

	free(shuffled_values);
	free(output_values);
}

int main (int argc, char *argv[]) {
	clock_t begin = clock();

	open_input(argc, argv);
	get_input();
	compute_network_properties();

	int *version = (int*) malloc (nr_of_blocks * sizeof(int));

	for (int io_pair = 0; io_pair < n; io_pair++) {
		found_result = 0;
		memset (version, EMPTY, nr_of_blocks * sizeof(int));
		generate_possibilities(version, io_pair);
		if (!found_result) {
			printf("Invalid INPUT/OUTPUT pair! No OMEGA network possible!\n");
		}
	}

	free(version);

	clock_t end = clock();
    double time_spent = (double)(end - begin) / CLOCKS_PER_SEC;
    printf("Total execution time = [%lf]\n", time_spent);

	return 0;
}