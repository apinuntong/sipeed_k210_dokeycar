import os
import  sensor, image, lcd, time
from fpioa_manager import fm
from machine import I2C
from board import board_info
from Maix import GPIO

#from board import board_info
i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)
fm.register(22, fm.fpioa.GPIOHS6, force=True)
pin12 = GPIO(GPIO.GPIOHS6, GPIO.OUT)
lcd.init()
lcd.clear()
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(2)
sensor.run(1)
lcd.init(type=2, freq=20000000, color=lcd.BLACK)
tim = time.ticks_ms()
f = open('/sd/dataset.csv', 'a')
tim_b = tim
idpg=0
bt =0
dirfo = 0
dirfoc = 0
eee1 = 0
tong3 = 0
toss1 = 0

img_co_l = 0
img_co_f = 0
img_co_r = 0

os.mkdir(str(dirfo))
clock = time.clock()
while True:

    tim = time.ticks_ms()

    if (tim - tim_b) >= 50 :
        tim_b = tim
        print(clock.fps())
        clock.tick()
        img = sensor.snapshot()
        tong = i2c.readfrom(0x12, 3)
        if (int(tong[2]) == 4) and (int(tong[0]) > 135) :
            if tong3 == 0 :
                tong3 = 1
                pin12.value(1)
            else :
                tong3 = 0
                pin12.value(0)
            idpg=idpg+1
            dirfoc = dirfoc+1
            if tong[1] < 85:
                img_co_l = img_co_l+1
            elif tong[1] < 170:
                img_co_f = img_co_f+1
            else:
                img_co_r = img_co_r+1
            f.write(str(dirfo)+"/"+str(idpg)+","+str(int(tong[0]))+","+str(int(tong[1]))+"\n")
            f.flush()
            img.save("/sd/"+str(dirfo)+"/"+str(idpg)+".jpg")
            if dirfoc == 100 :
                dirfoc = 0
                dirfo = dirfo+1
                os.mkdir(str(dirfo))
        img.draw_string(50, 0, "L = "+str(img_co_l), scale=2)
        img.draw_string(50, 20, "F = "+str(img_co_f), scale=2)
        img.draw_string(50, 40, "R = "+str(img_co_r), scale=2)
        lcd.display(img)

