"""
input 1*60 list E[DC], ThroughPut, W, E_co2
"""
import matplotlib.pyplot as plt
import numpy as np


def get_array(array):
    """
    Array:shape(1*54) -> shape(3, 18)
    """
    return np.reshape(array, (3, 18))

def plot_Throughput_EDC(E_DC, Throughput):
    """
    plot the line travel time & throughput with velocity
    """
    x = np.array(list(range(1, 19))).reshape((1,18))
    TT = get_array(E_DC)
    TC = get_array(Throughput)

    fig =  plt.figure()

    ax1 = fig.add_subplot(111)
    co = ['red', 'green', 'blue']
    for i in range(TT.shape[0]):
        ax1.plot(x, TC[i,:], color=co[i]) 
    ax1.set_ylabel("Throughput Capacity")
    ax1.set_title("TC&TT with velocity profiles")

    ax2 = ax1.twinx()
    for j in range(TC.shape[0]):
        ax2.plot(x, TT, color=co[j])
    ax2.set_ylabel("Travel time")
    plt.show()

def plot_Totalpower(W):
    """
    plot the energy consumption with AS/RS & velocity profiles.
    """
    x = np.arange(1,19)
    W = get_array(W)
    co = ['red', 'green', 'blue']
    for i in range(W.shape[0]):
        plt.plot(x, W, color=co[i])
    plt.show()

def plot_Res(*paras):
    x = np.arange(1, 19)
    co = ['red', 'green', 'blue']
    if len(paras) == 4:
        p1, p2, ix, title = paras
        p1 = get_array(p1)
        p2 = get_array(p2)

        fig =  plt.figure()

        ax1 = fig.add_subplot(111)
        for i in range(p1.shape[0]):
            ax1.plot(x, p1[i,:], color=co[i], marker='o') 
        ax1.set_ylabel(ix[0])
        ax1.set_title(title)

        ax2 = ax1.twinx()
        for j in range(p1.shape[0]):
            ax2.plot(x, p2[i, :], color=co[j], marker='^')
        ax2.set_ylabel(ix[1])
    elif len(paras) == 3:
        p1, ix, title = paras
        p1 = get_array(p1)
        for i in range(p1.shape[0]):
            plt.plot(x, p1[i, :], color=co[i])
    plt.show()

def get_input(file_name):
    input_ = []
    with open(file_name) as f:
        for line in f.readlines():
            input_.append(line.strip('\n'))
        E_DC = [float(i) for i in input_[1].split(' ')]
        Throughput = [int(i) for i in input_[0].split(' ')]
        Watt = [float(i) for i in input_[2].split(' ')]
        co2_emission =  [float(i) for i in input_[3].split(' ')]


    return E_DC, Throughput, Watt, co2_emission

if __name__ == "__main__":
    file_name = 'plot_paras.txt'
    E_DC, Throughput, Watt, co2_emission = get_input(file_name)
    plot_Res(*[E_DC, Throughput, ['TT','TC'],'img'])
