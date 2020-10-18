#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#define ROW 10000
#define COL 10000

void init_data (int m, int n, double *a, double *b, double *c)
{
   int i, j;

    for (j = 0; j < n; j++) {
        c[j] = 1.0;
    }

   #pragma omp parallel private (i,j) shared(a, b, n, m)
   for (i=0; i<m; i++)
   {
        a[i] = -2005.0;
        for (j = 0; j < n; j++) {
            b[i * n + j] = i;
        }
    }

}

void matrix_row(int m, int n, double *a, double *b, double *c)
{
   int i, j;

	omp_set_num_threads(8);
    #pragma omp parallel private (i, j) shared(a, b, c, n, m)
    {
        for (i = 0; i < m; i++) {
            a[i] = 0.0;
            for (j = 0; j < n; j++) {
                a[i] += b[i * n + j] * c[j];
            }
        }
    }
}

int main() {
    double *a = malloc (ROW * COL * sizeof(double));
    double *b = malloc (ROW * COL * sizeof(double));
    double *c = malloc (ROW * COL * sizeof(double));
    double t1, t2;

    t1 = omp_get_wtime();
    init_data(ROW, COL, a, b, c);
    t2 = omp_get_wtime();
    printf("Total execution time (init data) = %lf\n", (t2 - t1));

    t1 = omp_get_wtime();
    matrix_row(ROW, COL, a, b, c);
    t2 = omp_get_wtime();
    printf("Total execution time (init data) = %lf\n", (t2 - t1));

    free(a);
    free(b);
    free(c);
    return 0;
}