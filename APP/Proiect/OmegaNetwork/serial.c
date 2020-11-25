#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define DIRECT      1
#define INFERIOR    2
#define INVERSE     3
#define SUPERIOR    4

#define BLOCK_TYPES_NR 4
#define EMPTY -1

int BLOCK_TYPES[BLOCK_TYPES_NR] = {DIRECT, INFERIOR, INVERSE, SUPERIOR};

int N = 8;

void cartesian(int version[N]) {
	for (int i = 0; i < N; i++) {
		if (version[i] == EMPTY) {
			for (int j = 0; j < BLOCK_TYPES_NR; j++) {
				version[i] = BLOCK_TYPES[j];
				if (i == N - 1) {
                    for (int k = 0; k < N; k++) {
                        printf("%d, ", version[k]);
                    }
                    printf("\n");
                } else {
                    cartesian(version);
                }
			}
			version[i] = EMPTY;
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