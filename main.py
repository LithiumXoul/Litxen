from kivy.app import App
from kivy.graphics import Rectangle,Color,Line,Ellipse
from kivy.graphics.texture import Texture
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
import glob
import audioplayer
import time
import random

#Version 0.02

class Eq_Quiz:
    def __init__(self):
        self.app = App.get_running_app()

    def setup(self):
        self.show_popup('setup')
        self.score = 0
        self.quiz_no = 0
        self.total_quiz_no = 7

    def pause(self):#pause button callback. Pauses and Unpauses
        pause_btn = self.app.root.ids['pause_btn']
        if pause_btn.source == 'icons/resume.png':
            pause_btn.source = 'icons/pause.png'
            try:
                self.aud.unpause()
            except:
                self.aud.play()
        elif pause_btn.source == 'icons/pause.png':
            pause_btn.source = 'icons/resume.png'
            self.aud.pause()

    def raw_audio(self):#plays raw audio
        self.aud.switch_to(0)
        self.raw_audio_btn.current_state = 1
        self.fx_audio_btn.current_state = 0
        self.raw_audio_btn.update_state()
        self.fx_audio_btn.update_state()

    def fx_audio(self):#plats the fx audio
        self.aud.switch_to(1)
        self.raw_audio_btn.current_state = 0
        self.fx_audio_btn.current_state = 1
        self.raw_audio_btn.update_state()
        self.fx_audio_btn.update_state()

    def check_ans(self,ans):

        if self.chances_left == 0:
            return ''

        if int(ans) == self.quiz['correct_option']:
            self.score += self.chances_left
            self.score_label.text = str(self.score)

            self.show_popup('correct')
            self.chances_left = 0
            self.next_btn.source = 'icons/next.png'
            self.next_btn.on_release = self.reload
            

        else:
            self.chances_left -= 1
            if self.chances_left == 2:
                self.chances_left_btn.source = 'icons/chances_left_2.png'
            elif self.chances_left == 1:
                self.chances_left_btn.source = 'icons/chances_left_1.png'
            elif self.chances_left == 0:
                self.chances_left_btn.source = 'icons/chances_left_0.png'
                self.show_popup('wrong')
                self.next_btn.source = 'icons/next.png'
                self.next_btn.on_release = self.reload

    def reload(self,event=''):

        if self.quiz_no >= self.total_quiz_no:
            self.app.root.current = 'eq_finish'
            return ''

        self.show_popup('loading')
        self.quiz = self.generate_quiz()

        self.quiz_no += 1

        self.chances_left = 3
        self.chances_left_btn.source = 'icons/chances_left_3.png'
        self.next_btn.source = 'icons/back.png'
        self.next_btn.on_release = self.goto_menu
        self.gain_label.text = str(self.quiz['gain']) + ' db'
        self.band_label.text = str(self.quiz['band']) + ' band'
        self.quiz_label.text = str(self.quiz_no) + ' of ' + str(self.total_quiz_no)

        try:
            self.aud.unload()
        except:
            pass

        self.aud = audioplayer.AudioPlayer(self.quiz['song'])  
        self.aud.equo(self.quiz['correct_option'],self.quiz['gain'],band=self.quiz['band'])

        self.ans_btn_1.text = str(self.quiz['all_options'][0])
        self.ans_btn_2.text = str(self.quiz['all_options'][1])
        self.ans_btn_3.text = str(self.quiz['all_options'][2])
        self.ans_btn_4.text = str(self.quiz['all_options'][3])

        pause_btn = self.app.root.ids['pause_btn']
        pause_btn.source = 'icons/resume.png'

    def generate_quiz(self):
        song = random.choice(glob.glob('loops/*.wav'))

        freq_difference = 300
        start_freq = random.randint(200,1800-(freq_difference*4))

        all_options = [start_freq,start_freq+freq_difference,start_freq+(freq_difference*2),start_freq+(freq_difference*3)]
        correct_option = random.choice(all_options)

        try:#Becuase user might not choose the any options from the dropdown. In that case default
            band = self.band_input
        except:
            band = 300
        try:
            gain = self.gain_input
        except:
            gain = 6

        while (correct_option - band < 0) or (correct_option + band > 2000):
            band -= 50

        return {'song':song,'all_options':all_options,'band':band,'gain':gain,'correct_option':correct_option}

    def goto_menu(self):
        self.aud.unload()
        self.app.root.current = 'menu'

    def setup_screen(self,event=''):

        self.app.root.current = 'eq_quiz'

        self.raw_audio_btn = self.app.root.ids['raw_audio_btn']
        self.fx_audio_btn = self.app.root.ids['fx_audio_btn']

        self.ans_btn_1 = self.app.root.ids['ans_btn_1']
        self.ans_btn_2 = self.app.root.ids['ans_btn_2']
        self.ans_btn_3 = self.app.root.ids['ans_btn_3']
        self.ans_btn_4 = self.app.root.ids['ans_btn_4']

        self.chances_left_btn = self.app.root.ids['chances_left_btn']
        self.next_btn = self.app.root.ids['next_btn']

        self.gain_label = self.app.root.ids['gain_label']
        self.band_label = self.app.root.ids['band_label']
        self.quiz_label = self.app.root.ids['quiz_label']
        self.score_label = self.app.root.ids['score_label']

        self.score_label.text = str(self.score)

        self.raw_audio_btn.current_state = 1
        self.fx_audio_btn.current_state = 0

        self.reload()

    def change_band(self,band):
        self.band_input = band
        self.band_dropdown_btn.text = str(band)

    def change_gain(self,gain):
        self.gain_input = gain
        self.gain_dropdown_btn.text = str(gain)

    def show_popup(self,command):
        if command == 'wrong':
            root_content = BoxLayout(orientation="vertical")
            l = Label(text='Wrong :( Answer: ' + str(self.quiz['correct_option']))
            b1 = ChonkyButton(text='Next')
            b2 = ChonkyButton(text='Keep Listening')
            root_content.add_widget(l)
            root_content.add_widget(b1)
            root_content.add_widget(b2)

            popup = Popup(title='Wrong',
                content=root_content,
                size_hint=(0.4, 0.4),auto_dismiss=False)
            popup.open()

            b1.bind(on_release=self.reload,on_press=popup.dismiss)
            b2.bind(on_release=popup.dismiss)

        elif command == 'correct':
            root_content = BoxLayout(orientation="vertical")
            l = Label(text='That is correct!')
            b1 = ChonkyButton(text='Next')
            b2 = ChonkyButton(text='Keep Listening')
            root_content.add_widget(l)
            root_content.add_widget(b1)
            root_content.add_widget(b2)

            popup = Popup(title='correct!',
                content=root_content,
                size_hint=(0.4, 0.4),auto_dismiss=False)
            popup.open()

            b1.bind(on_release=self.reload,on_press=popup.dismiss)
            b2.bind(on_release=popup.dismiss)

        elif command == 'loading':
            popup = Popup(title='Loading!',
            content=Label(text='Loading the next quiz'),
            size_hint=(0.4, 0.4),auto_dismiss=False)
            popup.open()
            Clock.schedule_once(popup.dismiss, 2)

        elif command == 'setup':

            ##THE SETUP POPUP
            root_content = BoxLayout(orientation="vertical")
            #THIS PART CONTAINS CODE FOR BAND OPTION DROP DONW. RIP TO MY CLEAN CODING
            band_dropdown = DropDown(dismiss_on_select=True)
            self.band_dropdown_btn = ChonkyButton(text='Band')

            band_dropdown_b1 = Button(text='300',size_hint_y=None,height=30)
            band_dropdown_b2 = Button(text='400',size_hint_y=None,height=30)
            band_dropdown_b3 = Button(text='500',size_hint_y=None,height=30)

            band_dropdown_b1.bind(on_press=lambda instance: self.change_band(300),on_release=band_dropdown.dismiss)
            band_dropdown_b2.bind(on_press=lambda instance: self.change_band(400),on_release=band_dropdown.dismiss)
            band_dropdown_b3.bind(on_press=lambda instance: self.change_band(500),on_release=band_dropdown.dismiss)

            band_dropdown.add_widget(band_dropdown_b1)
            band_dropdown.add_widget(band_dropdown_b2)
            band_dropdown.add_widget(band_dropdown_b3)

            self.band_dropdown_btn.bind(on_release=band_dropdown.open)

            band_dropdown.bind(on_select = lambda instance, x: setattr(self.band_dropdown_btn, 'text', x))

            #THIS PART CONTAINS CODE FOR GAIN OPTION DROP DOWN. RIP TO MY CLEAN CODING

            gain_dropdown = DropDown()
            self.gain_dropdown_btn = ChonkyButton(text='Gain')

            gain_dropdown_b1 = Button(text='3db',size_hint_y=None,height=30)
            gain_dropdown_b2 = Button(text='6db',size_hint_y=None,height=30)
            gain_dropdown_b3 = Button(text='12db',size_hint_y=None,height=30)
            gain_dropdown_b4 = Button(text='18db',size_hint_y=None,height=30)

            gain_dropdown_b1.bind(on_press=lambda instance: self.change_gain(3),on_release=gain_dropdown.dismiss)
            gain_dropdown_b2.bind(on_press=lambda instance: self.change_gain(6),on_release=gain_dropdown.dismiss)
            gain_dropdown_b3.bind(on_press=lambda instance: self.change_gain(12),on_release=gain_dropdown.dismiss)
            gain_dropdown_b4.bind(on_press=lambda instance: self.change_gain(18),on_release=gain_dropdown.dismiss)

            gain_dropdown.add_widget(gain_dropdown_b1)
            gain_dropdown.add_widget(gain_dropdown_b2)
            gain_dropdown.add_widget(gain_dropdown_b3)
            gain_dropdown.add_widget(gain_dropdown_b4)

            self.gain_dropdown_btn.bind(on_release=gain_dropdown.open)

            gain_dropdown.bind(on_select = lambda instance, x: setattr(self.gain_dropdown_btn, 'text', x))

            b_continue = ChonkyButton(text='Continue')

            #FINISH OF THE UNCLEAN

            root_content.add_widget(self.band_dropdown_btn)
            root_content.add_widget(self.gain_dropdown_btn)
            root_content.add_widget(b_continue)

            popup = Popup(title='Eq!',
                content=root_content,
                size_hint=(0.4, 0.4))
            popup.open()

            b_continue.bind(on_release=self.setup_screen,on_press=popup.dismiss)

        else:
            popup = Popup(title='Coming soon!',
            content=Label(text='This feature is not yet added. Sorry :(('),
            size_hint=(0.4, 0.4))
            popup.open()
            Clock.schedule_once(popup.dismiss, 4)

