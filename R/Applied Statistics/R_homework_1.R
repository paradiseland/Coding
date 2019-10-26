library(ggplot2)
library(aplpack)
library(fmsb)

gddata <- read.table("D:/R_Workspace/R_exercise/gd_data.csv")
colnames(gddata) <- c("Region","type","value")
gddataface <- read.table("D:/R_Workspace/R_exercise/gd.txt")
gddatastar <- gddataface[-1]
colnames(gddatastar) <- c("products","adds","promotes","exports")
rownames(gddataface) <- c("广州市","韶关市","深圳市","珠海市","汕头市",
                          "佛山市","江门市","湛江市","茂名市","肇庆市",
                          "惠州市","梅州市","汕尾市","河源市","阳江市",
                          "清远市","东莞市","中山市","潮州市","揭阳市","云浮市")
rownames(gddatastar) <- c("广州市","韶关市","深圳市","珠海市","汕头市",
                          "佛山市","江门市","湛江市","茂名市","肇庆市",
                          "惠州市","梅州市","汕尾市","河源市","阳江市",
                          "清远市","东莞市","中山市","潮州市","揭阳市","云浮市")

#箱线图绘制
ggplot(gddata,aes(type,value))+geom_boxplot(
  fill = "white", colour = "#3366FF",outlier.colour = "red")

#小提琴图绘制
ggplot(gddata,aes(type,value))+geom_violin(fill = "#CD6600", 
                                           colour = "brown")

#雷达图绘制
summary(gddatastar)
#获得统计值中的最大最小值数据
matrix_maxmin <- matrix(c(3266.52,940.86,3210.18,350.60,2.41,0.68,2.17,0.01),
                        byrow = TRUE,nrow = 2,
                        dimnames = list(c("最大值","最小值"),
                                        c("products","adds","promotes","exports")))
gddataradar<-rbind(matrix_maxmin,gddatastar)
radarchart(gddataradar,axistype =2,pcol = topo.colors(22),plty =2,title ="Radar Chart")

#脸谱图绘制
faces(gddataface[,2:5],face.type = 1)

#星象图绘制
stars(gddatastar,key.loc=c(7,2,5),cex=0.8)
stars(gddatastar,key.loc=c(7,2,5),cex=0.8,draw.segments = TRUE,full = FALSE)

#热力图绘制
ggplot(data = gddata,mapping = aes(x = Region,y = type,fill = value))+geom_tile(aes(fill = value),colour = "grey50")

