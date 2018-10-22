# ADC3a.py

import smbus
import time
import datetime


bus = smbus.SMBus(1) # RPi revision 2 (0 for revision 1)
i2c_address = 0x4d  # default address

t = 0.000001
while True:
# Reads word (2 bytes) as int
    rd = bus.read_word_data(i2c_address, 0)
    block = bus.read_i2c_block_data(i2c_address, 0, 2)
    print(block)
    # Returned value is a list of 16 bytes
# Exchanges high and low bytes
    #data = ((rd & 0xFF) << 8) | ((rd & 0xFF00) >> 8)
# Ignores two least significiant bits
    #data = data >> 2
    print("read word date in Dec={%d},in hex={%x},time duration={%2f} "%(rd,rd,t)) 
    print(datetime.datetime.now())
    #t += 0.000001
    #time.sleep(t)
    
