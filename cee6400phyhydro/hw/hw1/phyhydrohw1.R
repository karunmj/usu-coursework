##Importing dataretrieval, ggplot tools
library(dataRetrieval)
library(ggplot2)

##Retrieve daily discharge for last 20 years
siteNo <- "06713500"
pCode <- "00060"
start.date <- "1990-01-01"
end.date <- "2016-09-01"
cherry_creek = readNWISdv(siteNo,"00060",start.date,end.date)


##Problem 5: Time series of daily discharge
Q=cherry_creek$X_00060_00003
dt=cherry_creek$Date
plot(dt,Q,type="l", xlab="Year", ylab="Daily discharge Q [cfs]")
title(main="Daily discharege for Cherry creek (06713500), Denver, CO")


##Problem 6: Average annual flow, peak flow, annual 7 day minimum flow 
yy=as.numeric(format.Date(dt,"%Y")) #year
mo=as.numeric(format.Date(dt,"%m")) #month
wy=ifelse(mo>=10,yy+1,yy) 
yrseq=unique(wy) #unique years
Qmean=rep(NA,length(yrseq)) #Annual Flow
Q7=rep(NA,length(yrseq)) #Annual 7 day min
Qmax=rep(NA,length(yrseq)) # Annual peak flow
#n=7 moving average function
ma7 <- function(x,n=7){filter(x,rep(1/n,n), sides=2)}
for(i in 1:length(yrseq)){
  yr=yrseq[i]
  #Average annual flow
  Qmean[i]=mean(Q[wy==yr])
  #Annual Peak flow
  Qmax[i]=max(Q[wy==yr])
  #Average 7 day minimum, which is the lowest of the flow rate sequence of 7 day moving average daily discharge values
  Q7temp = Q[wy==yr]
  print(Q7temp)
  Q7[i] = min(ma7(Q7temp),na.rm=TRUE)
  print(Q7[i])
}
plot(yrseq,Qmax,ylim=c(0,max(Qmax)), ylab="Flow rate [cfs]", xlab = "Year")
lines(yrseq,Qmean, col = 3)
points(yrseq,Q7,pch=2,col=2)


##Problem 7: Flow duration curve
x=sort(Qmean)
n=length(Qmean)
nmid=n/2+0.5
x[nmid]
median(Qmean)
p=(1:n-0.4)/(n+0.2)
approx(p,x,0.25)
approx(p,x,0.75)
quantile(Qmean,probs=c(0.25,0.5,0.75))
quantile(Q7,probs=c(0.25,0.5,0.75))

mean(Qmean)
sd(Qmean)
sd(Qmean)/mean(Qmean)

Qs=sort(Q)
n=length(Qs)
p=((1:n)-0.4)/(n+0.2)
plot(1-p,Qs,log="y")

normplot.r=function(x,labvals=c(0.1,0.2,0.5,0.8,0.9,0.95,0.99,0.995),b=0,exceed=F,log="",xlab="",ylab="")
{
  xs=sort(x)
  n=length(xs)
  i=1:n
  p=(i-b)/(n+1-2*b) # General plotting position, See Chow et al p396
  if(exceed)p=1-p
  q=qnorm(p) # Normal quantile
  plot(q,xs,xaxt="n",log=log,xlab=xlab,ylab=ylab)
  qv=qnorm(labvals)
  axis(1,at=qv,label=labvals)
} 

normplot.r(Q,log="y",exceed=T,xlab="Exceedence frequency",ylab="Q",b=0.4)


##Problem 8: Monthly mean streamflow
# Monthly mean streamflow
yrmo=yy*100+mo
yrmoseq=unique(yrmo)
Qmonth=rep(NA,length(yrmoseq))
for(i in 1:length(yrmoseq)){
  ii=yrmoseq[i]
  Qmonth[i]=mean(Q[yrmo==ii])
}
plot(1:length(yrmoseq),Qmonth,type="l", xlab ="Month number", ylab = "Monthly mean flow [cfs]", xaxt ='n')

#Mean of monthly streamflows
year=trunc(yrmoseq/100)
month=yrmoseq-year*100
Qmm=rep(NA,12)
for(mm in 1:12){
  Qmm[mm]=mean(Qmonth[month==mm])
}
plot(1:12,Qmm,type="l", xlab = "Month", ylab = "Mean of monthly streamflow [cfs]", xaxt = 'n')
axis(side = 1, c(1:12), labels = c("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"))







