import numpy
import matplotlib.pyplot as plt
from heapq import heappush, heappop, heapify
import plot
from P_R1A import *
import math

P_C = 0.9  # 通信概率
I = 1 #影响因子

close_set = set()
came_from = {}
gscore = {}
fscore = {}
openSet = []

dic_TR = {}

P_D = {}
non_detect_prob = {}


def heuristic_cost_estimate_dist(neighbor, goal):
    #return 0                #启发函数为0 则启用非启发式算法 否则下面代码为启发式算法
    x = neighbor[0] - goal[0]  #neighbor节点表示邻近节点
    y = neighbor[1] - goal[1]
    h_straight=abs(x)+abs(y)
    h_diagonal=min(x, y)
    return h_diagonal*math.sqrt(2)+(h_straight-2*h_diagonal) # Diagonal距离


def dist_between(a, b):   #计算当前节点和邻近节点的距离
    return ((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5

def acc_detect_prob(neighbor, current, non_detect_prob, mat_prob):
    '''
    用于计算累计探测概率
    '''
    acc_prob = non_detect_prob[current] * mat_prob[neighbor[0]][neighbor[1]]
    return acc_prob


def add_p_i(neighbor, current, non_detect_prob, mat_prob, TR, RFT):
    '''
    用于计算截住概率
    '''
    global P_C
    mu = TR - RFT
    sigma_TR = 0.3 * TR
    sigma_RFT = 0.3 * RFT
    sigma = math.sqrt(sigma_TR ** 2 + sigma_RFT ** 2)  # 以均值的30%作为标准偏差
    add_P_I = mat_prob[neighbor[0]][neighbor[1]] * P_C * Get_P_R1A(mu, sigma)

    return add_P_I


def reconstruct_path(came_from, current):
    '''
    生成从终点到起点的路径

    :param came_from:
    :param current:
    :return: 路径节点的列表
    '''
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path


def initiate_GlobeParameters():
    '''
    初始化A*算法的全局变量（清空）
    '''
    global close_set, came_from, gscore, fscore, openSet, P_D, non_detect_prob, dic_TR

    close_set.clear()
    came_from.clear()
    gscore.clear()
    fscore.clear()
    openSet.clear()

    dic_TR.clear()

    P_D.clear()
    non_detect_prob.clear()


# ==========================最短长度路径 （RFT采用算法）==================================== #
def astar_dist(array, start, goal, show_process=False):
    '''
    求最短距离的A*算法

    :param array: 地图矩阵
    :param start: 起始点
    :param goal: 目标点
    :param show_process: 是否展示搜索过程，默认False
    :return: 成功找到路径则返回True，否则False
    '''
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]  # 8个方向
    # directions = [(0,1),(0,-1),(1,0),(-1,0)] # 4个方向

    global close_set, came_from, gscore, fscore, openSet, non_detect_prob

    gscore[start] = 0
    fscore[start] = heuristic_cost_estimate_dist(start, goal)
    non_detect_prob[start] = 1 - array[start[0]][start[1]]
    P_D[start] = array[start[0]][start[1]]

    heappush(openSet, (fscore[start], start))  # 往堆中插入一条新的值

    # 当openSet非空时
    while openSet:

        current = heappop(openSet)[1]  # 从堆中弹出fscore最小的节点

        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j in directions:  # 对当前节点的 8 个相邻节点一一进行检查
            neighbor = current[0] + i, current[1] + j

            ## 判断节点是否在地图范围内，并判断是否为障碍物
            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 9:  # 9为障碍物
                        continue
                else:
                    # y边界
                    continue
            else:
                # x边界
                continue

            # 忽略已经在closelist中的点
            if neighbor in close_set:
                continue

            #  当前的权值通过父节点的权值计算得到
            tentative_gScore = gscore[current] + dist_between(current, neighbor)
            tmpValue = tentative_gScore + heuristic_cost_estimate_dist(neighbor, goal)

            tentative_P_detect = P_D[current] + acc_detect_prob(neighbor, current, non_detect_prob, array)
            non_pd = non_detect_prob[current] * (1 - array[neighbor[0]][neighbor[1]])

            if neighbor not in [i[1] for i in openSet]:  # 遍历邻结点
                heappush(openSet, (tmpValue, neighbor))
            elif tentative_gScore >= gscore.get(neighbor, numpy.inf):  # 此时不为最优路径
                continue
            else:
                tmpValue_fscore = fscore[neighbor]
                del openSet[openSet.index((tmpValue_fscore, (neighbor[0], neighbor[1])))]
                tmp_fscore = tentative_gScore + heuristic_cost_estimate_dist(neighbor, goal)
                openSet.append((tmp_fscore, (neighbor[0], neighbor[1])))
                heapify(openSet)

            # 修改当前最优路径
            came_from[neighbor] = current
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tmpValue
            non_detect_prob[neighbor] = non_pd
            P_D[neighbor] = tentative_P_detect

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for i in (i[1] for i in openSet):
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for i in close_set:
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)

    return False

 # ======================最小累积探测概率度路径================================ #
