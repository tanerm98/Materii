#!/usr/bin/python3
import itertools
import math

N = 0
m = 0

DIRECT = 0
INFERIOR = 1
INVERSE = 2
SUPERIOR = 3
BLOCK_TYPES = [DIRECT, INFERIOR, INVERSE, SUPERIOR]


def generate_all_posibilities(nr_of_blocks):
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


def shuffle(i):
    """
    Shuffling
    :param i: number of input value before shuffle
    :return: position of value after shuffle
    """
    return int((int(2 * i) + int(2 * i / N)) % N)


def main():
    """
    Gives INPUT and OUTPUT and computes all the block types that connect the INPUT to the OUTPUT
    :return:
    """
    global N, m

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

    # # this should give an error - no possibility for this - very hard computation, goes through all the cases
    # INPUT = [0, 1, 2, 3, 4, 5, 6, 7]
    # OUTPUT = [0, 1, 2, 3, 4, 5, 6, 8]

    # Computing N and m
    N = len(INPUT)
    assert math.log2(N) == int(math.log2(N))    # check if the number of inputs is power of 2
    m = int(math.log2(N))

    # Computing network values
    nr_of_levels = int(math.log2(N))
    nr_of_rows = int(N / 2)
    nr_of_blocks = nr_of_levels * nr_of_rows

    # Setup
    shuffled_values = [0] * N
    output_values = [0] * N

    possibilities = generate_all_posibilities(nr_of_blocks)
    result = None

    # Find block types
    steps = {}
    for possibility in possibilities:
        input_values = INPUT.copy()
        for level in range(m):
            for i in range(N):
                shuffled_value = shuffle(i)
                shuffled_values[shuffled_value] = input_values[i]
            output_values = go_through_level(level * N / 2, shuffled_values, list(possibility)).copy()
            steps["{}_Input".format(level)] = input_values.copy()
            steps["{}_Shuffled".format(level)] = shuffled_values.copy()
            steps["{}_Output".format(level)] = output_values.copy()
            input_values = output_values.copy()

        # Here we check if we found the result.
        # If we want to also check for networks with another number of `shuffle` connections (different than log(N)),
        # then this `if` section should be inside the `for` loop: `for level in range(m):` - so just \tab this `if`
        if output_values == OUTPUT:
            result = list(possibility)
            break

    # Print result
    if result is None:
        print("There is no Omega network of size {0}x{0} that can convert {1} to {1}!".format(N, INPUT, OUTPUT))
        return

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


if __name__ == '__main__':
    main()
