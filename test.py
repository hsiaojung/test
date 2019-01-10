'''
2018/10/03 made by Cyril Chang 
v0.1
'''
import subprocess
import decimal
import re
import sys
import time

from time import sleep
from threading import Thread
import os
import sys, signal
import time
import serial

import smbus
import time
import datetime
import os
import RPi.GPIO as GPIO


import netifaces as ni

timealreadyboot = 0
bootenable = 0


def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hostname = "8.8.8.8" #example

class switch(object):
    def __init__(self, value):
        self.value = value
        self.fall = False
 
    def __iter__(self):
        """Return the match method once, then stop"""
        yield self.match
        raise StopIteration
 
    def match(self, *args):
        """Indicate whether or not to enter a case suite"""
        if self.fall or not args:
            return True
        elif self.value in args: # changed for v1.5, see below
            self.fall = True
            return True
        else:
            return False
def lora_tx():

	ser = serial.Serial('/dev/ttyAMA0',115200,timeout=5)  # open serial port
	print("\r\n Testing lora_tx \r\n Check You have set to RX of LoRa already to get Tx sending string!\r\n")         # check which port was really used
	ser.write(b'p2p set_sync 12\r\n')
	time.sleep(1)
	state = ser.read(25)
	readback = state.decode('utf-8','ignore')
	print (readback)
	ser.write(b'p2p set_sync 12\r\n')
	time.sleep(1)
	state = ser.read(25)
	print (readback)
	readback = state.decode('utf-8','ignore')
	ser.write(b'p2p set_sf 7\r\n')
	time.sleep(1)
	state = ser.read(25)
	print (readback)
	readback = state.decode('utf-8','ignore')
	ser.write(b'p2p tx 1234567890\r\n')
	time.sleep(1)
	state = ser.read(40)
	print (readback)
	readback = state.decode('utf-8','ignore')
	print (readback)
	ser.close() 

def lora_rx():

	ser = serial.Serial('/dev/ttyAMA0',115200,timeout=26)  # open serial port
	print("\r\n Test LoRa, Rx side \r\n Check TX of LoRa standby!\r\n")         # check which port was really used
	ser.write(b'p2p set_sync 12\r\n')
	time.sleep(1)
	state = ser.read(25)
	readback = state.decode('utf-8','ignore')
	print (readback)
	ser.write(b'p2p set_sync 12\r\n')
	time.sleep(1)
	state = ser.read(25)
	print (readback)
	readback = state.decode('utf-8','ignore')
	ser.write(b'p2p set_sf 7\r\n')
	time.sleep(1)
	state = ser.read(25)
	print (readback)
	readback = state.decode('utf-8','ignore')
	ser.write(b'p2p rx 20000\r\n')
	time.sleep(1)
	state = ser.read(45)
	print (readback)
	readback = state.decode('utf-8','ignore')
	print (readback)
	ser.close() 
	if readback.find("12345678") >= 0:
	    print('== we get return AND it is we expect, Pass LoRa TEST!! ')  
	else :
	    print('== we get return, but it is not we expect, fail ! LoRa TEST!! ')       

	ser.close() 



            
def rs485_test():

	ser = serial.Serial('/dev/ttyS0',115200,timeout=23)  # open serial port
	print("\n we use [%s] to test and baud rate is at 115200"%ser.name)         # check which port was really used
	ser.write(b'\n\r \n\n if you see from remote SMG-01 machine,\n\r \n\n please enter [ exit ] to return!"')
	
	state = ser.read(4)
	readback = state.decode('utf-8','ignore')
	bytes.decode(state)

	#print (readback)
	print('============================================')
	if readback.find("exit") >= 0:
            		
            	print('\n\n we get answer of return AND it is we expect, Pass !!! ')	
		
	else :
		print('== \n\n we get return, but it is not we expect, failed !!! ')		
	ser.close() 
	print('\n ============================================')
	
def startShow():

    print("#######################################################################-\n")
    print("##                                                                  #-\n")
    print("##  SMG01's fnction Test Item                                       #-\n")
    print("##                                                              0.5 #-\n")
    print("#######################################################################-\n")
            
 
