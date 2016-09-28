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


##3. Depth duration to Intensity duration frequency problem
#Creating data frame of given data, from depth to intensity
rrank=c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24)
ep=c(0.04,0.08,0.12,0.16,0.20,0.24,0.28,0.32,0.36,0.40,0.44,0.48,0.52,0.56,0.60,0.64,0.68,0.72,0.76,0.80,0.84,0.88,0.92,0.96)

onehr=c(2.32,2.08,2.06,1.82,1.78,1.75,1.69,1.61,1.55,1.55,1.53,1.50,1.41,1.38,1.19,1.16,1.13,1.07,1.04,1.02,0.91,0.86,0.79,0.65)
onehrint = onehr/1

sixhr=c(5.23,4.58,3.93,3.73,3.65,3.24,2.84,2.54,2.52,2.50,2.48,2.42,2.19,2.15,2.05,2.03,1.84,1.82,1.69,1.64,1.60,1.58,1.56,1.43)
sixhrint =sixhr/6

twofourhr=c(6.24,5.55,5.39,4.58,3.83,3.68,3.51,3.29,3.09,2.97,2.95,2.92,2.73,2.63,2.57,2.42,2.25,2.09,2.06,1.91,1.82,1.80,1.60,1.57)
twofourhrint = twofourhr/24

#Plot intensity vs exceedence probability perc
epp=ep*100

plot(epp,onehrint, log ="xy")
fitonehrint = lm((onehrint)~(epp)) 
abline(fitonehrint,untf=TRUE)
abline(v=4,col="green")
abline(v=10,col="red")
abline(v=20,col="blue")
abline(v=50,col="yellow")
onecol=predict(fitonehrint,newdata = data.frame(epp=c(50,20,10,4)))

plot(epp,sixhrint,log = "xy")
fitsixhrint = lm((sixhrint)~(epp)) 
abline(fitsixhrint, untf = TRUE)
abline(v=4,col="green")
abline(v=10,col="red")
abline(v=20,col="blue")
abline(v=50,col="yellow")
sixcol=predict(fitsixhrint,newdata = data.frame(epp=c(50,20,10,4)))

plot(epp, twofourhrint,log = "xy")
fittwofourhrint = lm((twofourhrint)~(epp)) 
abline(fittwofourhrint, untf = TRUE)
abline(v=4,col="green")
abline(v=10,col="red")
abline(v=20,col="blue")
abline(v=50,col="yellow")
twofourcol=predict(fittwofourhrint,newdata = data.frame(epp=c(50,20,10,4)))

#Plot intensity duration frequency
rp = c(2, 5, 10, 25)
intdurfreq = data.frame(rp,onecol,sixcol,twofourcol)
