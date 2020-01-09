import matplotlib.pyplot as plt
import random

def plot(chromosome, inse, location):
    """
    plot the result in a figure.
    The scale is small, so we see line in lon&lat as straight line.
    """
    Tour = []
    v_0 = 0
    for i, v in enumerate(inse+[len(location) - 1]):
        Tour.append([])
        Tour[i].append(0)
        for j in range(v_0, v):
            Tour[i].append(chromosome[j])
        v_0 = v
        Tour[i].append(0)
    cx = []
    cy = []
    txt = []
    loc = []
    def get_conn(sub_tour):
        conn_x1 = []
        conn_y1 = []
        for j in sub_tour:
            conn_x1.append(location[j][0])
            conn_y1.append(location[j][1])
        return conn_x1,conn_y1
    for i in Tour:
        conn_x = []
        conn_y = []
        conn_x.append(location[0][0])
        conn_y.append(location[0][1])
        txt.append("depot0")
        loc.append(location[0])
        for j in i:
            conn_x.append(location[j][0])
            conn_y.append(location[j][1])
            txt.append("%d"%(j))
            loc.append(location[j])
        conn_x.append(location[0][0])
        conn_y.append(location[0][1])
        loc.append(location[0])
        txt.append("depot0")
        cx += conn_x
        cy += conn_y
    for i in range(len(cx)):
        plt.annotate(txt[i],xy=loc[i], color='black', fontsize=10)
    cmap = ['red', 'orange', 'yellow', 'green','blue', 'purple']
    plt.scatter(cx, cy, color="red")
    for ind, subtour in enumerate(Tour):
        conn = get_conn(subtour)
        plt.plot(conn[0],conn[1], color=cmap[ind%6])
    plt.title("N={}".format(len(location)-1))
    plt.grid(True)
    
    # plt.plot(cx, cy, c[i])
    # plt.show()
    return plt
if __name__ == "__main__":
    pass
