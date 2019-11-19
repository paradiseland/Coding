disease <- read.csv("C:/Coding/R/Applied Statistics/Data/ex1/test7.2.csv")

glm_disease <- glm(Y~X1+X2+X3,family=binomial,data=disease)
summary(glm_disease)

glm_new <- step(glm_disease,direction="both")
summary(glm_new)

pre <- predict(glm_new,data.frame(X2=2,X3=0))
(p <- exp(pre)/(1+exp(pre)))
pre1 <- predict(glm_new,data.frame(X2=2,X3=1))
(p1 <- exp(pre1)/(1+exp(pre1)))

# influence.measures(glm_disease)

interval_estimate <- function(fm,alpha=0.5) {
    Result <- summary(fm)$coefficients
    left <- exp(Result[,1]-Result[,2]*qnorm(1-alpha/2))
    right <- exp(Result[,1]+Result[,2]*qnorm(1-alpha/2))
    rownames <- dimnames(Result)[[1]]
    colnames <- c("Estimate","Left","Right")
    matrix(c(exp(Result[,1]),left,right),ncol=3,dimnames=list(rownames,colnames))
}

interval_estimate(glm_new)

(odds_ration <- exp(pre1)/exp(pre))

