#!/usr/bin/python3
import itertools
import math
import threading

N = 0
m = 0

nr_of_levels = 0
nr_of_rows = 0
nr_of_blocks = 0

middle_level_index = 0

DIRECT = 0
INFERIOR = 1
INVERSE = 2
SUPERIOR = 3
BLOCK_TYPES = [DIRECT, INFERIOR, INVERSE, SUPERIOR]

result = None

THREADS = 4


def generate_all_posibilities():
    """
    Generates all possible block types variations
    :param nr_of_blocks: the total number of blocks in the network
    :return: generated possibilities
    """
    blocks = [BLOCK_TYPES] * nr_of_blocks
    product = itertools.product(*blocks)

    return product


def go_through_level(start, values, blocks):
    """
    Simulates the shuffled input going through a level
    :param start: index or first block from level
    :param values: shuffled values
    :param blocks: all blocks
    :return: input processed through level
    """
    output = [0] * N

    for i in range(int(start), int(start + (N / 2))):
        j = int(2 * (i - start))

        if blocks[i] == DIRECT:
            output[j] = values[j]
            output[j + 1] = values[j + 1]
        elif blocks[i] == INFERIOR:
            output[j] = values[j + 1]
            output[j + 1] = values[j + 1]
        elif blocks[i] == INVERSE:
            output[j] = values[j + 1]
            output[j + 1] = values[j]
        elif blocks[i] == SUPERIOR:
            output[j] = values[j]
            output[j + 1] = values[j]

    return output


def shuffle(index, input_level_index):
    """
        - computes `rank` of Benes subnetwork (Benes network consists in multiple merged subnetworks)
        (`rank` = number of inputs for subnetwork)
            - if `input_level_index` == 0 -> return `i`
            - if `input_level_index` <= `middle_level_index` -> [`rank` = `N` / (2 ^ (`input_level_index` - 1))]
            - if `input_level_index` > `middle_level_index` -> [`rank` = `N` / (2 ^ `nr_of_levels` - `input_level_index` - 1)]
        - computes index of block where `i` is, `src_block_index`
            - src_block_index = int(i / 2) + 1
        - computes destination bloc, based on `rank`, `src_block_index` and `i`
            - i % 2 == 1:
                - TODO `dst_block_index`
                `dst_block_index` = upper(`src_block_index` / 2)
            - i % 2 == 0:
                - TODO `dst_block_index`
                `dst_block_index` = upper(`src_block_index` / 2) + `rank`/2
        - returns index of input from destination block, `shuffled`
            - `dst_block_index` % 2 == 1 -> 1
            - `dst_block_index` % 2 == 0 -> 2

    """

    return 0


def print_output(INPUT, OUTPUT, steps, nr_of_rows, nr_of_blocks):
    """
    :param INPUT: input values
    :param OUTPUT: output values
    :param steps: steps in each level
    :param nr_of_rows: N/2
    :param nr_of_blocks: N/2*log(N)
    """
    global result

    # Print result
    print("N: {}\nk: {}\n".format(N, m))
    print("Input: {}\nOutput: {}\n".format(INPUT, OUTPUT))

    print("Block types (as seen on the scheme):")
    network = []
    for i in range(nr_of_rows):
        blocks = []
        for j in range(0 + i, nr_of_blocks + i, nr_of_rows):
            if result[j] == DIRECT:
                blocks.append("DIRECT")
            elif result[j] == INFERIOR:
                blocks.append("INFERIOR")
            elif result[j] == INVERSE:
                blocks.append("INVERSE")
            elif result[j] == SUPERIOR:
                blocks.append("SUPERIOR")
        network.append(blocks)
    col_width = max(len(word) for row in network for word in row) + 2
    for row in network:
        padded_row = [word.ljust(col_width) for word in row]
        blocks_to_string = ""
        for block in padded_row:
            blocks_to_string += str(block)
        print(blocks_to_string)

    print("\nDetailed steps per level:")
    col_width = max(len(steps[step]) for step in steps) + 2
    step_nr = 0
    for step in steps:
        if step_nr % 3 == 0:
            print("Level {}:".format(int(step_nr / 3 + 1)))
        step_nr += 1
        print("{}: {}".format(str(step).ljust(col_width), str(steps[step]).ljust(col_width)))


