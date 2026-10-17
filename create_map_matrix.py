import numpy as np
from obstacle import *
from create_fences import *

fence = create_fences()

def create_mapmat_1(x_num, y_num, detect_prob_mark):
    global fence
    # map1 = np.ones((x_num,y_num), dtype=np.float)
    # map1 = map1*0.1 # 将矩阵个点的值设为0.1
    map1 = np.zeros((x_num, y_num), dtype=float)  # 全初始化为0

    for i, j in obstacles:
        map1[-j][i] = 9  # 9为障碍物

    for i, j in fence:
        map1[-j][i] = 9

    for i in detect_prob_mark:
        map1[-i[1]][i[0]] = detect_prob_mark[i]

    return map1