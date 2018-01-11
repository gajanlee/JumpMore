from func import *
from func.utils import *

screenshot_name = "autojump.png"
screenshot_loc = "/sdcard/" + screenshot_name
def screenshot():
    os.system("adb shell screencap -p " + screenshot_loc)

def pull_screenshot():
    os.system("adb pull " + screenshot_loc + " .")
    return Image.open(screenshot_name)

swipe_x1, swipe_y1, swipe_x2, swipe_y2 = 0, 0, 0, 0
def get_swipe_button():
    while swipe_x1 == 0:
        set_swipe_button()
    return swipe_x1, swipe_y1, swipe_x2, swipe_y2

def set_swipe_button():
    global swipe_x1, swipe_y1, swipe_x2, swipe_y2
    img = pull_screenshot()
    w, h = img.size
    swipe_x1, swipe_x2 = int(w / 2), int(w / 2)
    swipe_y1, swipe_y2 = int(1584 / 1920 * h), int(1584 / 1920 * h)



press_coefficient = 1.70
adjust = False

def adjust_press_coefficient():
    global adjust
    if adjust:
        return
    res = input("far(1) or near(0)?")
    global  press_coefficient
    if res == "1":
        press_coefficient = 0.90 * press_coefficient
    elif res == "0":
        press_coefficient = 1.10 * press_coefficient
    elif res == "2":
        adjust = True


def jump(distance):
    print(press_coefficient, distance)
    x1, y1, x2, y2 = get_swipe_button()
    press_time = int( max(distance * press_coefficient, 200))
    cmd = "adb shell input swipe {x1} {y1} {x2} {y2} {duration}".format(
        x1 = x1, y1 = y1, x2 = x2, y2 = y2,
        duration = press_time
    )
    os.system(cmd)
    print(cmd)

piece_body_width = 70

def find_points_in_board(img):
    w, h = img.size
    img_pixel = img.load()
    draw = ImageDraw.Draw(img)
    #  循环查找线
    scan_y = 0
    for i in range(int(h / 3), int(h * 2 / 3), int(h / 60)):
        last_pixel = img_pixel[0, i]
        for j in range(1, w):
            if img_pixel[j, i] != last_pixel:
                scan_y = i - int(h / 60)
                break
        if scan_y:
            break
    #draw.line((0,scan_y, w, scan_y), fill=(255, 0, 0), width=10)

    piece_xs = []
    piece_ys = []
    for i in range(scan_y, int(h * 2/ 3)):
        for j in range(1, w):
            pixel = img_pixel[j, i]
            if (50 < pixel[0] < 60) \
                    and (53 < pixel[1] < 63) \
                    and (95 < pixel[2] < 110):
                piece_xs.append(j)
                piece_ys.append(i)
                draw.point((j, i), fill=(255, 0, 0))

    board_xs = []
    board_ys = []
    # MAY BE BUG
    piece_x = avg(piece_xs)
    piece_y = avg(piece_ys)
    board_start_x, board_end_x = (avg(piece_xs), w) if avg(piece_xs) < w / 2 else (0, avg(piece_xs))

    background_pixel = img_pixel[w-1, h-1]
    board_x_sum = 0
    board_x_c = 0
    board_x = 0
    for i in range(scan_y, int(h * 2 / 3)):
        last_pixel = img_pixel[0, i]
        if board_x:
            break

        for j in range(int(board_start_x), int(board_end_x)):
            pixel = img_pixel[j, i]
            # 修掉脑袋比下一个小格子还高的情况的 bug
            if abs(j - piece_x) < piece_body_width:
                continue

            # 修掉圆顶的时候一条线导致的小 bug，这个颜色判断应该 OK，暂时不提出来
            # 找到与这一行颜色有差别的点
            if abs(pixel[0] - last_pixel[0]) \
                    + abs(pixel[1] - last_pixel[1]) \
                    + abs(pixel[2] - last_pixel[2]) > 10:
                board_x_sum += j
                board_x_c += 1
        if board_x_sum:
            board_x = board_x_sum / board_x_c

    # 从下向上找于这个方块颜色差距不大的点
    last_pixel = img_pixel[board_x, i]
    for k in range(i + 274, i, -1):  # 274 取开局时最大的方块的上下顶点距离
        pixel = img_pixel[board_x, k]
        if abs(pixel[0] - last_pixel[0]) \
                + abs(pixel[1] - last_pixel[1]) \
                + abs(pixel[2] - last_pixel[2]) < 10:   # 通过调整这个参数来调节木块等多色块
            break
    board_y = int((i + k) / 2)
    draw.line((0, board_y, w, board_y), fill=(255, 0, 0), width=10)
    draw.line((board_x, 0, board_x, h), fill=(255, 0, 0), width=10)
    #draw.line((board_x, 0, board_x, h), fill=(255, 0, 0), width=10)

    last_pixel = img_pixel[board_x, i]

    draw.line((0, avg(piece_ys), w, avg(piece_ys)), fill=(255, 0, 0), width=10)
    draw.line((avg(piece_xs),0, avg(piece_xs),h), fill=(255, 0, 0), width=10)

    del draw
    plt.imshow(img)
    #plt.show()
    print(w, h)
    img.close()
    return piece_x, piece_y, board_x, board_y

def avg(nums):
    return 0 if len(nums) == 0 else functools.reduce(add, nums, 0) / len(nums)

def avg2(num):
    count = 0
    def avg_inline(num):
        nonlocal count
        count += 1
        return num / count
    return avg_inline(num)



def run():
    screenshot()
    img = pull_screenshot()
    jump(distance(find_points_in_board(img)))

if __name__ == "__main__":
    set_swipe_button()
    while True:
        run()
        #adjust_press_coefficient()
        time.sleep(random.uniform(1.2, 1.5))
