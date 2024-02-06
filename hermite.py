# import numpy as np
# import cv2

# def hermite_interpolate(p0, p1, p2, p3, t):
#     """计算Hermite插值"""
#     m0 = (p2 - p0) / 2
#     m1 = (p3 - p1) / 2
#     a = 2 * (p1 - p2) + m0 + m1
#     b = -3 * (p1 - p2) - 2 * m0 - m1
#     c = m0
#     d = p1
#     return a * t**3 + b * t**2 + c * t + d

# def hermite_resize(image, new_width, new_height):
#     """使用Hermite插值法调整图像大小"""
#     old_height, old_width, channels = image.shape
#     resized_image = np.zeros((new_height, new_width, channels), np.uint8)

#     for y in range(new_height):
#         for x in range(new_width):
#             # 计算对应于旧图像中的坐标
#             gx = x / (new_width / old_width)
#             gy = y / (new_height / old_height)
#             gxi = int(gx)
#             gyi = int(gy)

#             # 计算插值像素
#             # 初始化一个用于存储插值后颜色值的数组，这里的 '3' 对应于图像的三个颜色通道（例如，RGB）
#             c = np.zeros(3)

#             # 遍历所有颜色通道（对于RGB图像，这将是0, 1, 2）
#             for channel in range(channels):
#                 # 为了进行Hermite插值，我们需要四个点。在这里，我们计算这四个点的坐标。
#                 # p0, p1, p2, p3分别代表这四个点。
#                 # 为了避免越界错误（即访问图像外的像素），我们使用max和min函数来限制坐标值。

#                 # p0是当前插值点前一个像素的位置
#                 p0 = image[max(gyi - 1, 0), max(gxi - 1, 0), channel]
                
#                 # p1是当前插值点的位置
#                 p1 = image[gyi, gxi, channel]
                
#                 # p2是当前插值点后一个像素的位置
#                 p2 = image[min(gyi + 1, old_height - 1), min(gxi + 1, old_width - 1), channel]
                
#                 # p3是当前插值点后两个像素的位置
#                 p3 = image[min(gyi + 2, old_height - 1), min(gxi + 2, old_width - 1), channel]

#                 # 使用Hermite插值函数计算插值点的颜色值。
#                 # 'gy - gyi' 是一个在0和1之间的小数，表示插值点在p1和p2之间的相对位置。
#                 c[channel] = hermite_interpolate(p0, p1, p2, p3, gy - gyi)


#             resized_image[y, x] = np.clip(c, 0, 255)

#     return resized_image


import numpy as np
import cv2

def hermite_interpolate(p0, p1, p2, p3, t):
    # Convert points to float for safe arithmetic operations
    p0, p1, p2, p3 = map(float, [p0, p1, p2, p3])
    m0 = (p2 - p0) / 2
    m1 = (p3 - p1) / 2
    a = 2 * (p1 - p2) + m0 + m1
    b = -3 * (p1 - p2) - 2 * m0 - m1
    c = m0
    d = p1
    return a * t**3 + b * t**2 + c * t + d

def hermite_resize(image, new_width, new_height):
    old_height, old_width, channels = image.shape
    # Convert image to float32 for processing
    image = image.astype(np.float32)
    resized_image = np.zeros((new_height, new_width, channels), np.float32)

    for y in range(new_height):
        for x in range(new_width):
            gx = x / (new_width / old_width)
            gy = y / (new_height / old_height)
            gxi = int(gx)
            gyi = int(gy)

            for channel in range(channels):
                p0 = image[max(gyi - 1, 0), max(gxi - 1, 0), channel]
                p1 = image[gyi, gxi, channel]
                p2 = image[min(gyi + 1, old_height - 1), min(gxi + 1, old_width - 1), channel]
                p3 = image[min(gyi + 2, old_height - 1), min(gxi + 2, old_width - 1), channel]

                c = hermite_interpolate(p0, p1, p2, p3, gy - gyi)
                resized_image[y, x, channel] = c

    # Clip values to range [0, 255] and convert back to uint8
    resized_image = np.clip(resized_image, 0, 255).astype(np.uint8)

    return resized_image

