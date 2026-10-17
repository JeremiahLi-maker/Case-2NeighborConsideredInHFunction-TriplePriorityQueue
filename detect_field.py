import matplotlib.pyplot as plt

list_detect1 = []
for i in range(40, 45, 1): # 外门右1
    list_detect1.append(((23, -i), 0.6))
for i in range(44, 50, 1):  #右上门  range(29, 35, 1) by 20220417
   list_detect1.append(((77, -i), 0.6))
for i in range(23, 25, 1): # 左上门
    list_detect1.append(((2, -i), 0.8))
for i in range(58, 60, 1): # 左下门
  list_detect1.append(((2, -i), 0.8))
for i in range(66, 71, 1):  # 右下门
   list_detect1.append(((77, -i), 0.8))
for i in range(26, 28, 1): # 最下面的门
   list_detect1.append(((i, -75), 0.8))

list_detect1.append(((11, -54), 0.6)) #里屋下最左
list_detect1.append(((12, -54), 0.6)) #里屋下最右
list_detect1.append(((10, -39), 0.6)) # 里屋左上二
list_detect1.append(((10, -52), 0.6)) # 里屋左下四
list_detect1.append(((10, -46), 0.6))# 里屋左下三
list_detect1.append(((10, -32), 0.6)) #里屋左上一
list_detect1.append(((17, -31), 0.6)) #最上门


list_detect2 = []  # 圆心坐标(28,24)中间最上
for i in range(23, 26, 1):
    list_detect2.append((21, -i))
for i in range(22, 28, 1):
    list_detect2.append((22, -i))
for i in range(22, 28, 1):
    list_detect2.append((23, -i))
for i in range(22, 28, 1):
    list_detect2.append((24, -i))
for i in range(22, 31, 1):
    list_detect2.append((25, -i))
for i in range(19, 31, 1):
    list_detect2.append((26, -i))
for i in range(19, 32, 1):
    list_detect2.append((27, -i))
for i in range(19, 32, 1):
    list_detect2.append((28, -i))
for i in range(18, 32, 1):
    list_detect2.append((29, -i))
for i in range(18, 31, 1):
    list_detect2.append((30, -i))
for i in range(18, 31, 1):
    list_detect2.append((31, -i))
for i in range(22, 30, 1):
    list_detect2.append((32, -i))
for i in range(27, 29, 1):
    list_detect2.append((33, -i))


list_detect3 = []  # 圆心坐标(6, 23)最左上
for i in range(16, 31, 1):
    list_detect3.append((6, -i))
for i in range(16, 31, 1):
    list_detect3.append((5, -i))
for i in range(17, 30, 1):
    list_detect3.append((4, -i))
for i in range(17, 30, 1):
    list_detect3.append((3, -i))
for i in range(21, 28, 1):
    list_detect3.append((7, -i))
for i in range(21, 28, 1):
    list_detect3.append((8, -i))
for i in range(23, 28, 1):
    list_detect3.append((9, -i))
for i in range(23, 28, 1):
    list_detect3.append((10, -i))
for i in range(23, 28, 1):
    list_detect3.append((11, -i))
for i in range(23, 27, 1):
    list_detect3.append((12, -i))
for i in range(23, 25, 1):
    list_detect3.append((13, -i))


list_detect4 = []  # 圆心坐标(5, 60)最左下
for i in range(53, 68, 1):
    list_detect4.append((5, -i))
for i in range(53, 68, 1):
    list_detect4.append((4, -i))
for i in range(54, 67, 1):
    list_detect4.append((3, -i))
for i in range(53, 68, 1):
    list_detect4.append((6, -i))
for i in range(56, 67, 1):
    list_detect4.append((7, -i))
for i in range(56, 67, 1):
    list_detect4.append((8, -i))
for i in range(56, 66, 1):
    list_detect4.append((9, -i))
for i in range(56, 65, 1):
    list_detect4.append((10, -i))
for i in range(57, 64, 1):
    list_detect4.append((11, -i))
for i in range(59, 62, 1):
    list_detect4.append((12, -i))


