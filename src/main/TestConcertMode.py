import kivy

kivy.require('1.11.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import *

root = Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex

#<SplitterStrip>:
#    border: self.parent.border if self.parent else (3, 3, 3, 3)
#    horizontal: '_h' if self.parent and self.parent.sizable_from[0] in  ('t', 'b') else ''
#    background_normal: '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/Documentation/Logos/Blank.png'
#    background_down: '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/Documentation/Logos/Blank.png'

<SplitterStrip>:
    border: (1, 1, 1, 1) #self.parent.border if self.parent else (3, 3, 3, 3)
    horizontal: '_h' if self.parent and self.parent.sizable_from[0] in  ('t', 'b') else ''

    #Playing around with background properties does not work, so it gets overlayed with stretched white image.
    #background_normal: '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/ToneFlow/img/Blank.png' #'atlas://data/images/defaulttheme/splitter{}{}'.format('_disabled' if self.disabled else '', self.horizontal)
    #background_down: '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/ToneFlow/img/Blank.png' #'atlas://data/images/defaulttheme/splitter_down{}{}'.format('_disabled' if self.disabled else '', self.horizontal)
    Image:
        pos: root.pos
        size: root.size
        allow_stretch: True
        keep_ratio: False
        source: '/home/pieter/THUIS/Programmeren/PYTHON/Projects/ToneFlowProject/ToneFlow/img/WhiteSquare.png' #'atlas://data/images/defaulttheme/splitter_grip' + root.horizontal


BoxLayout:

    id: background
    orientation: 'vertical'

    canvas.before:
        Color:
            rgba: get_color_from_hex('#111111FF')
        Rectangle:
            size: 60, self.height
            pos: self.pos[0], self.pos[1]

        Rectangle:
            size: 60, self.height
            pos: self.pos[0]+90, self.pos[1]

        Rectangle:
            size: 120, self.height
            pos: self.pos[0]+180, self.pos[1]

        Rectangle:
            size: 60, self.height
            pos: self.pos[0]+330, self.pos[1]

        Rectangle:
            size: 60, self.height
            pos: self.pos[0]+420, self.pos[1]

        Rectangle:
            size: 60, self.height
            pos: self.pos[0]+510, self.pos[1]


    Splitter:
        sizable_from: 'bottom'
        max_size: root.height
        min_size: 0 #root.height*0.60
        strip_size: 5
        keep_within_parent: True
        rescale_with_parent: True
        #border: (4, 4, 4, 4)

        BoxLayout:
            orientation: 'vertical'

            Label:
                text: 'Projected score'

                canvas.before:
                    StencilPush:
                    Rectangle:
                        pos: self.pos
                        size: self.width, self.height
                    StencilUse:
                    Color:
                        rgba: 1, 1, 1, 1.0
                    Rectangle:
                        size: self.width, 10.0
                        pos: 0,self.height * 0.20  #self.pos[0], self.pos[1] + self.height - 142
                        #texture: self.cloud_texture

                canvas:           

                    #C
                    Color:
                        rgba: get_color_from_hex('#FC0020FF')
                    RoundedRectangle:
                        size: 60, 160
                        pos: self.pos[0], self.pos[1] -50
                        segments: 15
                        radius: [15]

                    #C#  
                    Color:
                        rgba: get_color_from_hex('#FA6D1EFF')
                    RoundedRectangle:
                        size: 30, 20
                        pos: self.pos[0]+60, self.pos[1] +50
                        segments: 15
                        radius: [15]

                    #D
                    Color:
                        rgba: get_color_from_hex('#F7930AFF')
                    RoundedRectangle:
                        size: 60, 40
                        pos: self.pos[0]+90, self.pos[1]
                        segments: 15
                        radius: [15]

                    #D#  
                    Color:
                        rgba: get_color_from_hex('#FFC000FF')
                    RoundedRectangle:
                        size: 30, 120
                        pos: self.pos[0]+150, self.pos[1] +175
                        segments: 15
                        radius: [15]

                    #E
                    Color:
                        rgba: get_color_from_hex('#FFFE03FF')
                    RoundedRectangle:
                        size: 60, 20
                        pos: self.pos[0]+180, self.pos[1] -75
                        segments: 15
                        radius: [15]

                    #F
                    Color:
                        rgba: get_color_from_hex('#93D250FF')
                    RoundedRectangle:
                        size: 60, 30
                        pos: self.pos[0]+240, self.pos[1] +0
                        segments: 15
                        radius: [15]

                    #F#  
                    Color:
                        rgba: get_color_from_hex('#00AF50FF')
                    RoundedRectangle:
                        size: 30, 40
                        pos: self.pos[0]+300, self.pos[1] +275
                        segments: 15
                        radius: [15]

                    #G
                    Color:
                        rgba: get_color_from_hex('#10A192FF')
                    RoundedRectangle:
                        size: 60, 160
                        pos: self.pos[0]+330, self.pos[1] -25
                        segments: 15
                        radius: [15]

                    #G#  
                    Color:
                        rgba: get_color_from_hex('#0329E4FF')
                    RoundedRectangle:
                        size: 30, 40
                        pos: self.pos[0]+390, self.pos[1] +75
                        segments: 15
                        radius: [15]

                    #A
                    Color:
                        rgba: get_color_from_hex('#7900F1FF')
                    RoundedRectangle:
                        size: 60, 120
                        pos: self.pos[0]+420, self.pos[1] +125
                        segments: 15
                        radius: [15]

                    #A#  
                    Color:
                        rgba: get_color_from_hex('#AF5DFFFF')
                    RoundedRectangle:
                        size: 30, 160
                        pos: self.pos[0]+480, self.pos[1] +50
                        segments: 15
                        radius: [15]

                    #B
                    Color:
                        rgba: get_color_from_hex('#CB00CBFF')
                    RoundedRectangle:
                        size: 60, 20
                        pos: self.pos[0]+510, self.pos[1]
                        segments: 15
                        radius: [15]                        


                canvas.after:                
                    Color:
                        rgba: 0, 0, 0, 1.0
                    Line:
                        width: 1
                        points: 0,self.height * 0.20 +5,self.width,self.height * 0.20 +5 #zip(self.data.x, self.data.y)

                    StencilUnUse:
                    StencilPop:
            #Label:
                #text: 'something2'

    Label:
        text: 'Volume area'

        canvas:

            #C
            Color:
                rgba: get_color_from_hex('#FC0020FF')
            Rectangle:
                size: 60, 0.90 * self.height
                pos: self.pos[0], self.pos[1]

            #C#  
            Color:
                rgba: get_color_from_hex('#FA6D1EFF')
            Rectangle:
                size: 30, 0.05 * self.height
                pos: self.pos[0]+60, self.pos[1]

            #D
            Color:
                rgba: get_color_from_hex('#F7930AFF')
            Rectangle:
                size: 60, 0.15 * self.height
                pos: self.pos[0]+90, self.pos[1]

            #D#  
            Color:
                rgba: get_color_from_hex('#FFC000FF')
            Rectangle:
                size: 30, 0.23 * self.height
                pos: self.pos[0]+150, self.pos[1]

            #E
            Color:
                rgba: get_color_from_hex('#FFFE03FF')
            Rectangle:
                size: 60, 0.80 * self.height
                pos: self.pos[0] +180, self.pos[1]

            #F
            Color:
                rgba: get_color_from_hex('#93D250FF')
            Rectangle:
                size: 60, 0.50 * self.height
                pos: self.pos[0] +240, self.pos[1]

            #F#  
            Color:
                rgba: get_color_from_hex('#00AF50FF')
            Rectangle:
                size: 30, 0.10 * self.height
                pos: self.pos[0]+300, self.pos[1]

            #G
            Color:
                rgba: get_color_from_hex('#10A192FF')
            Rectangle:
                size: 60, 1.0 * self.height
                pos: self.pos[0]+330, self.pos[1]

            #G#  
            Color:
                rgba: get_color_from_hex('#0329E4FF')
            Rectangle:
                size: 30, 0.05 * self.height
                pos: self.pos[0] +390, self.pos[1]

            #A
            Color:
                rgba: get_color_from_hex('#7900F1FF')
            Rectangle:
                size: 60, 1.0 * self.height
                pos: self.pos[0]+420, self.pos[1]

            #A#  
            Color:
                rgba: get_color_from_hex('#AF5DFFFF')
            Rectangle:
                size: 30, 0.25 * self.height
                pos: self.pos[0] +480, self.pos[1]

            #B
            Color:
                rgba: get_color_from_hex('#CB00CBFF')
            Rectangle:
                size: 60, 0.75 * self.height
                pos: self.pos[0]+510, self.pos[1]

    #Button:
        #text: 'Alarm'
''')


class TestApp(App):
    def build(self):
        return root


if __name__ == '__main__':
    testapp = TestApp()

    main_widget = testapp.build()
    #
    # main_widget.ids.add_widget(Rectangle())

    testapp.run()