#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void f1() {
    for (int i = 0; i < 10; i++) {
        printf("f1 - iteration %d - thread %d\n", i, omp_get_thread_num());
        sleep(1);
    }
}

void f2() {
    for (int i = 0; i < 10; i++) {
        printf("\tf2 - iteration %d - thread %d\n", i, omp_get_thread_num());
        sleep(1);
    }
}

int main() {
    int i;
    #pragma omp parallel
    {
        #pragma omp sections
        {
            #pragma omp section
            {
                f1();
            }
            #pragma omp section
            {
                f2();
            }
        }

        printf("Ceva frumos in thread-ul %d\n", omp_get_thread_num());

        #pragma omp barrier

        #pragma omp single
        {
            printf("Ceva frumos in thread-ul %d, care e singur\n\n", omp_get_thread_num());
        }

        #pragma omp master
        {
            printf("Ceva frumos in thread-ul master %d\n", omp_get_thread_num());
        }
    }

    #pragma omp parallel for ordered private(i)
    for (i = 0; i < 10; i++) {
        #pragma omp ordered
        printf("iteration %d thread no. %d\n", i, omp_get_thread_num());
    }

    int sum = 0;
    #pragma omp parallel
    {
        #pragma omp atomic
        sum += 2;
    }
    printf("sum = %d\n", sum);

    #pragma omp parallel for lastprivate(i)
    for (i = 0; i < 20; i++) {
        // do stuff
    }
    printf("Value of i = %d\n", i);

    return 0;
}