def heuristic_cost_estimate_MD(neighbor, goal):   #最小累积探测概率估计函数Minimum Detection
    return 0  # 启发函数为0

 # ======================最小累积探测概率度路径================================ #
def astar_MinDetect(array, start, goal, point_TR, v, show_process=False):
    '''
    搜寻最小累积探测概率的路径
    '''

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    # directions = [(0,1),(0,-1),(1,0),(-1,0)] # 4个方向

    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, P_D, dic_TR

    gscore[start] = 0
    dic_TR[start] = 0
    fscore[start] = heuristic_cost_estimate_MD(start, goal)
    non_detect_prob[start] = 1 - array[start[0]][start[1]]
    P_D[start] = array[start[0]][start[1]]

    heappush(openSet, (fscore[start], dic_TR[start], start))

    while openSet:

        current = heappop(openSet)[2]
        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 9:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set:
                continue
            if i == 0 or j == 0:
                add_TR = 1.6 * 1 / v
            else:
                add_TR = 1.6 * (1 + 1) ** 0.5 / v

            if neighbor in point_TR:
                add_TR = add_TR + point_TR[neighbor]

            TR = dic_TR[current] + add_TR  # dic_TR[current] 累计TR ,add_TR 单步时间值

            tentative_gScore = gscore[current] + acc_detect_prob(neighbor, current, non_detect_prob, array)
            tmpValue = tentative_gScore + heuristic_cost_estimate_MD(neighbor, goal)
            tentative_P_detect = P_D[current] + acc_detect_prob(neighbor, current, non_detect_prob, array)
            non_pd = non_detect_prob[current] * (1 - array[neighbor[0]][neighbor[1]])

            if neighbor not in [i[2] for i in openSet]:
                heappush(openSet, (tmpValue, TR, neighbor))
            elif tentative_gScore > gscore.get(neighbor, numpy.inf):  # 此时不为最优路径
                continue
            elif tentative_gScore == gscore.get(neighbor, numpy.inf):
                if TR < dic_TR[neighbor]:
                    came_from[neighbor] = current
                    dic_TR[neighbor] = TR
                continue
            else:
                tmpValue_fscore = fscore[neighbor]
                del openSet[openSet.index((tmpValue_fscore, dic_TR[neighbor], (neighbor[0], neighbor[1])))]
                tmp_fscore = tentative_gScore + heuristic_cost_estimate_MD(neighbor, goal)
                openSet.append((tmp_fscore, dic_TR[neighbor], (neighbor[0], neighbor[1])))
                heapify(openSet)

            came_from[neighbor] = current
            dic_TR[neighbor] = TR
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tmpValue
            non_detect_prob[neighbor] = non_pd
            P_D[neighbor] = tentative_P_detect

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for i in (i[1] for i in openSet):
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for i in close_set:
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)

    return False

