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




def signal_handler(signal, frame):
    print("\nprogram exiting gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)



hostname = "8.8.8.8" #example

v1_index = 20
r1_indexh = 21
r1_indexl = 22
bvrctotal = 24

ti_index = 20
temp_index = 20
time_index = 20

parameter_vr = []
parameter_ti = []
parameter_ta = []


ticmd = ['mbpoll', '-1', '-P N', '-b 9600', '-a 247','-r 49', '-t 3:hex','-c 2','/dev/ttyUSB0']
testmd = ['mbpoll', '-1']
bvrcmd =  ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 1', '-t 3:hex', '-c 24',  '/dev/ttyUSB0']
timecmd = ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 81', '-t 3:hex', '-c 4',  '/dev/ttyUSB0']
btempcmd = ['mbpoll','-1','-P N', '-b 9600', '-a 247', '-r 17', '-t 3:hex', '-c 8',  '/dev/ttyUSB0']

# out_bytes = subprocess.call(cmd)
# out_bytes = response = subprocess.check_output(cmd, shell=True)
# out_bytes = response = subprocess.check_output(cmd2, shell=False)
# https://stackoverflow.com/questions/32942207/python-subprocess-calledprocesserror-command-returned-non-zero-exit-s

#  Python cookbook  https://python3-cookbook.readthedocs.io/zh_CN/latest/chapters/p02_strings_and_text.html
#  Python tutorial  http://www.runoob.com/python/python-tutorial.html
#  Python string:   https://www.tutorialspoint.com/python3/python_strings.htm

outbvr= b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 1, count = 24\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[1]: \t0x0002\n[2]: \t0x0000\n[3]: \t0x0000\n[4]: \t0x0002\n[5]: \t0x0000\n[6]: \t0x0000\n[7]: \t0x0002\n[8]: \t0x0000\n[9]: \t0x0000\n[10]: \t0x0002\n[11]: \t0x0000\n[12]: \t0x0000\n[13]: \t0x0002\n[14]: \t0x0000\n[15]: \t0x0000\n[16]: \t0x0001\n[17]: \t0x0000\n[18]: \t0x0000\n[19]: \t0x0002\n[20]: \t0x0000\n[21]: \t0x0000\n[22]: \t0x0002\n[23]: \t0x0000\n[24]: \t0x0000\n\n"
outtime = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 81, count = 4\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[81]: \t0x07E1\n[82]: \t0x0103\n[83]: \t0x061B\n[84]: \t0x2000\n\n"
outbtemp = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 17, count = 8\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[17]: \t0x0005\n[18]: \t0x0004\n[19]: \t0x0005\n[20]: \t0x0005\n[21]: \t0x0005\n[22]: \t0x0006\n[23]: \t0x0005\n[24]: \t0x0006\n\n"
outti = b"mbpoll 1.4 - FieldTalk(tm) Modbus(R) Master Simulator\nCopyright \xc2\xa9 2015-2018 Pascal JEAN, https://github.com/epsilonrt/mbpoll\nThis program comes with ABSOLUTELY NO WARRANTY.\nThis is free software, and you are welcome to redistribute it\nunder certain conditions; type 'mbpoll -w' for details.\n\nProtocol configuration: Modbus RTU\nSlave configuration...: address = [247]\n                        start reference = 49, count = 2\nCommunication.........: /dev/ttyUSB1,       9600-8N1 \n                        t/o 1.00 s, poll rate 1000 ms\nData type.............: 16-bit register, input register table\n\n-- Polling slave 247...\n[49]: \t0x0017\n[50]: \t0x0147\n\n"

def readBTS():


    process =  subprocess.Popen(ticmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    returncode = process.wait()
    
    outti_485 = process.stdout.read()
    #outti_485 = process.stdout.read().decode("utf-8")
    #print ("outti_485=%s"%outti_485)

    process =  subprocess.Popen(bvrcmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    returncode = process.wait()
    outbvr_485 = process.stdout.read()
    #outbvr_485 = process.stdout.read().decode("utf-8")
    #print ("outbvr_485=%s"%outbvr_485)

    process =  subprocess.Popen(btempcmd, stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    returncode = process.wait()
    outbtemp_485 = process.stdout.read()
    #outbtemp_485 = process.stdout.read().decode("utf-8")
    #print ("outbtemp_485=%s"%outbtemp_485)
    return outti_485,outbvr_485,outbtemp_485,1
    

	
def parseBTS(command,parameter,index):

  
	output = command.decode("utf-8")
	output = output.replace('\t',' ')
	output = output.replace('\n',':')
	#print(output)
	output = output.split(':')
	a = output


	#print( len(a))                        
	for x  in range(index, len(a) -1,2): 
		totalCount = a[x]
		totalCount = totalCount[2:]
		print ('totalCount:', totalCount)
		hextoint = int(totalCount,16) 
		print ('hextoint:', hextoint)
		parameter.append(hextoint)

	print (parameter) 


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
            
def rs485_test():

    
    ser = serial.Serial('/dev/ttyS0',baudrate=9600,timeout=1)
    baton  = 0
    cycle  = 1
    count = 0
    while True:
            count = count + 1
            
    
            if count > 8 :
                break
            print("writing baton={}".format(baton))
            ser.write((str(baton) + '\n').encode("utf-8"))
            #line = ser.readline()
            #print (line)
            
            
def startShow():

    print("#######################################################################-\n")
    print("##                                                                  #-\n")
    print("##  SMG01's fnction Test Item                                       #-\n")
    print("##                                                                  #-\n")
    print("#######################################################################-\n")
            
 
def task_menu():


    menu = {
        1: "Test info",
        2: "Test I2C0 function",
        3: "Test I2C1 function",
        4: "Test DHT11/22",
        5: "Test LoRa function over UART0",
        6: "Test ........?",
        7: "Test SD CARD",
        8: "Test USB Camera",
        9: "Test RS485 function over UART1"
    }

    for i in menu:
     
        print ("(%d) [%s]\n"%(i,menu[i]))
    lst = print_menu()
    print(lst)
 
def task_menu2():

    startShow()
    menu = {
        1: "Show i2c  info",
        2: "Test I2C0 function",
        3: "Test I2C1 function",
        4: "Test DHT11/22",
        5: "Test LoRa function over UART0",
        6: "Test MEM",
        7: "Test SD CARD",
        8: "Test USB Camera",
        9: "Test RS485 function over UART1",
       10: "Test WiFI"
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
            print('== Reading i2c dev from bus 0 ==') 
            os.system('i2cdetect -r -y 0')
            print('\n')
            break
        if case('3'):
            print('== Reading i2c dev from bus 1 ==') 
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
            os.system('i2cdetect -r -y 1')
            os.system('i2cdump  -y 1 0x5c')
            print('\n')
            print('\n')
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
            os.system('LoRa!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')
            print("\n")
            print("\n")
            break
        if case('6'):
            print("== Test and show MEM ==")
            os.system('free')
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
                print("We save picture to /dev/mmcblk1p2 (/mnt), you can poweroff and pull out sdcard to check picturec!")
                print("\n \n")
                
            else :
                print("Check SD card !,we need to usesdcard to save picture")
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
            print('== Test WiFi  now! ==') 


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