def i2c_current_sensor():

    bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
    i2c_address = 0x4d  # default address
    
    t = 0.001
    counter = 1
    while counter <= 300:
    # Reads word (2 bytes) as int
        rd = bus.read_word_data(i2c_address, 0)
        block = bus.read_i2c_block_data(i2c_address, 0, 2)
        print(block)
        # Returned value is a list of 16 bytes
    # Exchanges high and low bytes
        #data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
        #data = data >> 2
        print("!!! read word date in Dec={%d},in hex={%x} "%(rd,rd)) 
        print(datetime.datetime.now())
        #t += 0.000001
        time.sleep(t)
        counter += 1
        
def i2c_voltage_sensor():

    bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
    i2c_address = 0x4b  # default address
    counter = 1
    t = 0.05
    while counter <= 300:
    # Reads word (2 bytes) as int
        rd = bus.read_word_data(i2c_address, 0)
        block = bus.read_i2c_block_data(i2c_address, 0, 2)
        print(block)
        # Returned value is a list of 16 bytes
    # Exchanges high and low bytes
        #data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
    # Ignores two least significiant bits
        #data = data >> 2
        print("!!!read word date in Dec={%d},in hex={%x} "%(rd,rd)) 
        print(datetime.datetime.now())
        #t += 0.000001
        time.sleep(t)
        counter += 1
'''
def task_menu():


    menu = {
        0: "Test CPU and memory and emmc(hard disk)",
        1: "Modify Mac address",
        2: "Show Current sensor info",
        3: "Show Voltage sensor info",
        4: "Test DHT11/22",
        5: "Test LoRa function over UART0 TX",
        6: "Test LoRa function over UART0 Rx",
        7: "Test SD CARD",
        8: "Test USB Camera",
        9: "Test RS485 function over UART1",
        10:"Test LTE network"
        }

    for i in menu:
     
        print ("(%d) [%s]\n"%(i,menu[i]))
    lst = print_menu()
    print(lst)
 '''
def task_menu2(timealreadyboot,bootenable):

    startShow()
    menu = {
    
        0: " Stress test: CPU, Memory and EMMC (hard disk)",
        1: " Modify Mac address",
        2: " Show Current sensor info",
        3: " Show Voltage sensor info",
        4: " Test DHT11/22",
        5: " Test LoRa function over UART0 TX",
        6: " Test LoRa function over UART0 Rx",
        7: " Test SD CARD",
        8: " Test USB Camera,Take picture and save at SDCARD",
        9: " Test RS485 function over UART1",
        10:" Test LTE ",
        11:" Auto Login + boot count",
        12:" Disable Auto Login,back to normal!",
        13:" HDMI Pattern output",
        14:" GPIO 43 test by Flashing an LED every secound",
        15:" GPIO 42 test by Flashing an LED every half secound",
        16:" Read GPIO 12/13 ",
        17:" Test Ethernet by asking dhcp and ping google",
        25:" (unconfirmed)Test LoRa function over UART0 TX for A1 hardware Only!!",
        26:" (unconfirmed)Test LoRa function over UART0 Rx for A1 hardware Only!!",
        27:" (unconfirmed)Test RS485 function over UART1 for A1 hardware Only!!",
        28:" (unconfirmed)Test LTE for A1 hardware Only",
        99:" reboot"
    }
    while True:


    
        ()
        for i in menu:
     
            print ("(%d) [%s]"%(i,menu[i]))
            
        lst = print_menu2(timealreadyboot,bootenable)

def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except OSError:
        return False
    return 1
  
def boottimes():


    path = "/home/pi/bootcount"
    file = open(path, 'r')
    bc = file.readline()
    rc = int(bc)
    file.close() 

    
    file = open(path, 'w')
    rc = rc + 1
    ret = rc
    #print("rc=%d"%rc)
    file.write(str(rc))
    file.close()     
    return ret
    
def bootenables():


    path = "/home/pi/bootenable"
    file = open(path, 'r')
    bc = file.readline()
    rc = int(bc)
    file.close() 

    return rc
    
