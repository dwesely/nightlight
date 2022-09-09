# Trinket Nightlight

# import alarm
import board
import adafruit_dotstar as dotstar
import time
from digitalio import DigitalInOut, Direction, Pull
import rotaryio


# One pixel connected internally!
nightlight_brightness = 0.5
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=nightlight_brightness)

# button on the rotary encoder puts nightlight to sleep
switch = DigitalInOut(board.D1)
switch.direction = Direction.INPUT
switch.pull = Pull.UP

encoder = rotaryio.IncrementalEncoder(board.D3, board.D4)
last_position = None

######################### HELPERS ##############################

# Helper to give us a nice color swirl
def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    color = (0,0,0)
    if pos < 0:
        return  color
    if pos > 255:
        return  color
    if pos < 85:
        color = (int(pos * 3), int(255 - (pos * 3)), 0, nightlight_brightness)
    elif pos < 170:
        pos -= 85
        color = (int(255 - pos * 3), 0, int(pos * 3), nightlight_brightness) 
    else:
        pos -= 170
        color = (0, int(pos * 3), int(255 - pos * 3), nightlight_brightness)
    print(color)
    return(color)


######################### MAIN LOOP ##############################

i = 0
t = 0
starting_color_position = 65
timeout = 5000 * 60 * 10  # 10 minutes

while True:
    # Increment the timer
    t = t + 1

    if not switch.value:
        # Button pressed, go to sleep
        t = timeout

    if t > timeout:
        # going to sleep, fade out the dotstar
        R, G, B, L = dot[0]
        R = max(0, R - 1)
        G = max(0, G - 1)
        B = max(0, B - 1)
        # L = max(0, L - 0.001)
        dot[0] = [R, G, B, L]
        # print(dot.brightness)
        if max(dot[0]) <= 1.0:
            # TODO: deep sleep, wake up on interrupt
            pass
    # print(t)
    
    # Check for rotary encoder movement
    position = encoder.position
    if last_position is None or position != last_position:
        t = 0
        i = ((position + starting_color_position) * 2) % 256  # run from 0 to 255
        print(position, i)
        dot[0] = wheel(i & 255)
        t = 0
    last_position = position
