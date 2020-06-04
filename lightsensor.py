#!/usr/bin/python3
# standard
import datetime

# custom
import gardentools
import light

# raspberry pi specific
import RPi.GPIO as GPIO


def main():
    config = gardentools.get_config()
    pin = config['light_sensor']['pin']
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.IN, GPIO.PUD_DOWN)
    dark = GPIO.input(pin)
    if dark:
        dark = True
        if config['light']['enabled'] and config['light']['frequency'] == 'when dark':
            light_enabled = light.main()
        else:
            light_enabled = None
    else:
        dark = False
        light_enabled = None
    with gardentools.Logs('opengardener.db') as db:
        db.write(dark=dark, light_enabled=light_enabled)


if __name__ == '__main__':
    main()
