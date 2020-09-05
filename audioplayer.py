#Version 4, coolest one yet

from pydub import AudioSegment
from pydub.utils import mediainfo
import pygame
import fx_er

class AudioPlayer:
    def __init__(self,filename,init_channel_number=0):
        self.init_channel_number =init_channel_number #Init with this channel_number
        self.current_playing_channel = 0 #To determine if raw playing or fx playing

        info = mediainfo(filename)
        freq = int(info['sample_rate'])
        chan = int(info['channels'])

        pygame.mixer.pre_init(frequency=freq, size=-16, channels=chan)
        pygame.init()
        pygame.mixer.init()

        self.raw_audio_segment = AudioSegment.from_file(filename)#Audio segment from pydub(then converted to raw for pygame)
        self.fx_audio_segment = self.raw_audio_segment #this audio segment(which is the same) will later be fx_ed with pydub

    def play(self):
        extract_raw = self.raw_audio_segment.raw_data
        extract_fx = self.fx_audio_segment.raw_data
        self.raw_sound = pygame.mixer.Sound(buffer = extract_raw)
        self.fx_sound = pygame.mixer.Sound(buffer = extract_fx)
        self.raw_channel = pygame.mixer.Channel(self.init_channel_number)
        self.fx_channel = pygame.mixer.Channel(self.init_channel_number + 1)

        self.switch_to(self.current_playing_channel)
        self.raw_channel.play(self.raw_sound, loops = -1)
        self.fx_channel.play(self.fx_sound, loops = -1)

    def pause(self):
        self.raw_channel.pause()
        self.fx_channel.pause()

    def unpause(self):
        self.raw_channel.unpause()
        self.fx_channel.unpause()

    def switch_to(self,channel):#0 for raw and 1 for fx
        if channel == 0:
            #Try and except becuase user might switch without playing which
            #wouldn't be able to find self.raw_sound and self.fx_sound

            try:
                self.raw_sound.set_volume(1.0)
                self.fx_sound.set_volume(0.0)
                self.current_playing_channel = 0
            except:
                self.current_playing_channel = 0
        elif channel == 1:
            try:
                self.raw_sound.set_volume(0.0)
                self.fx_sound.set_volume(1.0)
                self.current_playing_channel = 1
            except:
                self.current_playing_channel = 1

    def unload(self):
        pygame.mixer.quit()
        self.raw_audio_segment = None
        self.fx_audio_segment = None

    def equo(self,freq,db,band=100,mod="peak"):
        work_seg = self.raw_audio_segment
        work_seg = fx_er.cheap_eq(work_seg,freq,band,mod,db)
        self.fx_audio_segment = work_seg