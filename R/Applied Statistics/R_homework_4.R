boys <-read.table("D:/R_Workspace/R_exercise/data_homework4/data_4.txt")
colnames(boys) <- c('X1','X2','X3')
matrix_C <-matrix(c(1,0,-6,0,1,-4),nr=2,nc=3,byrow = TRUE)
matrix_boys <- as.matrix(boys)
# 均值向量
X_mean <- as.matrix(apply(matrix_boys,2,mean))
p <- 3
n <- 6
u0 <- c(0,0,0)
Xm <- X_mean - u0
cX_mean <- matrix_C %*% X_mean
mm <- diag(1,6) - matrix(1,6,6)/6
# 样本离差阵
A <- t(matrix_boys)%*%mm%*%matrix_boys
T2 <- n*(n-1)*t(cX_mean)%*%solve(matrix_C%*%A%*%t(matrix_C))%*%cX_mean
co <- (n-p+1)/((p-1)*(n-1))
F_result <- co*T2
#求p值
p_value <- 1 - pf(F_result,p-1,n-p+1)
cat('T2:',T2)
cat('F_value:',F_result)
cat('p_value:',p_value)