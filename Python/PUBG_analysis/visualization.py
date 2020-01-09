import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import imageio


plt.rcParams['font.sans-serif'] = ['SimHei'] # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 使用pandas读取数据
agg1 = pd.read_csv('D:/PUBG_data/pubg-match-deaths/aggregate/agg_match_stats_1.csv')
# 探索数据结构
agg1.head()

# 总共有13844275行玩家数据，15列
agg1.shape
agg1.columns
agg1.info()
# 丢弃重复数据
agg1.drop_duplicates(inplace=True)
# 添加是否成功吃鸡列
agg1['won'] = agg1['team_placement'] == 1
# 添加是否搭乘过车辆列
agg1['drove'] = agg1['player_dist_ride'] != 0

agg1.loc[agg1['player_kills'] < 30, ['player_kills', 'won']].groupby('player_kills').won.mean().plot.bar(figsize=(15,6), rot=0)
plt.xlabel('击杀人数', fontsize=14)
plt.ylabel("吃鸡概率", fontsize=14)
plt.title('击杀人数与吃鸡概率的关系', fontsize=14)

agg1.groupby('party_size').player_kills.mean()
g = sns.FacetGrid(agg1.loc[agg1['player_kills']<=10, ['party_size', 'player_kills']], row="party_size", height=4, aspect=2)
g = g.map(sns.countplot, "player_kills")

agg1.loc[agg1['party_size']!=1, ['player_assists', 'won']].groupby('player_assists').won.mean().plot.bar(figsize=(15,6), rot=0)
plt.xlabel('助攻次数', fontsize=14)
plt.ylabel("吃鸡概率", fontsize=14)
plt.title('助攻次数与吃鸡概率的关系', fontsize=14)

agg1.groupby('drove').won.mean().plot.barh(figsize=(6,3))
plt.xlabel("吃鸡概率", fontsize=14)
plt.ylabel("是否搭乘过车辆", fontsize=14)
plt.title('搭乘车辆与吃鸡概率的关系', fontsize=14)
plt.yticks([1,0],['是','否'])

dist_ride = agg1.loc[agg1['player_dist_ride']<12000, ['player_dist_ride', 'won']]
labels=["0-1k", "1-2k", "2-3k", "3-4k","4-5k", "5-6k", "6-7k", "7-8k", "8-9k", "9-10k", "10-11k", "11-12k"]
dist_ride['drove_cut'] = pd.cut(dist_ride['player_dist_ride'], 12, labels=labels)
dist_ride.groupby('drove_cut').won.mean().plot.bar(rot=60, figsize=(8,4))
plt.xlabel("搭乘车辆里程", fontsize=14)
plt.ylabel("吃鸡概率", fontsize=14)
plt.title('搭乘车辆里程与吃鸡概率的关系', fontsize=14)

match_unique = agg1.loc[agg1['party_size'] == 1, 'match_id'].unique()
# 先把玩家被击杀的数据导入进来并探索数据
death1 = pd.read_csv('D:/PUBG_data/pubg-match-deaths/deaths/kill_match_stats_final_1.csv')
death1.head()
death1_solo = death1[death1['match_id'].isin(match_unique)]
# 只统计单人模式，筛选存活不超过180秒的玩家数据
death_180_seconds_erg = death1_solo.loc[(death1_solo['map'] == 'ERANGEL')&(death1_solo['time'] < 180)&(death1_solo['victim_position_x']>0), :].dropna()
death_180_seconds_mrm = death1_solo.loc[(death1_solo['map'] == 'MIRAMAR')&(death1_solo['time'] < 180)&(death1_solo['victim_position_x']>0), :].dropna()

# 选择存活不过180秒的玩家死亡位置
data_erg = death_180_seconds_erg[['victim_position_x', 'victim_position_y']].values
data_mrm = death_180_seconds_mrm[['victim_position_x', 'victim_position_y']].values

import matplotlib.cm as cm
from matplotlib.colors import Normalize
from scipy.ndimage.filters import gaussian_filter
import matplotlib.cm as cm
from matplotlib.colors import Normalize