def check_possibility(INPUT, OUTPUT, possibilities, start, end):
    global result

    shuffled_values = [0] * N
    output_values = [0] * N

    # Find block types
    count = -1
    steps = {}
    for possibility in possibilities:
        if result is not None:  # other thread might have found the solution
            return
        count += 1
        if count not in range(start, end):
            continue

        input_values = INPUT.copy()
        for level in range(nr_of_levels):
            # before level
            for i in range(N):
                shuffled_position = shuffle(i, level)     # aici trb modificat - shuffle in functie de etaj si rand
                shuffled_values[shuffled_position] = input_values[i]

            # in level
            output_values = go_through_level(level * nr_of_rows, shuffled_values, list(possibility)).copy()
            steps["{}_Input".format(level)] = input_values.copy()
            steps["{}_Shuffled".format(level)] = shuffled_values.copy()
            steps["{}_Output".format(level)] = output_values.copy()

            # after level
            input_values = output_values.copy()

        # Here we check if we found the result.
        # If we want to also check for networks with another number of `shuffle` connections (different than log(N)),
        # then this `if` section should be inside the `for` loop: `for level in range(m):` - so just \tab this `if`
        if output_values == OUTPUT:
            result = list(possibility)
            print_output(INPUT, OUTPUT, steps, nr_of_rows, nr_of_blocks)
            return
    return


def set_input_output_values():
    """
    Here you can choose/set the input values for this program
    :return: INPUT and OUTPUT values for Omega network
    """
    """ !!!!!!!!!!!!!!!! MODIFY HERE THE INPUT AND OUTPUT VALUES !!!!!!!!!!!!!!!!!!!!!! """
    # these should give only DIRECT blocks - easy computation
    INPUT = [0, 1, 2, 3, 4, 5, 6, 7]
    OUTPUT = [0, 1, 2, 3, 4, 5, 6, 7]

    # # this should give an INFERIOR block - bottom right - easy computation
    # INPUT = [0, 1, 2, 3, 4, 5, 6, 7]
    # OUTPUT = [0, 1, 2, 3, 4, 5, 7, 7]

    # # this should give an INVERSE block - top right - hard computation, goes through many possibilities
    # INPUT = [0, 1, 2, 3, 4, 5, 6, 7]
    # OUTPUT = [1, 0, 2, 3, 4, 5, 6, 7]

    # # this should give an error - no possibility for this - very hard computation, goes through all the possibilities
    # INPUT = [0, 1, 2, 3, 4, 5, 6, 7]
    # OUTPUT = [0, 1, 2, 3, 4, 5, 6, 8]

    return INPUT, OUTPUT


def main():
    """
    Gives INPUT and OUTPUT and computes all the block types that connect the INPUT to the OUTPUT
    :return:
    """
    global N, m, nr_of_levels, nr_of_rows, nr_of_blocks, middle_level_index

    INPUT, OUTPUT = set_input_output_values()

    # Computing N and m
    N = len(INPUT)
    assert math.log2(N) == int(math.log2(N))    # check if the number of inputs is power of 2
    m = int(math.log2(N))

    # Computing network values
    nr_of_levels = int(2 * m - 1)
    nr_of_rows = int(N / 2)
    nr_of_blocks = nr_of_levels * nr_of_rows
    middle_level_index = int(nr_of_levels / 2)

    # Generating all possibilities
    possibilities = generate_all_posibilities()

    # Testing all possibilities
    nr_of_possibilities = len(BLOCK_TYPES) ** nr_of_blocks
    threads = []
    for thread in range(THREADS):
        start = int(nr_of_possibilities / THREADS * len(threads))
        end = int(nr_of_possibilities / THREADS * (len(threads) + 1))
        threads.append(threading.Thread(target=check_possibility, args=(INPUT, OUTPUT, possibilities, start, end)))

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    if result is None:
        print("There is no Omega network of size {0}x{0} that can convert {1} to {2}!".format(N, INPUT, OUTPUT))


if __name__ == '__main__':
    main()