# ======================最脆弱路径（基于确定路径TR）================================ #
def heuristic_cost_estimate_detect( neighbor, goal, TR, RFT, v ):
    # return 0  # 启发函数为0 下面为整段为非启发式函数设计，注意启发函数H中的概率值放在astar_detect 函数里计算

    x = neighbor[0] - goal[0]
    y = neighbor[1] - goal[1]
    h_straight = abs(x) + abs(y)
    h_diagonal = min(x, y)
    n = h_diagonal * math.sqrt(2) + (h_straight - 2 * h_diagonal) # Diagonal距离

    TR =   TR +  n / v

    sigma_TR = 0.3 * TR
    sigma_RFT = 0.3 * RFT
    sigma = math.sqrt(sigma_TR ** 2 + sigma_RFT ** 2)

    cost_heuristic = I * Get_P_R1A(TR - RFT, sigma) * P_C  # mat_prob[neighbor[0]][neighbor[1]]

    return cost_heuristic


   # ======================最脆弱路径（基于确定路径TR）================================ #
def astar_detect(a,array, start, goal, point_TR, RFT, v, show_process=False):
    '''
    求最小截住概率的A*算法1

    '''

    Min_D=a  #a表示的概率场中概率最小的探测点
    print('最小探测概率=', Min_D)

    # 从终点开始寻找路径，交换起点和终点
    temp = start
    start = goal
    goal = temp

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    # directions = [(0,1),(0,-1),(1,0),(-1,0)] # 4个方向

    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, P_C, dic_TR,mat_prob

    dic_TR[start] = 0
    print('PROBstart',array[start[0]][start[1]])
    print('PROBgoal', array[goal[0]][goal[0]])
    gscore[start] = array[start[0]][start[1]] * P_C * Get_P_R1A(-RFT, 0.3 * RFT)
    fscore[start] = heuristic_cost_estimate_detect(start, goal, 0, RFT, v) * Min_D  #array[goal[0]][goal[0]] #array[start[0]][start[1]]
    non_detect_prob[start] = 1 - array[start[0]][start[1]]


    heappush(openSet, (fscore[start], dic_TR[start], start))

    while openSet:

        current = heappop(openSet)[2]

        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 9:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set:
                continue

            if i == 0 or j == 0:
                add_TR = 1.6 * 1 / v
            else:
                add_TR = 1.6 * (1 + 1) ** 0.5 / v

            if neighbor in point_TR:
                add_TR = add_TR + point_TR[neighbor]

            TR = dic_TR[current] + add_TR    #dic_TR[current] 累计TR ,add_TR 单步时间值

            tentative_gScore = (1 - array[neighbor[0]][neighbor[1]]) * gscore[current] + add_p_i(neighbor, current,
                                                                                                 non_detect_prob, array,
                                                                                                 TR, RFT)
            non_pd = non_detect_prob[current] * (1 - array[neighbor[0]][neighbor[1]])
            tmpValue = tentative_gScore - tentative_gScore * Min_D + heuristic_cost_estimate_detect(neighbor, goal, TR, RFT, v ) * Min_D #array[start[0]][start[1]]  #(1-non_pd) #array[neighbor[0]][neighbor[1]]  #array[neighbor] #(1- non_detect_prob[neighbor]) #

            if neighbor in [i[2] for i in openSet]:
                if tentative_gScore < gscore.get(neighbor, numpy.inf):
                    dic_TR[neighbor] = TR
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_gScore
                    fscore[neighbor] = tmpValue
                    non_detect_prob[neighbor] = non_pd
                elif tentative_gScore == gscore.get(neighbor, numpy.inf):
                    if TR < dic_TR[neighbor]:
                        dic_TR[neighbor] = TR
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_gScore
                        fscore[neighbor] = tmpValue
                        non_detect_prob[neighbor] = non_pd
                    elif TR == dic_TR.get(neighbor, numpy.inf):
                        dic_TR[neighbor] = TR
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_gScore
                        fscore[neighbor] = tmpValue
                        non_detect_prob[neighbor] = non_pd
            else:
                heappush(openSet, (tmpValue, TR, neighbor))
                dic_TR[neighbor] = TR
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gScore
                fscore[neighbor] = tmpValue
                non_detect_prob[neighbor] = non_pd

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for i in (i[1] for i in openSet):
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for i in close_set:
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)

    return False

