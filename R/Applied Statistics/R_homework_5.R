branches <-read.table("C:/Coding/R/Applied Statistics/Data/data_homework5/data_5.txt")
colnames(branches)<-c("y","x1","x2","x3","x4")

fm=lm(formula = branches$y~.,data = branches)
summary(fm)
cor(branches$x1,branches$y,method = "pearson")
cor(branches$x2,branches$y,method = "pearson")
cor(branches$x3,branches$y,method = "pearson")
cor(branches$x4,branches$y,method = "pearson")
cor(branches)

X <- as.matrix(branches[,-1])
ei <- eigen(t(X)%*%X)
lambda_max <- max(ei$values)
k <- c()
for (i in 1:4){k[i] <-sqrt(lambda_max/ei$values[i])} 

fm.step <- step(fm,direction = "backward")
fm.step <- step(fm,direction = "both")

cor(X124)
X124 <- as.matrix(branches[,c(-1,-4)])
ei124 <- eigen(t(X124)%*%(X124))
lambda_max_124 <- max(ei124$values)
k124 <- c()
for (i in 1:3){k124[i] <-sqrt(lambda_max_124/ei124$values[i])} 
k124

library(MASS)
fm_ridge <- lm.ridge(branches$y ~ ., lambda = seq(0, 150, length = 151), data = branches, model = TRUE)
fm_ridge$lambda[which.min(fm_ridge$GCV)]
fm_ridge$coef[which.min(fm_ridge$GCV)]
par(mfrow = c(1, 2))
matplot(fm_ridge$lambda, t(fm_ridge$coef), xlab = expression(lamdba), ylab = "Cofficients",type = "l", lty = 1:20)
abline(v = fm_ridge$lambda[which.min(fm_ridge$GCV)])
plot(fm_ridge$lambda, fm_ridge$GCV, type = "l", xlab = expression(lambda),ylab = expression(beta))
abline(v = fm_ridge$lambda[which.min(fm_ridge$GCV)])

library(ridge)
auto_ridge <- linearRidge(branches$y ~ ., data = branches)
summary(auto_ridge)

yX124 <- data.frame(branches[,-4])
auto_ridge124 <- linearRidge(yX124$y ~ ., data = yX124)
summary(auto_ridge124)
