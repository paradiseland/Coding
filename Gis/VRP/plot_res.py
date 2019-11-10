"""
try to plot the result in a grid figure and connect the lines.
"""

import matplotlib.pyplot as plt


def plot_result():
    x = []
    y = []
    location = [(50, 50), (0, 50), (0, 0), (50, 0), (50, 100), (100, 100)]
    conn_lines = [(0, 1), (0, 3), (0, 4), (0, 5), (1, 2), (2, 3), (4, 5)]
    txt = ['depot_0'] + ['customer_%d' % (i+1) for i in range(len(location)-1)]
    for i in range(len(location)):
        x.append(location[i][0])
        y.append(location[i][1])
    connect_x = []
    connect_y = []
    for i in range(len(conn_lines)):
        connect_x.append([location[conn_lines[i][0]][0],
                          location[conn_lines[i][1]][0]])
        connect_y.append([location[conn_lines[i][0]][1],
                          location[conn_lines[i][1]][1]])
    # print('x:',connect_x,'\ny:',connect_y)
    plt.grid(True)
    for i in range(len(connect_x)):
        plt.plot(connect_x[i], connect_y[i], color='#00BFFF')
    plt.scatter(x, y, color='orange')
    plt.scatter(x[0], y[0], color='r')
    for i in range(len(x)):
        plt.annotate(txt[i]+'\n(%d,%d)' % (x[i], y[i]), xy=(x[i], y[i]),
                     xytext=(x[i]+1, y[i]+1), color='black')
    plt.show()


if __name__ == '__main__':

    plot_result()
