#!/usr/bin/python3

# standard
import datetime
import os
import time

# custom
import gardentools

# raspberry pi specific
from picamera import PiCamera

NOW = datetime.datetime.now()
BASE_DIR = os.path.split(__file__)[0]


def get_photo_path(folder='{BASE_DIR}/static/img/plant'.format(BASE_DIR=BASE_DIR)):

    if not os.path.isdir(folder):
        os.makedirs(folder)
    file_name = '{}-{:02d}-{:02d}T{:02d}:{:02d}.jpg'.format(NOW.year, NOW.month, NOW.day, NOW.hour, NOW.minute)
    photo_path = os.path.join(folder, file_name)
    return photo_path


def take_picture(f=get_photo_path()):
    config = gardentools.get_config()
    camera = PiCamera()
    camera.resolution = config['camera']['resolution']
    camera.rotation = config['camera']['rotation']
    camera.start_preview()
    time.sleep(2)
    camera.capture(f)
    camera.stop_preview()
    return f


def main():
    picture = take_picture()
    gardentools.log('N/A', 'N/A', picture)


if __name__ == '__main__':
    main()
