from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Rectangle

#from pipe import Pipe

main_widget_kv = """
FloatLayout:
    Background:
        id: background
        canvas.before:
            #Rectangle:
                #size: self.size
                #pos: self.pos
                #source: "sky.png"
            Color:
                rgba: 1, 1, 0, 1
            Rectangle:
                size: self.width, 10
                pos: self.pos[0], self.pos[1] + self.height - 138
                #texture: self.cloud_texture
            
            Color:
                rgba: 1, .3, .8, .5
            Line:
                points: 0,0,110,150 #zip(self.data.x, self.data.y)
            
            #Rectangle:
                #size: self.width, 96
                #pos: self.pos[0], self.pos[1]
                #"texture: self.floor_texture
                
        
    Label:
        id: score
        size_hint_y: None
        height: 96
        text: "0"
        font_size: 40
    Button:
        text: "Start game"
        #background_normal: "transparent.png"
        #background_down: "transparent.png"
        id: start_button
        on_release:
            self.disabled = True
            self.opacity = 0
            app.start_game()
    #Bird:
    #    source: "bird1.png"
     #   size_hint: None, None
      #  size: 46, 34
       # pos: 20, (root.height - 96) / 2.0
        #id: bird
"""

class Background(Widget):
    cloud_texture = ObjectProperty(None)
    floor_texture = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # # Create textures
        # self.cloud_texture = Image(source="cloud.png").texture
        # self.cloud_texture.wrap = 'repeat'
        # self.cloud_texture.uvsize = (Window.width / self.cloud_texture.width, -1)
        #
        # self.floor_texture = Image(source="floor.png").texture
        # self.floor_texture.wrap = 'repeat'
        # self.floor_texture.uvsize = (Window.width / self.floor_texture.width, -1)

    # def on_size(self, *args):
        # self.cloud_texture.uvsize = (self.width / self.cloud_texture.width, -1)
        # self.floor_texture.uvsize = (self.width / self.floor_texture.width, -1)

    # def scroll_textures(self, time_passed):
        # Update the uvpos of the texture
        # self.cloud_texture.uvpos = ( (self.cloud_texture.uvpos[0] + time_passed/2.0)%Window.width , self.cloud_texture.uvpos[1])
        # self.floor_texture.uvpos = ( (self.floor_texture.uvpos[0] + time_passed)%Window.width, self.floor_texture.uvpos[1])

        # # Redraw the texture
        # texture = self.property('cloud_texture')
        # texture.dispatch(self)
        #
        # texture = self.property('floor_texture')
        # texture.dispatch(self)

from random import randint
from kivy.properties import NumericProperty

# class Bird(Image):
#     velocity = NumericProperty(0)
#
#     def on_touch_down(self, touch):
#         self.source = "bird2.png"
#         self.velocity = 150
#         super().on_touch_down(touch)
#
#     def on_touch_up(self, touch):
#         self.source = "bird1.png"
#         super().on_touch_up(touch)



class MainApp(App):

    pipes = []
    GRAVITY = 300
    was_colliding = False

    #def on_start(self):
    #    Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)

    def build(self):
        self.main_widget = Builder.load_string(main_widget_kv)
        return self.main_widget

    def move_bird(self, time_passed):
        bird = self.root.ids.bird
        bird.y = bird.y + bird.velocity * time_passed
        bird.velocity = bird.velocity - self.GRAVITY * time_passed
        self.check_collision()

    def check_collision(self):
        bird = self.root.ids.bird
        # Go through each pipe and check if it collides
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                # Check if bird is between the gap
                if bird.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding

    def game_over(self):
        self.root.ids.bird.pos = (20, (self.root.height - 96) / 2.0)
        for pipe in self.pipes:
            self.root.remove_widget(pipe)
        self.frames.cancel()
        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1


    def next_frame(self, time_passed):
        pass
        # self.move_bird(time_passed)
        #self.move_pipes(time_passed)
        #self.root.ids.background.scroll_textures(time_passed)

    def start_game(self):
        self.root.ids.score.text = "0"
        self.was_colliding = False
        self.pipes = []
        #Clock.schedule_interval(self.move_bird, 1/60.)
        self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

        # # Create the pipes
        # num_pipes = 5
        # distance_between_pipes = Window.width / (num_pipes - 1)
        # for i in range(num_pipes):
        #     pipe = Rectangle()
        #     pipe.pipe_center = randint(96 + 100, self.root.height - 100)
        #     pipe.size_hint = (None, None)
        #     pipe.pos = (Window.width + i*distance_between_pipes, 96)
        #     pipe.size = (64, self.root.height - 96)
        #
        #     self.pipes.append(pipe)
        #     self.root.add_widget(pipe)
        #
        # # Move the pipes
        # #Clock.schedule_interval(self.move_pipes, 1/60.)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Check if we need to reposition the pipe at the right side
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width




if __name__ == "__main__":

    MainApp().run()