# ======================最脆弱路径（基于最小TR）================================ #
def acc_p_i(neighbor, mat_prob, TR, RFT):
    '''
    用于计算截住概率
    '''
    global P_C

    mu = TR[neighbor] - RFT
    sigma_TR = 0.3 * TR[neighbor]
    sigma_RFT = 0.3 * RFT
    sigma = math.sqrt(sigma_TR ** 2 + sigma_RFT ** 2)
    acc_prob = mat_prob[neighbor[0]][neighbor[1]] * P_C * Get_P_R1A(mu, sigma)

    return acc_prob


def heuristic_cost_estimate_detect_1(neighbor, goal, dict_TR, RFT, v):
   #  return 0                #启发函数为0

    global P_C
    TR = dict_TR[neighbor] #TR值直接取miniTR值
    sigma_TR = 0.3 * TR
    sigma_RFT = 0.3 * RFT
    sigma = math.sqrt(sigma_TR ** 2 + sigma_RFT ** 2)

    cost_heuristic = I * Get_P_R1A(TR - RFT, sigma) * P_C

    return cost_heuristic

 # ======================最脆弱路径（基于最小TR）================================ #
def astar_detect_1(a, array, start, goal, minTR, RFT, point_TR, v, show_process=False):
    '''
    求最小截住概率的A*算法2，敌手在知晓被探测之后要立刻选择前往目标的最短路径
    '''
    Min_D=a  #a表示的概率场中概率最小的探测点
    print('最小探测概率=', Min_D)

    # 从终点开始寻找路径，交换起点和终点
    temp = start
    start = goal
    goal = temp

    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    # directions = [(0,1),(0,-1),(1,0),(-1,0)] # 4个方向

    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, dic_TR

    dic_TR[start] = 0
    gscore[start] = array[start[0]][start[1]] * P_C * Get_P_R1A(-RFT, 0.3 * RFT)
    fscore[start] = heuristic_cost_estimate_detect_1(start, goal, minTR, RFT, v) * Min_D   #array[start[0]][start[1]]
    non_detect_prob[start] = 1 - array[start[0]][start[1]]

    heappush(openSet, (fscore[start], dic_TR[start], start))

    while openSet:

        current = heappop(openSet)[2]

        if current == goal:
            return reconstruct_path(came_from, current)

        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j

            if 0 <= neighbor[0] < array.shape[0]:
                if 0 <= neighbor[1] < array.shape[1]:
                    if array[neighbor[0]][neighbor[1]] == 9:
                        continue
                else:
                    continue
            else:
                continue

            if neighbor in close_set:
                continue
            if i == 0 or j == 0:
                add_TR = 1.6 * 1 / v
            else:
                add_TR = 1.6 * (1 + 1) ** 0.5 / v

            if neighbor in point_TR:
                add_TR = add_TR + point_TR[neighbor]

            TR = dic_TR[current] + add_TR    #dic_TR[current] 累计TR ,add_TR 单步时间值

            tentative_gScore = (1 - array[neighbor[0]][neighbor[1]]) * gscore[current] + acc_p_i(neighbor, array, minTR,
                                                                                                 RFT)
            tmpValue = tentative_gScore - tentative_gScore * Min_D + heuristic_cost_estimate_detect_1(neighbor, goal, minTR, RFT, v) * Min_D
            non_pd = non_detect_prob[current] * (1 - array[neighbor[0]][neighbor[1]])

            if neighbor in [i[2] for i in openSet]:
                if tentative_gScore < gscore.get(neighbor, numpy.inf):
                    dic_TR[neighbor] = TR
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_gScore
                    fscore[neighbor] = tmpValue
                    non_detect_prob[neighbor] = non_pd
                elif tentative_gScore == gscore.get(neighbor, numpy.inf):
                    if TR < dic_TR[neighbor]:
                        dic_TR[neighbor] = TR
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_gScore
                        fscore[neighbor] = tmpValue
                        non_detect_prob[neighbor] = non_pd
                    elif TR == dic_TR.get(neighbor, numpy.inf):
                        dic_TR[neighbor] = TR
                        came_from[neighbor] = current
                        gscore[neighbor] = tentative_gScore
                        fscore[neighbor] = tmpValue
                        non_detect_prob[neighbor] = non_pd
            else:
                heappush(openSet, (tmpValue, TR, neighbor))
                dic_TR[neighbor] = TR
                came_from[neighbor] = current
                gscore[neighbor] = tentative_gScore
                fscore[neighbor] = tmpValue
                non_detect_prob[neighbor] = non_pd

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for i in (i[1] for i in openSet):
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for i in close_set:
                x = i[1]
                y = -i[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.001)

    return False


