#include <stdio.h>
#include <mpi.h>

int main (int argc, char **argv) {
    int rank, proc;

    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &proc);

    if (rank == 0) {
        printf("Hello world from process no. %d\n", rank);
    }

    if (rank != 0) {
        printf("Hello world from process no. %d\n", rank);
    }

    MPI_Finalize();
    return 0;
}