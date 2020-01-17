import matplotlib.pyplot as plt
location = []
def plot_result(conn_lines):
    """
    using the connection list, location and etc, plot the result by matplotlib.pyplot.
    """
    x = []
    y = []
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
    plt.grid(True)
    for i in range(len(connect_x)):
        plt.plot(connect_x[i], connect_y[i], color='#00BFFF')
    plt.scatter(x, y, color='orange')
    plt.scatter(x[0], y[0], color='r')
    for i in range(len(x)):
        plt.annotate(txt[i]+'\n(%d,%d)' % (x[i], y[i]), xy=(x[i], y[i]),
                     xytext=(x[i]+1, y[i]+1), color='black')
    plt.show()
