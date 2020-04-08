from sklearn import svm
import pandas as pd
import numpy as np
from sklearn.metrics import recall_score,precision_score,roc_curve

dataset = pd.read_csv("Credit1.csv")
dataset = dataset.dropna(how='any')

length = len(dataset)
train_num = int(.8*length)
choose = np.random.choice(len(dataset),train_num, replace = False)

not_choose = list(set(range(len(dataset))).difference(choose))

col = dataset.columns.values.tolist()
col1 = col[3:]
data_x = np.array(dataset[col1])
train_x = data_x[choose]

test_x = data_x[not_choose]

data_y = np.array(dataset['Label'])
train_y = data_y[choose]
test_y = data_y[not_choose]

clf = svm.SVC(kernel = 'linear')
 
clf.fit(train_x, train_y)

print("权重系数w:\n", clf.coef_[0])

predict_result = clf.predict(test_x)

res = predict_result == test_y


# chazhun 1 True/pre1
# chaquan True 1/test1 
recall = recall_score(test_y, predict_result)
pre = precision_score(test_y, predict_result)

print("查全率：", recall,"\n查准率：", pre)

fpr0, tpr0, thresholds0 = roc_curve(test_y, predict_result)
ks0 = max(tpr0 - fpr0)

print("ks值:",ks0)
