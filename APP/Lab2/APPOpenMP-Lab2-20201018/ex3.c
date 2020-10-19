#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define A 65
#define Z 90
#define LETTERS 26
#define CHUNK 25

int alphabet[LETTERS];

void serial() {
	FILE *fp[101];
    char buff[101][11];
    char filename[10];

    for (int i = 0; i < LETTERS; i++) {
        alphabet[i] = 0;
    }

    for (int i = 1; i <= 100; i++) {
        sprintf(filename, "files/f%d", i);
        fp[i] = fopen(filename, "r");
        fgets(buff[i], 100, (FILE*)fp[i]);

        for (int j = 1; j < strlen(buff[i]); j++) {
            if ((buff[i][j] >= A) && (buff[i][j] <= Z)) {
                alphabet[buff[i][j] - A]++;
            }
        }
        fclose(fp[i]);
    }
}

void parallel() {
	FILE *fp[101];
    char buff[101][11];
    char filename[10];

    #pragma omp parallel shared(alphabet, fp, buff) private(filename)
    {
        #pragma omp for schedule(static, CHUNK)
        for (int i = 0; i < LETTERS; i++) {
            alphabet[i] = 0;
        }

		#pragma omp for schedule(static, CHUNK)
        for (int i = 1; i <= 100; i++) {
            sprintf(filename, "files/f%d", i);
            fp[i] = fopen(filename, "r");
            fgets(buff[i], 100, (FILE*)fp[i]);

            for (int j = 1; j < strlen(buff[i]); j++) {
                if ((buff[i][j] >= A) && (buff[i][j] <= Z)) {
                    alphabet[buff[i][j] - A]++;
                }
            }
            fclose(fp[i]);
        }
    }
}

int main() {
	double t1, t2;

	t1 = omp_get_wtime();
	serial();
	t2 = omp_get_wtime();
	for (int i = 0; i < LETTERS; i++) {
        char c = A + i;
        printf("%c:%d, ", c, alphabet[i]);
    }
	printf("\nSerial execution time: %g\n",t2 - t1);

	t1 = omp_get_wtime();
    parallel();
    t2 = omp_get_wtime();
    for (int i = 0; i < LETTERS; i++) {
        char c = A + i;
        printf("%c:%d, ", c, alphabet[i]);
    }
    printf("\nParallel execution time: %g\n",t2 - t1);

	return(0);
}