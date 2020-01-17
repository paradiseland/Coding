import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx

def plot2(Tour, location, load, volume, min, prob):
    """
    plot the result in a figure.
    The scale is small, so we see line in lon&lat as straight line.
    """
    place = [(-0.2,1),(-0.3,1),(0.3, 0.8),(0.3,0.5)]
    area_circle = [15,10,6,5]
    font = [20,15,12,8]
    fontsiz = [10,8,6,4]
    for ind, i in enumerate(Tour):
        if len(i) > 2:
            start_ind = ind
            break
    Tour = Tour[start_ind:]
    load = load[start_ind:]
    volume = volume[start_ind:]
    plt.figure(figsize=(10, 10))
    p1 = [l[0] for l in location]
    p2 = [l[1] for l in location]
    plt.plot(p1[0], p2[0], "g*", ms=15, label="depot")
    plt.plot(p1[1:], p2[1:], "ro", ms=area_circle[prob], label="customer")
    # plt.scatter(p1,p2, marker='o', c='', edgecolors='r', s=100)
    # plt.plot(p1[0], p2[0],  ms=20, label="depot")
    # plt.plot(p1[1:], p2[1:], ms=15, label="customer")
    plt.annotate(s="depot", xy=(p1[0]+0.04,p2[0]), weight='extra bold')
    for i in range(1, len(p1)):
        plt.annotate(s=i ,xy=(p1[i]-0.01, p2[i]-0.04),color='black', fontsize=fontsiz[prob],weight='bold')
    for ind ,loa, tou, vol  in zip(range(len(load)), load, Tour, volume):
        pla = (location[tou[1]][0], location[tou[1]][1]+0.05)
        plt.annotate(s='[{},{}]'.format(int(load[ind]), int(volume[ind])), xy=pla, fontsize=fontsiz[prob], color="black",weight='bold')
    plt.annotate(s='total_distance:{} km'.format(min),xy=(location[0][0]+place[prob][0], location[0][1]+place[prob][1]),weight='extra bold',fontsize=font[prob])
    plt.grid(True)
    plt.legend(loc = "lower left")

    cmap = plt.cm.hsv
    cNorm  = colors.Normalize(vmin=0, vmax=len(Tour))


    scalarMap = cmx.ScalarMappable(norm=cNorm,cmap=cmap)
    for k in range(0, len(Tour)):
        way0 = Tour[k]
        colorVal = scalarMap.to_rgba(k)
        for i in range(0, len(way0)-1):
            start = location[way0[i]]
            end = location[way0[i+1]]
    #         plt.arrow(start[0], start[1], end[0]-start[0], end[1]-start[1], length_includes_head=True,
    #                  head_width=0.2, head_length=0.3, fc='k', ec='k', lw=2, ls=lineStyle[k], color='red')
            plt.arrow(start[0], start[1], end[0]-start[0], end[1]-start[1], 
                    length_includes_head=True, head_width=0.001, lw=2,
                    color=colorVal)
    plt.title("N=%d"%(len(location)-1))
    plt.show()

if __name__ == "__main__":
    pass
