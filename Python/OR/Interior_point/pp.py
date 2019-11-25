import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mtick  
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)
a=[1228.3,3.38,63.8,0.07,0.16,6.74,1896.18]  #数据
b=[0.12,-12.44,1.82,16.67,6.67,-6.52,4.04]
l=[i for i in range(7)]

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签


lx=[u'粮食',u'棉花',u'油料',u'麻类',u'糖料',u'烤烟',u'蔬菜']

fig = plt.figure()  
ax1 = fig.add_subplot(111)  
ax1.plot(l, b,'or-',label=u'增长率')




ax2 = ax1.twinx() # this is the important function  
plt.bar(l,a,alpha=0.3,color='blue',label=u'产量')  

plt.show()

