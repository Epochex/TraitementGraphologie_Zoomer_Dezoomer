import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.core.window import Window
import cv2
from PIL import Image as PILImage
from io import BytesIO
from kivy.graphics.texture import Texture

from interpolation import nearest_neighbor_resize
from bilineaire import bilinear_resize
from hermite import hermite_resize


class ImageResizerApp(App):
    
    def build(self):
        self.title = 'Image Resizer'

        # schéma directeur
        main_layout = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # Disposition à gauche : image originale et bouton d'importation
        left_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # image originale
        self.original_image_widget = Image(size_hint=(1, .9))
        left_layout.add_widget(self.original_image_widget)

        # Bouton d'ajout pour sélectionner un fichier
        open_button = Button(text='Open Image', size_hint=(1, .1), background_color=[0, 1, 0, 1])
        open_button.bind(on_press=self.open_file)
        left_layout.add_widget(open_button)

        # Disposition à droite : boutons de la méthode d'interpolation, cases de saisie de la largeur et de la hauteur et image traitée.
        right_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # Première ligne : Bouton de la méthode d'interpolation
        interpolation_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        # Créer et ajouter des boutons de méthode d'interpolation
        # Modifier la liaison des boutons
        nn_button = Button(text='Nearest Neighbor', background_color=[1, 0, 0, 1])
        nn_button.bind(on_press=self.apply_resize)
        bilinear_button = Button(text='Bilinear', background_color=[0, 1, 0, 1])
        bilinear_button.bind(on_press=self.apply_resize)
        hermite_button = Button(text='Hermite', background_color=[0, 0, 1, 1])
        hermite_button.bind(on_press=self.apply_resize)


        # Ajout de boutons à une mise en page
        for button in [nn_button, bilinear_button, hermite_button]:
            interpolation_layout.add_widget(button)
        
        # Deuxième ligne : champs de saisie de la largeur et de la hauteur
        size_input_layout = BoxLayout(orientation='horizontal', size_hint=(1, .05)) #.05est de modifier la hauteur
        width_label = Label(text='width(X):', size_hint=(.15, 1))  # réduire la largeur
        self.width_input = TextInput(text='200', input_filter='int', size_hint=(.25, 1))  # réduire la largeur
        height_label = Label(text='height(Y):', size_hint=(.15, 1))  # réduire la largeur
        self.height_input = TextInput(text='200', input_filter='int', size_hint=(.25, 1))  # réduire la largeur
        # Ajout de boîtes de saisie de largeur et de hauteur et de leurs étiquettes à la mise en page
        size_input_layout.add_widget(width_label)
        size_input_layout.add_widget(self.width_input)
        size_input_layout.add_widget(height_label)
        size_input_layout.add_widget(self.height_input)

        # Ajout d'images traitées
        self.resized_image_widget = Image(size_hint=(1, .8))
        right_layout.add_widget(self.resized_image_widget)

        # Ajouter deux mises en page horizontales à la mise en page de droite
        right_layout.add_widget(interpolation_layout)
        right_layout.add_widget(size_input_layout)
        

        # Ajouter des mises en page latérales gauche et droite à la mise en page principale
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        return main_layout
    

    def open_file(self, instance):
        user_path = os.path.expanduser('~')  # Obtenir le répertoire personnel de l'utilisateur
        pictures_path = os.path.join(user_path, 'Pictures')  # Supposons que vous souhaitiez ouvrir le catalogue d'images de l'utilisateur

        content = FileChooserListView(path=pictures_path,
                                    filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp'],
                                    on_submit=self.select_image)  # Remplacer par on_submit
        self.popup = Popup(title='Select an image', content=content,
                        size_hint=(0.9, 0.9))
        self.popup.open()

    def select_image(self, filechooser, selection, touch):
        # L'événement on_submit transmet les paramètres du sélecteur de fichiers, de la sélection et du toucher.
        if selection:
            filepath = selection[0]
            print(f"选中的文件: {filepath}")  # Imprime le chemin d'accès au fichier sélectionné
            try:
                self.original_image = cv2.imread(filepath)
                if self.original_image is not None:
                    self.display_image(self.original_image_widget, self.original_image)
                else:
                    print("Impossible de charger l'image, veuillez vérifier le chemin d'accès et le format du fichier")
            except Exception as e:
                print(f"Erreur de chargement ou d'affichage des images: {e}")
            self.popup.dismiss()



    def apply_resize(self, instance):
        if hasattr(self, 'original_image'):
            try:
                new_width = int(self.width_input.text)
                new_height = int(self.height_input.text)
            except ValueError:
                print("Veuillez saisir un numéro valide :( ")
                return

            # Décider de la méthode d'interpolation à utiliser en fonction du texte du bouton
            if instance.text == 'Nearest Neighbor':
                resized_image = nearest_neighbor_resize(self.original_image, new_width, new_height)
            elif instance.text == 'Bilinear':
                resized_image = bilinear_resize(self.original_image, new_width, new_height)
            elif instance.text == 'Hermite':
                resized_image = hermite_resize(self.original_image, new_width, new_height)
            else:
                print("Unkown method")
                return

            self.display_image(self.resized_image_widget, resized_image)


    def display_image(self, widget, image):
        # Conversion des images OpenCV en images PIL
        pil_image = PILImage.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # Conversion des images PIL en textures
        texture = self.pil_to_kivy_texture(pil_image)
        
        # 将纹理分配给Kivy图像小部件Attribution de textures aux widgets d'images Kivy
        widget.texture = texture

    def pil_to_kivy_texture(self, pil_image):
        """ 将PIL图像转换为Kivy纹理 """
        pil_image = pil_image.convert('RGBA')  # Assurez-vous que l'image est en mode RGBA
        pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)  # Retourner l'image verticalement
        data = pil_image.tobytes()
        size = pil_image.size
        
        texture = Texture.create(size=size, colorfmt='rgba')
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        return texture




if __name__ == '__main__':
    ImageResizerApp().run()
