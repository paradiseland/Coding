salary <- read.csv("C:/Coding/R/Applied Statistics/Data/ex1/test7.1.csv")
lm_salary <- lm(y~x1+x2+x3+x4,data=salary)
summary(lm_salary)

step_salary <- step(lm_salary,direction="forward")
step_salary <- step(lm_salary,direction="backward")
step_salary <- step(lm_salary,direction="both")

beta.int <- function(fm,alpha=0.5) {
    # coe:A
    A <- summary(fm)$coefficients
    # degree of freedom:df
    df <- fm$df.residual
    # interval estimation:1st-2nd*t_distribution
    left <- A[,1]-A[,2]*qt(1-alpha/2,df)
    right <- A[,1]+A[,2]*qt(1-alpha/2,df)
    rownames <- dimnames(A)[[1]]
    colnames <- c("Estimate","Left","Right")
    matrix(c(A[,1],left,right),ncol=3,dimnames=list(rownames,colnames))
}

beta.int(step_salary)

y_res <- residuals(step_salary)
y_rst <- rstandard(step_salary)
(y_rst)

# RES RST analysis
y_fit <- predict(step_salary)
plot(y_res~y_fit)
plot(y_rst~y_fit)
text(y_fit[4],y_rst[4],labels=4,adj=1.2)
text(y_fit[35],y_rst[35],labels=35,adj=1.2)

# QQ test
qqnorm(y_res)
qqline(y_res)

# K-S test
ks.test(y_res,"pnorm",mean(y_res),sd(y_res))
# Pearson x2 test
pearson <- table(cut(y_res,br=c(-7000,-3000,0,3000,30000)))
p <- pnorm(c(-2900,5,3200,3100),mean(y_res),sd(y_res))
p <- c(p[1],p[2]-p[1],p[3]-p[2],1-p[3])
chisq.test(pearson,p=p) 
# Normal Wtest
shapiro.test(y_res)

step_salary_log <- update(step_salary,log(.)~.)
y_rst_log <- rstandard(step_salary_log)
y_fit_log <- predict(step_salary_log)
plot(y_rst_log~y_fit_log)
text(y_fit_log[35],y_rst_log[35],labels=35,adj=1.2)

lm_salary_del <- lm(log(y)~x1+x2+x3+x4,data=salary[-c(4,35),])
step_salary_del <- step(lm_salary_del,direction="both")
y_rst_del <- rstandard(step_salary_del)
y_fit_del <- predict(step_salary_del)
plot(y_rst_del~y_fit_del)

par(mfrow=c(2,2))
# residual vs fitted
plot(step_salary_log)
influence.measures(step_salary_log)

preds <- data.frame(x1=20000,x4=20)
predict(step_salary,newdata=preds,interval="prediction",level=0.95)

