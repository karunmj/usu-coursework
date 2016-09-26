##1. Double mass curve analysis
#Creating a data frame of given data
year = c(1970,1971,1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983,1984,1985,1986)
A = c(1010,1005,1067,1051,801,1411,1222,1012,1153,1140,829,1165,1170,1264,1200,942,1166)
B = c(1161,978,1226,880,1146,1353,1018,751,1059,1223,1003,1120,989,1056,1261,811,969)
C = c(780,1041,1027,825,933,1584,1215,832,918,781,782,865,956,1102,1058,710,1158)
D = c(949,784,1067,1014,923,930,981,683,824,1056,796,1121,1286,1044,991,875,1202)
E = c(1135,970,1158,1022,821,1483,1174,771,1188,967,1088,963,1287,1190,1283,873,1209)
annppt=data.frame(year,A,B,D,E,C)

#Average ABDE
avg_abde = rep(NA,nrow(annppt))
for (i in 1:nrow(annppt)){
  avg_abde[i] = rowMeans(annppt[i,2:5])
}

#Cumulative average ABDE and C
cum_avg_abde = cumsum(avg_abde)
cum_c = cumsum(annppt['C'])

#Plot bw cum_avg_abde and cum_c
plot(cum_avg_abde,cum_c[,1],xaxt='n')
axis(side = 1, at=cum_avg_abde, labels = c("1970", "1971", "1972", "1973", "1974", "1975", "1976", "1977", "1978", "1979", "1980", "1981", "1982", "1983", "1984", "1985", "1986"))

#Calculating fit, k value (assuming bw 1970-1974 and 1975-1986)
fitpre = lm(cum_c[,1][1:5]~cum_avg_abde[1:5]) 
fitpost = lm(cum_c[,1][6:17]~cum_avg_abde[6:17])
abline(fitpre)
abline(fitpost)
sloppre = summary(fitpre$coefficients)[6]
sloppost = summary(fitpost$coefficients)[1]
k=sloppost/sloppre

#Multiplying 1970-1974 C data with k
Cnew=c(C[1:5]*k,C[6:17])

  
##2. Number of gauges question


##3. Intensity duration frequency problem