# ======================独立检测点整体概率启发函数================================ #
def detection_field_ratio(array):
    """Return p from the paper: detection-field area / walkable map area."""
    walkable = array != 9
    walkable_count = int(numpy.count_nonzero(walkable))
    detection_count = int(numpy.count_nonzero((array > 0) & walkable))
    return detection_count / walkable_count if walkable_count else 0.0


def estimate_independent_detection_points(array, current, goal,
                                          cell_size=1.6, p_field=None):
    """Estimate m=E(Phi)=p*N_grids using the paper's cell-diagonal model."""
    if p_field is None:
        p_field = detection_field_ratio(array)

    dx = abs(current[0] - goal[0])
    dy = abs(current[1] - goal[1])
    diagonal_distance = min(dx, dy) * math.sqrt(2) + abs(dx - dy)
    physical_distance = diagonal_distance * cell_size
    cell_diagonal = cell_size * math.sqrt(2)
    remaining_grids = physical_distance / cell_diagonal if cell_diagonal else 0.0
    return max(0, int(p_field * remaining_grids))


def independent_interruption_probability(p_n, p_capture, m):
    """Probability that at least one of m independent points interrupts successfully."""
    single_success = max(0.0, min(1.0, p_n * p_capture))
    return 1.0 - (1.0 - single_success) ** max(0, int(m))


def heuristic_cost_estimate_independent(neighbor, goal, current_g, TR, RFT,
                                        array, p_capture, cell_size=1.6, v=1.0,
                                        p_field=None):
    """Aggregate independent-point heuristic used by astar_detect_independent."""
    p_n = float(array[neighbor[0]][neighbor[1]])
    m = estimate_independent_detection_points(
        array, neighbor, goal, cell_size, p_field=p_field)
    dx = abs(neighbor[0] - goal[0])
    dy = abs(neighbor[1] - goal[1])
    diagonal_distance = min(dx, dy) * math.sqrt(2) + abs(dx - dy)
    future_TR = TR + diagonal_distance * cell_size / v
    sigma_TR = 0.3 * future_TR
    sigma_RFT = 0.3 * RFT
    sigma = math.sqrt(sigma_TR ** 2 + sigma_RFT ** 2)
    p_ra = Get_P_R1A(future_TR - RFT, sigma) if sigma else 0.0
    p_capture_n = P_C * p_ra
    future_success = independent_interruption_probability(p_n, p_capture_n, m)
    return max(0.0, (1.0 - current_g) * future_success)


