import sensor, image, time ,lcd
import KPU as kpu
from fpioa_manager import fm
from machine import I2C
from board import board_info
from Maix import GPIO
i2c = I2C(I2C.I2C0, freq=100000, scl=35, sda=34)

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.set_vflip(1)
sensor.run(1)

clock = time.clock()
toss1 = 0


lcd.init(type=2, freq=20000000, color=lcd.BLACK)

#task = kpu.load(0x400000)
task = kpu.load("/sd/to1.kmodel")
##datazzz = bytes([int(128),int(128),int(0)])
try:
    while(True):
        toss = toss1
        toss1 = time.ticks_ms()
        #print(1000/(toss1-toss))
        #img = image.Image("/sd/dataset/55.jpg")
        img = sensor.snapshot()
        #img = img.draw_rectangle(0,0,320,80,color=(0,0,0),fill=True)
        ##img = img.draw_rectangle(130,180,90,240-180,color=(0,0,0),fill=True)
        img = img.resize(160,160)

        ##img = img.draw_rectangle(0,180,224,320,color=(0,0,0),fill=True)
        a = img.pix_to_ai()
        #print(img[0])

        a = kpu.set_outputs(task,0,1,1,1)
        fmap = kpu.forward(task,img)
        plist=fmap[:]
        #pmax=max(plist)
        #max_index=plist.index(pmax)
        #print(plist)
        txx = (plist[0])*127
        print(txx)
        ##txx = txx*1.5
        if txx > 127 :
            txx = 127
        if txx < -127 :
            txx = -127
        #print(txx)
        datazzz = bytes([int(128),int(txx+127),int(0)])
        ####print(datazzz)
        i2c.writeto(0x12,bytes([int(128),int(txx+127),int(0)]))
        lcd.display(img)
        lcd.draw_string(90, 0, str(int(1000/(toss1-toss)))+" fps", lcd.RED,lcd.BLACK)
        #lcd.display(img2)

except KeyboardInterrupt :
    a = kpu.deinit(task)
