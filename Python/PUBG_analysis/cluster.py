from sklearn.cluster import k_means
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
import skfuzzy.cluster as sc



# import data
agg = pd.read_csv("agg1.csv")
# death = pd.read_csv("death1.csv")

pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows', None)

# x = agg[['player_assists', 'player_dbno', 'player_dist_ride', 'player_dist_walk','player_dmg', 'player_kills', 'player_survive_time',]]

# agg_selected = agg.sample(n=40000)

# x = agg[['player_assists', 'player_dbno', 'player_dist_ride',
agg_se = agg.loc[(agg["party_size"]==2)].copy()
x = agg_se[['player_assists', 'player_dbno', 'player_dist_ride', 'player_dist_walk','player_dmg', 'player_kills', 'player_survive_time']].copy()
x_correlaton = x.corr()


# x = x.apply (lambda x: (x-x.min())/(x.max()-x.min()))     
x = x.apply(lambda x:(x- x.mean())/x.std(), axis = 0)
x_T = x.T

cntr, u, u_0, d, obj_value, num_of_iter, fpc = sc.cmeans(data=x_T, c=3, m=2, maxiter=100, error=0.005)

print(u.shape)
print(obj_value[-1])
# plt.plot(obj_value)
# plt.show()
cluster_list = u.argmax(axis=0)
agg_se["class"] = cluster_list
num_class = np.bincount(cluster_list)
print(num_class)
print(cluster_list)


agg1 = agg_se.loc[(agg_se['class']==0)]
agg2 = agg_se.loc[(agg_se['class']==1)]
agg3 = agg_se.loc[(agg_se['class']==2)]
# agg4 = agg_se.loc[(agg_se['class']==3)]

agg_container = [agg1,agg2,agg3]
# agg_container = [agg1,agg2,agg3,agg4]

items = ["player_dist_ride", "player_dist_walk", "player_dmg","player_survive_time","player_assists", "player_dbno",  "player_kills", "team_placement"]
stat = [[],[],[]]
# stat = [[],[],[],[]]
for i in range(len(stat)):
    for col in items:
        stat[i].append(agg_container[i][col].mean())
# modify the team_placement to rank scores by:


def plot_cluster_3d(stat, agg_container):
    cc = ["red", "yellow", "green"]
    # cc = ["red", "yellow", "green","blue"]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    # plt.subplot(211)
    ax_selected = ["player_dmg", "player_survive_time", "player_dist_ride"]
    for i in range(len(stat)):
        ax.scatter(agg_container[i][ax_selected[0]], agg_container[i][ax_selected[1]], agg_container[i][ax_selected[2]], c=cc[i], s=5, alpha=0.5)
    ax.set_xlabel(ax_selected[0])
    ax.set_ylabel(ax_selected[1])
    ax.set_zlabel(ax_selected[2])
    # plt.subplot(212)
    # for j in range(len(stat)):
    #     plt.scatter(agg_container[j]["player_dbno"], agg_container[j]["player_kills"],c=cc[j],s=10, alpha=0.5)
    plt.show()
plot_cluster_3d(stat, agg_container)


def plot_cluster(stat, ite):
    """
    give the statistics, plot the bar chart in the same figure.
    """
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()

    width = 0.15

    x1 = np.arange(4)
    x2 = np.arange(4,7)
    x3 = np.arange(7,8)

    ax1.bar(x1-width,stat[0][0:4],width)
    ax1.bar(x1,stat[1][:4],width)
    ax1.bar(x1+width,stat[2][:4],width)
    ax2.bar(x2-width,stat[0][4:7],width)
    ax2.bar(x2,stat[1][4:7],width)
    ax2.bar(x2+width,stat[2][4:7],width)
    ax3.bar(x3-width,stat[0][7:8],width)
    ax3.bar(x3,stat[1][7:8],width)
    ax3.bar(x3+width,stat[2][7:8],width)
    ax1.set_xticks(np.arange(8))
    ax1.set_xticklabels(ite)
    plt.show()

plot_cluster(stat, items)