class Low_Eq_Quiz:
    def __init__(self):
        self.app = App.get_running_app()

    def reload(self):
        self.app.root.show_popup()

    def setup(self):
        self.show_popup()

    def show_popup(self,command='sorry'):
        if command == 'sorry':
            popup = Popup(title='Coming soon!',
                content=Label(text='This feature is not yet added. Sorry :(('),
                size_hint=(0.4, 0.4))
            popup.open()
            Clock.schedule_once(popup.dismiss, 4)

class Comp_Quiz:
    def __init__(self):
        self.app = App.get_running_app()

    def reload(self):
        self.app.root.show_popup()

    def setup(self):
        self.show_popup()

    def show_popup(self,command='sorry'):
        if command == 'sorry':
            popup = Popup(title='Coming soon!',
                content=Label(text='This feature is not yet added. Sorry :(('),
                size_hint=(0.4, 0.4))
            popup.open()
            Clock.schedule_once(popup.dismiss, 4)

class Reverb_Quiz:
    def __init__(self):
        self.app = App.get_running_app()

    def reload(self):
        self.app.root.show_popup()

    def setup(self):
        self.show_popup()

    def show_popup(self,command='sorry'):
        if command == 'sorry':
            popup = Popup(title='Coming soon!',
                content=Label(text='This feature is not yet added. Sorry :(('),
                size_hint=(0.4, 0.4))
            popup.open()
            Clock.schedule_once(popup.dismiss, 4)

