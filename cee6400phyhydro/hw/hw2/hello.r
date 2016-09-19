per = 0.5
ref=1
refa=c(ref)

for(i in 1:5){
  refa=append(refa, refa[i]*1.05)
}

print(ref)



