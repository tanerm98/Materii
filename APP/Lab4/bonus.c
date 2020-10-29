#include <stdio.h>
#include <mpi.h>
#include <stdlib.h>

#define SIZE 100
#define ROOT 0

int main (int argc, char **argv) {
    int rank, proc;
    int v[100], *part_v, *part_sums, sum = 0, part_sum = 0, coefficient;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc);

	// only works for SIZE % proc == 0
    int chunk = SIZE / proc;
    int start = rank * chunk;
    int stop = (rank + 1) * chunk;

    part_v = (int*) malloc (chunk * sizeof(int));
    part_sums = (int*) malloc (proc * sizeof(int));

    if (rank == ROOT) {
        for (int i = 0; i < SIZE; i++) {
            v[i] = i + 1;   // suma de la 1 la SIZE
        }

        printf("Please input a coefficient!\n");
        scanf("%d", &coefficient);
        MPI_Bcast (
            /* data         = */ &coefficient,
            /* count        = */ 1,
            /* datatype     = */ MPI_INT,
            /* source       = */ ROOT,
            /* communicator = */ MPI_COMM_WORLD
        );

        MPI_Scatter(v, chunk, MPI_INT, part_v, chunk, MPI_INT, ROOT, MPI_COMM_WORLD);

        for (int i = 0; i < chunk; i++) {
            part_sum += part_v[i];
        }
        part_sum *= coefficient;

        MPI_Gather(&part_sum, 1, MPI_INT, part_sums, 1, MPI_INT, ROOT, MPI_COMM_WORLD);

        for (int i = 0; i < proc; i++) {
            sum += part_sums[i];
        }

        printf("The total sum is %d!\n", sum);
    }

    if (rank != 0) {
        MPI_Bcast (
            /* data         = */ &coefficient,
            /* count        = */ 1,
            /* datatype     = */ MPI_INT,
            /* source       = */ ROOT,
            /* communicator = */ MPI_COMM_WORLD
        );

        MPI_Scatter(v, chunk, MPI_INT, part_v, chunk, MPI_INT, ROOT, MPI_COMM_WORLD);

        for (int i = 0; i < chunk; i++) {
            part_sum += part_v[i];
        }
        part_sum *= coefficient;

        MPI_Gather(&part_sum, 1, MPI_INT, part_sums, 1, MPI_INT, ROOT, MPI_COMM_WORLD);
    }

    MPI_Finalize();
    return 0;
}