import winsound


def alert(x, y, w, h, smooth_lines):
    lx1 = smooth_lines[0][0]
    ly1 = smooth_lines[0][1]
    lx2 = smooth_lines[0][2]
    ly2 = smooth_lines[0][3]
    rx1 = smooth_lines[1][0]
    ry1 = smooth_lines[1][1]
    rx2 = smooth_lines[1][2]
    ry2 = smooth_lines[1][3]

    flag = 0  # if flag = 1 represents foreign body invasion
    if (rx2 - rx1) * (y - ry1) - (ry2 - ry1) * (x - rx1) <= 0 and (lx2 - lx1) * (
        y - ly1
    ) - (ly2 - ly1) * (x - lx1) >= 0:
        # print("left-top wrong")
        flag = 1
    if (rx2 - rx1) * ((y + h) - ry1) - (ry2 - ry1) * (x - rx1) <= 0 and (lx2 - lx1) * (
        (y + h) - ly1
    ) - (ly2 - ly1) * (x - lx1) >= 0:
        # print("left-low wrong")
        flag = 1
    if (rx2 - rx1) * (y - ry1) - (ry2 - ry1) * ((x + w) - rx1) <= 0 and (lx2 - lx1) * (
        y - ly1
    ) - (ly2 - ly1) * ((x + w) - lx1) >= 0:
        # print("right-top wrong")
        flag = 1
    if (rx2 - rx1) * ((y + h) - ry1) - (ry2 - ry1) * ((x + w) - rx1) <= 0 and (
        lx2 - lx1
    ) * ((y + h) - ly1) - (ly2 - ly1) * ((x + w) - lx1) >= 0:
        # print("right-low wrong")
        flag = 1

    if flag == 1:
        winsound.Beep(2222, 111)  # 主板蜂鸣器
        winsound.MessageBeep()  # 喇叭