class StatusBar(BoxLayout):
    #Thanks to u/xmzhang from r/kivy for this class code

    def __init__(self, **args):
        super(StatusBar, self).__init__(**args)
        self.texture = Texture.create(size=(2, 2), colorfmt='rgba')
        p1_color = [0, 0, 0, 0]
        p2_color = [0, 0, 0, 0]
        p3_color = [0, 0, 0, 100]
        p4_color = [0, 0, 0, 100]
        p = p1_color + p2_color + p3_color + p4_color
        buf = bytes(p)
        self.texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        with self.canvas:
            self.rect = Rectangle(pos=self.pos, size=self.size, texture=self.texture)

        self.bind(size=self.update_rect)
        self.bind(pos=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

class ChonkyButton(ButtonBehavior,Label):
    def __init__(self,**kwargs):
        super(ChonkyButton,self).__init__(**kwargs)

        self.draw_canvas()
    def draw_canvas(self,**kwargs):
        rect_color = get_color_from_hex('#181d27')
        with self.canvas.before:
            Color(*rect_color)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        self.bind(pos=self.update_canvas_bind,
                  size=self.update_canvas_bind)

    def update_canvas_bind(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size
        
    def on_touch_down(self,touch):
        if self.collide_point(*touch.pos):
            rect_color = get_color_from_hex('#11151c')
            with self.canvas.before:
                Color(*rect_color)
                self.rect = Rectangle(size=self.size,pos=self.pos)
        super(ChonkyButton,self).on_touch_down(touch)

    def on_touch_up(self,touch):
        rect_color = get_color_from_hex('#181d27')
        with self.canvas.before:
            Color(*rect_color)
            self.rect = Rectangle(size=self.size,pos=self.pos)
        super(ChonkyButton,self).on_touch_up(touch)

class SwitchButton(ButtonBehavior, Label):
    def __init__(self,**kwargs):
        super(SwitchButton,self).__init__(**kwargs)

        self.current_state = 0
        self.draw_canvas()
    def draw_canvas(self,**kwargs):
        rect_color = get_color_from_hex('#181d27')
        line_color = get_color_from_hex('#3a7d44')
        with self.canvas.before:
            Color(*rect_color)
            self.rect = Rectangle(size=self.size,pos=self.pos)
            Color(*line_color)
            self.line = Line(points=[self.pos[0],self.pos[1],self.size[0],self.pos[1]])

        self.bind(pos=self.update_canvas_bind,
                  size=self.update_canvas_bind)

    def update_canvas_bind(self, instance, value):
        self.rect.pos = (self.pos[0],self.pos[1])
        self.rect.size = (self.size[0],self.size[1])
        self.line.points = [self.pos[0],self.pos[1],self.pos[0] + self.size[0],self.pos[1]]
        self.update_state()

    def update_state(self):
        if self.current_state == 0:
            self.line.width = 1
            self.canvas.after.clear()
            circle_color = get_color_from_hex('#2a5b31')
            with self.canvas.after:
                Color(*circle_color)
                self.circle = Ellipse(pos=(((self.pos[0] + self.size[0]) - 20) , (self.pos[1] + (self.size[1] / 2) - 5)),size=(10,10))

        elif self.current_state == 1:
            self.line.width = 2
            self.canvas.after.clear()
            circle_color = get_color_from_hex('#3a7d44')
            with self.canvas.after:
                Color(*circle_color)
                self.circle = Ellipse(pos=(((self.pos[0] + self.size[0]) - 20) , (self.pos[1] + (self.size[1] / 2) - 5)),size=(10,10))

class ImageButton(ButtonBehavior, Image):
    pass

class RootWidget(ScreenManager):
    def __init__(self,**kwargs):
        super(RootWidget,self).__init__(**kwargs)
        self.eq = Eq_Quiz()
        self.low_eq = Low_Eq_Quiz()
        self.comp = Comp_Quiz()
        self.reverb = Reverb_Quiz()

    def show_popup(self,command=''):

        if command == 'credits':
            popup = Popup(title='Made by LithiumXoul!',
            content=Label(text='https://soundcloud.com/lithium_xoul\nAll music used here are CC0'),
            size_hint=(0.4, 0.4))
            popup.open()
            

class litxen(App):
    def build(self):
        return RootWidget()

litxen().run()