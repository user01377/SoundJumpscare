import pyaudio
import time
from math import log10
import audioop  
import pygame
import random

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
# rms = 1
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

def decibalCheck():
    return 20 * log10(rms)

rms = 1

pygame.mixer.init() 
pygame.mixer.music.load(".//jumpscare.wav")
pygame.mixer.music.set_volume(1)

print("program is ON")


while stream.is_active():
    soundCheck = random.randint(0,100)
    #print(decibalCheck()) #prints "decibel level"
    if decibalCheck() >= -22:
        if soundCheck % 2 == 0:
            pygame.mixer.music.play() 
    time.sleep(.2)

stream.stop_stream()
stream.close()

p.terminate()
