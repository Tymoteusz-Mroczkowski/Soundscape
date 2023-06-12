from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize
import random, time, threading
from pydub.silence import detect_silence

import signal
import sys
from pynput import keyboard

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

class Destiny(Soundscape):
    def __init__(self):
        self.ftl = True if random.randint(0,1) == 0 else False
        self.timer = "not set"
        self.gate = 'closed'
        super().__init__()
    
    def starter(self):
        # Register the signal handler function
        signal.signal(signal.SIGINT, Destiny.exit_handler)

        Destiny.non_blocking_function(self.ftl_change,())
        Destiny.non_blocking_function(self.playAmbience,())
        time.sleep(3)
    
    def loadFiles(self):
        # loading audio files
        self.begin = Destiny.trim_silence(AudioSegment.from_file('Sounds/stargate begin roll.mp3'))
        self.chevron = [Destiny.trim_silence(AudioSegment.from_file('Sounds/chevron/%s.mp3' % i)) for i in range(2,6)]
        self.roll = [normalize(Destiny.trim_silence(AudioSegment.from_file('Sounds/roll/%s.mp3' % i)),+7.5) for i in range(1,8)]
        self.wormholeOpen = [Destiny.trim_silence(AudioSegment.from_file('Sounds/open/%s.mp3' % i)) for i in range(1,4)]
        self.close = [Destiny.trim_silence(AudioSegment.from_file('Sounds/close/%s.mp3' % i)) for i in range(1,5)]
        self.fail = [Destiny.trim_silence(AudioSegment.from_file('Sounds/fail/%s.wav' % i)) for i in range(1,4)]
        self.steam = Destiny.trim_silence(AudioSegment.from_file('Sounds/steam.mp3'))
        self.wormholeLoop = normalize(Destiny.trim_silence(AudioSegment.from_file('Sounds/wormhole_loop.wav')), 0)
        self.transit = [normalize(AudioSegment.from_file('Sounds/transit/eh_go_%s.wav' % i), +10) for i in range(1,9)]

        self.doorLocked = normalize(AudioSegment.from_file('Sounds/door/buttons/locked_signal.wav'), +5)
        self.doorButton = normalize(AudioSegment.from_file('Sounds/door/buttons/dest_door_button.wav'), +15)
        self.doorOpen = [normalize(AudioSegment.from_file('Sounds/door/open/%s.wav' % i), +5) for i in range(1,3)]
        self.doorClose = [normalize(AudioSegment.from_file('Sounds/door/close/%s.wav' % i), +5) for i in range(1,5)]

        self.computer = [normalize(AudioSegment.from_file('Sounds/computer/%s.wav' % i), +15) for i in range(1,3)]

        self.FTL_ambient = [normalize(AudioSegment.from_file('Sounds/ambience/--%s.wav' % ((i) if (i>=10) else ('0'+str(i)))), +5) for i in range(1,26)]
        self.STL_ambient = [normalize(AudioSegment.from_file('Sounds/ambience/STL-0%s.wav' % i), 0) for i in range(1,3)]


        self.lightSwitch = [normalize(AudioSegment.from_file('Sounds/lightSwitch/dest_light_on_%s.wav' % i), +10) for i in range(1,4)]

        self.ftlJump = normalize(AudioSegment.from_file('Sounds/destiny_ftl_jump_in.wav'), 0)
        self.ftlDrop = normalize(AudioSegment.from_file('Sounds/destiny_ftl_jump_out.wav'), 0)

        self.timerStart = normalize(AudioSegment.from_file('Sounds/timer_start.wav'), 0)
        self.timerStop = normalize(AudioSegment.from_file('Sounds/timer_stop.wav'), 0)

        self.alarm = normalize(AudioSegment.from_file('Sounds/destiny_alarm.wav'), 0)

    def keyHandler(self):
        Destiny.handlerFlag = True
        def on_press(key):
            if key.char == 'g':
                if self.ftl:
                    self.ftl_change()
                    time.sleep(5)
                Destiny.non_blocking_function(self.destinyDial,())
            if key.char == 'f':
                Destiny.non_blocking_function(self.ftl_change,())
            if key.char == 'd':
                Destiny.non_blocking_function(self.destinyDoor,())
        #while not exit_flag:
        with keyboard.Listener(
            on_press=on_press,
            on_release=None) as listener:
            listener.join()
        Destiny.handlerFlag = False
    
    def loop(self):
        while not Destiny.exit_flag:
            if not Destiny.handlerFlag:  Destiny.non_blocking_function(self.keyHandler,())
            if random.uniform(0,1) > 0.5:
                self.destinyComputer()
            if random.uniform(0,1) > 0.66:
                self.destinyDoor()
            if self.gate=='closed' and ((not self.ftl and random.uniform(0,1) > 0.95) or (self.ftl and random.uniform(0,1) > 0.99)):
                if self.ftl:
                    self.ftl_change()
                    time.sleep(random.uniform(3,10))
                Destiny.non_blocking_function(self.destinyDial,())
            if random.uniform(0,1) > 0.9:
                self.destinyLight()
            if not self.ftl and random.uniform(0,1) > 0.95 and self.gate=='closed': # chance of jumping to ftl
                self.ftl_change()
            if self.ftl and random.uniform(0,1) > 0.95: # change of dropping from ftl
                self.ftl_change()
            time.sleep(random.uniform(0,5))
            
    def ftl_change(self):
        if self.ftl:
            print('\nDropping out of FTL\n')
            self.ftl = False
            Destiny.non_blocking_sound(self.ftlDrop)
            time.sleep(self.ftlDrop.duration_seconds-1)
            if random.uniform(0,1) > 0.2:
                print('\nStarting Timer\n')
                Destiny.non_blocking_sound(self.timerStart)
                self.timer="set"
                if random.uniform(0,1) > 0.25:
                    time.sleep(random.uniform(2,10))
                    Destiny.non_blocking_function(self.destinyDial,())
        else:
            print('\Jumping to FTL\n')
            if self.timer=="set":
                print('\nTimer stopped\n')
                self.timer = "expired"
                for _ in range(3):
                    Destiny.non_blocking_sound(self.timerStop)
                    time.sleep(self.timerStop.duration_seconds-0.2)
            while self.gate != "closed":
                print('\nWaiting for gate shutdown\n')
                play(self.alarm)
            self.ftl = True
            Destiny.non_blocking_sound(self.ftlJump)

    def playAmbience(self):
        while not Destiny.exit_flag:
            if self.ftl:
                print('\nPlaying FTL ambience\n')
                trackNum = random.randint(0,24)
                Destiny.non_blocking_sound(self.FTL_ambient[trackNum])
                time.sleep(self.FTL_ambient[trackNum].duration_seconds-random.uniform(0.8,1.5))
            else:
                print('\nPlaying STL ambience\n')
                trackNum = random.randint(0,1)
                Destiny.non_blocking_sound(self.STL_ambient[trackNum])
                time.sleep(self.STL_ambient[trackNum].duration_seconds-random.uniform(0.75,1))

    def destinyComputer(self):
        print('\nClicking Buttons\n')
        for _ in range(random.randint(1,16)):
            Destiny.non_blocking_sound(self.computer[random.randint(0,1)])
            time.sleep(random.uniform(0.1,1))

    def destinyDoor(self):
        print('\ndoor\n')
        if random.uniform(0,1)>0.9:
            print('\nremote\n')
            if random.randint(0,1)==0:
                print('\nopen\n')
                Destiny.non_blocking_sound(self.doorOpen[random.randint(0,1)])
                time.sleep(5)
            else:
                print('\nclose\n')
                Destiny.non_blocking_sound(self.doorClose[random.randint(0,3)])
                time.sleep(6)
        else:
            print('\nbutton\n')
            Destiny.non_blocking_sound(self.doorButton)
            time.sleep(self.doorButton.duration_seconds)
            if random.uniform(0,1)>0.9:
                print('\nlocked\n')
                Destiny.non_blocking_sound(self.doorLocked)
                time.sleep(self.doorLocked.duration_seconds)
                return
            
            if random.uniform(0,1)>0.6:
                print('\nclosing\n')
                Destiny.non_blocking_sound(self.doorClose[random.randint(0,3)])
                time.sleep(6)
                return
            print('\nopening\n')
            Destiny.non_blocking_sound(self.doorOpen[random.randint(0,1)])
            time.sleep(5 + random.uniform(1,15))
            print('\nclosing\n')
            if random.uniform(0,1) < 0.4:
                Destiny.non_blocking_sound(self.doorButton)
                time.sleep(self.doorButton.duration_seconds)
            Destiny.non_blocking_sound(self.doorClose[random.randint(1,3)])
            time.sleep(6)

    def destinyLight(self):
        print('\nStuff turning on and off\n')
        Destiny.non_blocking_sound(self.lightSwitch[random.randint(0,2)])
        time.sleep(random.uniform(0,1))

    def wormhole(self):
        openNum = random.randint(0,1)
        Destiny.non_blocking_sound(self.wormholeOpen[openNum])
        time.sleep(self.wormholeOpen[openNum].duration_seconds-0.5)
        
        cargo = (True if random.uniform(0,1) > 0.5 else False)
        
        for _ in range(random.randint(0,5)):
            Destiny.non_blocking_sound(self.wormholeLoop)
            totalTime = 0
            if cargo:
                for _ in range(random.randint(0,6)):
                    Destiny.non_blocking_sound(self.transit[random.randint(0,7)])
                    elapsed = random.uniform(0,5/6)
                    time.sleep(elapsed)
                    totalElapsed += elapsed
            time.sleep(self.wormholeLoop.duration_seconds-random.uniform(0,1)-totalElapsed)
        

        closeNum = random.randint(0,2)
        Destiny.non_blocking_sound(self.close[closeNum])
        time.sleep(self.close[closeNum].duration_seconds)

    def destinyDial(self):
        if self.gate != 'closed': return
        self.gate = 'active'
        failRate = 0.1
        # dialing the gate
        Destiny.non_blocking_sound(self.begin)
        time.sleep(max(self.begin.duration_seconds-0.5,0))
        if random.uniform(0,1) > 0.75: # incoming
            self.timer = "expired"
            rollnum = random.randint(3,5)
            Destiny.non_blocking_sound(self.roll[rollnum])
            time.sleep(max(self.roll[rollnum].duration_seconds-0.15,0))
            chevnum = random.randint(0,3)
            play(self.chevron[chevnum])
            gate = "open"
            self.wormhole()
            Destiny.non_blocking_sound(self.steam)
            time.sleep(self.steam.duration_seconds)
            gate = "closed"
            time.sleep(random.uniform(0,5))
            if self.timer != 'set':
                self.timer = 'set' if random.uniform(0,1)>0.1 else 'not set'
            return
        for i in range(7): # outgoing
            rollnum = random.randint(0,5)
            Destiny.non_blocking_sound(self.roll[rollnum])
            time.sleep(max(self.roll[rollnum].duration_seconds-0.15,0))
            if self.timer=="expired":
                failNum = random.randint(0,2)
                Destiny.non_blocking_sound(self.fail[failNum])
                time.sleep(self.wormholeOpen[failNum].duration_seconds)
                gate = 'closed'
                return
            
            chevnum = random.randint(0,3)
            Destiny.non_blocking_sound(self.chevron[chevnum])
            time.sleep(max(self.chevron[chevnum].duration_seconds-0.15,0))
            if i<6:
                print("Chevron %s encoded\n" % str(i+1))
            else:
                print("Chevron %s locked\n" % str(i+1))

        if random.uniform(0,1) <= failRate: # dialing failiure
            failNum = random.randint(0,2)
            Destiny.non_blocking_sound(self.fail[failNum])
            time.sleep(self.wormholeOpen[failNum].duration_seconds)
            gate = 'closed'
            return
        else: # dialing success
            gate = "open"
            self.wormhole()
            play(self.steam)
            gate = 'closed'
        gate = 'closed'

Destiny()