#!/usr/bin/python3

# custom
import camera
import pump
import gardentools

# raspberry pi specific
import RPi.GPIO as GPIO


def main():
    config = gardentools.get_config()
    moisture_pin = config['moisture_sensor']['pin']
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(moisture_pin, GPIO.IN, GPIO.PUD_DOWN)
    dry = GPIO.input(moisture_pin)
    if dry:
        dry = True
        if config['pump']['enabled'] and config['pump']['frequency'] == 'when dry':
            watered = pump.pump()
        else:
            watered = 'N/A'
        if config['camera']['enabled'] and config['pump']['frequency'] == 'when dry':
            photo = camera.take_picture()
        else:
            photo = None
    else:
        dry = False
        watered = 'N/A'
        photo = None
    gardentools.log(dry, watered, photo)


if __name__ == '__main__':
    main()
