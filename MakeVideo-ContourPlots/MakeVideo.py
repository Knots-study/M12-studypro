import pathlib
import csv
import numpy as np
import matplotlib.pyplot as plt

Inputfiles = pathlib.Path('input/').glob('*.csv')

number = 0
for DepWater in Inputfiles:
    number += 1
    print(DepWater.name)
    path = "input/" + str(DepWater.name)
    npcsv =  np.flipud(np.delete(np.genfromtxt(path, delimiter=','),1316,1))

    x = np.arange(1316)
    y = np.arange(1316)
    xx, yy = np.meshgrid(x, y)

    cont = plt.contourf(xx, yy, npcsv, cmap = "jet")
    plt.colorbar(cont)
    plt.title(DepWater.name)
    plt.savefig("output/" + str(number).zfill(4) +".png")
    plt.clf()

