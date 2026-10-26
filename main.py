from create_map_matrix import *
from A_star import *
from detect_field import *
from P_R1A import *
from plot import *
from matplotlib.pyplot import MultipleLocator
import  xlsxwriter
import pandas as pd

import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # 换成这个，会显示图形窗口
import matplotlib.pyplot as plt
import time

#=====将二维最小TR矩阵数据值输出到excel表中
def save(map_tr, path):
    # path 例如 'maptr.xlsx'
    workbook = xlsxwriter.Workbook(path)          # 创建工作簿（这里就指定文件名）
    sheet1 = workbook.add_worksheet('sheet1')     # 新建工作表

    # 写入 map_tr 中的数据
    rows, cols = map_tr.shape
    for i in range(rows):
        for j in range(cols):
            sheet1.write(i, j, float(map_tr[i, j]))   # 写每个单元格的值
    workbook.close()




def draw_path(start, target, path, type, draw_openlist=True, draw_closelist=True):

    if path == False:
        print("Can not find the path!")  # 不能找到通往终点的路径
    else:
        print("Done!")  # 输出Done!表示找到了最短路径

    plot.draw_outline(start, target)
    if draw_openlist:
        for i in (i[1] for i in openSet):
            # 绘制openlist中的节点
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
    '''if draw_closelist:
        for i in close_set:
            # 绘制closelist中的节点
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")'''

    for i in path:
        # 绘制找到的路径
        x = i[1]
        y = -i[0]
        plt.fill_between([x, x + 1], y - 1, y, facecolor="blue")

    plt.fill_between([start[0], start[0] + 1], -start[1] - 1, -start[1], facecolor="magenta")
    plt.fill_between([target[0], target[0] + 1], -target[1] - 1, -target[1], facecolor="cyan")

    if type == 'distance':
        print("Distance=", gscore[path[0]] * 1.6)  # 路径距离
        print("number of grids:", len(path))  # 路径的节点数
    elif type == 'detection':
        print("P_I=", gscore[path[0]])  #
        print("number of grids:", len(path))  # 路径的节点数
    else: # print P_D
        print("P_D=", P_D[path[0]])
        print("number of grids:", len(path))  # 路径的节点数


    plt.show()


def draw_path2(start, target, path, type, draw_openlist=True, draw_closelist=True):

    if path == False:
        print("Can not find the path!")  # 不能找到通往终点的路径
    else:
        print("Done!")  # 输出Done!表示找到了最短路径

    plot.draw_outline(start, target)
    if draw_openlist:
        for i in (i[2] for i in openSet):
            # 绘制openlist中的节点
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
    '''if draw_closelist:
        for i in close_set:
            # 绘制closelist中的节点
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")'''

    for i in path:
        # 绘制找到的路径
        x = i[1]
        y = -i[0]
        plt.fill_between([x, x + 1], y - 1, y, facecolor="blue")

    plt.fill_between([start[0], start[0] + 1], -start[1] - 1, -start[1], facecolor="magenta")
    plt.fill_between([target[0], target[0] + 1], -target[1] - 1, -target[1], facecolor="cyan")

    if type == 'distance':
        print("Distance=", gscore[path[0]] * 1.6)  # 路径距离
        print("number of grids:", len(path))  # 路径的节点数
    elif type == 'detection':
        print("P_I=", gscore[path[0]])  #
        print("number of grids:", len(path))  # 路径的节点数
    else: # print P_D
        print("P_D=", P_D[path[0]])
        print("number of grids:", len(path))  # 路径的节点数


    plt.show()


