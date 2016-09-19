library(dataRetrieval)

##1.Sensitivity of tp wrt S, ap
#wrt S, keeping ap constant
S=1.74e17
ap=0.3
A=5.10e14
sig=5.78e-8
for(i in 1:5){
  S=append(S, S[i]*1.05)
}
tp=(S*(1-ap)/(sig*A))^1/4
plot(S/S[1],tp/tp[1],type="l")
#wrt ap, keeping S constant
ap=0.3
for(i in 1:5){
  ap=append(ap, ap[i]*1.05)
}
tp=(S*(1-ap)/(sig*A))^1/4
points(ap/ap[1],tp/tp[1],col = 3)

##2. (Refer notes)

##3. (Refer notes)

##4. Sensitivity of Ts wrt f
ku=0.18
kl=0.075
f=0.95
W=1.07e13
Qe=4.08e16
Qh=8.67e15
for(i in 1:5){
  f=append(f, f[i]*1.05)
}
Ts=(((3-3*ap-2*ku-kl)*S-1.5*Qe-Qh+2*W)/(3-2*f)*sig*A)^(1/4)
plot(f/f[1],Ts/Ts[1],type="l")

##5. For a watershed, 
#precipitation
ppt = read.csv("usu/usu-coursework/cee6400phyhydro/hw/hw2/PRISM_ppt_stable_4km_1990_2015_39.7577_-105.0108.csv", skip = 10)  
ppt_avg = mean(unlist(ppt[2]))

#runoff
siteNo <- "06713500"
pCode <- "00060"
start.date <- "1990-01-01"
end.date <- "2015-12-31"
cherry_creek = readNWISdv(siteNo,"00060",start.date,end.date)
Q=cherry_creek$X_00060_00003
dt=cherry_creek$Date
yy=as.numeric(format.Date(dt,"%Y")) #year
mo=as.numeric(format.Date(dt,"%m")) #month
#wy=ifelse(mo>=10,yy+1,yy) Not doing for water years but instead regular for now
yrseq=unique(yy) #unique years
Qmean=rep(NA,length(yrseq)) #Annual Flow
for(i in 1:length(yrseq)){
  yr=yrseq[i]
  #Average annual flow
  Qmean[i]=mean(Q[yy==yr])
}
cherry_creek_area = 7040 #mi2, from WaterStats ?? or just 4km2?
ro = (Qmean/(cherry_creek_area*(5280)^2))*86400*365*12*25.4
ro_avg = mean(ro)

#evapotranspirtion
et = ppt[2] - ro
et_avg = mean(unlist(et))

#b. Seasonal distribution of precipitation and runoff
for(i in 1:length(yrseq)){
    yr=yrseq[i]
    Qspring[i] = mean(Q[yy==yr & mo %in% c(1,2,3,4)])
    Qsummer[i] = mean(Q[yy==yr & mo %in% c(5,6,7,8)])
    Qwinter[i] = mean(Q[yy==yr & mo %in% c(9,10,11,12)])
}    
#TODO
#divide by are to get mm/yrors
#obtain monthly ppt data from prism and then do the same


#c. Runoff ratio (w)
w = mean(ro)/mean(unlist(ppt[2]))

##6. For a watershed, 
#a. Mean annual air temp and regional PET
meanannualtemp = read.csv("usu/usu-coursework/cee6400phyhydro/hw/hw2/PRISM_tmean_stable_4km_1990_2015_39.7577_-105.0108.csv", skip = 10)  
pet = 1.2e10*exp((-4620)/(meanannualtemp[2]+273.15))
pet_avg = mean(unlist(pet))

#b. Best fit value for 'w', storage parameter, until RO matches your values of watershed
#ro_avg = ppt_avg*(1-((ppt_avg)/((ppt_avg^w)+(pet_avg^w))^(1/w)))
fs <- function(w,y) {(ppt_avg*(1-((ppt_avg)/((ppt_avg^w)+(pet_avg^w))^(1/w))))-y}
w=uniroot(fs,y=ro_avg,lower=-10,upper=10)[1]

#c. Elasticity of runoff to precipitation
numr = 1-(1/(1+(ppt_avg/pet_avg)^w)^(1+1/w))
denr = 1-(pet_avg/(ppt_avg^w+pet_avg^w)^(1/w))
el = numr/denr

#d. Relative change in runoff
meanannualtempk = mean(unlist(meanannualtemp[2])) + 273.15
numra1=5.54e13*exp(-4620/mean(unlist(meanannualtempk)))
denmra1=(mean(unlist(meanannualtemp))^2)*ppt_avg*(1+(pet_avg/ppt_avg)^w)^(1+(1/w))
denmra2=(1-(pet_avg/(ppt_avg^w+pet_avg^w)^(1/w)))
rc=-1*(numra1/(denmra2*denmra1))



