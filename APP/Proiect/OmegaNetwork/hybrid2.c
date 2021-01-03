#include "header.h"
#include <pthread.h>
#include <mpi.h>

#define ROOT 0

int P = 1;
int rank;

struct thread_data {
	int tid;
	int **v;
	int count;
    int *found_result;
    int io_pair;
};

void check_possibility_pthread(int *version, int io_pair, int *found_result) {
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

void generate_possibilities_pthread(int *version, int io_pair, int *found_result) {
	if (!(*found_result)) {
        for (int i = 2; i < nr_of_blocks; i++) {
	        if (version[i] == EMPTY) {
	            for (int j = 0; j < BLOCK_TYPES_NR; j++) {
	                version[i] = BLOCK_TYPES[j];
	                if (i == nr_of_blocks - 1) {
	                    if (!(*found_result)) {
                            check_possibility_pthread(version, io_pair, found_result);
	                    }
	                } else {
	                    generate_possibilities_pthread(version, io_pair, found_result);
	                }
	            }
	            version[i] = EMPTY;
	            return;
	        }
	    }
    }
}

void *pthread_task(void *arguments) {
    int tid, **v, count, *found_result, io_pair;

	struct thread_data *args = (struct thread_data *)arguments;
	tid = args->tid;
	v = args->v;
	count = args->count;
	found_result = args->found_result;
	io_pair = args->io_pair;

	int start = tid * (double)count / P;
    int end = fmin((tid + 1) * (double)count / P, count);

	for (int i = start; i < end; i++) {
        int *version = (int*) malloc (nr_of_blocks * sizeof(int));
        memset (version, EMPTY, nr_of_blocks * sizeof(int));
        memcpy (version, v[i], 2 * sizeof(int));

        if (!(*found_result)) {
            generate_possibilities_pthread(version, io_pair, found_result);
        }

        free(version);
    }
}

void generate_parallel_possibilities(int io_pair, int *found_result) {

	if (nr_of_blocks == 1) {
        int version[1];
        for (int i = 0; i < BLOCK_TYPES_NR; i++) {
            if (!(*found_result)) {
                version[0] = BLOCK_TYPES[i];
                check_possibility_pthread(version, io_pair, found_result);
            }
        }
        return;
    }

	int **v;
	int count = 0;

	v = (int**) malloc (16 * sizeof(int*));
	for (int i = 0; i < 16; i++) {
		v[i] = (int*) malloc (2 * sizeof(int));
	}

    for (int i = 0; i < BLOCK_TYPES_NR; i++) {
        for (int j = 0; j < BLOCK_TYPES_NR; j++) {
			v[count][0] = BLOCK_TYPES[i];
			v[count][1] = BLOCK_TYPES[j];
			count++;
        }
    }

	int ret;
	pthread_t threads[P];
	for (int i = 0; i < P; i++) {
		struct thread_data *data = (struct thread_data*) malloc (sizeof(struct thread_data));
        data->tid = i;
        data->v = v;
        data->count = count;
        data->found_result = found_result;
        data->io_pair = io_pair;

        ret = pthread_create(&(threads[i]), NULL, pthread_task, (void*)data);
        if (ret < 0) {
            printf("[ERROR] Could not create thread with ID = '%d'\n", i);
        }
	}
	for (int i = 0; i < P; i++) {
        pthread_join(threads[i], NULL);
    }
}

int main (int argc, char *argv[]) {
	clock_t begin = clock();

	MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &P);

    if (rank == 0) {
        open_input(argc, argv);
        get_input();
        compute_network_properties();
    }

    MPI_Bcast (
        /* data         = */ &N,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );
    MPI_Bcast (
        /* data         = */ &n,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );
    MPI_Bcast (
        /* data         = */ &m,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );
    MPI_Bcast (
        /* data         = */ &nr_of_rows,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );
    MPI_Bcast (
        /* data         = */ &nr_of_blocks,
        /* count        = */ 1,
        /* datatype     = */ MPI_INT,
        /* source       = */ ROOT,
        /* communicator = */ MPI_COMM_WORLD
    );

	int start = rank * (double)n / P;
    int end_ = fmin((rank + 1) * (double)n / P, n);

	for (int io_pair = start; io_pair < end_; io_pair++) {
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