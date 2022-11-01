# -*- coding: utf-8 -*-
import pyproj
import os
import csv
import math

transformer = pyproj.Transformer.from_crs("epsg:4326", "epsg:6677", always_xy=True)

def main():
    x_dm = []; y_dm = []#分布型モデル("d"istributed "m"odel)におけるグリッドの中心座標が入るリスト
    calc_grid_dm(28725.0136, -102174.9934, 494, 782, 150.0, x_dm, y_dm)
    calc(x_dm, y_dm, 494, 782, "hatogawarain_2022.csv")

def calc_grid_dm(ulx, uly, gxnum, gynum, gsize, x_dm, y_dm):
    for i in range(gxnum):
        for j in range(gynum): 
            x = ulx - i * gsize
            y = uly + j * gsize
            x_dm.append(x), y_dm.append(y)


def calc(x_dm, y_dm, gxnum, gynum, filename):
    margin = 1000.0
    max_xdm = max(x_dm); min_xdm = min(x_dm)
    max_ydm = max(y_dm); min_ydm = min(y_dm)
    XYrain = []

    id = 0
    files = os.listdir("./input/source_data")
    with open("./input/source_data/" + files[0],mode="r") as f:
        reader = csv.reader(f,delimiter=',')
        for row in reader:
            x, y = transformer.transform(float(row[0]), float(row[1]))
            if(min_xdm - margin <= x <= max_xdm + margin and min_ydm - margin <= y <= max_ydm + margin):
                XYrain.append([x,y,id]) #xy座標変換した降雨量データが入っている
            id = id + 1
            print("id: ",id)
    
    body = []
    count = 0
    for gridx, gridy in zip(x_dm, y_dm):
        ans_rain = 0 #ダミー値
        min_dis = 1<<32 #ダミー値
        for raindata in XYrain:
            dis = math.sqrt((raindata[0]-gridx)**2+(raindata[1]-gridy)**2)
            if(min_dis > dis):
                min_dis = dis
                ans_rain = raindata[2]
        body.append(ans_rain)
        count = count + 1
        print("count: ",count)

    output_rain = ["" for k in range(gxnum)]
    for j in range(gxnum * gynum):
        output_rain[int(j/gynum)] += f"{body[j]},"
            
    with open(filename,mode="w") as f1:
        f1.write("\n".join(output_rain))



if __name__ == "__main__":
    main()