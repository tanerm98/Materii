#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define MAX_SIZE 1000000
#define LETTERS 26

#define ROOT 0

#define A 65
#define Z 90
#define a 97
#define z 122

int main (int argc, char **argv) {
    int rank, proc;
    int SIZE, chunk_, chunk, start, stop;
    int i, j, rest;
    char *v, *part_v;
    int alphabet[LETTERS], *total;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc);

    v = (char*) calloc (MAX_SIZE, sizeof(char));

    if (rank == ROOT) {
        printf("Please input a string!\n");
        fgets(v, MAX_SIZE, stdin);
        SIZE = strlen(v);

		// Add padding
        if (SIZE % proc != 0) {
            rest = proc - (SIZE % proc);
            while (rest > 0) {
                v[SIZE++] = 0;
                rest--;
            }
        }
    }

    MPI_Bcast (
        /* data         = */ &SIZE,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );

	chunk_ = SIZE / proc;
    start = rank * chunk_;
    stop = fmin((rank + 1) * chunk_, SIZE);
    chunk = stop - start;

    part_v = (char*) calloc (chunk, sizeof(char));
    total = (int*) calloc (LETTERS * proc, sizeof(int));
    memset (alphabet, 0, LETTERS * sizeof(int));

    MPI_Scatter(v, chunk, MPI_UNSIGNED_CHAR, part_v, chunk, MPI_UNSIGNED_CHAR, ROOT, MPI_COMM_WORLD);

    for (i = 0; i < chunk; i++) {
        if ((part_v[i] >= A) && (part_v[i] <= Z)) {
			alphabet[part_v[i] - A]++;
        } else if ((part_v[i] >= a) && (part_v[i] <= z)) {
            alphabet[part_v[i] - a]++;
        }
    }

    MPI_Gather(&alphabet, LETTERS, MPI_INT, total, LETTERS, MPI_INT, ROOT, MPI_COMM_WORLD);

	if (rank == ROOT) {
		for (i = 0; i < LETTERS; i++) {
            for (j = 1; j < proc; j++) {
                total[i] += total[i + j * LETTERS];
            }
        }

        for (i = 0; i < LETTERS; i++) {
            if (total[i] != 0) {
	            printf("%c: %d\n", A + i, total[i]);
            }
        }
	}

    MPI_Finalize();
    return 0;
}