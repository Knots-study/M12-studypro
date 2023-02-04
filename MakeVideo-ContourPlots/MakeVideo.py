import pathlib
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

Inputfiles = pathlib.Path('input/').glob('*.csv')
files = []
for DepWater in Inputfiles:
    files.append("input/" + str(DepWater.name))
    print("input/" + str(DepWater.name))

#max_depth = 0.0
#num = 0
#for DepWater in files:
    #num += 1
    #print(DepWater)
    #if num == 60:
        #break
    #with open(DepWater,mode="r") as f:
        #reader = csv.reader(f,delimiter=',')
        #for row in reader:
            #for k in range(1316):
                #max_depth = max(max_depth,float(row[k]))
#print(max_depth)

number = 0

for DepWater in files:

    #number += 1
    #if(number==60):
       # break
    #print(DepWater)
    npcsv =  np.flipud(np.delete(np.genfromtxt(DepWater, delimiter=','),95,1))

    x = np.arange(104)
    y = np.arange(95)
    xx, yy = np.meshgrid(x, y)

    fig = plt.figure()
    fig.add_subplot(111)
    plt.title("市野川流域(東松山地域周辺)の最大浸水深の比較", fontname="MS Gothic")
    cont = plt.contourf(xx, yy, npcsv, cmap = "jet")
    plt.colorbar(cont,orientation="vertical")
    plt.ax.set_yticklabels(["m"])
    #cont.set_clim(0,max_depth)
    plt.savefig("output/" + str(number).zfill(4) +".png")
    plt.clf()
    plt.close()

