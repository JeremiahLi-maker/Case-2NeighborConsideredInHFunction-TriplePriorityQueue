from matplotlib.pyplot import MultipleLocator
from obstacle import *
from create_fences import *
from detect_field import *


def draw_obstacles(o_list):
    for obstacle in o_list:
        plt.fill_between([obstacle[0], obstacle[0] + 1], obstacle[1] - 1, obstacle[1], facecolor="black")


def draw_outline(start, target):
    global detect_prob_mark
    '''
    绘制抽象地图的轮廓，开始点和目标点
    '''

    x = []
    y = []

    plt.axis([0, 80, -78, 0])
    ax = plt.gca()
    ax.set_aspect(1)
    x_major_locator = MultipleLocator(1)
    ax.xaxis.set_major_locator(x_major_locator)
    y_major_locator = MultipleLocator(1)
    ax.yaxis.set_major_locator(y_major_locator)

    plt.plot(x, y)  # 绘制一个空图

    draw_obstacles(obstacles)

    fence = create_fences()
    draw_obstacles(fence)

    draw_detect_prob_1(list_detect1)
    draw_detect_prob_2(list_detect2, (28, -24), k=-0.07, p_0=0.7) #中间1
    draw_detect_prob_2(list_detect3, (6, -23), k=-0.07, p_0=0.7) #左上
    draw_detect_prob_2(list_detect4, (5, -60), k=-0.07, p_0=0.7) #左下
    draw_detect_prob_2(list_detect5, (75, -71), k=-0.07, p_0=0.7) #右下
    draw_detect_prob_2(list_detect6, (60, -28), k=-0.07, p_0=0.7) #右上
    draw_detect_prob_2(list_detect7, (26, -59), k=-0.07, p_0=0.7) #中间4
    draw_detect_prob_2(list_detect8, (9, -40), k=-0.07, p_0=0.7) #室内左
    draw_detect_prob_2(list_detect9, (25, -38), k=-0.07, p_0=0.7) #中间2
    draw_detect_prob_2(list_detect10, (25, -48), k=-0.07, p_0=0.7) #中间3
    draw_detect_prob_2(list_detect11, (13, -42), k=-0.07, p_0=0.7)  #室内中
    draw_detect_prob_2(list_detect12, (11, -51), k=-0.07, p_0=0.7) #室内左下

    # draw_detect_prob_2(list_detect13, (24, -74), k=-0.045, p_0=0.5)

    plt.fill_between([start[0], start[0] + 1], -start[1] - 1, -start[1], facecolor="magenta")
    plt.fill_between([target[0], target[0] + 1], -target[1] - 1, -target[1], facecolor="cyan")

    plt.tick_params(axis='both', labelsize=0, length=0)  # 隐藏坐标的数字和刻度
    plt.grid(True)