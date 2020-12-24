#!/usr/bin/env python
'''
sudo apt install python3-pip
sudo pip3 install Jetson.GPIO
sudo groupadd -f -r gpio
sudo usermod -a -G gpio YOUR-USER-NAME-HERE

Link: https://github.com/NVIDIA/jetson-gpio
Ref Doc: Jetson.GPIO.pdf
'''



import RPi.GPIO as GPIO
import time
output_pin = 4 # BOARD pin 7, BCM pin 4
def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)
    print("Press CTRL+C to exit")
    curr_value = GPIO.HIGH
    try:
        while True:
            time.sleep(1)
            # Toggle the output every second
            print("Outputting {} to pin {}".format(curr_value, output_pin))
            GPIO.output(output_pin, curr_value)
            curr_value ^= GPIO.HIGH
    finally:
        GPIO.cleanup()
if __name__ == '__main__':
 main()
