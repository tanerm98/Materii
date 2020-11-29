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

int N = 0;  // number of input/output values (must be power of 2)
int m = 0;  // number of levels per network (computed from N)

int n = 0;  // number of input/output pairs | number of networks to compute

int nr_of_rows = 0;     // number of rows per network
int nr_of_blocks = 0;   // number of blocks in network

int **INPUT, **OUTPUT;

FILE *input_file = NULL;

void open_input(int argc, char *argv[]) {
	if (argc == 2) {
		printf("Getting input from file '%s'...\n", argv[1]);
        input_file = fopen(argv[1], "r");
    } else {
        printf("Getting input from STDIN...\n");
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

	INPUT = (int**) calloc (n, sizeof(int*));
	OUTPUT = (int**) calloc (n, sizeof(int*));

	for (i = 0; i < n; i++) {
		INPUT[i] = (int*) calloc (N, sizeof(int));
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

		OUTPUT[i] = (int*) calloc (N, sizeof(int));
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
        printf("\n");
	}
}

void compute_network_properties() {
	m = log2(N);
    printf("Number of levels: %d\n", m);

    nr_of_rows = N / 2;
    printf("Number of rows: %d\n", nr_of_rows);

    nr_of_blocks = m * nr_of_rows;
    printf("Number of blocks: %d\n", nr_of_blocks);
}

void generate_possibilities(int *version) {
	for (int i = 0; i < nr_of_blocks; i++) {
		if (version[i] == EMPTY) {
			for (int j = 0; j < BLOCK_TYPES_NR; j++) {
				version[i] = BLOCK_TYPES[j];
				if (i == nr_of_blocks - 1) {
                    for (int k = 0; k < nr_of_blocks; k++) {
                        printf("%d, ", version[k]);
                    }
                    printf("\n");
                } else {
                    generate_possibilities(version);
                }
			}
			version[i] = EMPTY;
			return;
		}
	}
}

int main (int argc, char *argv[]) {

	open_input(argc, argv);
	get_input();
	compute_network_properties();

	int *version = (int*) calloc (nr_of_blocks, sizeof(int));
	memset (version, EMPTY, nr_of_blocks * sizeof(int));

	generate_possibilities(version);

	return 0;
}