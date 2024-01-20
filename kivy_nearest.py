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

        # 主布局
        main_layout = BoxLayout(orientation='horizontal', padding=5, spacing=5)

        # 左侧布局：原始图像和导入按钮
        left_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # 原始图像
        self.original_image_widget = Image(size_hint=(1, .9))
        left_layout.add_widget(self.original_image_widget)

        # 添加选择文件的按钮
        open_button = Button(text='Open Image', size_hint=(1, .1), background_color=[0, 1, 0, 1])
        open_button.bind(on_press=self.open_file)
        left_layout.add_widget(open_button)

        # 右侧布局：插值方法按钮、宽度和高度输入框及处理后的图像
        right_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)

        # 第一行：插值方法按钮
        interpolation_layout = BoxLayout(orientation='horizontal', size_hint=(1, .1))
        # 创建并添加插值方法按钮
        # 修改按钮的绑定
        nn_button = Button(text='Nearest Neighbor', background_color=[1, 0, 0, 1])
        nn_button.bind(on_press=self.apply_resize)
        bilinear_button = Button(text='Bilinear', background_color=[0, 1, 0, 1])
        bilinear_button.bind(on_press=self.apply_resize)
        hermite_button = Button(text='Hermite', background_color=[0, 0, 1, 1])
        hermite_button.bind(on_press=self.apply_resize)


        # 将按钮添加到布局中
        for button in [nn_button, bilinear_button, hermite_button]:
            interpolation_layout.add_widget(button)
        
        # 第二行：宽度和高度输入框
        size_input_layout = BoxLayout(orientation='horizontal', size_hint=(1, .05)) #.05是修改高度
        width_label = Label(text='width(X):', size_hint=(.15, 1))  # 减小宽度
        self.width_input = TextInput(text='200', input_filter='int', size_hint=(.25, 1))  # 减小宽度
        height_label = Label(text='height(Y):', size_hint=(.15, 1))  # 减小宽度
        self.height_input = TextInput(text='200', input_filter='int', size_hint=(.25, 1))  # 减小宽度
        # 将宽度和高度输入框及其标签添加到布局中
        size_input_layout.add_widget(width_label)
        size_input_layout.add_widget(self.width_input)
        size_input_layout.add_widget(height_label)
        size_input_layout.add_widget(self.height_input)

        # 添加处理后的图像
        self.resized_image_widget = Image(size_hint=(1, .8))
        right_layout.add_widget(self.resized_image_widget)

        # 将两个水平布局添加到右侧布局
        right_layout.add_widget(interpolation_layout)
        right_layout.add_widget(size_input_layout)
        

        # 将左侧和右侧布局添加到主布局中
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        return main_layout
    

    def open_file(self, instance):
        user_path = os.path.expanduser('~')  # 获取用户的主目录
        pictures_path = os.path.join(user_path, 'Pictures')  # 假定你想打开用户的图片目录

        content = FileChooserListView(path=pictures_path,
                                    filters=['*.png', '*.jpg', '*.jpeg', '*.gif', '*.bmp'],
                                    on_submit=self.select_image)  # 改用 on_submit
        self.popup = Popup(title='Select an image', content=content,
                        size_hint=(0.9, 0.9))
        self.popup.open()

    def select_image(self, filechooser, selection, touch):
        # on_submit 事件会传递 filechooser, selection 和 touch 三个参数
        if selection:
            filepath = selection[0]
            print(f"选中的文件: {filepath}")  # 打印选中的文件路径
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

            # 根据按钮的文本来决定使用哪种插值方法
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
        # 将OpenCV图像转换为PIL图像
        pil_image = PILImage.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        
        # 将PIL图像转换为纹理
        texture = self.pil_to_kivy_texture(pil_image)
        
        # 将纹理分配给Kivy图像小部件
        widget.texture = texture

    def pil_to_kivy_texture(self, pil_image):
        """ 将PIL图像转换为Kivy纹理 """
        pil_image = pil_image.convert('RGBA')  # 确保图像是RGBA模式
        pil_image = pil_image.transpose(PILImage.FLIP_TOP_BOTTOM)  # 垂直翻转图像
        data = pil_image.tobytes()
        size = pil_image.size
        
        texture = Texture.create(size=size, colorfmt='rgba')
        texture.blit_buffer(data, colorfmt='rgba', bufferfmt='ubyte')
        return texture




if __name__ == '__main__':
    ImageResizerApp().run()
