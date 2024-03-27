import numpy as np
import math
from scipy.ndimage import median_filter




def bilinear_resize(image, new_width, new_height):
    src_height, src_width, num_channels = image.shape
    # 对原始图像进行边缘扩展
    extended_image = np.pad(image, ((1, 1), (1, 1), (0, 0)), 'edge')
    # 调整扩展后图像的高度和宽度
    ext_height, ext_width, _ = extended_image.shape

    resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
    scale_w = src_width / new_width
    scale_h = src_height / new_height

    for i in range(new_height):
        for j in range(new_width):
            # 由于进行了边缘扩展，源坐标需要加1以偏移到正确的位置
            src_x = j * scale_w + 1
            src_y = i * scale_h + 1
            src_x_int = math.floor(src_x)
            src_y_int = math.floor(src_y)
            src_x_float = src_x - src_x_int
            src_y_float = src_y - src_y_int

            # 边界处理现在可以通过扩展的图像进行，不再需要特殊考虑边界条件
            for k in range(num_channels):
                value = (1. - src_y_float) * (1. - src_x_float) * extended_image[src_y_int, src_x_int, k] + \
                        (1. - src_y_float) * src_x_float * extended_image[src_y_int, src_x_int + 1, k] + \
                        src_y_float * (1. - src_x_float) * extended_image[src_y_int + 1, src_x_int, k] + \
                        src_y_float * src_x_float * extended_image[src_y_int + 1, src_x_int + 1, k]
                resized_image[i, j, k] = value

    return resized_image




# def bilinear_resize(image, new_width, new_height, filter_size=3):
#     # 对原始图像应用中值滤波进行去噪
#     image_denoised = median_filter(image, size=filter_size)

#     src_height, src_width, num_channels = image_denoised.shape
#     # 对去噪后的图像进行边缘扩展
#     extended_image = np.pad(image_denoised, ((1, 1), (1, 1), (0, 0)), 'edge')
#     ext_height, ext_width, _ = extended_image.shape

#     resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
#     scale_w = src_width / new_width
#     scale_h = src_height / new_height

#     for i in range(new_height):
#         for j in range(new_width):
#             src_x = j * scale_w + 1  # 加1是因为边缘扩展后原点偏移
#             src_y = i * scale_h + 1
#             src_x_int = math.floor(src_x)
#             src_y_int = math.floor(src_y)
#             src_x_float = src_x - src_x_int
#             src_y_float = src_y - src_y_int

#             for k in range(num_channels):
#                 value = (1. - src_y_float) * (1. - src_x_float) * extended_image[src_y_int, src_x_int, k] + \
#                         (1. - src_y_float) * src_x_float * extended_image[src_y_int, src_x_int + 1, k] + \
#                         src_y_float * (1. - src_x_float) * extended_image[src_y_int + 1, src_x_int, k] + \
#                         src_y_float * src_x_float * extended_image[src_y_int + 1, src_x_int + 1, k]
#                 resized_image[i, j, k] = np.clip(value, 0, 255)  # 确保值在合法范围内

#     return resized_image




# def bilinear_resize(image, new_width, new_height):
#     # 获取原始图像的高度、宽度和通道数
#     src_height, src_width, num_channels = image.shape
    
#     # 创建一个新的图像数组，用于存储调整尺寸后的图像，初始值为0
#     resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
    
#     # 计算宽度和高度的缩放因子
#     scale_w = src_width / new_width
#     scale_h = src_height / new_height

#     # 遍历新图像的每个像素
#     for i in range(new_height):
#         for j in range(new_width):
#             # i：纵坐标y，j：横坐标x
#             # 计算当前像素在原始图像中对应的坐标
#             # 添加0.5的偏移是为了找到像素中心的坐标
#             # src_x = (j + 0.5) * scale_w - 0.5
#             # src_y = (i + 0.5) * scale_h - 0.5
#             src_x = j * scale_w
#             src_y = i * scale_h

#             # 计算源坐标的整数部分，即原始图像中像素的位置
#             # 整数部分的用处：
#             # 定位基准像素：源坐标的整数部分（src_x_int 和 src_y_int）用于确定原始图像中最接近目标像素位置的基准像素点。
#             # 这些基准像素点是参与插值计算的四个像素点中的一个（通常是左上角的那一个）。
#             # 参与邻近像素选择：通过整数部分确定的像素点及其右侧和下方的像素点
#             # （即(src_x_int, src_y_int), (src_x_int + 1, src_y_int), (src_x_int, src_y_int + 1), 和 (src_x_int + 1, src_y_int + 1)）
#             # 是进行双线性插值所需的四个邻近像素点。
#             src_x_int = math.floor(src_x)
#             src_y_int = math.floor(src_y)

#             # 计算源坐标的小数部分，用于计算权重
#             # 小数部分的用处：
#             # 计算权重：源坐标的小数部分（src_x_float 和 src_y_float）表示目标像素位置相对于最近基准像素点的精确偏移量。
#             # 这些小数部分用于计算插值权重，即确定每个邻近像素点对最终插值结果的贡献程度。
#             # 插值计算：小数部分决定了目标像素在水平和垂直方向上与四个基准像素的接近程度，
#             # 进而决定了这些基准像素在最终插值结果中的权重。例如，如果src_x_float 接近 1，
#             # 这意味着目标像素在水平方向上更接近右侧的像素；如果src_y_float 接近 0，这意味着目标像素在垂直方向上更接近上方的像素。
            
#             #目标像素在由最近的四个源像素形成的单元格内的相对位置
#             src_x_float = src_x - src_x_int
#             src_y_float = src_y - src_y_int

#             # 如果计算的坐标超出了原始图像的范围，直接使用边缘的像素值
#             if src_x_int + 1 >= src_width or src_y_int + 1 >= src_height:
#                 resized_image[i, j, :] = image[src_y_int, src_x_int, :]
#                 continue

#             # 遍历每个通道，进行双线性插值
#             for k in range(num_channels):
#                 # 计算四个邻近像素的权重，并根据权重和像素值计算新像素的值
#                 # 权重是基于源坐标的小数部分和相对位置计算的
#                 value = (1. - src_y_float) * (1. - src_x_float) * image[src_y_int, src_x_int, k] + \
#                         (1. - src_y_float) * src_x_float * image[src_y_int, src_x_int + 1, k] + \
#                         src_y_float * (1. - src_x_float) * image[src_y_int + 1, src_x_int, k] + \
#                         src_y_float * src_x_float * image[src_y_int + 1, src_x_int + 1, k]
#                 # 将计算得到的值赋给新图像的对应像素
#                 resized_image[i, j, k] = value

#     # 返回调整尺寸后的图像
#     return resized_image
