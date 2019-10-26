data6_1 <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework6/data6_1.txt")
colnames(data6_1) <- c("Year","t","GDP","K","L","lnGDP","lnK","lnL")

data6_2 <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework6/data6_2.txt")
colnames(data6_2) <- c("x3","x1","x2","y")

model_6_1 <- nls(GDP ~ A*(K^alpha)*(L^beta),data=data6_1,start=list(A=0.45,alpha=0.5,beta=0.5))
summary(model_6_1)

model_6_2 <- glm(y~x1+x2+x3, family=binomial(link='logit'), data=data6_2)
summary(model_6_2)
logit.step <-step(model_6_2,direction='both')
summary(logit.step)

male_30 <- data.frame(x1=30,x3=1)
female_30 <- data.frame(x1=30,x3=0)
pre1<-predict(logit.step,male_30)
pre2<-predict(logit.step,female_30)
p1 <- exp(pre1)/(1+exp(pre1))
p2 <- exp(pre2)/(1+exp(pre2))
c(p1,p2)
