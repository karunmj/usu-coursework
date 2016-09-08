#  Installing the needed USGS packages
install.packages("dataRetrieval")
library(dataRetrieval)

#vignette("dataRetrieval")  # This displays the help PDF

# A handy URL for site identification is http://maps.waterdata.usgs.gov/mapper/index.html 
siteNumber="10109001"
LoganDaily = readNWISdv(siteNumber,"00060","","")
head(LoganDaily)
Q=LoganDaily$X_00060_00003
dt=LoganDaily$Date
plot(dt,Q,type="l")

# Checking some of the USGS numbers
mean(LoganDaily$X_00060_00003[2:31])
LoganDaily[31,]

# Water year flows
yy=as.numeric(format.Date(dt,"%Y"))
mo=as.numeric(format.Date(dt,"%m"))
wy=ifelse(mo>=10,yy+1,yy)
yrseq=unique(wy)
Qmean=rep(NA,length(yrseq))
Q7=rep(NA,length(yrseq))
Qmax=rep(NA,length(yrseq))
for(i in 1:length(yrseq)){
  yr=yrseq[i]
  Qmean[i]=mean(Q[wy==yr])
  Q7[i]=min(Q[wy==yr])
  Qmax[i]=max(Q[wy==yr])
}
plot(yrseq,Qmean,type="l")
plot(yrseq,Qmax,ylim=c(0,max(Qmax)))
lines(yrseq,Qmean)
points(yrseq,Q7,pch=2,col=2)

# Statistics on this data
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

# Monthly mean streamflow
yrmo=yy*100+mo
yrmoseq=unique(yrmo)
Qmonth=rep(NA,length(yrmoseq))
for(i in 1:length(yrmoseq)){
  ii=yrmoseq[i]
  Qmonth[i]=mean(Q[yrmo==ii])
}
plot(1:length(yrmoseq),Qmonth,type="l")
year=trunc(yrmoseq/100)
month=yrmoseq-year*100
Qmm=rep(NA,12)
for(mm in 1:12){
  Qmm[mm]=mean(Qmonth[month==mm])
}
plot(1:12,Qmm,type="l")




  