from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize
import random, time, threading
from pydub.silence import detect_silence

import signal
import sys
from pynput import keyboard

exit_flag = False
handlerFlag = False
def keyHandler():
    global handlerFlag
    handlerFlag = True
    def on_press(key):
        if key.char == 'g':
            if ftl:
                ftl_change()
                time.sleep(2)
            non_blocking_function(destinyDial,())
        if key.char == 'f':
            non_blocking_function(ftl_change,())
        if key.char == 'd':
            non_blocking_function(destinyDoor,())
    #while not exit_flag:
    with keyboard.Listener(
        on_press=on_press,
        on_release=None) as listener:
        listener.join()
    handlerFlag = False

def exit_handler(signal, frame):
    global exit_flag
    # Code to execute when the user exits the application
    print("Exiting the application...")
    exit_flag = True
    # Additional cleanup or actions can be performed here
    sys.exit(0)

# Register the signal handler function
signal.signal(signal.SIGINT, exit_handler)

def trim_silence(sound): # by ChatGPT
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

def non_blocking_sound(sound):
    thread = threading.Thread(target=play, args=(sound,))
    thread.start()
    if exit_flag:
        thread.join()

def non_blocking_function(func, args=()):
    thread = threading.Thread(target=func, args=args)
    thread.start()
    if exit_flag:
        thread.join()

# loading audio files
begin = trim_silence(AudioSegment.from_file('Sounds/stargate begin roll.mp3'))
chevron = [trim_silence(AudioSegment.from_file('Sounds/chevron/%s.mp3' % i)) for i in range(2,6)]
roll = [normalize(trim_silence(AudioSegment.from_file('Sounds/roll/%s.mp3' % i)),+7.5) for i in range(1,8)]
wormholeOpen = [trim_silence(AudioSegment.from_file('Sounds/open/%s.mp3' % i)) for i in range(1,4)]
close = [trim_silence(AudioSegment.from_file('Sounds/close/%s.mp3' % i)) for i in range(1,5)]
fail = [trim_silence(AudioSegment.from_file('Sounds/fail/%s.wav' % i)) for i in range(1,4)]
steam = trim_silence(AudioSegment.from_file('Sounds/steam.mp3'))
wormholeLoop = normalize(trim_silence(AudioSegment.from_file('Sounds/wormhole_loop.wav')), 0)
transit = [normalize(AudioSegment.from_file('Sounds/transit/eh_go_%s.wav' % i), +10) for i in range(1,9)]

doorLocked = normalize(AudioSegment.from_file('Sounds/door/buttons/locked_signal.wav'), +5)
doorButton = normalize(AudioSegment.from_file('Sounds/door/buttons/dest_door_button.wav'), +15)
doorOpen = [normalize(AudioSegment.from_file('Sounds/door/open/%s.wav' % i), +5) for i in range(1,3)]
doorClose = [normalize(AudioSegment.from_file('Sounds/door/close/%s.wav' % i), +5) for i in range(1,5)]

computer = [normalize(AudioSegment.from_file('Sounds/computer/%s.wav' % i), +15) for i in range(1,3)]

FTL_ambient = [normalize(AudioSegment.from_file('Sounds/ambience/--%s.wav' % ((i) if (i>=10) else ('0'+str(i)))), +5) for i in range(1,26)]
STL_ambient = [normalize(AudioSegment.from_file('Sounds/ambience/STL-0%s.wav' % i), 0) for i in range(1,3)]


lightSwitch = [normalize(AudioSegment.from_file('Sounds/lightSwitch/dest_light_on_%s.wav' % i), +10) for i in range(1,4)]

ftlJump = normalize(AudioSegment.from_file('Sounds/destiny_ftl_jump_in.wav'), 0)
ftlDrop = normalize(AudioSegment.from_file('Sounds/destiny_ftl_jump_out.wav'), 0)

timerStart = normalize(AudioSegment.from_file('Sounds/timer_start.wav'), 0)
timerStop = normalize(AudioSegment.from_file('Sounds/timer_stop.wav'), 0)

alarm = normalize(AudioSegment.from_file('Sounds/destiny_alarm.wav'), 0)

ftl = True if random.randint(0,1) == 0 else False
timer = False
gate = 'closed'

def ftl_change():
    global ftl, timer
    if ftl:
        print('\nDropping out of FTL\n')
        ftl = False
        non_blocking_sound(ftlDrop)
        time.sleep(ftlDrop.duration_seconds-1)
        if random.uniform(0,1) > 0.2:
            print('\nStarting Timer\n')
            non_blocking_sound(timerStart)
            timer=True
            if random.uniform(0,1) > 0.25:
                time.sleep(random.uniform(2,10))
                non_blocking_function(destinyDial,())
    else:
        print('\Jumping to FTL\n')
        if timer:
            print('\nTimer stopped\n')
            timer = False
            play(timerStop)
            while gate != "closed":
                print('\nWaiting for gate shutdown\n')
                play(alarm)
        ftl = True
        non_blocking_sound(ftlJump)

def playAmbience():
    while not exit_flag:
        if ftl:
            print('\nPlaying FTL ambience\n')
            trackNum = random.randint(0,24)
            non_blocking_sound(FTL_ambient[trackNum])
            time.sleep(FTL_ambient[trackNum].duration_seconds-random.uniform(0.8,1.5))
        else:
            print('\nPlaying STL ambience\n')
            trackNum = random.randint(0,1)
            non_blocking_sound(STL_ambient[trackNum])
            time.sleep(STL_ambient[trackNum].duration_seconds-random.uniform(0.75,1))

