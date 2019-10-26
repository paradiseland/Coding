#homework3
library(ggplot2)
library(zoo)
library(lmtest)

#1.1 sign test
fish <- c( 13.32 , 13.06, 14.02, 11.86, 13.58, 13.77, 13.51, 14.42, 14.44,15.43)
Me <- median(fish)
std_me <- 14.6
bool_ <- c(fish > std_me)
p <- 0.5^10 + 10*(0.5^10)  #求p(x<=1) 

#1.2 Wilcoxon signed ranks test
wilcox.test(fish,alternative = c("two.sided"),mu = 14.6,conf.level = 0.95,exact = FALSE)

# 2 test normality:
# Pearsons chi-squared test,Kolmogorov-Sminov test
problem_data_2 <- c(-0.70,-5.60,2.00,2.80,0.70,3.50,4.00,5.80,7.10,-0.50,2.50,-1.60,1.70,3.00,0.40,4.50,4.60,2.50,6.00,-1.40)
group_problem_2 <- table(cut(problem_data_2,br=c(-6,1,3,8)))
# pnorm 返回正态分布的累积分布函数
p <- pnorm(c(1,3,8),mean(problem_data_2),sd(problem_data_2))
# 求解各部分正态占比
p <- c(p[1],p[2]-p[1],1-p[2])
chisq.test(group_problem_2,p=p)
# Kolmogorov-Smirnov test
# 使用jitter作小扰动以消除重复值
ks.test(jitter(problem_data_2),"pnorm",mean(problem_data_2),sd(problem_data_2))

# 4
data_4th <- read.table("D:/R_Workspace/R_exercise/data_homework3/4th_data.txt")
colnames(data_4th) <- c("No.","X","Y")
data_4th <- data_4th[-1,]
data_4th <- data_4th[-1]
rownames(data_4th) <- c(1:53)
data_4th$Y <- as.numeric(as.character(data_4th$Y))
data_4th$X <- as.numeric(as.character(data_4th$X))
data_4th <- data_4th[order(data_4th$X),] #对第一字段x排序
fm <- lm(Y ~ X,data = data_4th)

#model:y = -0.831307+0.0036828*x
line_x <- seq(0,3601,length.out = 53)
line_y <- -0.831307+0.0036828*line_x
ggplot(data_4th,aes(x=data_4th$X,y=data_4th$Y))+geom_point(color = "green")+geom_point(aes(x=line_x,y=line_y),color = "red",size = 0.5)+geom_line(aes(x=line_x,y=line_y)) 
# residual scatter point
ggplot()+geom_point(aes(x=seq(1,53),y=residuals(fm)),color = "red")
bptest(fm)
# 拟合：fitted(fm)

# weighted LS
m <- seq(-2,2,0.5)
result_of_loglik <- vector(length = length(m),mode = "list")
result_of_test <- vector(length = length(m),mode = "list")
for (j in 1:9)
  {w <- data_4th$X^(-m[j]) # 计算权向量
   fm_weighted <- lm(Y~X,weights = w,data_4th)
   # 记录对数似然统计量与回归方程结果
   result_of_loglik[[j]] <- logLik(fm_weighted)
   result_of_test[[j]] <- summary(fm_weighted)
}

fm_weighted <- lm(Y~X,weights = data_4th$X^(-1.5),data_4th)
cor(abs((sqrt(data_4th$X^(-1.5)) * residuals(fm_weighted))),data_4th$X,method = "spearman")

y_trans <- sqrt(data_4th$Y)
data_4_trans <- data.frame(data_4th$X,y_trans)
fm_trans <- lm(y_trans~data_4th.X,data_4_trans)
summary(fm_trans)

SSE <- sum(((fitted(fm_trans))^2 - data_4th$Y)^2)
SST<-sum(((fitted(fm_trans))^2-rep(mean(data_4th$Y),length.out=53))^2)
cor((fitted(fm_trans))^2 - data_4th$Y,data_4th$X,method = "spearman")
R_sqare <- 1-SSE/SST

