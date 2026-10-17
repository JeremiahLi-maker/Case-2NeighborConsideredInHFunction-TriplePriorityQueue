import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

x = []
y = []

plt.axis([0, 100, 0, 10])
ax = plt.gca()
ax.set_aspect(1)
x_major_locator = MultipleLocator(1)
ax.xaxis.set_major_locator(x_major_locator)
y_major_locator = MultipleLocator(1)
ax.yaxis.set_major_locator(y_major_locator)
plt.xticks([]),plt.yticks([])   #隐藏坐标轴


if __name__ == '__main__':
    plt.plot(x, y)  # 绘制一个空图
    cc = np.arange(0,100,0.1)
    cc_list = cc.tolist()
    # for i in cc:
    #     print(type(i))
    for i in cc_list:
        xx = i/100
        G_value = -220*xx + 220
        color_i = (1,G_value/255,10/255,1)
        plt.fill_between([i, i+0.1], 0, 10, facecolor=[color_i])
    plt.show()