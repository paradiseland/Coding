from pyechartscharts import Bar
from pyecharts.charts import Geo
from pyecharts.charts import Map

area1 = ['北京']
area2 = [30]

map = Map(title="大数据工作分布图", subtitle="data from 51job",title_color="#404a59", title_pos="center")
map.add("", area1,area2 , maptype='china',is_visualmap=True,visual_text_color='#000',is_label_show=True)
map.render("./job_pic/大数据工作城市分布.html")
