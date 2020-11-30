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

void print_output(int *blocks, int io_pair) {
	// construct row separator
	char *row_separator = (char*) malloc (10 * m * sizeof(char));
	memset(row_separator, '-', 10 * m * sizeof(char));

	// construct header
	char *header = (char*) calloc (10 * m, sizeof(char));
	char word[20];
	char *LEVEL = "LEVEL";
	for (int level = m - 1; level >= 0; level--) {
		sprintf(word, "(%s %d)", LEVEL, level);
		strcat(header, word);

		// add padding
		int padding = 10 - strlen(header) % 10;
		if (padding != 10) {
			for (int i = 0; i < padding; i++) {
				strcat(header, " ");
			}
		}
	}

	printf("\nOMEGA network for INPUT/OUTPUT pair no. %d:\n\n", io_pair + 1);
	printf("         %s\n         %s\n", header, row_separator);

	for (int row = 0; row < nr_of_rows; row++) {
		printf("(ROW %d) ", row);
		for (int level = row; level < nr_of_blocks; level += nr_of_rows) {
			switch(blocks[level]) {
				case DIRECT:
					printf("|  DIRECT ");
					break;
				case INFERIOR:
                    printf("| INFERIOR");
                    break;
                case INVERSE:
                    printf("| INVERSE ");
                    break;
                case SUPERIOR:
                    printf("| SUPERIOR");
                    break;
                default:
                    break;
			}
		}
		printf("|\n         %s\n", row_separator);
	}
	printf("\n");
}

int main (int argc, char *argv[]) {

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

	return 0;
}