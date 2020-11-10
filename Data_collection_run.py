import os
import uos
import  sensor, image, lcd, time
from fpioa_manager import fm
from machine import I2C
from board import board_info
from Maix import GPIO

#from board import board_info
sensor.reset(dual_buff=True)
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(2)
sensor.run(1)
lcd.init(type=2, freq=20000000, color=lcd.BLACK)
i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)
fm.register(22, fm.fpioa.GPIOHS6, force=True)
pin12 = GPIO(GPIO.GPIOHS6, GPIO.OUT)
dirfo = 0
dirfoc = 0
idpg=0
olddatasetnum = 0
try:
    if i2c.scan()[0] == 18 :
        print("I2C OK")
        lcd.draw_string(85, 110, "I2C OK", lcd.WHITE, lcd.RED)
        time.sleep(1)
except:
    print("no I2C")
    while 1 :
        lcd.draw_string(85, 110, "no I2C", lcd.WHITE, lcd.RED)
        time.sleep(1)
try:
    print(uos.listdir("/sd"))
except:
    print("no sd dir")
    while 1 :
        lcd.draw_string(85, 110, "no sd dir", lcd.WHITE, lcd.RED)
        time.sleep(1)
try:
    print("load old dataset.csv")
    uos.rename('/sd/dataset.csv', '/sd/dataset.txt')
    f=open('/sd/dataset.txt','r')
    labels=f.readlines()
    f.close()
    olddatasetnum = len(labels)
    idpg = olddatasetnum
    dirfoc = len(labels)%100
    dirfo = int(len(labels)/100)
    print(dirfo,dirfoc)
    uos.rename('/sd/dataset.txt', '/sd/dataset.csv')
except:
    print("not dataset.csv")
    lcd.draw_string(45, 110, "read old dataset error", lcd.WHITE, lcd.RED)
    time.sleep(5)

tim = time.ticks_ms()

tim_b = tim

bt =0

eee1 = 0
tong3 = 0
toss1 = 0

img_co_l = 0
img_co_f = 0
img_co_r = 0


try:
  os.mkdir("/sd/"+str(dirfo))
except:
  print("An exception occurred")
try:
    f = open('/sd/dataset.csv', 'a')
except:
    print("no '/sd/dataset.csv'")
clock = time.clock()
while True:

    tim = time.ticks_ms()
    try:
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
                    os.mkdir("/sd/"+str(dirfo))
            a = img.draw_string(50, 0, "L = "+str(img_co_l), scale=2)
            a = img.draw_string(50, 20, "F = "+str(img_co_f), scale=2)
            a = img.draw_string(50, 40, "R = "+str(img_co_r), scale=2)
            a = img.draw_string(50, 60, "OD = "+str(olddatasetnum), scale=2)
            lcd.display(img)
    except:
        print("error")