list_detect5 = []  # 圆心坐标(75, 71) 最右下
for i in range(64, 75, 1):
    list_detect5.append((75, -i))
for i in range(68, 75, 1):
    list_detect5.append((74, -i))
for i in range(68, 75, 1):
    list_detect5.append((73, -i))
for i in range(68, 75, 1):
    list_detect5.append((72, -i))
for i in range(68, 75, 1):
    list_detect5.append((71, -i))
for i in range(68, 75, 1):
    list_detect5.append((70, -i))
for i in range(68, 75, 1):
    list_detect5.append((69, -i))
for i in range(68, 75, 1):
    list_detect5.append((68, -i))
for i in range(64, 75, 1):
    list_detect5.append((76, -i))


list_detect6 = []  # 圆心坐标(60, 28) 最右上
for i in range(27, 36, 1):
    list_detect6.append((60, -i))
for i in range(27, 36, 1):
    list_detect6.append((59, -i))
for i in range(27, 35, 1):
    list_detect6.append((58, -i))
for i in range(27, 35, 1):
    list_detect6.append((57, -i))
for i in range(27, 35, 1):
    list_detect6.append((56, -i))
for i in range(27, 35, 1):
    list_detect6.append((55, -i))
for i in range(27, 35, 1):
    list_detect6.append((54, -i))
for i in range(27, 35, 1):
    list_detect6.append((53, -i))
for i in range(27, 35, 1):
    list_detect6.append((61, -i))
for i in range(27, 35, 1):
    list_detect6.append((62, -i))
for i in range(27, 35, 1):
    list_detect6.append((63, -i))
for i in range(27, 35, 1):
    list_detect6.append((64, -i))
for i in range(27, 35, 1):
    list_detect6.append((65, -i))
for i in range(27, 35, 1):
    list_detect6.append((66, -i))
for i in range(27, 35, 1):
    list_detect6.append((67, -i))


list_detect7 = []  # 圆心坐标(26, 59)中间第四
for i in range(52, 66, 1):
    list_detect7.append((26, -i))
for i in range(52, 66, 1):
    list_detect7.append((25, -i))
for i in range(56, 66, 1):
    list_detect7.append((24, -i))
for i in range(56, 66, 1):
    list_detect7.append((23, -i))
for i in range(56, 66, 1):
    list_detect7.append((22, -i))
for i in range(56, 66, 1):
    list_detect7.append((21, -i))
for i in range(56, 66, 1):
    list_detect7.append((20, -i))
for i in range(56, 66, 1):
    list_detect7.append((19, -i))
for i in range(52, 66, 1):
    list_detect7.append((27, -i))
for i in range(52, 66, 1):
    list_detect7.append((28, -i))
for i in range(52, 66, 1):
    list_detect7.append((29, -i))
for i in range(52, 58, 1):
    list_detect7.append((30, -i))
for i in range(52, 57, 1):
    list_detect7.append((31, -i))
for i in range(52, 56, 1):
    list_detect7.append((32, -i))


list_detect8 = []  # 圆心坐标(9, 40)里屋最左
for i in range(35, 42, 1):
    list_detect8.append((9, -i))
for i in range(35, 42, 1):
    list_detect8.append((8, -i))


list_detect9 = []  # 圆心坐标(25, 38)中间第二
for i in range(31, 46, 1):
    list_detect9.append((25, -i))
for i in range(31, 46, 1):
    list_detect9.append((26, -i))
for i in range(31, 46, 1):
    list_detect9.append((27, -i))
for i in range(31, 46, 1):
    list_detect9.append((28, -i))
for i in range(31, 46, 1):
    list_detect9.append((29, -i))
for i in range(31, 46, 1):
    list_detect9.append((30, -i))
for i in range(31, 46, 1):
    list_detect9.append((31, -i))
for i in range(31, 46, 1):
    list_detect9.append((32, -i))


list_detect10 = []  # 圆心坐标(25, 48) 中间第三
for i in range(41, 56, 1):
    list_detect10.append((25, -i))
for i in range(41, 56, 1):
    list_detect10.append((26, -i))
