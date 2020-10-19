#!/usr/bin/env python3

import logging
import math
import threading
import time

logging.getLogger().setLevel(logging.INFO)

N = 10
BARRIER = threading.Barrier(N ** 3)

A = []
B = []
C = []
V = []

def init_matrixes():
    global A, B, C, V

    A = []
    B = []
    C = []
    V = []

    row = []
    zeros = []
    for i in range(N):
        row.append(i)
        zeros.append(0)

    for i in range(N):
        A.append(row.copy())
        B.append(row.copy())
        C.append(zeros.copy())

    for i in range(N):
        V.append([])
        for j in range(N):
            V[i].append([])
            V[i][j] = zeros.copy()

def show_matrix(X):
    print("####################")
    for row in X:
        print(row)
    print("####################")


def multiply_sequential():
    global A, B, C

    for i in range(N):
        for j in range(N):
            C[i][j] = 0
            for k in range(N):
                C[i][j] += A[i][k] * B[k][j]


def crcw_thread(i, j, k):
    global A, B, C

    logging.info("Computing A[{}][{}] * B[{}][{}]...".format(i, k, k, j))
    product = A[i][k] * B[k][j]

    logging.info("Adding product to C[{}][{}]...".format(i, j))
    C[i][j] += product

def multiply_crcw():
    global A, B, C

    processors = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                processors.append(threading.Thread(target=crcw_thread, args=(i, j, k)))

    for i in range(len(processors)):
        processors[i].start()

    for i in range(len(processors)):
        processors[i].join()


def crew_thread(i, j, k):
    global A, B, C, V

    logging.info("Computing V[{}][{}][{}]...".format(i, j, k))
    V[i][j][k] = A[i][k] * B[k][j]

    logging.info("Reducing V[{}][{}][0]...".format(i, j))
    for m in range(int(math.log2(N))):
        if (k % (2 ** (m + 1))) == 0:
            if (k + (2 ** m)) < N:
                V[i][j][k] += V[i][j][k + (2 ** m)]

    C[i][j] += V[i][j][0]

def multiply_crew():
    global A, B, C, V

    processors = []
    for i in range(N):
        for j in range(N):
            for k in range(N):
                processors.append(threading.Thread(target=crew_thread, args=(i, j, k)))
    for i in range(len(processors)):
        processors[i].start()
    for i in range(len(processors)):
        processors[i].join()

def main():
    global A, B, C

    init_matrixes()
    start_time_1 = time.time()
    multiply_sequential()
    seq_elapsed_time = time.time() - start_time_1
    # show_matrix(C)

    init_matrixes()
    start_time_2 = time.time()
    multiply_crcw()
    crcw_elapsed_time = time.time() - start_time_2
    # show_matrix(C)

    init_matrixes()
    start_time_3 = time.time()
    multiply_crew()
    crew_elapsed_time = time.time() - start_time_3
    # show_matrix(C)

    logging.info("Sequential: {}s".format(seq_elapsed_time))
    logging.info("CRCW: {}s".format(crcw_elapsed_time))
    logging.info("CREW: {}s".format(crew_elapsed_time))


if __name__ is main():
    main()

