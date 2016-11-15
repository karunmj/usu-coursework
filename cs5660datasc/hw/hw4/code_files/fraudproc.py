import pandas as pd 

fraud = pd.read_csv("outputel37.txt", header = None, index_col = False, sep = "\t")

countyid = fraud[0]

count2006 = fraud[1]
count2006 = count2006.map(eval).apply(pd.Series)

count2008 = fraud[3]
count2008 = count2008.map(eval).apply(pd.Series)

#Increase in 2008 for party 1
inc1 = ((count2008[1]-count2006[1])/count2006[1])*100

#Increase in 2008 for party 2
inc2 = ((count2008[2]-count2006[2])/count2006[2])*100

#Increase in 2008 for party 3
inc3 = ((count2008[3]-count2006[3])/count2006[3])*100

fraudproc = pd.concat([countyid, inc1, inc2, inc3], join='outer', axis=1)

fraudproc.to_csv(path_or_buf="fraudproc.txt")

sort1 = fraudproc.sort_values([1], ascending = 0) #None above
sort2 = fraudproc.sort_values([2], ascending = 0) #None above 50
sort3 = fraudproc.sort_values([3], ascending = 0) #Couple above 50