def astar_detect_independent(a, array, start, goal, point_TR, RFT, v,
                             show_process=False, cell_size=1.6):
    """Search with the aggregate independent-detection-point heuristic."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, P_D, dic_TR
    Min_D = a
    p_field = detection_field_ratio(array)

    temp = start
    start = goal
    goal = temp
    dic_TR[start] = 0
    gscore[start] = array[start[0]][start[1]] * P_C * Get_P_R1A(-RFT, 0.3 * RFT)
    non_detect_prob[start] = 1 - array[start[0]][start[1]]
    fscore[start] = gscore[start]
    heappush(openSet, (fscore[start], dic_TR[start], start))

    while openSet:
        current = heappop(openSet)[2]
        if current == goal:
            return reconstruct_path(came_from, current)
        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j
            if not (0 <= neighbor[0] < array.shape[0] and
                    0 <= neighbor[1] < array.shape[1]):
                continue
            if array[neighbor[0]][neighbor[1]] == 9 or neighbor in close_set:
                continue

            add_TR = (cell_size / v if i == 0 or j == 0
                      else cell_size * math.sqrt(2) / v)
            if neighbor in point_TR:
                add_TR += point_TR[neighbor]
            TR = dic_TR[current] + add_TR

            p_n = array[neighbor[0]][neighbor[1]]
            tentative_gScore = ((1 - p_n) * gscore[current] +
                                p_n * P_C * Get_P_R1A(TR - RFT,
                                                      math.sqrt((0.3 * TR) ** 2 +
                                                                (0.3 * RFT) ** 2)))
            h_value = heuristic_cost_estimate_independent(
                neighbor, goal, tentative_gScore, TR, RFT, array,
                P_C, cell_size, v, p_field=p_field)
            tmpValue = tentative_gScore + h_value

            if neighbor in [item[2] for item in openSet]:
                if tentative_gScore >= gscore.get(neighbor, numpy.inf):
                    continue
                old_item = next(item for item in openSet if item[2] == neighbor)
                openSet.remove(old_item)
                heappush(openSet, (tmpValue, TR, neighbor))
                came_from[neighbor] = current
                dic_TR[neighbor] = TR
                gscore[neighbor] = tentative_gScore
                fscore[neighbor] = tmpValue
                non_detect_prob[neighbor] = non_detect_prob[current] * (1 - p_n)
                continue

            heappush(openSet, (tmpValue, TR, neighbor))
            came_from[neighbor] = current
            dic_TR[neighbor] = TR
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tmpValue
            non_detect_prob[neighbor] = non_detect_prob[current] * (1 - p_n)

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for item in (item[2] for item in openSet):
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for item in close_set:
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)
    return False


def dijkstra_detect(a, array, start, goal, point_TR, RFT, v,
                    show_process=False, cell_size=1.6):
    """Dijkstra search using only the accumulated interruption cost G(n)."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, P_D, dic_TR

    temp = start
    start = goal
    goal = temp
    dic_TR[start] = 0
    gscore[start] = array[start[0]][start[1]] * P_C * Get_P_R1A(-RFT, 0.3 * RFT)
    fscore[start] = gscore[start]
    non_detect_prob[start] = 1 - array[start[0]][start[1]]
    heappush(openSet, (gscore[start], dic_TR[start], start))

    while openSet:
        current = heappop(openSet)[2]
        if current == goal:
            return reconstruct_path(came_from, current)
        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j
            if not (0 <= neighbor[0] < array.shape[0] and
                    0 <= neighbor[1] < array.shape[1]):
                continue
            if array[neighbor[0]][neighbor[1]] == 9 or neighbor in close_set:
                continue

            add_TR = (cell_size / v if i == 0 or j == 0
                      else cell_size * math.sqrt(2) / v)
            if neighbor in point_TR:
                add_TR += point_TR[neighbor]
            TR = dic_TR[current] + add_TR
            p_n = array[neighbor[0]][neighbor[1]]
            sigma = math.sqrt((0.3 * TR) ** 2 + (0.3 * RFT) ** 2)
            tentative_gScore = ((1 - p_n) * gscore[current] +
                                p_n * P_C * Get_P_R1A(TR - RFT, sigma))

            if tentative_gScore >= gscore.get(neighbor, numpy.inf):
                continue

            if neighbor in [item[2] for item in openSet]:
                old_item = next(item for item in openSet if item[2] == neighbor)
                openSet.remove(old_item)

            heappush(openSet, (tentative_gScore, TR, neighbor))
            came_from[neighbor] = current
            dic_TR[neighbor] = TR
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tentative_gScore
            non_detect_prob[neighbor] = non_detect_prob[current] * (1 - p_n)

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for item in (item[2] for item in openSet):
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for item in close_set:
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)
    return False


def minimum_detection_probability(array):
    """Return the minimum nonzero detection probability on the map."""
    values = array[(array > 0) & (array != 9)]
    return float(numpy.min(values)) if values.size else 0.0


