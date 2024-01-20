import numpy as np
import cv2

def nearest_neighbor_resize(image, new_width, new_height):
    old_height, old_width, channels = image.shape
    resized_image = np.zeros((new_height, new_width, channels), np.uint8)

    x_scale = old_width / new_width
    y_scale = old_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            nearest_x = min(old_width - 1, int(x * x_scale))
            nearest_y = min(old_height - 1, int(y * y_scale))
            resized_image[y, x] = image[nearest_y, nearest_x]

    return resized_image
