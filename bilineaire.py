import numpy as np


def bilinear_resize(image, new_width, new_height):
    src_height, src_width, num_channels = image.shape
    resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)

    for i in range(new_height):
        for j in range(new_width):
            x = (i + 0.5) * (src_height / new_height) - 0.5
            y = (j + 0.5) * (src_width / new_width) - 0.5

            x1 = int(np.floor(x))
            y1 = int(np.floor(y))
            x2 = min(x1 + 1, src_height - 1)
            y2 = min(y1 + 1, src_width - 1)

            a = x - x1
            b = y - y1

            for k in range(num_channels):
                resized_image[i, j, k] = (image[x1, y1, k] * (1 - a) * (1 - b) +
                                          image[x1, y2, k] * (1 - a) * b +
                                          image[x2, y1, k] * a * (1 - b) +
                                          image[x2, y2, k] * a * b)

    return resized_image
