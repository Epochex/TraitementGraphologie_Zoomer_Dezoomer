import numpy as np
import cv2

#  Algorithme du plus proche voisin non amélioré 
# def nearest_neighbor_resize(image, new_width, new_height):
#     old_height, old_width, channels = image.shape
#     resized_image = np.zeros((new_height, new_width, channels), np.uint8)

#     x_scale = old_width / new_width
#     y_scale = old_height / new_height

#     for y in range(new_height):
#         for x in range(new_width):
#             nearest_x = min(old_width - 1, int(x * x_scale))
#             nearest_y = min(old_height - 1, int(y * y_scale))
#             resized_image[y, x] = image[nearest_y, nearest_x]

#     return resized_image

#Code après application du flou gaussien pour le lissage
# import numpy as np
# import cv2

# def nearest_neighbor_resize(image, new_width, new_height):
#     old_height, old_width, channels = image.shape
#     resized_image = np.zeros((new_height, new_width, channels), np.uint8)

#     x_scale = old_width / new_width
#     y_scale = old_height / new_height

#     for y in range(new_height):
#         for x in range(new_width):
#             nearest_x = min(old_width - 1, int(x * x_scale))
#             nearest_y = min(old_height - 1, int(y * y_scale))
#             resized_image[y, x] = image[nearest_y, nearest_x]

#     # Post-traitement : application du flou gaussien pour le lissage
#     #Utilisé pour appliquer un flou gaussien à l'image redimensionnée après un zoom. La taille du noyau du flou gaussien est fixée à (5, 5), 
#     #ce qui signifie qu'une zone de 5x5 est utilisée pour calculer la moyenne pondérée gaussienne pour chaque pixel, 
#     # et 0 signifie qu'OpenCV calculera automatiquement l'écart-type de la fonction gaussienne à partir de la taille du noyau.
#     resized_image = cv2.GaussianBlur(resized_image, (5, 5), 0)

#     return resized_image

# Code amélioré pour l'application du filtrage bilatéral
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

    # Post-traitement : application d'un filtrage bilatéral pour le lissage des bords.
    d = 5  # diamètre du quartier
    sigmaColor = 25  # Variance standard de l'espace couleur
    sigmaSpace = 25  # Variance standard dans l'espace des coordonnées
    resized_image = cv2.bilateralFilter(resized_image, d, sigmaColor, sigmaSpace)

    return resized_image





