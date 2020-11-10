#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <math.h>
#include <string.h>

#define MAX_SIZE 1000000
#define LETTERS 26

#define A 65
#define Z 90
#define a 97
#define z 122

int main (int argc, char **argv) {
    int SIZE;
    int i, rest;
    char *v;
    int alphabet[LETTERS];
    int tid;

    v = (char*) calloc (MAX_SIZE, sizeof(char));
    memset (alphabet, 0, LETTERS * sizeof(int));

    printf("Please input a string!\n");
    fgets(v, MAX_SIZE, stdin);

    SIZE = strlen(v);

    #pragma omp parallel shared(v, alphabet) private(tid, i)
    {
        #pragma omp for schedule (guided, 4)
        for (i = 0; i < SIZE; i++) {
            if ((v[i] >= A) && (v[i] <= Z)) {
                alphabet[v[i] - A]++;
            } else if ((v[i] >= a) && (v[i] <= z)) {
                alphabet[v[i] - a]++;
            }
        }

        #pragma omp for schedule (static, 4)
        for (i = 0; i < LETTERS; i++) {
            if (alphabet[i] != 0) {
                printf("%c: %d\n", A + i, alphabet[i]);
            }
        }
    }

    return 0;
}