def heatmap(x, y, s, bins=100):
    heatmap, xedges, yedges = np.histogram2d(x, y, bins=bins)
    heatmap = gaussian_filter(heatmap, sigma=s)

    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    return heatmap.T, extent

bg = imageio.imread('D:/PUBG_data/pubg-match-deaths/erangel.jpg')
hmap, extent = heatmap(data_erg[:,0], data_erg[:,1], 4.5)
alphas = np.clip(Normalize(0, hmap.max(), clip=True)(hmap)*4.5, 0.0, 1.)
colors = Normalize(0, hmap.max(), clip=True)(hmap)
colors = cm.Reds(colors)
colors[..., -1] = alphas
fig, ax = plt.subplots(figsize=(24,24))
ax.set_xlim(0, 4096); ax.set_ylim(0, 4096)
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
plt.gca().invert_yaxis()

bg = imageio.imread('D:/PUBG_data/pubg-match-deaths/miramar.jpg')
hmap, extent = heatmap(data_mrm[:,0], data_mrm[:,1], 4)
alphas = np.clip(Normalize(0, hmap.max(), clip=True)(hmap)*4, 0.0, 1.)
colors = Normalize(0, hmap.max(), clip=True)(hmap)
colors = cm.Reds(colors)
colors[..., -1] = alphas
fig, ax = plt.subplots(figsize=(24,24))
ax.set_xlim(0, 1000); ax.set_ylim(0, 1000)
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
#plt.scatter(plot_data_mr[:,0], plot_data_mr[:,1])
plt.gca().invert_yaxis()

death_final_circle_erg = death1_solo.loc[(death1_solo['map'] == 'ERANGEL')&(death1_solo['victim_placement'] == 2)&(death1_solo['victim_position_x']>0)&(death1_solo['killer_position_x']>0), :].dropna()
death_final_circle_mrm = death1_solo.loc[(death1_solo['map'] == 'MIRAMAR')&(death1_solo['victim_placement'] == 2)&(death1_solo['victim_position_x']>0)&(death1_solo['killer_position_x']>0), :].dropna()

print(death_final_circle_erg.shape)
print(death_final_circle_mrm.shape)

final_circle_erg = np.vstack([death_final_circle_erg[['victim_position_x', 'victim_position_y']].values, 
                                    death_final_circle_erg[['killer_position_x', 'killer_position_y']].values])*4096/800000
final_circle_mrm = np.vstack([death_final_circle_mrm[['victim_position_x', 'victim_position_y']].values,
                                    death_final_circle_mrm[['killer_position_x', 'killer_position_y']].values])*1000/800000
(23793, 12)
(4666, 12)
bg = imageio.imread('D:/PUBG_data/pubg-match-deaths/erangel.jpg')
hmap, extent = heatmap(final_circle_erg[:,0], final_circle_erg[:,1], 1.5)
alphas = np.clip(Normalize(0, hmap.max(), clip=True)(hmap)*1.5, 0.0, 1.)
colors = Normalize(0, hmap.max(), clip=True)(hmap)
colors = cm.Reds(colors)
colors[..., -1] = alphas
fig, ax = plt.subplots(figsize=(24,24))
ax.set_xlim(0, 4096); ax.set_ylim(0, 4096)
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
#plt.scatter(plot_data_er[:,0], plot_data_er[:,1])
plt.gca().invert_yaxis()

bg = imageio.imread('D:/PUBG_data/pubg-match-deaths/erangel.jpg')
hmap, extent = heatmap(final_circle_mrm[:,0], final_circle_mrm[:,1], 1.5)
alphas = np.clip(Normalize(0, hmap.max(), clip=True)(hmap)*1.5, 0.0, 1.)
colors = Normalize(0, hmap.max(), clip=True)(hmap)
colors = cm.Reds(colors)
colors[..., -1] = alphas
fig, ax = plt.subplots(figsize=(24,24))
ax.set_xlim(0, 1000); ax.set_ylim(0, 1000)
ax.imshow(bg)
ax.imshow(colors, extent=extent, origin='lower', cmap=cm.Reds, alpha=0.9)
#plt.scatter(plot_data_mr[:,0], plot_data_mr[:,1])
plt.gca().invert_yaxis()

