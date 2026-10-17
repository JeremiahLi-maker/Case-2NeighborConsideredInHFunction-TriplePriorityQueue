# 围栏的坐标
def create_fences():
    list = []
    for i in range(2, 78, 1):
        list.append((i, -1))

    for i in range(2, 44, 1): # range(2, 29, 1) by 20220417
        list.append((77, -i))

    for i in range(50, 66, 1): # range(35, 66, 1) by 20220417
        list.append((77, -i))

    for i in range(71, 76, 1):
        list.append((77, -i))

    for i in range(28, 78, 1):
        list.append((i, -75))

    for i in range(28, 78, 1):
        list.append((i, -75))

    for i in range(2, 26, 1):
        list.append((i, -75))

    for i in range(60, 75, 1):
        list.append((2, -i))

    for i in range(25, 58, 1):
        list.append((2, -i))

    for i in range(2, 23, 1):
        list.append((2, -i))

    return list
