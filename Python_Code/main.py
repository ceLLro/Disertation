# AprilTags Application via OpenMV Cam M7


import sensor, image, time, math, pyb
from pyb import LED, Timer, Pin

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA) # we run out of memory if the resolution is much bigger...
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)  # must turn this off to prevent image washout...
sensor.set_auto_whitebal(False)  # must turn this off to prevent image washout...
clock = time.clock()

#pin layout
tim = pyb.Timer(4, freq=1000)
p0 = pyb.Pin(pyb.Pin.board.P0, pyb.Pin.OUT_PP)
p7 = tim.channel(1, pyb.Timer.PWM, pin=pyb.Pin("P7"))

#led layout
red_led   = LED(1)
green_led = LED(2)
blue_led  = LED(3)

#control car actions
def status(state, found):
    if(state == None or found == None):
        p0.value(0)
        p7.pulse_width_percent(0)
        ledMapping(0)
    elif(state == 1):
        p0.value(0)
        p7.pulse_width_percent(65)
        ledMapping(1)
    elif(state == 2):
        p0.value(1)
        p7.pulse_width_percent(30)
        ledMapping(2)
    elif(state == 3):
        p0.value(0)
        p7.pulse_width_percent(0)
        ledMapping(3)

#turn on leds based on status
def ledMapping(pattern):
    if(pattern == 0):    #turned off state
        red_led.off()
        green_led.off()
        blue_led.off()
    elif(pattern == 1):  #forward state
        red_led.off()
        green_led.on()
        blue_led.off()
    elif(pattern == 2):  #backward state
        red_led.on()
        green_led.off()
        blue_led.off()
    elif(pattern == 3):  #stop state
        red_led.off()
        green_led.off()
        blue_led.on()

#tag id's
def tag_id(tag):
    if(tag.id() == 0):
        return 0
    elif(tag.id() == 1):
        return 1
    elif(tag.id() == 2):
        return 2
    else:
        return 3
    
while(True):

    clock.tick()
    id_tag = 3
    isValid = False

    img = sensor.snapshot()
    for tag in img.find_apriltags(): # defaults to TAG36H11 without "families".

        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
        isValid = True
        id_tag = tag.id()

    status(id_tag, isValid)
    print(clock.fps())