def heuristic_cost_estimate_recursive(neighbor, goal, current_g, TR, RFT,
                                      array, p_min, p_field, cell_size=1.6,
                                      v=1.0):
    """Paper Eq. (8): recursively estimate H(n)=P_s^I-P_n^I."""
    m = estimate_independent_detection_points(
        array, neighbor, goal, cell_size, p_field=p_field)
    dx = abs(neighbor[0] - goal[0])
    dy = abs(neighbor[1] - goal[1])
    diagonal_distance = min(dx, dy) * math.sqrt(2) + abs(dx - dy)
    future_TR = TR + diagonal_distance * cell_size / v
    sigma = math.sqrt((0.3 * future_TR) ** 2 + (0.3 * RFT) ** 2)
    p_ra = Get_P_R1A(future_TR - RFT, sigma) if sigma else 0.0
    q_n = P_C * p_ra

    cumulative_probability = current_g
    for _ in range(m):
        cumulative_probability = (p_min * q_n +
                                  (1.0 - p_min) * cumulative_probability)
    return max(0.0, cumulative_probability - current_g)


def astar_detect_recursive(a, array, start, goal, point_TR, RFT, v,
                           show_process=False, cell_size=1.6):
    """A* search using the recursive heuristic from paper Eq. (8)."""
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                  (1, 1), (1, -1), (-1, 1), (-1, -1)]
    global close_set, came_from, gscore, fscore, openSet, non_detect_prob, P_D, dic_TR

    p_min = minimum_detection_probability(array)
    p_field = detection_field_ratio(array)
    temp = start
    start = goal
    goal = temp
    dic_TR[start] = 0
    gscore[start] = array[start[0]][start[1]] * P_C * Get_P_R1A(-RFT, 0.3 * RFT)
    non_detect_prob[start] = 1 - array[start[0]][start[1]]
    fscore[start] = gscore[start]
    heappush(openSet, (fscore[start], dic_TR[start], start))

    while openSet:
        current = heappop(openSet)[2]
        if current == goal:
            return reconstruct_path(came_from, current)
        close_set.add(current)

        for i, j in directions:
            neighbor = current[0] + i, current[1] + j
            if not (0 <= neighbor[0] < array.shape[0] and
                    0 <= neighbor[1] < array.shape[1]):
                continue
            if array[neighbor[0]][neighbor[1]] == 9 or neighbor in close_set:
                continue

            add_TR = (cell_size / v if i == 0 or j == 0
                      else cell_size * math.sqrt(2) / v)
            if neighbor in point_TR:
                add_TR += point_TR[neighbor]
            TR = dic_TR[current] + add_TR
            p_n = array[neighbor[0]][neighbor[1]]
            sigma = math.sqrt((0.3 * TR) ** 2 + (0.3 * RFT) ** 2)
            tentative_gScore = ((1 - p_n) * gscore[current] +
                                p_n * P_C * Get_P_R1A(TR - RFT, sigma))
            h_value = heuristic_cost_estimate_recursive(
                neighbor, goal, tentative_gScore, TR, RFT, array,
                p_min, p_field, cell_size, v)
            tmpValue = tentative_gScore + h_value

            if tentative_gScore >= gscore.get(neighbor, numpy.inf):
                continue
            if neighbor in [item[2] for item in openSet]:
                old_item = next(item for item in openSet if item[2] == neighbor)
                openSet.remove(old_item)
            heappush(openSet, (tmpValue, TR, neighbor))
            came_from[neighbor] = current
            dic_TR[neighbor] = TR
            gscore[neighbor] = tentative_gScore
            fscore[neighbor] = tmpValue
            non_detect_prob[neighbor] = non_detect_prob[current] * (1 - p_n)

        if show_process:
            plt.cla()
            plot.draw_outline(start[::-1], goal[::-1])
            for item in (item[2] for item in openSet):
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="green")
            for item in close_set:
                x, y = item[1], -item[0]
                plt.fill_between([x, x + 1], y - 1, y, facecolor="purple")
            plt.pause(0.01)
    return False
