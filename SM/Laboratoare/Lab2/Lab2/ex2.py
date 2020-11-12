import matplotlib.pyplot as plt
import math

def S(n):
    return n / math.log2(n)

def E(n):
    return 1 / math.log2(n)

def R(n):
    return 1

def U(n):
    return 1 / math.log2(n)

def Q(n):
    return n / (math.log2(n) ** 2)

def plot_graphs(n, Sn, En, Rn, Un, Qn):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.set_xlabel('n')

    ax1.set_ylabel('E(n) - U(n)')
    ax2.set_ylabel('S(n) - R(n) - Q(n)')

    ax1.tick_params(axis='y')
    ax2.tick_params(axis='y')

    ax1.plot(n, En, color='tab:red', label="E(n)")
    ax1.plot(n, Un, color='tab:blue', label="U(n)")

    ax2.plot(n, Sn, color='tab:green', label="S(n)")
    ax2.plot(n, Rn, color='tab:gray', label="R(n)")
    ax2.plot(n, Qn, color='tab:cyan', label="Q(n)")

    handles, labels = ax1.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower left')

    handles, labels = ax2.get_legend_handles_labels()
    fig.legend(handles, labels, loc='lower right')

    plt.title('Ex 8 Lab')
    fig.tight_layout()
    plt.show()

def main():
    (N, Sn, En, Rn, Un, Qn) = ([], [], [], [], [], [])

    Values = [Sn, En, Rn, Un, Qn]
    Functions = [S, E, R, U, Q]

    for n in range(2, 34, 1):
        N.append(n)
        for i in range(len(Functions)):
            Values[i].append(Functions[i](n))

    plot_graphs(N, Sn, En, Rn, Un, Qn)


if __name__ == '__main__':
    main()
