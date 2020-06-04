#!/usr/bin/python3
# standard
import datetime
import re

# custom
import gardentools

# raspberry pi specific
import RPi.GPIO as GPIO

# third party
import requests


def get_time(line):
    time_regex = re.compile('[0-9]{1,2}:[0-9]{2}:[0-9]{2}')
    match = re.findall(time_regex, line)[0]
    times = [int(n) for n in match.split(':')]
    now = datetime.datetime.now()
    hour = times[0]
    minute = times[1]
    second = times[2]
    if 'sunset' in line.lower():
        hour += 12
    return datetime.datetime(now.year, now.month, now.day, hour, minute, second)


def time_is_appropriate(config):
    now = datetime.datetime.now()
    start = config['light'].get('start')
    stop = config['light'].get('stop')
    location = config['light'].get('location')
    if ':' in start:
        start = datetime.datetime(now.year, now.month, now.day, int(start.split(':')[0]), int(start.split(':')[1]))
    elif start == 'sunrise' and location:
        response = requests.get('https://sunrise-sunset.org/search?location={}'.format(location))
        for line in response.text.split('\n'):
            if 'Sunrise time:' in line:
                start = get_time(line)
                break
    if ':' in stop:
        stop = datetime.datetime(now.year, now.month, now.day, int(stop.split(':')[0]), int(stop.split(':')[1]))
    elif stop == 'sunset' and location:
        response = requests.get('https://sunrise-sunset.org/search?location={}'.format(location))
        for line in response.text.split('\n'):
            if 'Sunset time:' in line:
                stop = get_time(line)
                break
    # if they have incorrectly set their times, we'll just proceed anyways
    if not start or not stop or start == stop or start > stop:
        return True
    if start <= now < stop:
        return True
    else:
        return False


def main():
    config = gardentools.get_config()
    pin = config['light']['pin']
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    if time_is_appropriate(config):
        GPIO.output(pin, 0)
        on = True
    else:
        GPIO.output(pin, 1)
        on = False
    return on


if __name__ == '__main__':
    main()
