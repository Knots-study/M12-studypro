# -*- coding: utf-8 -*-
import numpy as np
from math import sqrt 
import csv

id_max = 494*782

def calc_xy(phi_deg, lambda_deg, phi0_deg, lambda0_deg):
    """ 緯度経度を平面直角座標に変換する
    - input:
        (phi_deg, lambda_deg): 変換したい緯度・経度[度]（分・秒でなく小数であることに注意）
        (phi0_deg, lambda0_deg): 平面直角座標系原点の緯度・経度[度]（分・秒でなく小数であることに注意）
    - output:
        x: 変換後の平面直角座標[m]
        y: 変換後の平面直角座標[m]
    """
    # 緯度経度・平面直角座標系原点をラジアンに直す
    phi_rad = np.deg2rad(phi_deg)
    lambda_rad = np.deg2rad(lambda_deg)
    phi0_rad = np.deg2rad(phi0_deg)
    lambda0_rad = np.deg2rad(lambda0_deg)

    # 補助関数
    def A_array(n):
        A0 = 1 + (n**2)/4. + (n**4)/64.
        A1 = -     (3./2)*( n - (n**3)/8. - (n**5)/64. ) 
        A2 =     (15./16)*( n**2 - (n**4)/4. )
        A3 = -   (35./48)*( n**3 - (5./16)*(n**5) )
        A4 =   (315./512)*( n**4 )
        A5 = -(693./1280)*( n**5 )
        return np.array([A0, A1, A2, A3, A4, A5])

    def alpha_array(n):
        a0 = np.nan # dummy
        a1 = (1./2)*n - (2./3)*(n**2) + (5./16)*(n**3) + (41./180)*(n**4) - (127./288)*(n**5)
        a2 = (13./48)*(n**2) - (3./5)*(n**3) + (557./1440)*(n**4) + (281./630)*(n**5)
        a3 = (61./240)*(n**3) - (103./140)*(n**4) + (15061./26880)*(n**5)
        a4 = (49561./161280)*(n**4) - (179./168)*(n**5)
        a5 = (34729./80640)*(n**5)
        return np.array([a0, a1, a2, a3, a4, a5])

    # 定数 (a, F: 世界測地系-測地基準系1980（GRS80）楕円体)
    m0 = 0.9999 
    a = 6378137.
    F = 298.257222101

    # (1) n, A_i, alpha_iの計算
    n = 1. / (2*F - 1)
    A_array = A_array(n)
    alpha_array = alpha_array(n)

    # (2), S, Aの計算
    A_ = ( (m0*a)/(1.+n) )*A_array[0] # [m]
    S_ = ( (m0*a)/(1.+n) )*( A_array[0]*phi0_rad + np.dot(A_array[1:], np.sin(2*phi0_rad*np.arange(1,6))) ) # [m]

    # (3) lambda_c, lambda_sの計算
    lambda_c = np.cos(lambda_rad - lambda0_rad)
    lambda_s = np.sin(lambda_rad - lambda0_rad)

    # (4) t, t_の計算
    t = np.sinh( np.arctanh(np.sin(phi_rad)) - ((2*np.sqrt(n)) / (1+n))*np.arctanh(((2*np.sqrt(n)) / (1+n)) * np.sin(phi_rad)) )
    t_ = np.sqrt(1 + t*t)

    # (5) xi', eta'の計算
    xi2  = np.arctan(t / lambda_c) # [rad]
    eta2 = np.arctanh(lambda_s / t_)

    # (6) x, yの計算
    x = A_ * (xi2 + np.sum(np.multiply(alpha_array[1:],
                                       np.multiply(np.sin(2*xi2*np.arange(1,6)),
                                                   np.cosh(2*eta2*np.arange(1,6)))))) - S_ # [m]
    y = A_ * (eta2 + np.sum(np.multiply(alpha_array[1:],
                                        np.multiply(np.cos(2*xi2*np.arange(1,6)),
                                                    np.sinh(2*eta2*np.arange(1,6)))))) # [m]
    # return
    return x, y # [m]

def main():
    XYZ = []#グリッドの中心XY座標を求める
    for i in range(494):
        for j in range(782): 
            X_grid = 28725.0136 - i*150.0
            Y_grid = -102174.9934 + j*150.0
            XYZ.append([X_grid,Y_grid])

    for day in range(712,715):
        for i in range(48):
            XYrain = []#xy座標と降雨量データ
            body = []#出力する降雨量データ
            time_str = str(int(i/2))
            time_str += '00' if i%2==0 else '30'
            timer = str(day) + "_" + time_str.zfill(4)
            open_filename = "2019" + str(timer) + ".csv"
            print("open "+ open_filename +" now!")

            id=0
            with open(open_filename,mode="r") as f:
                reader = csv.reader(f,delimiter=',')
                for row in reader:
                    if(138.69<=float(row[0]) and float(row[0])<=140.01):#経度⇒緯度⇒降雨の順番
                        if(35.58<=float(row[1]) and float(row[1])<=36.27):
                            x, y = calc_xy(float(row[1]), float(row[0]), 36., 139+50./60)
                            XYrain.append([x,y,id]) #xy座標変換した降雨量データが入っている
                    id = id+1
            count = 0

            ###降雨量データの中心と地形データの中心の距離を計算する
            for grid in XYZ:
                ans_rain = 0 #ダミー値
                min_dis = 1<<32 #ダミー値
                count = count+1
                if(count%100==0):
                    print(count)
                for raindata in XYrain:
                    dis = sqrt((raindata[0]-grid[0])**2+(raindata[1]-grid[1])**2)
                    if(min_dis > dis):
                        min_dis = dis
                        ans_rain = raindata[2]
                body.append(ans_rain)

            output_rain = ["" for k in range(494)]
            for j in range(id_max):
                output_rain[int(j/782)] += f"{body[j]},"
            
            with open("xyrain_2019.csv",mode="w") as f1:
                f1.write("\n".join(output_rain))

if __name__ == "__main__":
    main()