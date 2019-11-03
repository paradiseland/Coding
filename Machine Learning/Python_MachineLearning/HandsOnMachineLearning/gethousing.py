"""
data preprocessing
"""
import os
import tarfile
import hashlib
import numpy as np
from six.moves import urllib
import pandas as pd
import matplotlib.pyplot as plt

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml/master/"
HOUSING_PATH = "datasets/housing"
HOUSING_URL = DOWNLOAD_ROOT + HOUSING_PATH + "/housing.tgz"


def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    """get source data:housing from github"""  
    if not os.path.isdir(housing_path):
        os.makedirs(housing_path)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()


# fetch_housing_data()

def load_housing_data(housing_path=HOUSING_PATH):
    """load the data"""
    csv_path = os.path.join(housing_path,"housing.csv")
    return pd.read_csv(csv_path)


housing = load_housing_data()
housing.head()
housing.info()
housing["ocean_proximity"].value_counts()
housing.describe()



housing.hist(bins=50, figsize=(20,15)) # bins:num of bars.
plt.show()

# 创建测试集
def split_train_set(data,test_ratio):
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]
train_set, test_set = split_train_set(housing,0.2)

# 确认生成的是同样测试集
def test_set_check(idetifier,test_ratio,hash):
    return hash(np.int(idetifier)).digest()[-1] < 256* test_ratio
def split_train_test_by_id(data,test_ratio,id_column,hash=hashlib.md5):
    ids = data[id_column]
    in_test_set = ids.apply(lambda id_:test_set_check(id_,test_ratio,hash))
    return data.loc[~in_test_set],data.loc[in_test_set]
# 以行索引作为id
housing_with_id = housing.reset_index()
train_set,test_set = split_train_test_by_id(housing_with_id,0.2,"index")

# # 测试集和训练集的产生可以用sklearn
# from sklearn.model_selection import train_test_split
# train_set,test_set = train_test_split(housing,test_size=0.2,random_state=42)

# 创建收入类别属性 ceil进一法取整
housing["income_cat"] = np.ceil(housing["median_income"] / 1.5)

# 对收入类别分层抽样
from sklearn.model_selection import StratifiedShuffleSplit
split = StratifiedShuffleSplit(n_splits=1,test_size=0.2,random_state=42)
for train_index,test_index in split.split(housing,housing["income_cat"]):
    strat_train_set = housing.loc[train_index]
    strat_test_set = housing.loc[test_index]

# 删除incom_cat属性，回归原样
for set in (strat_train_set,strat_test_set):
    set.drop(["income_cat"], axis=1, inplace=True)

# 仅使用训练集作可视化
housing = strat_train_set.copy()
housing.plot(kind="scatter", x="longitude", y="latitude")
plt.show()
# 突出高密度地区的可视化
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.1)

# 利用颜色表来可视化不同地区房价
housing.plot(kind="scatter", x="longitude", y="latitude", alpha=0.4,s=housing["population"]/100,
             label="population", c="median_house_value",cmap=plt.get_cmap("jet"),colorbar=True,)
plt.legend()
plt.show()

# 各属性相关系数
corr_matrix = housing.corr()
# 查看每个属性与房价中位数关系
corr_matrix["median_house_value"].sort_values(ascending=False)

# 绘制属性间的相关性矩阵
from pandas.plotting import scatter_matrix
attributes = ["median_house_value", "median_income", "total_rooms","housing_median_age"]
scatter_matrix(housing[attributes],figsize=(12, 8))
plt.show()

# 最有潜力影响房价的是收入中位数
housing.plot(kind="scatter",x="median_income",y="median_house_value",alpha=0.1)
plt.show()

# 新建某些特征：如卧室总数与房间总数之比
housing["rooms_per_household"] = housing["total_rooms"] / housing["households"]
housing["bedrooms_per_room"] = housing["total_bedrooms"] / housing["total_rooms"]
housing["population_per_household"] = housing["population"] / housing["households"]
corr_matrix = housing.corr()

# 对缺值NA数据的处理 放弃属性、地区、补全中位数/均值
median_total_bedrooms = housing["total_bedrooms"].median()
housing.dropna(subset=["total_bedrooms"])
housing.drop("total_bedrooms",axis=1)
housing["total_bedrooms"].fillna(median_total_bedrooms)

# sklearn中imputer处理缺失值
from sklearn.preprocessing import Imputer
imputer =Imputer(strategy="median")

# 因为中位数仅能在数据上计算，所以最后一列没有数字型的要删掉
housing_num = housing.drop("ocean_proximity", axis=1)
imputer.fit(housing_num)

X = imputer.transform(housing_num)
housing_tr = pd.DataFrame(X,columns=housing_num.columns)

# ocean_proximity is text instead of num. need to encode to num
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
housing_cat = housing["ocean_proximity"]
housing_cat_encoded = encoder.fit_transform(housing_cat)
# encoder.classes_ 的属性可以读出该编码器的映射
# 独热向量 LabelBinarizer
