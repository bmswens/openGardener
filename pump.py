#!/usr/bin/python3

# standard
import time

# custom
import gardentools
import camera

# raspberry pi specific
import RPi.GPIO as GPIO


def pump():
    config = gardentools.get_config()
    pin = config['pump']['pin']
    duration = config['pump']['duration']
    GPIO.setup(pin, GPIO.OUT, initial=1)
    GPIO.output(pin, 0)
    time.sleep(duration)
    GPIO.output(pin, 1)
    watered = True
    return watered


def main():
    config = gardentools.get_config()
    GPIO.setmode(GPIO.BOARD)
    watered = pump()
    if config['camera']['enabled'] and config['camera']['frequency'] == 'on pump':
        photo = camera.take_picture()
    else:
        photo = 'N/A'
    gardentools.log('N/A', watered, photo)


if __name__ == '__main__':
    main()
