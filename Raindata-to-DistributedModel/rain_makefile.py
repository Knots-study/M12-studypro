# -*- coding: utf-8 -*-
import numpy as np
from math import sqrt 
import csv

id_max = 494*782

def main():

    count = 1
    for day in range(712,715):
        for i in range(0,24):
            if day == 712:
                if i<9:
                    continue
            elif day == 714:
                if i>8:
                    continue
            for j in range(1,121):
                if day == 713 and i == 15:
                    if j == 119 or j==120:
                        continue
                open_filename = str(day).zfill(4) + str(i).zfill(2) + "_" + str(j) + ".csv"
                #print("open "+ open_filename +" now!")

                idrain = []#xy座標と降雨量データ
                with open(open_filename,mode="r") as f:
                    reader = csv.reader(f,delimiter=',')
                    for row in reader:
                        idrain.append(float(row[2])/100.0)

                output_rain = ["" for k in range(494)]
                with open("xyrain_2022hatogawa.csv",mode="r") as f1:
                    reader = csv.reader(f1,delimiter=',')
                    id = 0
                    for row in reader:
                        for k in range(782):
                            output_rain[id] += f"{idrain[int(row[k])]},"
                        id = id + 1
                
                with open(r"D:\raintocsv_QGIS\2022\rain_2022hatogawa\xyrain_2022hatogawa_" + str(count) +".csv",mode="w") as f2:
                    f2.write("\n".join(output_rain))
                
                print("finish "+ str(count/5760 * 100) + "％ now!")

                count = count + 1
                


if __name__ == "__main__":
    main()