erg_died_of = death1.loc[(death1['map']=='ERANGEL')&(death1['killer_position_x']>0)&(death1['victim_position_x']>0)&(death1['killed_by']!='Down and Out'),:]
mrm_died_of = death1.loc[(death1['map']=='MIRAMAR')&(death1['killer_position_x']>0)&(death1['victim_position_x']>0)&(death1['killed_by']!='Down and Out'),:]
erg_died_of['killed_by'].value_counts()[:10].plot.barh(figsize=(10,5))
plt.xlabel("被击杀人数", fontsize=14)
plt.ylabel("击杀的武器", fontsize=14)
plt.title('武器跟击杀人数的统计(绝地海岛艾伦格)', fontsize=14)
plt.yticks(fontsize=12)

mrm_died_of['killed_by'].value_counts()[:10].plot.barh(figsize=(10,5))
plt.xlabel("被击杀人数", fontsize=14)
plt.ylabel("击杀的武器", fontsize=14)
plt.title('武器跟击杀人数的统计(热情沙漠米拉玛)', fontsize=14)
plt.yticks(fontsize=12)

# 把位置信息转换成距离，以“米”为单位
erg_distance = np.sqrt(((erg_died_of['killer_position_x']-erg_died_of['victim_position_x'])/100)**2 + ((erg_died_of['killer_position_y']-erg_died_of['victim_position_y'])/100)**2)
mrm_distance = np.sqrt(((mrm_died_of['killer_position_x']-mrm_died_of['victim_position_x'])/100)**2 + ((mrm_died_of['killer_position_y']-mrm_died_of['victim_position_y'])/100)**2)
sns.distplot(erg_distance.loc[erg_distance<400])

erg_died_of.loc[(erg_distance > 800)&(erg_distance < 1500), 'killed_by'].value_counts()[:10].plot.bar(rot=30)
plt.xlabel("狙击的武器", fontsize=14)
plt.ylabel("被狙击的人数", fontsize=14)
plt.title('狙击武器跟击杀人数的统计(绝地海岛艾伦格)', fontsize=14)
plt.yticks(fontsize=12)

mrm_died_of.loc[(mrm_distance > 800)&(mrm_distance < 1000), 'killed_by'].value_counts()[:10].plot.bar(rot=30)
plt.xlabel("狙击的武器", fontsize=14)
plt.ylabel("被狙击的人数", fontsize=14)
plt.title('狙击武器跟击杀人数的统计(热情沙漠米拉玛)', fontsize=14)
plt.yticks(fontsize=12)

erg_died_of.loc[erg_distance<10, 'killed_by'].value_counts()[:10].plot.bar(rot=30)
plt.xlabel("近战武器", fontsize=14)
plt.ylabel("被击杀的人数", fontsize=14)
plt.title('近战武器跟击杀人数的统计(绝地海岛艾伦格)', fontsize=14)
plt.yticks(fontsize=12)

mrm_died_of.loc[mrm_distance<10, 'killed_by'].value_counts()[:10].plot.bar(rot=30)
plt.xlabel("近战武器", fontsize=14)
plt.ylabel("被击杀的人数", fontsize=14)
plt.title('近战武器武器跟击杀人数的统计(热情沙漠米拉玛)', fontsize=14)
plt.yticks(fontsize=12)

erg_died_of['erg_dist'] = erg_distance
erg_died_of = erg_died_of.loc[erg_died_of['erg_dist']<800, :]
top_weapons_erg = list(erg_died_of['killed_by'].value_counts()[:10].index)
top_weapon_kills = erg_died_of[np.in1d(erg_died_of['killed_by'], top_weapons_erg)].copy()
top_weapon_kills['bin'] = pd.cut(top_weapon_kills['erg_dist'], np.arange(0, 800, 10), include_lowest=True, labels=False)
top_weapon_kills_wide = top_weapon_kills.groupby(['killed_by', 'bin']).size().unstack(fill_value=0).transpose()

top_weapon_kills_wide = top_weapon_kills_wide.div(top_weapon_kills_wide.sum(axis=1), axis=0)
from bokeh.models.tools import HoverTool
from bokeh.palettes import brewer
from bokeh.plotting import figure, show, output_notebook
from bokeh.models.sources import ColumnDataSource
def  stacked(df):
    df_top = df.cumsum(axis=1)
    df_bottom = df_top.shift(axis=1).fillna(0)[::-1]
    df_stack = pd.concat([df_bottom, df_top], ignore_index=True)
    return df_stack

