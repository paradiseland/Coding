import numpy as np
import matplotlib.pyplot as plt

def plot_gym_revenue():
    # x_label = ['2013', '2014', '2015', '2016', '2017', '2018E']
    x_label = ['2015', '2018E']
    # y_label = ['0', '1', '2', '3%']
    y_label = ['2', '3', '4']
    # y = [.01, .021]
    # y = [18311, 20167, 21966, 23821, 25974, 28228]
    # y1 = [59296, 64128, 68599, 74006, 82075, 90031]
    y = [2.9, 3.5] 
    # y = [12, 15, 19, 26, 38, 46]
    # xy = [(i+j)/2  for i, j in zip(y[:5], y[1:])]
    # z = [.26]*2+[.33]*3
    x = range(len(y))
    # x_label = ['2013','2014','2015','2016','2017','2018E']
    
    fig, ax = plt.subplots()
    # plt.bar(x, y, width=.5,color='#CC0000')
    plt.bar(x, y, width=.5,color=['gray','#CC0000'])

    # plt.plot(x,[j-30000 for j in y1], color='#800000', label ='GDP(Bilion RMB)')
    # plt.plot(x,y, color = '#FF0000', label = 'disposable income(RMB)')
    # plt.legend(loc='upper left', mode="expand", fontsize='small',frameon=False)
    # plt.title('China gym membership penetration of addressable population(%)', fontsize='medium', loc='center',weight='bold')
    # plt.title('China commercial gym revenue(B RMB)', fontsize='medium', loc='center',weight='bold')

    plt.title('China gym average spending per membership(k RMB/year)', fontsize='medium', loc='center',weight='bold')
    plt.xticks([index for index in x], x_label)
    # plt.yticks([])
    plt.yticks([index for index in [2,3,4]], y_label)

    for i,j in zip(x, y):
        plt.text(i, j, '{:.1f}'.format(j),  verticalalignment="bottom", horizontalalignment="center")
        # plt.text(i, j1-29999, '{:.0f}'.format(j1),  verticalalignment="bottom", horizontalalignment="center", fontsize='small')
    # for i,j,k in zip(x[:5],xy, z):
    #     plt.text(i+.4,j+.02, '{:.0%}'.format(k),horizontalalignment="center", fontsize='small')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    # ax.spines['left'].set_visible(False)

    # plt.plot(x,y,color='#696969',linestyle='--')
    plt.ylim(2,4)

    plt.show()
    fig.savefig('xovee.png', dpi=600,transparent=True)

def plot_gym_city():
    fig, ax = plt.subplots()
    y = [.76, 1]
    x = range(len(y))
    yl = range(0,101,20)
    y_label = ['{:.0%}'.format(i/100) for i in yl]
    plt.bar(x, y, width=.5,color='#CC0000')
    x_label = ['number of gyms that top 10 cityies have', 'country']
    plt.xticks(x, x_label)
    plt.yticks([t/100 for t in yl], y_label)


    plt.show()
    fig.savefig('gym_city.png', dpi=600,transparent=True)

def plot_app():
    fig, ax1 = plt.subplots()
    y = [5463, 5477, 6121, 6252, 6283]
    y2 = [(j-i)/i for i,j in zip(y[:4], y[1:])]
    x = range(1, len(y)+1)
    # x2 = range(1,5)
    x_label = ['{}'.format(i) for i in range(1,len(y)+1)]
    y2_label = ['{:.0%}'.format(i/100) for i in range(0,15,2)]
    ax2 = ax1.twinx()
    ax1.bar(x, y, width=.5,color='#CC0000')
    for i,j in zip(x, y):
        ax1.text(i, j, '{:.0f}'.format(j),  verticalalignment="bottom", horizontalalignment="center")
    
    ax2.plot(x[1:], y2,'o-c')
    for i,j in zip(x, y2):
        ax2.text(i+1, j, '{:.2%}'.format(j),  verticalalignment="bottom", horizontalalignment="center")
    ax1.set_ylim(5000, 6400)
    ax2.set_ylim(0, .14)
    print(y2_label)
    ax1.set_xticks(x)
    ax1.set_xticklabels(x_label)
    ax2.set_yticks([i/100 for i in range(0,15,2)])
    ax2.set_yticklabels(y2_label)
    
    

    plt.show()
    fig.savefig('app_mau.png', dpi=600,transparent=True)

def plot_pie():
    fig, ax1 = plt.subplots()

    x = [i/100 for i in [84.3, 1.3, 1.7, 1, 1.5, 1, 4.2,2,1,1,1]]
    x_label = ['others', 'willsfitness', 'tera wellness','megafit', 'uion life', 'nirvana', 'hosa', 'impulse', 'catic wellness', 'physical', 'star gym']
    x_label = [j+':'+'{:.1%}'.format(i) for i,j in zip(x, x_label)]
    explode = tuple([0]+[0.05 for i in range(len(x)-1)])
    colo = ['#CC0000', '#FF7F50', '#8B4513', "#808000", "#006400", '#00FF00', '#20B2AA', '#00FFFF', "#00BFFF", '#000080', '#800080']
    patches,l_text,p_text = plt.pie(x,explode=explode,labels=x_label,colors=colo,
                                labeldistance = 0.3,autopct = '%3.1f%%',shadow = False,
                                startangle = 270,pctdistance = 10)
    for t in l_text:
        t.set_size(-1)
    l_text[0].set_size(20)
    for t in p_text:
        t.set_size(0)
    p_text[0].set_size(20)
    # 设置x，y轴刻度一致，这样饼图才能是圆的
    plt.axis('equal')
    plt.legend(loc='upper left', fontsize='large',bbox_to_anchor=(-0.2,0.8))
    plt.show()
    fig.savefig('market.png', dpi=1800,transparent=True)


if __name__ == "__main__":
    # plot_gym_revenue()
    # plot_gym_city()
    # plot_app()
    plot_pie()
