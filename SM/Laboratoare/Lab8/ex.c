#include <math.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_SIZE 1000000
#define LETTERS 26

#define A 65
#define Z 90
#define a 97
#define z 122

#define P 4

char *string;
int *alphabet;
int N;

pthread_mutex_t lock1, lock2;

void *compute_characters_number(void *thread_id) {
	int ID = *((int*)thread_id);
	int start, end;

	start = ID * (double)N / P;
    end = fmin((ID + 1) * (double)N / P, N);

	for (int i = start; i < end; i++) {
        if ((string[i] >= A) && (string[i] <= Z)) {
            pthread_mutex_lock(&lock1);
            alphabet[string[i] - A]++;
            pthread_mutex_unlock(&lock1);
        } else if ((string[i] >= a) && (string[i] <= z)) {
            pthread_mutex_lock(&lock2);
            alphabet[string[i] - a]++;
            pthread_mutex_unlock(&lock2);
        }
    }
}

int main (int argc, char **argv) {
    int chunk_, chunk, start, stop;
    int i, rest, ret;

    string = (char*) calloc (MAX_SIZE, sizeof(char));
    alphabet = (int*) calloc (LETTERS, sizeof(int));

    printf("Please input a string!\n");
    fgets(string, MAX_SIZE, stdin);
    N = strlen(string);

    pthread_t threads[P];
    for (i = 0; i < P; i++) {
        int *thread_id = malloc(sizeof(int));
        *thread_id = i;
        ret = pthread_create(&(threads[i]), NULL, compute_characters_number, (void*)thread_id);
        if (ret < 0) {
            printf("[ERROR] Could not create thread with ID = '%d'\n", i);
        }
    }
    for (i = 0; i < P; i++) {
        pthread_join(threads[i], NULL);
    }

    for (i = 0; i < LETTERS; i++) {
        if (alphabet[i] != 0) {
            printf("%c: %d\n", A + i, alphabet[i]);
        }
    }

    return 0;
}