#5
data_5th <- read.table("D:/R_Workspace/R_exercise/data_homework3/5th_data.txt")
colnames(data_5th) <- c("No.","x","y")
data_5th <- data_5th[-1,]
data_5th <- data_5th[-1]
data_5th$y <- as.numeric(as.character(data_5th$y))
data_5th$x <- as.numeric(as.character(data_5th$x))
# data_5th <- data_5th[order(data_5th$x),]
rownames(data_5th) <- c(1:20)
fm2 <- lm(y ~ x,data = data_5th)
summary(fm2)
# model: y = -1.434832 + 0.176163*x
#residual scatter point
ggplot()+geom_point(aes(x=seq(1,20),y=residuals(fm2)),color = "red")
ggplot()+geom_point(aes(x=seq(1,20),y=residuals(fm2)),color = "red")+geom_line(aes(x=seq(1,20) ,y = residuals(fm2)),color = "red",size = 0.6)
# dwtest
dwtest(fm2)
#iteration to elimiate the autocorrelation
res_5th <- residuals(fm2)

# iteration_1
DW = 0.66325
d_L = 1.41
rho = 1- DW/2
beta0 <- -1.434832
beta1 <- 0.176163
beta0t <- (beta0)*(1-rho)
beta1t <- beta1

x_t <- data_5th$x
y_t <- data_5th$y

{for (i in 20:2)
  {y_t[[i]] <- data_5th$y[i] - rho*data_5th$y[i-1]
   x_t[[i]] <- data_5th$x[i] - rho*data_5th$x[i-1]
  }
  y_t[[1]] <- y_t[1]
  x_t[[1]] <- x_t[1]
  data_5_iter <- data.frame(x_t,y_t)
  fm2_iter <- lm(y_t~x_t,data_5_iter)
  summary(fm2_iter)
  dwtest(fm2_iter)
} 
# DW1 = 0.86608
# iteration_2
DW = 0.86608
d_L = 1.41
rho = 1- DW/2
beta0t <- (beta0)*(1-rho)
beta1t <- beta1

x_t1 <- x_t
y_t1 <- y_t

{for (i in 20:2)
{y_t1[[i]] <- y_t[i] - rho*y_t[i-1]
x_t1[[i]] <- x_t[i] - rho*x_t[i-1]
}
  y_t1[[1]] <- y_t[1]
  x_t1[[1]] <- x_t[1]
  data_5_iter <- data.frame(x_t1,y_t1)
  fm2_iter <- lm(y_t1~x_t1,data_5_iter)
  summary(fm2_iter)
  dwtest(fm2_iter)
} 

  # diff1
  y_delta <- vector(length = 20)
  x_delta <- vector(length = 20)
  for (i in 20:2)
  {y_delta[[i]] <- data_5th$y[i] - data_5th$y[i-1]
   x_delta[[i]] <- data_5th$x[i] - data_5th$x[i-1]
  }
  y_delta[[1]] <- data_5th$y[1]
  x_delta[[1]] <- data_5th$x[1]
  data_5_delta <- data.frame(x_delta,y_delta)
  fm2_diff <- lm(y_delta~x_delta-1,data_5_delta)
  summary(fm2_diff)
  dwtest(fm2_diff)

  # diff2
  y_delta1 <- vector(length = 20)
  x_delta1 <- vector(length = 20)
  for (i in 20:2)
  {y_delta1[[i]] <- y_delta[i] - y_delta[i-1]
  x_delta1[[i]] <- x_delta[i] - x_delta[i-1]
  }
  y_delta1[[1]] <- y_delta[1]
  x_delta1[[1]] <- x_delta[1]
  data_5_delta1 <- data.frame(x_delta,y_delta)
  fm2_diff2 <- lm(y_delta1~x_delta1-1,data_5_delta1)
  summary(fm2_diff2)
  dwtest(fm2_diff2)
  