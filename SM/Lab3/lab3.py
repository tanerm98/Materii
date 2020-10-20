#!/usr/bin/python3
import math

N = 8
m = int(math.log2(N))

def shuffle(i):
    return int((int(2 * i) + int(2 * i / N)) % N)

def main():
    inputt = list(range(N))
    intermediary = [0] * N
    output = []

    for _ in range(m):
        for i in range(N):
            shuffled_value = shuffle(i)
            intermediary[shuffled_value] = inputt[i]
        output = intermediary.copy() # intermediary -> output TODO
        inputt = output.copy()
        intermediary = [0] * N

    for i in range(N):
        print(output[i])


if __name__ == '__main__':
    main()
