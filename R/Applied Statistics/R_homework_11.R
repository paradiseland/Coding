urban_industry <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework11/data_11.txt",header=T)
rownames(urban_industry) <- c("metallurgy","electricity","coal","chemistry","machinery","building materials","forest workers","food","textile","sewing","leather","paper","cultural and educational art supplies")
x <- urban_industry
colnames(urban_industry) <- c("net fixed value","num of employees","total industrial output value","total labor producitivity","achievement/100yuan","capital profit&tax rate","fuel consumptionn","energy utilization efficiency")
cor(x)
cor_data <- cor(urban_industry)

PCA <- princomp(urban_industry, cor=T)

PCA$loadings

screeplot(PCA,type="lines")

PCA$scores
var <- PCA$sdev^2
sum(var[1:3])/sum(var)


library(mvstats)
princomp.rank(PCA,m=3,plot=T)
