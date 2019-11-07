data_8 <- read.table("C:/Coding/R/Applied Statistics/Data/data_homework8/data_8.txt")
colnames(data_8) <- c("DXBZ","CZBZ","WMBZ")
rownames(data_8) <- c("北京","天津","河北","山西","内蒙古","辽宁","吉林","黑龙江","上海","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","广西","海南","四川","贵州","云南","西藏","陕西","甘肃","青海","宁夏","新疆")
library(stats)
# euclidean distance
euclidean <- dist(data_8,method="euclidean")

complete <- hclust(euclidean,method='complete')
fig_complete <- as.dendrogram(complete,hang=-1)
plot(fig_complete,main="最长距离法")  


aver <- hclust(euclidean,method="average")
fig_average <- as.dendrogram(aver,hang=-1)
plot(fig_average,main="类平均法")

centgravity <- hclust(euclidean,method="centroid")
fig_centgravity <- as.dendrogram(aver,hang=-1)
plot(fig_centgravity,main="重心法")

ward <- hclust(euclidean,method="ward.D")
fig_ward <- as.dendrogram(aver,hang=-1)
plot(fig_ward,main="ward法")



km <- kmeans(data_8, 4, iter.max = 10,nstart=20)
fitted(km)

library(fpc)
plotcluster(scale(data_8), km$cluster)
