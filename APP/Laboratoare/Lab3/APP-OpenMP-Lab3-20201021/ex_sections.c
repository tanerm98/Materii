/******************************************************************************
* FILE: omp_workshare2.c
* DESCRIPTION:
*   OpenMP Example - Sections Work-sharing - C Version
*   In this example, the OpenMP SECTION directive is used to assign
*   different array operations to each thread that executes a SECTION. 
* AUTHOR: Blaise Barney  5/99
* LAST REVISED: 07/16/07
******************************************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define N 10000000
float *a, *b, *c, *d;

int main (int argc, char *argv[]) 
{

	a = (float*) malloc (N * sizeof(float));
	b = (float*) malloc (N * sizeof(float));
	c = (float*) calloc (N, sizeof(float));
	d = (float*) calloc (N, sizeof(float));

    int i;
    double t1,t2;
    /* Some initializations */
    #pragma omp parallel for private(i) shared(a, b)
    for (i = 0; i < N; i++) {
        a[i] = i * 1.5;
        b[i] = i + 22.35;
    }

	////////////////////////////SERIAL//////////////////////////////////////////////////////////////////////////////////
    t1 = omp_get_wtime();
    for (i=0; i<N; i++) {
        c[i] = a[i] + b[i];
    }
    for (i=0; i<N; i++) {
        d[i] = a[i] * b[i];
    }
    t2 = omp_get_wtime();
    printf("Duration serial:                                    %g\n",t2-t1);

	////////////////////////////////PARALLEL FORS///////////////////////////////////////////////////////////////////////
    t1 = omp_get_wtime();
    #pragma omp parallel for private(i) shared(c)
    for (i=0; i<N; i++) {
        c[i] = a[i] + b[i];
    }
    #pragma omp parallel for private(i) shared(d)
    for (i=0; i<N; i++) {
        d[i] = a[i] * b[i];
    }
    t2 = omp_get_wtime();
    printf("Duration parallel fors:                             %g\n",t2-t1);

	////////////////////////////////2 PARALLEL SECTIONS/////////////////////////////////////////////////////////////////
    t1 = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                for (i=0; i<N; i++) {
                    c[i] = a[i] + b[i];
                }
            }
            #pragma omp section
            {
                for (i=0; i<N; i++) {
                    d[i] = a[i] * b[i];
                }
            }
        }
    }
    t2 = omp_get_wtime();
    printf("Duration 2 parallel sections:                       %g\n",t2-t1);

    /////////////////////////////////2 PARALLEL SECTIONS WITH PARALLEL FORS/////////////////////////////////////////////
    t1 = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                #pragma omp parallel for private(i) shared(c)
                for (i=0; i<N; i++) {
                    c[i] = a[i] + b[i];
                }
            }
            #pragma omp section
            {
                #pragma omp parallel for private(i) shared(d)
                for (i=0; i<N; i++) {
                    d[i] = a[i] * b[i];
                }
            }
        }
    }
    t2 = omp_get_wtime();
    printf("Duration 2 parallel sections with parallel fors:    %g\n",t2-t1);

    return 0;
}
