#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DIRECT      0
#define INFERIOR    1
#define INVERSE     2
#define SUPERIOR    3

#define BLOCK_TYPES_NR 4
#define EMPTY -1

int BLOCK_TYPES[BLOCK_TYPES_NR] = {DIRECT, INFERIOR, INVERSE, SUPERIOR};

int N = 8;

void cartesian(int *version) {
	int copy[N];
	memcpy(copy, version, N * sizeof(int));

	for (int i = 0; i < N; i++) {
		if (copy[i] == EMPTY) {
			for (int j = 0; j < BLOCK_TYPES_NR; j++) {
				copy[i] = BLOCK_TYPES[j];
				if (i == N - 1) {
                    for (int k = 0; k < N; k++) {
                        printf("%d, ", copy[k]);
                    }
                    printf("\n");
                } else {
                    cartesian(copy);
                }
			}
			return;
		}
	}
}

int main() {

	int version[N];
	memset (version, EMPTY, N * sizeof(int));
	cartesian(version);

	return 0;
}