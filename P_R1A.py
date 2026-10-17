from queue import Queue
from detect_field import list_detect1
import math
#保护元素引起的时间延迟，如门的时间延迟为30s
special_point_TR = {}
for i, j in list_detect1:  #针对的是所有的门，可回溯至detection_field代码文件确认
    x = -i[1]
    y = i[0]
    point = (x, y)
    special_point_TR[point] = 30  # 门的延迟暂设为30s

#通过每个点到目标节点的TR时间遍历计算确定最小的TR时间，返回到main函数的基于最小TR的识别算法
def generate_TR(map, start, point_TR, v):  #point_TR  特殊的点，这里计算代表有时间延迟的点，比如门位置点
    '''
    求每个节点到终点的最小时间，以确定临界探测区域
    '''
    matrix_TR = {}
    q = Queue(maxsize=0)
    q.put(start)
    matrix_TR[start] = 0
    while not q.empty():
        current = q.get()
        #print(current,":out")
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # 8个方向
        for i, j in directions:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < map.shape[0] and 0 <= neighbor[1] < map.shape[1] and map[neighbor[0]][
                neighbor[1]] != 9:

                if i == 0 or j == 0:
                    add_TR = 1.6 * 1 / v
                else:
                    add_TR = 1.6 * (1 + 1) ** 0.5 / v

                if neighbor in point_TR:
                    add_TR = add_TR + point_TR[neighbor]

                if neighbor not in matrix_TR:
                    matrix_TR[neighbor] = matrix_TR[current] + add_TR
                    q.put(neighbor)
                    #print(neighbor,":in")
                elif matrix_TR[current] + add_TR < matrix_TR[neighbor]:
                    matrix_TR[neighbor] = matrix_TR[current] + add_TR

    return matrix_TR


def Get_P_R1A(mu, sigma):
    '''
    计算P_(R|A)

    :param mu: 均值
    :param sigma: 标准偏差
    :return: P_R|A
    '''
    return math.exp(1.7 * mu / sigma) / (1 + math.exp(1.7 * mu / sigma))
