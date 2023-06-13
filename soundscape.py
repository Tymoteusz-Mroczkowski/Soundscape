from pydub.playback import play
import threading
from pydub.silence import detect_silence

import sys

class Soundscape():
    exit_flag = False
    handlerFlag = False
    
    def __init__(self):
        self.loadFiles()
        self.starter()
        self.loop()

    def loadFiles(self):
        pass
    
    def starter(self):
        pass
    
    def loop(self):
        pass
    
    def keyHandler(self):
        pass
    
    @classmethod
    def exit_handler(self, signal, frame):
        # Code to execute when the user exits the application
        print("Exiting the application...")
        Soundscape.exit_flag = True
        # Additional cleanup or actions can be performed here
        sys.exit(0)
    
    @classmethod
    def trim_silence(self, sound): # by ChatGPT
        # Set the parameters for silence detection
        silence_threshold = -50  # dBFS (adjust as needed)
        silence_min_duration = 250  # milliseconds (adjust as needed)

        # Detect the silence regions in the sound
        silence_regions = detect_silence(sound, silence_thresh=silence_threshold, min_silence_len=silence_min_duration)

        # Trim the sound based on the detected silence regions
        if len(silence_regions) > 0:
            # Trim the silence at the beginning
            start_trim = silence_regions[0][0]
            trimmed_sound = sound[start_trim:]

            # Trim the silence at the end
            end_trim = sound.duration_seconds * 1000 - silence_regions[-1][1]
            trimmed_sound = trimmed_sound[:-end_trim]

            return trimmed_sound
        else:
            return sound  # No silence detected, return the original sound
    
    @classmethod
    def non_blocking_sound(self, sound):
        thread = threading.Thread(target=play, args=(sound,))
        thread.start()
        if Soundscape.exit_flag:
            thread.join()
    
    @classmethod
    def non_blocking_function(self, func, args=()):
        thread = threading.Thread(target=func, args=args)
        thread.start()
        if Soundscape.exit_flag:
            thread.join()