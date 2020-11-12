#include <stdio.h>
#include <mpi.h>

#define SIZE 100

int main (int argc, char **argv) {
    int rank, proc;
    int v[SIZE], sum = 0, part_sum = 0;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc);

	// only works for SIZE % proc == 0
    int chunk = SIZE / proc;
    int start = rank * chunk;
    int stop = (rank + 1) * chunk;

    if (rank == 0) {
        for (int i = 0; i < SIZE; i++) {
            v[i] = i + 1;   // suma de la 1 la SIZE
        }
        for (int i = 1; i < proc; i++) {
            MPI_Send (
                /* data         = */ v,
                /* count        = */ SIZE,
                /* datatype     = */ MPI_INT,
                /* destination  = */ i,
                /* tag          = */ 0,
                /* communicator = */ MPI_COMM_WORLD
            );
        }

        for (int i = start; i < stop; i++) {
            part_sum += v[i];
        }
        sum += part_sum;

        for (int i = 1; i < proc; i++) {
            MPI_Recv (
                /* data         = */ &part_sum,
                /* count        = */ 1,
                /* datatype     = */ MPI_INT,
                /* source       = */ i,
                /* tag          = */ 0,
                /* communicator = */ MPI_COMM_WORLD,
                /* status       = */ MPI_STATUS_IGNORE
            );
            sum += part_sum;
        }

        printf("The total sum is %d!\n", sum);
    }

    if (rank != 0) {
        MPI_Recv (
        	/* data         = */ v,
        	/* count        = */ SIZE,
        	/* datatype     = */ MPI_INT,
        	/* source       = */ 0,
        	/* tag          = */ 0,
        	/* communicator = */ MPI_COMM_WORLD,
        	/* status       = */ MPI_STATUS_IGNORE
        );

        for (int i = start; i < stop; i++) {
            part_sum += v[i];
        }

        MPI_Send (
            /* data         = */ &part_sum,
            /* count        = */ 1,
            /* datatype     = */ MPI_INT,
            /* destination  = */ 0,
            /* tag          = */ 0,
            /* communicator = */ MPI_COMM_WORLD
        );
    }

    MPI_Finalize();
    return 0;
}