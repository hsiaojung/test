'''
2018/10/03 made by Cyril Chang 
v0.1
'''
import subprocess
import decimal
import re
import sys
from time import sleep
from threading import Thread
import os
import sys, signal
import time
import serial

import smbus
import time
import datetime

import netifaces as ni


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
    print("##                                                                  #-\n")
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
def task_menu2():

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
        10:" Test LTE network"
    }
    while True:


    
        ()
        for i in menu:
     
            print ("(%d) [%s]"%(i,menu[i]))
       
        lst = print_menu2()

def exists(path):
    """Test whether a path exists.  Returns False for broken symbolic links"""
    try:
        os.stat(path)
    except OSError:
        return False
    return 1


def print_menu2():

      
    item = input('\n --Input item you want to test.....\n')
  
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
            os.system("sudo ethtool -E eth0 magic 0x9500 offset 0 value 0xA5" +  thetext[2:4])

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
                os.system('fswebcam /mnt/SMG-01.jpg')
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
            
            print('== \n\n please wait for 16s to complete ppp0 connection!!!!\n\n ==')
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
        if case('19'):
            os.system("sudo ethtool -e eth0 ")
            print ("\n")
            for i in range(0x0200):
                 os.system("sudo ethtool -E eth0 magic 0x9500 offset %s value 0xff"%i)
                 print(i)
                  
            os.system("sudo ethtool -e eth0 ")     
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
       while(1):
            try:
              
              task_menu2()
              
            except KeyboardInterrupt:
              print('interrupted!')
    
                          
                
if __name__ == "__main__":
    main()