if __name__ == '__main__':

    v = 3  # 敌手速度 m/s
    v1 = 2.5  # 响应力量速度 m/s

    start = (79, 45)    # 原值(79, 45)
    target = (9, 35)

    plot.draw_outline(start, target)  # 先调用一次，detect_prob_mark才会有数据
    plt.show()


    # ==========================构建二维模型==================================== #
    map1 = create_mapmat_1(78, 80, detect_prob_mark)
    print(detect_prob_mark)
    #从探测场中筛选出概率值最小的探测点
    a = 1
    for key, value in detect_prob_mark.items():
        if value < a:
            a = value
            b = key
    print(a)  #a为最小值
    print(b)  #b为最小值的坐标位置

    # ==========================最短长度路径（astar_dist RFT算法函数一致）==================================== #
    detect_prob_mark.clear()  # 因为探测概率是全局变量，每画图一次会在原基础上累加，故需初始化
    path1 = astar_dist(map1, start[::-1], target[::-1], show_process=False)
    draw_path(start, target, path1, type='distance',draw_closelist=True, draw_openlist=True)
    print('P_D=',P_D[target[::-1]])
    print('num of closelist:', len(close_set))
    #save(detect_prob_mark, 'detect_prob_mark02.xls')
    # ======================最小累积探测概率度路径================================ #
    initiate_GlobeParameters() # 因为每次路径搜索后的信息存在几个全局变量内，使用前务必初始化
    detect_prob_mark.clear() #因为探测概率是全局变量，每画图一次会在原基础上累加，故需初始化
    path_MD = astar_MinDetect(map1, start[::-1], target[::-1], point_TR=special_point_TR, v=v, show_process=False)
    draw_path(start, target, path_MD,type='',draw_openlist=False, draw_closelist=False)
    print('num of closelist:', len(close_set))


    # ======================响应力量的路径及RFT（astar_dist 基于最短距离一样的启发式搜索算法）================================ #
    start_ResponceForce = (31, 68)  # 响应力量的起点
    initiate_GlobeParameters()
    detect_prob_mark.clear() #因为探测概率是全局变量，每画图一次会在原基础上累加，故需初始化
    path2 = astar_dist(map1, start_ResponceForce[::-1], target[::-1], show_process=False) #基于最短距离计算
    draw_path(start_ResponceForce, target, path2, type='distance',draw_closelist=True,draw_openlist=True)
    RFT = gscore[path2[0]] * 1.6 / v1 + 20  # 响应力量响应时间为从起点跑到目标点的距离+20s(响应部队集结所需时间)
    print('RFT=', RFT)
    print('num of closelist:', len(close_set))


    # ======================最脆弱路径（基于确定路径TR）================================ #
    initiate_GlobeParameters()
    detect_prob_mark.clear() #因为探测概率是全局变量，每画图一次会在原基础上累加，故需初始化
    path3 = astar_detect(a,map1, start[::-1], target[::-1], point_TR=special_point_TR, RFT=RFT, v=v, show_process=False)
    draw_path2(start, target, path3, type='detection',draw_closelist=True,draw_openlist=True)
    print('P_D=', 1 - non_detect_prob[path3[0]])
    print('num of closelist:', len(close_set))



    # ======================最脆弱路径（基于最小TR）================================ #
    initiate_GlobeParameters()
    detect_prob_mark.clear() #因为探测概率是全局变量，每画图一次会在原基础上累加，故需初始化
    min_TR = generate_TR(map1, target[::-1], point_TR=special_point_TR, v=v)
    map_tr = np.ones((78,80), dtype=float) #初始化为1
    map_tr = -1*map_tr # -1 标识方格节点为障碍物，非负值表示该节点可通过，节点上的数值代表当前节点到目标节点索要花费的最小时间
    for i in min_TR:
        map_tr[i[0]][i[1]] = min_TR[i]
    save(map_tr, 'maptr.xlsx')  # 调用上面新的 save 函数
    path4 = astar_detect_1(a, map1, start[::-1], target[::-1], minTR=min_TR, RFT=RFT, point_TR=special_point_TR, v=v,show_process=False)
    draw_path(start,target, path4, type='detection', draw_openlist=False, draw_closelist=False)
    print('P_D=', 1 - non_detect_prob[path4[0]])
    print('num of closelist:', len(close_set))


    # ======================新增：独立检测点整体概率启发函数================================ #
    initiate_GlobeParameters()
    detect_prob_mark.clear()
    independent_start_time = time.perf_counter()
    path5 = astar_detect_independent(
        a, map1, start[::-1], target[::-1], point_TR=special_point_TR,
        RFT=RFT, v=v, show_process=False, cell_size=1.6)
    independent_elapsed_ms = (time.perf_counter() - independent_start_time) * 1000

    draw_path2(start, target, path5, type='detection',
               draw_openlist=True, draw_closelist=True)
    print('P_D=', 1 - non_detect_prob[path5[0]])
    print('num of closelist:', len(close_set))
    print('\n===== 独立检测点整体概率启发函数统计 =====')
    print('网格总数量:', map1.size)
    print('栅元尺寸:', 1.6)
    print('TR:', dic_TR[path5[0]])
    print('PI:', gscore[path5[0]])
    print('路径节点数量（个）:', len(path5))
    print('已遍历节点数量（个）:', len(close_set))
    print('运行总耗时（ms）:', independent_elapsed_ms)


    # ======================新增：仅使用 G(n) 的 Dijkstra 算法================================ #
    initiate_GlobeParameters()
    detect_prob_mark.clear()
    dijkstra_start_time = time.perf_counter()
    path6 = dijkstra_detect(
        a, map1, start[::-1], target[::-1], point_TR=special_point_TR,
        RFT=RFT, v=v, show_process=False, cell_size=1.6)
    dijkstra_elapsed_ms = (time.perf_counter() - dijkstra_start_time) * 1000

    draw_path2(start, target, path6, type='detection',
               draw_openlist=True, draw_closelist=True)
    print('P_D=', 1 - non_detect_prob[path6[0]])
    print('num of closelist:', len(close_set))
    print('\n===== 仅使用 G(n) 的 Dijkstra 算法统计 =====')
    print('网格总数量:', map1.size)
    print('栅元尺寸:', 1.6)
    print('TR:', dic_TR[path6[0]])
    print('PI:', gscore[path6[0]])
    print('路径节点数量（个）:', len(path6))
    print('已遍历节点数量（个）:', len(close_set))
    print('运行总耗时（ms）:', dijkstra_elapsed_ms)


    # ======================新增：论文递推式启发函数================================ #
    initiate_GlobeParameters()
    detect_prob_mark.clear()
    recursive_start_time = time.perf_counter()
    path7 = astar_detect_recursive(
        a, map1, start[::-1], target[::-1], point_TR=special_point_TR,
        RFT=RFT, v=v, show_process=False, cell_size=1.6)
    recursive_elapsed_ms = (time.perf_counter() - recursive_start_time) * 1000

    draw_path2(start, target, path7, type='detection',
               draw_openlist=True, draw_closelist=True)
    print('P_D=', 1 - non_detect_prob[path7[0]])
    print('num of closelist:', len(close_set))
    print('\n===== 论文递推式启发函数统计 =====')
    print('网格总数量:', map1.size)
    print('栅元尺寸:', 1.6)
    print('TR:', dic_TR[path7[0]])
    print('PI:', gscore[path7[0]])
    print('路径节点数量（个）:', len(path7))
    print('已遍历节点数量（个）:', len(close_set))
    print('运行总耗时（ms）:', recursive_elapsed_ms)


