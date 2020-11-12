#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define SIZE 1000000

int main() {

    int a[SIZE], i;
    long sum = 0;

	#pragma omp parallel for private(i) shared(a)
    for (i = 0; i < SIZE; i++) {
        a[i] = i;
    }

    #pragma omp parallel for reduction(+:sum ) private(i)
	for (i = 0; i < SIZE; i++) {
	    sum += a[i];
	}


    printf("Total sum = %ld\n", sum);

    return 0;
}