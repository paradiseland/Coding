# ST means a company may bankrupt.
data_9 <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework9/data_9.txt")
rownames(data_9) <- c("ST中源", "ST宇航","ST耀华","ST万杰","ST钛白","ST筑信","ST东航","洪城股份","工大首创","交大南洋","九鼎新材","恩华药业","东百集团","广东明珠","中国国航")
colnames(data_9) <- c('x1','x2','x3','x4','G')

X<- data.frame(x1=78.3563,x2=0.8895,x3=1.8001,x4=14.1022)

data_9_1 <- subset(data_9,G==1)
data_9_2 <- subset(data_9,G==2)


library(MASS)
# linear discriminant
(lda_co <- lda(G ~ x1+x2+x3+x4,data=data_9))
G_ <- predict(lda_co)
newG_lda <- G_$class
cbind(data_9$G,G_$x,newG_lda)
tab_lda <- table(data_9$G,newG_lda)
sum(diag(prop.table(tab_lda)))

# nonolinear discriminant
(qda_co <- qda(G ~ x1+x2+x3+x4,data=data_9))
G_qda <- predict(qda_co)
newG_qda <- G_qda$class
cbind(data_9$G,G_$x,newG_qda)
tab_qda <- table(data_9$G,newG_qda)
sum(diag(prop.table(tab_qda)))

# distance discriminant
library(mvstats)
dist_co <- discrim.dist(cbind(data_9$x1,data_9$x2,data_9$x3,data_9$x4),as.factor(data_9$G))
tab_dist <- table(data_9$G,dist_co$newG)
sum(diag(prop.table(tab_dist)))

# bayes discriminant
bayes_co <- lda(G ~ x1+x2+x3+x4,data=data_9,prior=c(8,7)/15)

# make a discriminant on a concrete data
(G_pre_lda <- predict(lda_co,X))

(G_pre_qda <- predict(qda_co,X))

(G_pre_dist <- discrim.dist(cbind(data_9$x1,data_9$x2,data_9$x3,data_9$x4),as.factor(data_9$G),X))

(G_pre_dist <- predict(bayes_co,X))


G_pre_bayes <- predict()