for i in range(41, 56, 1):
    list_detect10.append((27, -i))
for i in range(41, 56, 1):
    list_detect10.append((28, -i))
for i in range(41, 56, 1):
    list_detect10.append((29, -i))
for i in range(41, 56, 1):
    list_detect10.append((30, -i))
for i in range(41, 56, 1):
    list_detect10.append((31, -i))
for i in range(41, 56, 1):
    list_detect10.append((32, -i))


list_detect11 = []  # 圆心坐标(13, 42)里屋中间
for i in range(35, 50, 1):
    list_detect11.append((13, -i))
for i in range(35, 50, 1):
    list_detect11.append((14, -i))
for i in range(35, 50, 1):
    list_detect11.append((15, -i))
for i in range(35, 50, 1):
    list_detect11.append((16, -i))
for i in range(35, 50, 1):
    list_detect11.append((17, -i))
for i in range(35, 50, 1):
    list_detect11.append((18, -i))
for i in range(41, 43, 1):
    list_detect11.append((19, -i))
for i in range(41, 43, 1):
    list_detect11.append((20, -i))

list_detect12 = []  # 圆心坐标(11, 51)里屋左最下
for i in range(44, 55, 1):
    list_detect12.append((11, -i))
for i in range(51, 53, 1):
    list_detect12.append((12, -i))
for i in range(13, 18, 1):
    list_detect12.append((i, -51))

# list_detect13 = []  # 圆心坐标(23, 74)
# for i in range(67,75,1):
#     list_detect13.append((24,-i))
# for i in range(67,75,1):
#     list_detect13.append((23,-i))
# for i in range(67,75,1):
#     list_detect13.append((22,-i))
# for i in range(67,75,1):
#     list_detect13.append((21,-i))
# for i in range(67,75,1):
#     list_detect13.append((20,-i))
# for i in range(67,75,1):
#     list_detect13.append((19,-i))
# for i in range(67,75,1):
#     list_detect13.append((18,-i))
# for i in range(67,75,1):
#     list_detect13.append((17,-i))
# for i in range(67,75,1):
#     list_detect13.append((25,-i))
# for i in range(67,75,1):
#     list_detect13.append((26,-i))
# for i in range(67,75,1):
#     list_detect13.append((27,-i))
# for i in range(67,75,1):
#     list_detect13.append((28,-i))
# for i in range(67,75,1):
#     list_detect13.append((29,-i))
# for i in range(67,75,1):
#     list_detect13.append((30,-i))
# for i in range(67,75,1):
#     list_detect13.append((31,-i))

detect_prob_mark = {}  # 记录节点的探测概率 (x,y):probability


def funprop (a,b):
    return ( 1 - (1 - a) * ( 1 - b ))


def draw_detect_prob_1(list):  #门位置探测概率
    global detect_prob_mark
    for point, prob in list:
        if point in detect_prob_mark:
            detect_prob_mark[point] =  funprop(prob,detect_prob_mark[point])
        else:
            detect_prob_mark[point] = prob
        G_value = -220 * detect_prob_mark[point] + 220
        color_i = (1, G_value / 255, 10 / 255, 1)
        plt.fill_between([point[0], point[0] + 1], point[1] - 1, point[1], facecolor=[color_i])


def draw_detect_prob_2(list, center, k, p_0): #辐射状探测点概率分布
    global detect_prob_mark
    for i in list:
        distance = (((i[0] - center[0]) ** 2 + (i[1] - center[1]) ** 2) ** 0.5) * 1.6
        prob = k * distance + p_0
        if prob < 0:  # 不可能出现小于0的概率
            continue
        if i in detect_prob_mark:
            detect_prob_mark[i] = funprop(prob,detect_prob_mark[i])    #prob

        else:
            detect_prob_mark[i] = prob
        G_value = -220 * detect_prob_mark[i] + 220
        color_i = (1, G_value / 255, 10 / 255, 1)
        plt.fill_between([i[0], i[0] + 1], i[1] - 1, i[1], facecolor=[color_i])



