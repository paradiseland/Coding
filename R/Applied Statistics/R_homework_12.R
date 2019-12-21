enterprises <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework12/data_12.txt",header=T)
rownames(enterprises) = enterprises[,2]
enterprises <- enterprises[,c(-1,-2)]
cor(enterprises)
library(mvstats)
(Fac <- factpc(enterprises,3)) # 主成分法因子分析
(Fa1 <- factanal(enterprises,3,rot='varimax'))
(Fa1 <- factanal(enterprises,3,scores='regression'))
Fa1$scores
Fac1 = factpc(enterprises,3,scores='regression')
Fac1$scores
factanal.rank(Fa1,plot=T)
biplot(Fa1$scores,Fa1$loading)
Fac$Vars # 方差及贡献率