hover = HoverTool(
    tooltips=[
            ("index", "$index"),
            ("weapon", "@weapon"),
            ("(x,y)", "($x, $y)")
        ],
    point_policy='follow_mouse'
    )

areas = stacked(top_weapon_kills_wide)

colors = brewer['Spectral'][areas.shape[1]]
x2 = np.hstack((top_weapon_kills_wide.index[::-1],
                top_weapon_kills_wide.index)) /0.095

TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"
output_notebook()
p = figure(x_range=(1, 800), y_range=(0, 1), tools=[TOOLS, hover], plot_width=800)
p.grid.minor_grid_line_color = '#eeeeee'

source = ColumnDataSource(data={
    'x': [x2] * areas.shape[1],
    'y': [areas[c].values for c in areas],
    'weapon': list(top_weapon_kills_wide.columns),
    'color': colors
})
p.patches('x', 'y', source=source, legend_label="weapon",
          color='color', alpha=0.8, line_color=None)
p.title.text = "Top10武器在各距离下的击杀百分比（绝地海岛艾伦格）"
p.xaxis.axis_label = "击杀距离（0-800米）"
p.yaxis.axis_label = "百分比"
show(p)

mrm_died_of['erg_dist'] = mrm_distance
mrm_died_of = mrm_died_of.loc[mrm_died_of['erg_dist']<800, :]
top_weapons_erg = list(mrm_died_of['killed_by'].value_counts()[:10].index)
top_weapon_kills = mrm_died_of[np.in1d(mrm_died_of['killed_by'], top_weapons_erg)].copy()
top_weapon_kills['bin'] = pd.cut(top_weapon_kills['erg_dist'], np.arange(0, 800, 10), include_lowest=True, labels=False)
top_weapon_kills_wide = top_weapon_kills.groupby(['killed_by', 'bin']).size().unstack(fill_value=0).transpose()

top_weapon_kills_wide = top_weapon_kills_wide.div(top_weapon_kills_wide.sum(axis=1), axis=0)
def  stacked(df):
    df_top = df.cumsum(axis=1)
    df_bottom = df_top.shift(axis=1).fillna(0)[::-1]
    df_stack = pd.concat([df_bottom, df_top], ignore_index=True)
    return df_stack

hover = HoverTool(
    tooltips=[
            ("index", "$index"),
            ("weapon", "@weapon"),
            ("(x,y)", "($x, $y)")
        ],
    point_policy='follow_mouse'
    )

areas = stacked(top_weapon_kills_wide)

colors = brewer['Spectral'][areas.shape[1]]
x2 = np.hstack((top_weapon_kills_wide.index[::-1],
                top_weapon_kills_wide.index)) /0.095

TOOLS="pan,wheel_zoom,box_zoom,reset,previewsave"
output_notebook()
p = figure(x_range=(1, 800), y_range=(0, 1), tools=[TOOLS, hover], plot_width=800)
p.grid.minor_grid_line_color = '#eeeeee'

source = ColumnDataSource(data={
    'x': [x2] * areas.shape[1],
    'y': [areas[c].values for c in areas],
    'weapon': list(top_weapon_kills_wide.columns),
    'color': colors
})

p.patches('x', 'y', source=source, legend_label="weapon",
          color='color', alpha=0.8, line_color=None)
p.title.text = "Top10武器在各距离下的击杀百分比（热情沙漠米拉玛）"
p.xaxis.axis_label = "击杀距离（0-800米）"
p.yaxis.axis_label = "击杀百分比"
show(p)

kill_by_self = death1.loc[death1['killer_name']==death1['victim_name'], "killed_by"]
kill_by_self.value_counts()[:10].plot.barh()
plt.xlabel("自毙的人数", fontsize=14)
plt.ylabel("自毙的方式", fontsize=14)
plt.title('自己把自己干倒的方式与人数', fontsize=14)
plt.yticks(fontsize=12)
