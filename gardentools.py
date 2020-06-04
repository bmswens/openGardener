# The purpose of this file is to keep webapp.py more clean

# standard
import os
import datetime
import sqlite3

# third party
import yaml

# keeps time standard
NOW = datetime.datetime.now()
BASE_DIR = os.path.split(os.path.realpath(__file__))[0]


class Logs:

    def __init__(self, path='opengardener.db'):
        self.db = sqlite3.connect(path)
        self.cursor = self.db.cursor()
        self.columns = [
            "datetime",
            "dry",
            "watered",
            "dark",
            "photo_path",
        ]

        self.cursor.execute('CREATE TABLE IF NOT EXISTS garden_logs ('
                            '{}, '
                            '{}, '
                            '{}, '
                            '{}, '
                            '{} TEXT)'.format(*self.columns))

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.db.commit()
        self.db.close()
        return True

    def write(self, **kwargs):
        kwargs['datetime'] = datetime.datetime.now().isoformat()
        data = [kwargs.get(column) for column in self.columns]
        self.cursor.execute('INSERT INTO garden_logs VALUES (?, ?, ?, ?, ?)', data)

    def get(self, limit=None):
        data = []
        if limit:
            query = 'SELECT * from garden_logs LIMIT {limit}'.format(limit=limit)
        else:
            query = 'SELECT * from garden_logs'
        for row in self.cursor.execute(query):
            record = {}
            for index, header in enumerate(self.columns):
                if header == 'datetime':
                    record[header] = datetime.datetime.strptime(row[index], '%Y-%m-%dT%H:%M:%S.%f')
                elif header == 'photo_path':
                    record[header] = self.clean_path(row[index])
                else:
                    record[header] = self.clean(row[index])
            data.append(record)
        return data

    @staticmethod
    def clean(data):
        if data is None:
            return "N/A"
        else:
            return bool(data)

    @staticmethod
    def clean_path(photo_path):
        if photo_path:
            return photo_path[photo_path.find('/static'):]
        else:
            return 'N/A'

    def get_latest_image(self):
        query = 'SELECT * FROM garden_logs WHERE photo_path IS NOT NULL LIMIT 1'
        results = [path for path in self.cursor.execute(query)]
        if not results:
            return None
        else:
            row = results[0]
            photo_path = self.clean_path(row[3])
            return photo_path


def get_config(f='settings.yml'):
    try:
        with open(f) as in_file:
            config = yaml.safe_load(in_file.read())
        return config
    except FileNotFoundError:
        return {}


def assign_type(value):
    """
    For casting values returned form settings forms.
    :param value:
    :return value as correct Python type:
    """
    if value.isnumeric():
        value = int(value)
    elif value == 'on':
        value = True
    elif value == 'off':
        value = False
    elif 'x' in value:
        value = [int(v) for v in value.split('x')]
    return value


def form_to_dict(form):
    """
    Takes an HTTP form response and casts it to a nested dict to be converted to .yaml
    :param form:
    :return settings:
    """
    settings = {}
    for key in form:
        value = assign_type(form[key])
        if '.' in key:
            keys = key.split('.')
            if keys[0] not in settings:
                settings[keys[0]] = {}
            settings[keys[0]][keys[1]] = value
    for mod in settings:
        if not settings[mod].get('enabled'):
            settings[mod]['enabled'] = False
    return settings


def settings_to_cron(settings, cron_file='/etc/cron.d/openGardener'):
    """
    Takes settings dict and writes a valid cron file on it to /etc/cron.d/
    :param settings:
    :param cron_file: Where to put the crontab
    :return:
    """
    scripts = {
        'camera': os.path.join(BASE_DIR, 'camera.py'),
        'moisture_sensor': os.path.join(BASE_DIR, 'moisture.py'),
        'pump': os.path.join(BASE_DIR, 'pump.py'),
        'light_sensor': os.path.join(BASE_DIR, 'lightsensor.py'),
        'light': os.path.join(BASE_DIR, 'light.py')
    }
    jobs = []
    for setting in scripts:
        enabled = settings[setting].get('enabled')
        frequency = settings[setting].get('frequency')
        cd = 'cd {BASE_DIR} &&'.format(BASE_DIR=BASE_DIR)
        python = '{BASE_DIR}/venv/bin/python3'.format(BASE_DIR=BASE_DIR)
        script = scripts[setting]
        if enabled and ':' in frequency:
            hours, minutes = frequency.split(':')
            hours = int(hours)
            minutes = int(minutes)
            if hours <= 1:
                hours = ''
            else:
                hours = '/{hours}'.format(hours=hours)
            if minutes <= 1:
                minutes = ''
            else:
                minutes = '/{minutes}'.format(minutes=minutes)
            cronjob = '*{minutes} *{hours} * * * pi {cd} {python} {script}'.format(
                hours=hours,
                minutes=minutes,
                script=script,
                cd=cd,
                python=python
            )
            jobs.append(cronjob)
    with open(cron_file, 'w') as output:
        output.write(
            "# cronjob generated by settings passed via openGardener's web interface\n"
            "SHELL=/bin/sh\n"
            "PATH=/etc:/bin:/sbin:/usr/bin:/usr/sbin\n"
        )
        for cronjob in jobs:
            output.write('{cronjob}\n'.format(cronjob=cronjob))
        output.write('\n')
