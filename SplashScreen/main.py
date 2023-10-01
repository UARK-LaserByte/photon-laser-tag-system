
#creating the splash screen
from kivy.app import App
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.uix.boxlayout import BoxLayout


class SplashScreen(App):

    #loads image
    def build(self):
        layout = BoxLayout(orientation = 'vertical')
        self.image = Image(source = 'logo.jpg')
        layout.add_widget(self.image)

        fade_animation = Animation(opacity=0, duration=3)
        fade_animation.start(self.image)

        return layout


if __name__ == '__main__':
    SplashScreen().run()