data_10 <- read.table("C:/Coding/R/Applied Statistics/Data/ex2/test10.1.dat",head=TRUE)
X <- data_10
d <- dist(scale(X))
method <- c("single","complete", "average", "centroid", "ward.D")
for(m in method){
hc<-hclust(d, m)
# cutree 给定类别数或距离阈值确定最终聚类
class<-cutree(hc, k=5)
print(m)
print(sort(class))
}

for(m in method){
hc<-hclust(d, m)
windows()
# plclust(hc, hang=-1) 
#绘制谱系图
plot(hc,hang=-1)
re<-rect.hclust(hc, k=5, border="red") #绘制给出分类数量或分类阈值的分类结果
print(m); print(re)
}

library(ggplot2)
plot(x,hc$height,type='b')
a <- data.frame(x,hc$height)
ggplot(a,aes(x=x,y=hc$height))+geom_line(linetype=1)

(km <- kmeans(scale(X),5,nstart=20))


DDA2 <- function(TrnG1,TrnG2,TstG=NULL,var.equal=FALSE) {
    if(isnull(TstG) == TRUE)
}


DDA2<-function (TrnG1, TrnG2, TstG = NULL, var.equal = FALSE){ 
    if (is.null(TstG) == TRUE) TstG<-rbind(TrnG1,TrnG2)   
#rbind()将矩阵按行合并，如果不输入待测样本，则待测样本为两个训练样本的合并，即进行回判 
    if (is.vector(TstG) == TRUE)  
    TstG<-t(as.matrix(TstG))  
    else if (is.matrix(TstG) != TRUE)     
        TstG<-as.matrix(TstG)     
    if (is.matrix(TrnG1) != TRUE) 
        TrnG1<-as.matrix(TrnG1) 
    if (is.matrix(TrnG2) != TRUE) 
        TrnG2<-as.matrix(TrnG2)
    #将 TrnG1, TrnG2, TstG 转化为矩阵
    nx<-nrow(TstG) #取矩阵的行数
    blong<-matrix(rep(0, nx), nrow=1, byrow=TRUE, dimnames=list("blong", 1:nx))
    mu1<-colMeans(TrnG1); mu2<-colMeans(TrnG2) #计算样本均值
    if (var.equal == TRUE || var.equal == T){
        S<-var(rbind(TrnG1,TrnG2))     #计算合并的协方差阵 
        w<-mahalanobis(TstG, mu2, S)-mahalanobis(TstG, mu1, S)   #计算马氏距离之差 
}  
else{
    S1<-var(TrnG1); S2<-var(TrnG2) 
    w<-mahalanobis(TstG, mu2, S2)-mahalanobis(TstG, mu1, S1) 
    } 
    # 根据差值大于 0 与否，来判断类别归属  
    for (i in 1:nx){
        if (w[i]>0)  blong[i]<-1  
        else  blong[i]<-2 
}
blong 
}

# case10.2.1=read.table("clipboard", header=T)
classG1= case10.2.1 [1:11,2:5] #选取训练样本 1
classG2= case10.2.1 [12:27,2:5] #选取训练样本 2
#可以利用 var(classG1)和 var(classG2)计算两个训练样本的协方差矩阵，观察是否相等
newdata= case10.2.1 [28:30,2:5] #选取待测样本
# source("DDA2.R") #载入自编程序 DDA2.R
DDA2(classG1,classG2) #执行程序 DDA2.R
DDA2(classG1, classG2, newdata)


case10.2.2=read.table("clipboard", header=T) #选 D1:H28
attach(case10.2.2)
library(MASS)
ld=lda(G~x1+x2+x3+x4); ld #也可以尝试用 qda()非线性判别
Z=predict(ld) #预测判定结果
newG=Z$class #新分类
cbind(G, newG, Z$x) #合并新旧分类及判别函数值
tab=table(G, newG); tab #新旧分类列表比较
sum(diag(prop.table(tab))) #计算判别符合率
# case10.2.2=read.table("clipboard", header=T) #选 D1:H31
newdata= case10.2.1[28:30, 2:5] #选取待判样本
predict(ld, newdata= newdata)


distinguish.bayes<-function
(TrnX, TrnG, p=rep(1, length(levels(TrnG))),
TstX = NULL, var.equal = FALSE){
if (is.null(TstX) == TRUE) TstX<-TrnX #如果不输入 TstX,则待测样本为训练样本
if (is.vector(TstX) == TRUE) TstX<-t(as.matrix(TstX))
else if (is.matrix(TstX) != TRUE)
TstX<-as.matrix(TstX)
if (is.matrix(TrnX) != TRUE) TrnX<-as.matrix(TrnX) #将 TstX 转化为矩阵
nx<-nrow(TstX)
blong<-matrix(rep(0, nx), nrow=1, dimnames=list("blong", 1:nx))
g<-length(levels(TrnG))
mu<-matrix(0, nrow=g, ncol=ncol(TrnX))
for (i in 1:g)
mu[i,]<-colMeans(TrnX[TrnG==i,])
D<-matrix(0, nrow=g, ncol=nx)
if (var.equal == TRUE || var.equal == T){
for (i in 1:g){
d2 <- mahalanobis(TstX, mu[i,], var(TrnX))
D[i,] <- d2 - 2*log(p[i])
}
}
else{
for (i in 1:g){
S<-var(TrnX[TrnG==i,])
d2 <- mahalanobis(TstX, mu[i,], S)
D[i,] <- d2 - 2*log(p[i])+log(det(S))
}
}
#针对每一个 j，取最小的 D[i,j]对应的 i，作为对应的类别归属
for (j in 1:nx){
dmin<-Inf
for (i in 1:g)
if (D[i,j]<dmin){
dmin<-D[i,j]; blong[j]<-i
}
 }
blong
}

case10.2.2 <- read.table("clipboard",header=T)
GL <- factor(G)
distinguish.bayes(case10.2.2,GL)
