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
	print("we use [%s] to test"%ser.name)         # check which port was really used
	ser.write(b'\n\rif you see from remote machine,\n\rplease enter [ exit ] to return!"')
	
	state = ser.read(4)
	readback = state.decode('utf-8','ignore')
	bytes.decode(state)

	#print (readback)
	if readback.find("exit") >= 0:
            	print('== we get return AND it is we expect, Pass!! ')	
		
	else :
		print('== we get return, but it is not we expect, failed!! ')		
	ser.close() 
	
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
        print("read word date in Dec={%d},in hex={%x} "%(rd,rd)) 
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
        print("read word date in Dec={%d},in hex={%x} "%(rd,rd)) 
        print(datetime.datetime.now())
        #t += 0.000001
        time.sleep(t)
        counter += 1

def task_menu():


    menu = {
        1: "Modify Mac address",
        2: "Show Current sensor info",
        3: "Show Voltage sensor info",
        4: "Test DHT11/22",
        5: "Test LoRa function over UART0 TX",
        6: "Test LoRa function over UART0 Rx",
        7: "Test SD CARD",
        8: "Test USB Camera",
        9: "Test RS485 function over UART1"
        0: "Test LTE function (network)"
    }

    for i in menu:
     
        print ("(%d) [%s]\n"%(i,menu[i]))
    lst = print_menu()
    print(lst)
 
def task_menu2():

    startShow()
    menu = {
        1: "Modify Mac address",
        2: "Show Current sensor info",
        3: "Show Voltage sensor info",
        4: "Test DHT11/22",
        5: "Test LoRa function over UART0 TX",
        6: "Test LoRa function over UART0 Rx",
        7: "Test SD CARD",
        8: "Test USB Camera",
        9: "Test RS485 function over UART1"
        0: "Test LTE function (network)"
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
        if case('1'):
            print('== Reading from DHT22:11 4~GPIO ==')
            os.system('i2cdetect -l')
            break
        if case('2'):
            print('== Reading i2c dev from bus 1 ,0x4d ==')
            i2c_current_sensor()
            print('\n')
            break
        if case('3'):
            print('== Reading i2c dev from bus 1 ,0x4b==')
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
            print('== Reading from DHT22:11 4~GPIO ==')
            os.system('sudo /home/pi/test/Adafruit_Python_DHT/examples/AdafruitDHT.py 11 4')
            print('\n') 
            print("\n")
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
            print('== Test USB camera now! ==') 
            ret = exists('/dev/mmcblk1')
            
            if ret == 1:
                os.system('mount /dev/mmcblk1p2 /mnt')    
                os.system('fswebcam /mnt/image.jpg')
                os.system('umount /mnt')  
                print("We save picture to /dev/mmcblk1p2 (/mnt), you can poweroff and pull out sdcard to check picture!")
                print("\n \n")
                
            else :
                print("Check SD card !,we need to use sdcard to save picture")
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
            print('== Test RS485 over UART now! ==') 
            print('== Please open remote terminal to connect this unit first ==') 
            rs485_test()
            print("\n \n")
            break
        if case('10'):
            print('== Test LTE! ==\n\n') 
            print('== please insert you sim card first==') 
            

            print("\n \n")
            break            
            
        if case(''):
            print("bye!")
            print("\n \n")
            exit(1)
def main():
                
       #logging.info('Hello pi!')
       
       while(1):
            
            response = os.system("ping -c 1 " + hostname)
    
            #and then check the response...
            if response == 0:
                print ("host is up!")
                break
            else:
                print ("host is down!")
                sleep(5)
       while(1):
            try:
              
              task_menu2()
              
            except KeyboardInterrupt:
              print('interrupted!')
    
                          
                
if __name__ == "__main__":
    main()

