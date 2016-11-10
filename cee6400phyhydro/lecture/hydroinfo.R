#1. suction, moisture content
n = 0.477
psia = 35.6
b = 7.75
thetar = 0.15

z=seq(0,1.5,0.1)


#classwork
Ksat = 0.612
w = 2
n = 0.477
psia = 35.6
b = 7.75
psif = psia * (2*b+3)/(2*b+6) 
theta0 = 0.3 
Dtheta = n - theta0
P = Dtheta*psif
F = c(0.1,1:6) 
fc = Ksat*(1+P/F)
plot(F,fc,type = 'l')
Fp = (Ksat*P)/(w-Ksat)
tp = Fp/w