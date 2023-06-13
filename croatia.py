from soundscape import Soundscape
import random
from pynput import keyboard
import signal
import time
from pydub import AudioSegment
from pydub.effects import normalize
from pydub.playback import play

class Croatia(Soundscape):
    def loadFiles(self):
        self.waves = [AudioSegment.from_file('Sounds/Croatia/Ambience/amb--0%s.wav' % i) for i in range(1,7)]
        self.cicadas = [AudioSegment.from_file('Sounds/Croatia/Ambience/cicadas--0%s.wav' % i) for i in range(1,7)]
        self.horn = AudioSegment.from_file('Sounds/Croatia/Events/Foghorn.wav')
     
    def playAmbience(self):
        if self.exit_flag:
            exit(0)
        def waves():
            while not self.exit_flag:
                waveNum = random.randint(0,5)
                Soundscape.non_blocking_sound(self.waves[waveNum])
                if self.exit_flag:
                    exit(0)
                time.sleep(self.waves[waveNum].duration_seconds*0.8)
        def cicadas():
            while not self.exit_flag:
                num = random.randint(0,5)
                Soundscape.non_blocking_sound(self.cicadas[num])
                if self.exit_flag:
                    exit(0)
                time.sleep(self.cicadas[num].duration_seconds*0.8)
        Soundscape.non_blocking_function(waves)
        Soundscape.non_blocking_function(cicadas)
    
    def starter(self):
        self.playAmbience()
    
    def playHorn(self):
        Soundscape.non_blocking_sound(self.horn)
        time.sleep(self.horn.duration_seconds)
    
    def loop(self):
        while not self.exit_flag:
            if random.uniform(0,1) <= 1/60:
                self.playHorn()
            time.sleep(1)

Croatia()