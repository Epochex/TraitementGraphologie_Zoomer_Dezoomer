import numpy as np
import math
from scipy.ndimage import median_filter

# La méthode d'interpolation bilinéaire la plus élémentaire pour le traitement des déflations d'images
# def bilinear_resize(image, new_width, new_height):
#     src_height, src_width, num_channels = image.shape
#     resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
#     scale_w = src_width / new_width
#     scale_h = src_height / new_height

#     for i in range(new_height):
#         for j in range(new_width):
#             src_x = j * scale_w
#             src_y = i * scale_h
#             src_x_int = math.floor(src_x)
#             src_y_int = math.floor(src_y)
#             src_x_float = src_x - src_x_int
#             src_y_float = src_y - src_y_int

#             if src_x_int + 1 >= src_width or src_y_int + 1 >= src_height:
#                 resized_image[i, j, :] = image[src_y_int, src_x_int, :]
#                 continue

#             for k in range(num_channels):
#                 value = (1. - src_y_float) * (1. - src_x_float) * image[src_y_int, src_x_int, k] + \
#                         (1. - src_y_float) * src_x_float * image[src_y_int, src_x_int + 1, k] + \
#                         src_y_float * (1. - src_x_float) * image[src_y_int + 1, src_x_int, k] + \
#                         src_y_float * src_x_float * image[src_y_int + 1, src_x_int + 1, k]
#                 resized_image[i, j, k] = value

#     return resized_image


# #Ajout du code amélioré pour le traitement des bords
# def bilinear_resize(image, new_width, new_height):
#     src_height, src_width, num_channels = image.shape
#     # Effectuer une expansion des contours sur l'image originale
#     extended_image = np.pad(image, ((1, 1), (1, 1), (0, 0)), 'edge')
#     # Ajuster la hauteur et la largeur de l'image développée
#     ext_height, ext_width, _ = extended_image.shape

#     resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
#     scale_w = src_width / new_width
#     scale_h = src_height / new_height

#     for i in range(new_height):
#         for j in range(new_width):
#             # En raison de l'expansion des bords, 
#             # les coordonnées de la source doivent être additionnées de 1 pour être décalées vers la position correcte.
#             src_x = j * scale_w + 1
#             src_y = i * scale_h + 1
#             src_x_int = math.floor(src_x)
#             src_y_int = math.floor(src_y)
#             src_x_float = src_x - src_x_int
#             src_y_float = src_y - src_y_int

#             # Le traitement des limites peut désormais être effectué 
#             # avec des images étendues et ne nécessite plus une prise en compte particulière des conditions limites.
#             for k in range(num_channels):
#                 value = (1. - src_y_float) * (1. - src_x_float) * extended_image[src_y_int, src_x_int, k] + \
#                         (1. - src_y_float) * src_x_float * extended_image[src_y_int, src_x_int + 1, k] + \
#                         src_y_float * (1. - src_x_float) * extended_image[src_y_int + 1, src_x_int, k] + \
#                         src_y_float * src_x_float * extended_image[src_y_int + 1, src_x_int + 1, k]
#                 resized_image[i, j, k] = value

#     return resized_image



# Méthode d'amélioration par l'ajout d'une expansion des bords et d'un filtrage médian
import numpy as np
import math
from scipy.ndimage import median_filter

def bilinear_resize(image, new_width, new_height, filter_size=3):
    # Appliquer le filtre médian à l'image originale pour la débruiter
    image_denoised = median_filter(image, size=filter_size)

    src_height, src_width, num_channels = image_denoised.shape
    # Expansion des bords des images débruitées
    extended_image = np.pad(image_denoised, ((1, 1), (1, 1), (0, 0)), 'edge')

    resized_image = np.zeros((new_height, new_width, num_channels), dtype=np.uint8)
    scale_w = src_width / new_width
    scale_h = src_height / new_height

    for i in range(new_height):
        for j in range(new_width):
            src_x = j * scale_w + 1  # Plus 1 car l'origine est décalée après l'expansion des bords
            src_y = i * scale_h + 1
            src_x_int = math.floor(src_x)
            src_y_int = math.floor(src_y)
            src_x_float = src_x - src_x_int
            src_y_float = src_y - src_y_int

            for k in range(num_channels):
                value = (1. - src_y_float) * (1. - src_x_float) * extended_image[src_y_int, src_x_int, k] + \
                        (1. - src_y_float) * src_x_float * extended_image[src_y_int, src_x_int + 1, k] + \
                        src_y_float * (1. - src_x_float) * extended_image[src_y_int + 1, src_x_int, k] + \
                        src_y_float * src_x_float * extended_image[src_y_int + 1, src_x_int + 1, k]
                resized_image[i, j, k] = np.clip(value, 0, 255)  # S'assurer que les valeurs se situent dans les limites légales

    return resized_image




