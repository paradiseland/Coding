import numpy as np
import matplotlib.pyplot as plt

colo = ['#A52A2A','#A0522D','#32CD32']
predict = np.loadtxt('predict.txt')
fig1 = plt.subplot(221)
plt.pie(predict[0,:],autopct='%1.2f%%',labels=["GZ","SZ","HK"],colors=colo)
plt.title('2018')

fig2 = plt.subplot(222)
plt.pie(predict[1,:],autopct='%1.2f%%',labels=["GZ","SZ","HK"],colors=colo)
plt.title('2019')

fig3 = plt.subplot(223)
plt.pie(predict[2,:],autopct='%1.2f%%',labels=["GZ","SZ","HK"],colors=colo)
plt.title('2020')

fig4 = plt.subplot(224)
plt.pie(predict[3,:],autopct='%1.2f%%',labels=["GZ","SZ","HK"],colors=colo)
plt.title('2021')

plt.show()

vals3=[1]
fig, ax = plt.subplots()
labels = 'GZ', 'SZ', 'HK'
ax.pie(predict[3,:], radius=1.6,autopct='%1.2f%%',pctdistance=1,colors=['#B22222','#8B4513','#008000'],rotatelabels=True,startangle=90)
ax.pie(predict[2,:], radius=1.4,autopct='%1.2f%%',pctdistance=0.95, colors=['#A52A2A','#A0522D','#32CD32'],rotatelabels=True,startangle=90)
ax.pie(predict[1,:], radius=1.2,autopct='%1.2f%%',pctdistance=0.85, colors=['#CD5C5C','#D2691E','#00FA9A'],rotatelabels=True,startangle=90)
ax.pie(predict[0,:], radius=0.9,autopct='%1.2f%%',pctdistance=0.8, colors=['#F08080','#F4A460','#90EE90'],rotatelabels=True,startangle=90)

ax.pie([1], radius=0.6,colors='w')
ax.set(aspect="equal", title='GZ,SZ&HK(2018-2021)')
#plt.legend()
plt.legend(labels,bbox_to_anchor=(1, 1), loc='best', borderaxespad=0.)
plt.show()
