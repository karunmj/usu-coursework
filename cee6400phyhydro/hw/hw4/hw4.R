##10: Grain size distribution curve
diameter = c(0.002, 0.005, 0.020, 0.074, 0.42, 2, 4.76, 9.5, 19, 50)
perc = c(30, 35, 42, 60, 80, 95, 98, 100, 100, 100)

plot(diameter, perc, log = 'x', xlab='Diameter (mm)', ylab = 'Percentage finer by weight', main = 'Grain size distribution curve', xaxt = 'n', type = 'b', ylim = c(0,100))
axis(1, at = c(0.001, 0.002, 0.01, 0.05, 0.1, 1, 2, 10, 100), labels = c('0.001', '0.002', '0.01', '0.05', '0.1', '1', '2', '10', '100'))
abline(v=0.002,col="blue")
abline(v=0.05,col="red")
abline(v=2,col="green")

#Excluding particles whose size is greater than 2mm and proportioning the remaining
twommfiner_diam = diameter[1:6]
twommfiner_perc = perc[1:6]
twommfiner_propperc = c()
for (i in 1:length(twommfiner_diam)) {
    print(i)
    print(twommfiner_perc[i])
    twommfiner_propperc[i] = (twommfiner_perc[i]/twommfiner_perc[6])*100
}

lines(twommfiner_diam, twommfiner_propperc, log = 'x')
legend("bottomright", cex=0.8, legend = c("Full sample","Finer than 2mm"), lty = c(1, 1), pch = c('o', ''))
#locator()
abline(h=31.6, col = 'blue')
abline(h=58, col = 'red')
abline(h=100, col = 'green')
text(0.005, 15, "%Clay", col = "black")
#arrows(x0=, y0=, x1=, y1=, col='black', length=0.1, lwd=2)
text(0.005, 45, "%Silt", col = "black")
text(0.005, 80, "%Sand", col = "black")


sandperc = 100-58
siltperc = 58-31.6
clayperc = 31.6

##11
##12
##13
##14
##15
##16
