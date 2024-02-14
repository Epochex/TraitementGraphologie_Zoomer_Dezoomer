
import numpy as np
import cv2

def hermite_interpolate(p0, p1, p2, p3, t):
    # 将输入点转换为浮点数，以确保在算术运算中的准确性。
    p0, p1, p2, p3 = map(float, [p0, p1, p2, p3])
    
    # 计算切线斜率，即插值的一阶导数。这里使用相邻点来估算。
    m0 = (p2 - p0) / 2  # 前导数
    m1 = (p3 - p1) / 2  # 后导数
    
    # 根据Hermite插值的公式，计算多项式系数。
    a = 2 * (p1 - p2) + m0 + m1
    b = -3 * (p1 - p2) - 2 * m0 - m1
    c = m0
    d = p1
    
    # 根据t的值（介于0到1之间），计算并返回插值点的值。
    return a * t**3 + b * t**2 + c * t + d


def hermite_resize(image, new_width, new_height):
    # 获取原图像的高度、宽度和颜色通道数。
    old_height, old_width, channels = image.shape
    
    # 将图像数据类型转换为float32，以便进行计算。
    image = image.astype(np.float32)
    
    # 创建一个新的图像数组，用于存储调整大小后的图像。
    resized_image = np.zeros((new_height, new_width, channels), np.float32)

    # 遍历新图像的每个像素。
    for y in range(new_height):
        for x in range(new_width):
            # 计算新坐标(x, y)对应的原图像中的坐标(gx, gy)。
            gx = x / (new_width / old_width)
            gy = y / (new_height / old_height)
            gxi = int(gx)  # 获取gx的整数部分
            gyi = int(gy)  # 获取gy的整数部分

            # 对每个颜色通道进行插值。
            for channel in range(channels):
                # 选择用于插值的四个点。为避免数组越界，使用max和min函数限制索引。
                p0 = image[max(gyi - 1, 0), max(gxi - 1, 0), channel]
                p1 = image[gyi, gxi, channel]
                p2 = image[min(gyi + 1, old_height - 1), min(gxi + 1, old_width - 1), channel]
                p3 = image[min(gyi + 2, old_height - 1), min(gxi + 2, old_width - 1), channel]

                # 使用Hermite插值计算当前位置的颜色值。
                c = hermite_interpolate(p0, p1, p2, p3, gy - gyi)
                resized_image[y, x, channel] = c

    # 将浮点数值裁剪到0-255范围并转换为uint8，以匹配图像数据的标准格式。
    resized_image = np.clip(resized_image, 0, 255).astype(np.uint8)

    return resized_image