def enableUsbPwr():


    import RPi.GPIO as GPIO


    print('==\n  Enable GPIO37 for USB_PWR_EN') 
    pin=37
    import RPi.GPIO as GPIO
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def print_menu2(timealreadyboot,bootenable):

    if bootenable == 1:
        '''
        import time
        count = 0
        a = 6
        while (count < a):
            count_now = a - count
            print("please ctrl-c to exit this count=%d,time=%s\n"%(count_now,timealreadyboot))
            time.sleep(1)#sleep 1 second
            count += 1

        print('done')
        os.system('sudo reboot') 
        '''
        
        item = input('\n --Input item you want to test  || (bootcount='+str(timealreadyboot)+')\n')
    else:
        item = input('\n --Input item you want to test \n')

    for case in switch(item):
        if case('0'):
            print('== Test cpu and memory==')
            os.system('sudo stress --cpu 4 --vm-bytes 600M -i 1 -d 1 --hdd-bytes 512M &')
            os.system('top')
            os.system('sudo killall -9 stress')
            print('==CPU and memory \n\n\n==')
            break
        if case('1'):
            print('== please input mac address you want to set!\n\n\n==')
            print('\nFor Example,you should input like this->  0x000d4826c96e \n')
            
            thetext = input('\n\n please Enter mac address:\n\n')
            print(thetext)   
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 0 value 0xA5")

            print ("thetext[1]: ", thetext[2:4])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 1 value 0x" +  thetext[2:4])
            print ("thetext[2]: ", thetext[4:6])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 2 value 0x" +  thetext[4:6])

            print ("thetext[3]: ", thetext[6:8])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 3 value 0x" +  thetext[6:8])
            print ("thetext[4]: ", thetext[8:10])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 4 value 0x" +  thetext[8:10])
            print ("thetext[5]: ", thetext[10:12])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 5 value 0x" +  thetext[10:12])
            print ("thetext[6]: ", thetext[12:14])
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 6 value 0x" +  thetext[12:14])
            print ("\n")
              
            os.system("sudo ethtool -e eth0 ")
            print ("\n")

            

            break
        if case('2'):
            print('== Reading i2c dev from bus 1 ,0x4d ==\n\n')
            i2c_current_sensor()
            print('\n')
            break
        if case('3'):
            print('== Reading i2c dev from bus 1 ,0x4b==\n\n')
            i2c_voltage_sensor()
            print('\n')
            ''' 
            Ap Level:
            sudo apt-get install -y python-smbus
            sudo apt-get install -y i2c-tools
            /boot/config.txt
            dtparam=i2c_arm=on
            dtparam=i2c_vc=on
            dtparam=spi=on
            /etc/modules:
            i2c-bcm2708&nbsp;
            i2c-dev
            '''
            break
        if case('4'):
            # sudo apt-get update
            # sudo apt-get install build-essential python-dev python-openssl git
            #git clone https://github.com/adafruit/Adafruit_Python_DHT.git && cd Adafruit_Python_DHT
            #sudo python setup.py install
            #cd examples
            #sudo ./AdafruitDHT.py 11 4
            print('== Reading from DHT22:11 4~GPIO ==\n\n\n')
            print('=========================================')
            os.system('sudo /home/pi/test/Adafruit_Python_DHT/examples/AdafruitDHT.py 11 4')
            print('=========================================')
            print('done!\n')
            break
        if case('5'):
            print('== start lora_tx module ==')
            lora_tx()
            print("\n")
            break
        if case('6'):
            print('== start lora_rx module ==')
            lora_rx()
            print("\n \n")
            break
            
        if case('7'):
        
            print('== show SD card info ==')
            
            #EDIT /boot/config.txt to add these:dtoverlay=sdio,poll_once=off
            
            ret = exists('/dev/mmcblk1')
            
            if ret == 1:
                os.system('mount /dev/mmcblk1p2 /mnt')    
                os.system('touch /mnt/testSDCARD')  
                print("DEVICE :SD card is live,ok")
                os.system('rm /mnt/testSDCARD')  
                os.system('umount /mnt')  
                print("\n \n")
                
            else :
                print("Check SD card !,it does not exist")
                print("\n \n")
             
            break
        if case('8'):
            #https://www.raspberrypi.org/documentation/usage/webcams/
            # sudo apt-get install fswebcam 
            print('== Test USB camera now! this function also verify USB interface! ==')
            
            ret = exists('/dev/mmcblk1')
            
            if ret == 1:
                os.system('mount /dev/mmcblk1p1 /mnt')    
                os.system('fswebcam --skip 3 /mnt/SMG-01.jpg')
                os.system('umount /mnt')  
                print("\n\n We save picture named 'SMG-01.jpg' into /dev/mmcblk1p1 (/mnt), you can pull out sdcard to check picture if it exist!!")
                print("\n \n")
                
            else :
                print("\n\n Check your SD card !,we need to use sdcard to save picture to verify")
                print("\n \n")
            

            break
        if case('9'):
            #system("systemctl stop serial-getty@ttyAMA0.service");
            #system("systemctl disable serial-getty@ttyAMA0.service");
            #sudo apt install python3-pip   
            #sudo apt-get install python3-serial
            #pip3 install pyserial 
            #enable uart first! /boot/config enable_uart=1
            #serial-getty@ttyS0.service  
            #sudo systemctl disable serial-getty@ttyS0.service 
            print('== \n \n Test RS485 over UART now! ==') 
            print('== \n \n  Please open remote terminal to connect this unit first ==') 
            rs485_test()
            print("\n \n")
            break
            
        if case('10'):
            print('==\n  Test LTE! ==\n\n') 
            print('== please remeber to insert you sim card first==') 
            
            print('\n\n please wait for 16s to complete ppp0 connection!!!!\n\n ==')
            print('== if any error happening you will see a stop!\n\n ==')
            os.system('sudo pon 4GLTE & ')
            sleep(16)
            print("\n \n")
            ni.ifaddresses('ppp0')
            ip = ni.ifaddresses('ppp0')[ni.AF_INET][0]['addr']
             
            if (len(ip[2]) == 0):
                print('Could not find IP of interface %s. Failed !!!!.\n\n' % (ip))
            else :
                print('Can get IP from 4G LTE module %s. PASS !!!!.\n\n' % (ip))
                os.system('sudo route add default gw '+ ip)  
                os.system('sudo ping -c 20 8.8.8.8')
                os.system('sudo poff 4GLTE & ')
                print(" \n please wait to off line for 8S\n \n")
                sleep(8)
                print("\n please wait to off line for 4S\n \n")
                print("\n \n")
                break
            
        if case('79'):
            os.system("sudo ethtool -e eth0 ")
            print ("\n")
            for i in range(0x0200):
                 os.system("sudo ethtool -E eth0 magic 0x9500 offset %s value 0xff"%i)
                 print(i)
                  
            os.system("sudo ethtool -e eth0 ")     
            break             
        if case('65'):
            print('==\n  Test LTE part2 by python at command mode ! ==\n\n') 
            print('== please remeber to insert you sim card first==') 
            print('\n\n please wait for 16s to complete ppp0 connection!!!!\n\n ==')
            print('== if any error happening you will see a stop!\n\n ==')
            os.system('sudo pon 4GLTE & ')
            sleep(16)
            print("get interface...1\n \n")
            ans = ni.ifaddresses('ppp0')
            print("get interface...2\n \n")
            print(ans)
            print("get interface ip\n \n")
            ip = ni.ifaddresses('ppp0')[ni.AF_INET][0]['addr']
            print("check interface and interface ip\n \n") 
            if (len(ip[2]) == 0):
                print('Could not find IP of interface %s. Failed !!!!.\n\n' % (ip))
            else :
                print('Can get IP from 4G LTE module %s. PASS !!!!.\n\n' % (ip))
                os.system('sudo route add default gw '+ ip)  
                os.system('sudo ping -c 20 8.8.8.8')
                os.system('sudo poff 4GLTE & ')
                print(" \n please wait to off line for 8S\n \n")
                sleep(8)
                print("\n please wait to off line for 4S\n \n")
                print("\n \n")
            break
                
        if case('23'):
            print('==\n  Test LTE part2 by python at command mode ! ==\n\n') 
            print('== please remeber to insert you sim card first==') 
            print('\n\n please wait for 16s to complete ppp0 connection!!!!\n\n ==')
            print('== if any error happening you will see a stop!\n\n ==')
            os.system('sudo pon 4GLTE & ')
            sleep(16)
            print("get interface...1\n \n")
            ans = ni.ifaddresses('ppp0')
            print("get interface...2\n \n")
            print(ans)
            print("get interface ip\n \n")
            ip = ni.ifaddresses('ppp0')[ni.AF_INET][0]['addr']
            print("check interface and interface ip\n \n") 
            if (len(ip[2]) == 0):
                print('Could not find IP of interface %s. Failed !!!!.\n\n' % (ip))
            else :
                print('Can get IP from 4G LTE module %s. PASS !!!!.\n\n' % (ip))
                os.system('sudo route add default gw '+ ip)  
                os.system('sudo ping -c 20 8.8.8.8')
                os.system('sudo poff 4GLTE & ')
                print(" \n please wait to off line for 8S\n \n")
                sleep(8)
                print("\n please wait to off line for 4S\n \n")
                print("\n \n")
            break        
                
        if case('11'):
            #https://www.raspberrypi.org/forums/viewtopic.php?t=127042
            print('==\n enable and force into auto login mode ! ==\n\n') 
            print('==\n this entering also clean boot count! ==\n\n')           
            os.system('sudo cp /home/pi/test/getty@tty1.service.d/autologin.conf /etc/systemd/system/getty@tty1.service.d/noclear.conf')
            #https://www.raspberrypi.org/documentation/linux/usage/rc-local.md
            os.system(' sudo cp /home/pi/test/rc.local.autoup   /etc/rc.local')
            os.system(' sudo cp /home/pi/test/bashrcyes /home/pi/.bashrc')
            path = "/home/pi/bootcount"
            
            file = open(path, 'w+')
            file.write('0')
            file.close()      

            path = "/home/pi/bootenable"
            file = open(path, 'w+')
            file.write('1')
            file.close()  
            break
            
        if case('12'):
            print('==\n back to normal mode without auto login ! ==\n\n') 
            print('==\n this entering also clean boot count! ==\n\n') 
            os.system('sudo cp /home/pi/test/getty@tty1.service.d/noclear.conf /etc/systemd/system/getty@tty1.service.d/noclear.conf')   
            os.system(' sudo cp /home/pi/test/rc.local.ori   /etc/rc.local')
            path = "/home/pi/bootcount"
            os.system(' sudo cp /home/pi/test/bashrcno /home/pi/.bashrc')
            file = open(path, 'w+')
            file.write('0')
            file.close() 

            path = "/home/pi/bootenable"
            file = open(path, 'w+')
            file.write('0')
            file.close() 
            '''
            import time
            count = 0
            a = 6
            while (count < a):
                count_now = a - count
                print(count_now)
                print("\n please ctrl-c to exit this count\n")
                time.sleep(1)#sleep 1 second
                count += 1
                
            print('done')
            os.system('ls -la') 

            '''
            break
        if case('13'):
            # https://monkeyinmysoup.gitbooks.io/raspberry-pi/content/3.4-HDMI-output.html
            # https://github.com/LeipeLeon/PiPatternGenerator
            # http://yehnan.blogspot.com/2014/09/raspberry-pi.html
            # https://raspberrypi.stackexchange.com/questions/2169/how-do-i-force-the-raspberry-pi-to-turn-on-hdmi
            '''
            hdmi_force_hotplug=1
            hdmi_drive=2
            
            dmi_force_hotplug=1 sets the Raspbmc to use HDMI mode even if no HDMI monitor is detected. hdmi_drive=2 sets the Raspbmc to normal HDMI mode (Sound will be sent if supported and enabled). Without this line, the Raspbmc would switch to DVI (with no audio) mode by default.
            
            '''
            os.system('sudo fbi -T 1 -noverbose /home/pi/test/test.bmp -a')
         
            break
        if case('14'):
            ## https://www.raspberrypi.org/forums/viewtopic.php?t=210720
            print('==\n  Test GPIO 43 by setting on and off==\n\n') 
            pin=43 
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            for i in range(15):
                GPIO.output(pin, GPIO.LOW)
                sleep(1)
                GPIO.output(pin, GPIO.HIGH)
                sleep(1)

            GPIO.output(pin, GPIO.LOW)    
            GPIO.cleanup()
            break
        if case('15'):
            print('==\n  Test GPIO 42 by setting on and off==\n\n') 
            pin=42
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            for i in range(15):
                GPIO.output(pin, GPIO.LOW)
                sleep(0.5)
                GPIO.output(pin, GPIO.HIGH)
                sleep(0.5)

            GPIO.output(pin, GPIO.LOW)    
            GPIO.cleanup()
            break
        if case('16'):
            print('==\n  Test GPIO  by reading GPIO12/13 status==\n\n') 
            pin=12
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            #GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
            GPIO.setup(pin, GPIO.IN)
            print("read GPIO12 =",GPIO.input(pin)) 
            GPIO.cleanup()

            pin=13
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            #GPIO.setup(pin, GPIO.IN, GPIO.PUD_UP)
            GPIO.setup(pin, GPIO.IN)
            print("read GPIO13 =",GPIO.input(pin)) 
            GPIO.cleanup()
            print("\n\n\n")
        if case('17'):
            print('==\n  Test Network(ETH0) by requesting dhcp server to Ping 8.8.8.8==\n\n')
            os.system('sudo dhclient eth0')
            os.system('sudo dhclient eth0')
            time.sleep(2)
            response = os.system("ping -c 1 " + hostname)
            if response == 0:
                print ("\n  ETH0 is up!\n\n\n")
                break
            else:
                print ("\n  Etho is failed!\n\n\n")
            break
        if case('25'):
            print('== start lora_tx module ==')
            print('==\n  Enable GPIO39 for LORA PWR') 
            pin=39
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            
            print("\n")
            time.sleep(2)
            lora_tx()
            time.sleep(1)
            print('==\n  disable GPIO39 for LORA PWR') 
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            print("\n")
            
            break
        if case('26'):
            print('== start lora_rx module ==')
            print('==\n  Enable GPIO39 for LORA PWR') 
            pin=39
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            print("\n")
            time.sleep(2)
            lora_rx()
            time.sleep(1)
            print('==\n  disable GPIO39 for LORA PWR') 
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            
            
            print("\n \n")
            break

            
         if case('27'):
            print('== \n \n Test RS485 over UART now! ==') 
            print('== \n \n  Please open remote terminal to connect this unit first ==') 
            print('==\n  Enable GPIO5 for RS485 PWR') 
            pin=5
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            print("\n")
            time.sleep(2)
            rs485_test()
            time.sleep(1)
            print("\n \n")
            print('==\n  disable GPIO5 for RS485 PWR') 
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            print("\n \n")
            break
         if case('28'):
            print('==\n  Enable GPIO38 for LTE PWR') 
            pin=38
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(2)
            print('==\n  Test LTE! ==\n\n') 
            print('== please remeber to insert you sim card first==') 
            
            print('\n\n please wait for 16s to complete ppp0 connection!!!!\n\n ==')
            print('== if any error happening you will see a stop!\n\n ==')
            os.system('sudo pon 4GLTE & ')
            sleep(16)
            print("\n \n")
            ni.ifaddresses('ppp0')
            ip = ni.ifaddresses('ppp0')[ni.AF_INET][0]['addr']
             
            if (len(ip[2]) == 0):
                print('Could not find IP of interface %s. Failed !!!!.\n\n' % (ip))
            else :
                print('Can get IP from 4G LTE module %s. PASS !!!!.\n\n' % (ip))
                os.system('sudo route add default gw '+ ip)  
                os.system('sudo ping -c 20 8.8.8.8')
                os.system('sudo poff 4GLTE & ')
                print(" \n please wait to off line for 8S\n \n")
                sleep(8)
                print("\n please wait to off line for 4S\n \n")
                print("\n \n")
                break

                
            print('==\n  disable GPIO38 for LTE PWR') 
            import RPi.GPIO as GPIO
            GPIO.setwarnings(False) 
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            break   
                  
        if case('99'):
            print('==\n reboot system ! ==\n\n') 
          
            os.system('sudo reboot')   
           
            break
                 
        if case(''):
            print("bye!")
            print("\n \n")
            exit(1)
def main():
                
       #logging.info('Hello pi!')
       '''
       while(1):
            try:

            response = os.system("ping -c 1 " + hostname)
    
            #and then check the response...
            if response == 0:
                print ("host is up!")
                break
            else:
                print ("host is down!")
                sleep(5)
       '''     
       timealreadyboot = boottimes()
       bootenable = bootenables()
       enableUsbPwr()
       while(1):
            try:
              
              task_menu2(timealreadyboot,bootenable)
              
            except KeyboardInterrupt:
              print('interrupted!')
    
                          
                
if __name__ == "__main__":
    main()