def destinyComputer():
    print('\nClicking Buttons\n')
    for _ in range(random.randint(1,16)):
        non_blocking_sound(computer[random.randint(0,1)])
        time.sleep(random.uniform(0.1,1))

def destinyDoor():
    print('\ndoor\n')
    if random.uniform(0,1)>0.9:
        print('\nremote\n')
        if random.randint(0,1)==0:
            print('\nopen\n')
            non_blocking_sound(doorOpen[random.randint(0,1)])
            time.sleep(5)
        else:
            print('\nclose\n')
            non_blocking_sound(doorClose[random.randint(0,3)])
            time.sleep(6)
    else:
        print('\nbutton\n')
        non_blocking_sound(doorButton)
        time.sleep(doorButton.duration_seconds)
        if random.uniform(0,1)>0.9:
            print('\nlocked\n')
            non_blocking_sound(doorLocked)
            time.sleep(doorLocked.duration_seconds)
            return
        
        if random.uniform(0,1)>0.6:
            print('\nclosing\n')
            non_blocking_sound(doorClose[random.randint(0,3)])
            time.sleep(6)
            return
        print('\nopening\n')
        non_blocking_sound(doorOpen[random.randint(0,1)])
        time.sleep(5 + random.uniform(1,15))
        print('\nclosing\n')
        if random.uniform(0,1) < 0.4:
            non_blocking_sound(doorButton)
            time.sleep(doorButton.duration_seconds)
        non_blocking_sound(doorClose[random.randint(1,3)])
        time.sleep(6)

def destinyLight():
    print('\nStuff turning on and off\n')
    non_blocking_sound(lightSwitch[random.randint(0,2)])
    time.sleep(random.uniform(0,1))

def wormhole():
    openNum = random.randint(0,1)
    non_blocking_sound(wormholeOpen[openNum])
    time.sleep(wormholeOpen[openNum].duration_seconds-0.5)
    
    cargo = (True if random.uniform(0,1) > 0.5 else False)
    
    for _ in range(random.randint(0,5)):
        non_blocking_sound(wormholeLoop)
        totalTime = 0
        if cargo:
            for _ in range(random.randint(0,6)):
                non_blocking_sound(transit[random.randint(0,7)])
                timer = random.uniform(0,5/6)
                time.sleep(timer)
                totalTime += timer
        time.sleep(wormholeLoop.duration_seconds-random.uniform(0,1)-totalTime)
    

    closeNum = random.randint(0,2)
    non_blocking_sound(close[closeNum])
    time.sleep(close[closeNum].duration_seconds)

def destinyDial():
    global gate, timer
    if gate != 'closed': return
    oldTimer = timer
    gate = 'active'
    failRate = 0.1
    # dialing the gate
    non_blocking_sound(begin)
    time.sleep(max(begin.duration_seconds-0.5,0))
    if random.uniform(0,1) > 0.75: # incoming
        timer = False
        rollnum = random.randint(3,5)
        non_blocking_sound(roll[rollnum])
        time.sleep(max(roll[rollnum].duration_seconds-0.15,0))
        chevnum = random.randint(0,3)
        play(chevron[chevnum])
        gate = "open"
        wormhole()
        non_blocking_sound(steam)
        time.sleep(steam.duration_seconds)
        gate = "closed"
        time.sleep(random.uniform(0,5))
        if not oldTimer:
            timer = True if random.uniform(0,1)>0.1 else False
        return
    for i in range(7): # outgoing
        rollnum = random.randint(0,5)
        non_blocking_sound(roll[rollnum])
        time.sleep(max(roll[rollnum].duration_seconds-0.15,0))
        if oldTimer and not timer:
            failNum = random.randint(0,2)
            non_blocking_sound(fail[failNum])
            time.sleep(wormholeOpen[failNum].duration_seconds)
            gate = 'closed'
            return
        
        chevnum = random.randint(0,3)
        non_blocking_sound(chevron[chevnum])
        time.sleep(max(chevron[chevnum].duration_seconds-0.15,0))
        if i<6:
            print("Chevron %s encoded\n" % str(i+1))
        else:
            print("Chevron %s locked\n" % str(i+1))

    if random.uniform(0,1) <= failRate: # dialing failiure
        failNum = random.randint(0,2)
        non_blocking_sound(fail[failNum])
        time.sleep(wormholeOpen[failNum].duration_seconds)
        gate = 'closed'
        return
    else: # dialing success
        gate = "open"
        wormhole()
        play(steam)
        gate = 'closed'
    gate = 'closed'

non_blocking_function(ftl_change,())
non_blocking_function(playAmbience,())
while not exit_flag:
    if not handlerFlag:  non_blocking_function(keyHandler,())
    if random.uniform(0,1) > 0.5:
        destinyComputer()
    if random.uniform(0,1) > 0.66:
        destinyDoor()
    if gate=='closed' and ((not ftl and random.uniform(0,1) > 0.8) or (ftl and random.uniform(0,1) > 0.99)):
        if ftl:
            ftl_change()
            time.sleep(random.uniform(3,10))
        non_blocking_function(destinyDial,())
    if random.uniform(0,1) > 0.9:
        destinyLight()
    if not ftl and random.uniform(0,1) > 0.95 and gate=='closed': # chance of jumping to ftl
        ftl_change()
    if ftl and random.uniform(0,1) > 0.95: # change of dropping from ftl
        ftl_change()
    time.sleep(random.uniform(0,5))