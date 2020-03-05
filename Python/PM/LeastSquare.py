import numpy as np

sheet = np.loadtxt('data.txt')

X = np.ones((len(sheet),2))
X[:,[1]] = sheet[:,[1]]
Y = sheet[:,[-1]]

# (X^T X)^(-1) X^Ty
beta = np.dot(np.dot(np.linalg.inv(np.dot(X.T, X)), X.T), Y)

print(beta)

[[ 3.11361202]
 [-0.40900852]]
