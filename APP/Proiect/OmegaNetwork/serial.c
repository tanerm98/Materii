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