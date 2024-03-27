
import numpy as np
import cv2

def hermite_interpolate(p0, p1, p2, p3, t):
    # Convertit les points d'entrée en nombres à virgule flottante pour garantir la précision des opérations arithmétiques.
    p0, p1, p2, p3 = map(float, [p0, p1, p2, p3])
    
    # Calculer la pente de la tangente, qui est la dérivée de premier ordre de l'interpolation. Ici, elle est estimée à l'aide des points voisins.
    m0 = (p2 - p0) / 2  # dérivé
    m1 = (p3 - p1) / 2  # dérivée
    
    # Calcul des coefficients polynomiaux
    a = 2 * (p1 - p2) + m0 + m1
    b = -3 * (p1 - p2) - 2 * m0 - m1
    c = m0
    d = p1
    
    # En fonction de la valeur de t (entre 0 et 1), la valeur du point interpolé est calculée et renvoyée.
    return a * t**3 + b * t**2 + c * t + d


def hermite_resize(image, new_width, new_height):
    
    old_height, old_width, channels = image.shape
    
    # Convertit le type de données de l'image en float32 pour les calculs.
    image = image.astype(np.float32)
    
    # Crée un nouveau tableau d'images pour stocker les images redimensionnées.
    resized_image = np.zeros((new_height, new_width, channels), np.float32)

    # Itérer à travers chaque pixel de la nouvelle image.
    for y in range(new_height):
        for x in range(new_width):
            # Calculer les coordonnées (gx, gy) dans l'image originale correspondant aux nouvelles coordonnées (x, y).
            gx = x / (new_width / old_width)
            gy = y / (new_height / old_height)
            gxi = int(gx)  
            gyi = int(gy)  

            # L'interpolation est effectuée pour chaque canal de couleur.
            for channel in range(channels):
                # Sélectionnez les quatre points à utiliser pour l'interpolation. Pour éviter les tableaux hors limites, limitez les index à l'aide des fonctions max et min
                p0 = image[max(gyi - 1, 0), max(gxi - 1, 0), channel]
                p1 = image[gyi, gxi, channel]
                p2 = image[min(gyi + 1, old_height - 1), min(gxi + 1, old_width - 1), channel]
                p3 = image[min(gyi + 2, old_height - 1), min(gxi + 2, old_width - 1), channel]

                # Utiliser l'interpolation Hermite pour calculer la valeur de la couleur à la position actuelle.
                c = hermite_interpolate(p0, p1, p2, p3, gy - gyi)
                resized_image[y, x, channel] = c

    # Récolte les valeurs à virgule flottante dans la plage 0-255 et les convertit en uint8 pour correspondre au format standard des données d'image.
    resized_image = np.clip(resized_image, 0, 255).astype(np.uint8)

    return resized_image


