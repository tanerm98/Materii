#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define DIRECT      1
#define INFERIOR    2
#define INVERSE     3
#define SUPERIOR    4

#define BLOCK_TYPES_NR 4
#define EMPTY -1

int BLOCK_TYPES[BLOCK_TYPES_NR] = {DIRECT, INFERIOR, INVERSE, SUPERIOR};
char BLOCK_NAMES[BLOCK_TYPES_NR][10] = {"DIRECT", "INFERIOR", "INVERSE", "SUPERIOR"};

int N = 0;  // number of input/output values (must be power of 2)
int m = 0;  // number of levels per network (computed from N)

int n = 0;  // number of input/output pairs | number of networks to compute

int nr_of_rows = 0;     // number of rows per network
int nr_of_blocks = 0;   // number of blocks in network

int **INPUT, **OUTPUT;

FILE *input_file = NULL;

int found_result = 0;


void open_input(int argc, char *argv[]);
void get_input();
void compute_network_properties();
void generate_possibilities(int *version, int io_pair);
int shuffle(int i);
void check_possibility(int *version, int io_pair);
int* go_through_level(int start, int *values, int *blocks);
void print_output(int *blocks, int io_pair);

void open_input(int argc, char *argv[]) {
	if (argc >= 2) {
		printf("Getting input from file '%s'...\n\n", argv[1]);
        input_file = fopen(argv[1], "r");
    } else {
        printf("Getting input from STDIN...\n\n");
        input_file = stdin;
    }

	if (input_file == NULL) {
        printf("[ERROR] Could not open input!\n");
        exit(1);
    }
}

void get_input() {
	int ret, i, j;

	printf("Number of input/output values: ");
	ret = fscanf(input_file, "%d", &N);
	if ((!ret) || (N <= 0)) {
		printf("[ERROR] please input correct value for 'N'!\n");
		exit(1);
	}
	if (input_file != stdin) {
		printf("%d\n", N);
	}
	if ((N & (N - 1)) != 0) {
		printf("N must be a power of 2!\n");
		exit(1);
	}

	printf("Number of input/output pairs: ");
    ret = fscanf(input_file, "%d", &n);
	if ((!ret) || (n <= 0)) {
        printf("[ERROR] please input correct value for 'n'!\n");
        exit(1);
    }
    if (input_file != stdin) {
        printf("%d\n", n);
    }
    printf("\n");

	INPUT = (int**) malloc (n * sizeof(int*));
	OUTPUT = (int**) malloc (n * sizeof(int*));

	for (i = 0; i < n; i++) {
		INPUT[i] = (int*) malloc (N * sizeof(int));
		printf("INPUT  no. %d: ", i + 1);
		for (j = 0; j < N; j++) {
		    ret = fscanf(input_file, "%d", &INPUT[i][j]);
			if (!ret) {
			    printf("[ERROR] please input correct values for INPUT no. %d!\n", i + 1);
			    free(INPUT);
                free(OUTPUT);
			    exit(1);
			}
			if (input_file != stdin) {
		        printf("%d ", INPUT[i][j]);
            }
		}
		printf("\n");

		OUTPUT[i] = (int*) malloc (N * sizeof(int));
		printf("OUTPUT no. %d: ", i + 1);
		for (j = 0; j < N; j++) {
            ret = fscanf(input_file, "%d", &OUTPUT[i][j]);
            if (!ret) {
                printf("[ERROR] please input correct values for OUTPUT no. %d!\n", i + 1);
                free(INPUT);
                free(OUTPUT);
                exit(1);
            }
            if (input_file != stdin) {
                printf("%d ", OUTPUT[i][j]);
            }
        }
        printf("\n\n");
	}
}

void compute_network_properties() {
	m = log2(N);
    printf("Number of levels:  %d\n", m);

    nr_of_rows = N / 2;
    printf("Number of rows:    %d\n", nr_of_rows);

    nr_of_blocks = m * nr_of_rows;
    printf("Number of blocks: %d\n", nr_of_blocks);

    printf("\n");
}

int shuffle(int i) {
	return (int)(((2 * i) + (int)(2 * i / N)) % N);
}

int* go_through_level(int start, int *values, int *blocks) {
	int *output = (int*) malloc (N * sizeof(int));

    for (int i = start; i < start + N / 2; i++) {
        int j = 2 * (i - start);

        if (blocks[i] == DIRECT) {
            output[j] = values[j];
            output[j + 1] = values[j + 1];
        } else if (blocks[i] == INFERIOR) {
            output[j] = values[j + 1];
            output[j + 1] = values[j + 1];
        } else if (blocks[i] == INVERSE) {
            output[j] = values[j + 1];
            output[j + 1] = values[j];
        } else if (blocks[i] == SUPERIOR) {
            output[j] = values[j];
            output[j + 1] = values[j];
        }
    }

    return output;
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