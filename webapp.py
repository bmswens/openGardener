# standard
import json
import shutil
import os

# custom
import gardentools

# third party
import flask
import yaml

webapp = flask.Flask(__name__)
HOST = '127.0.0.1:8080'


@webapp.route('/')
def home():
    with open('logs/logs.json') as in_file:
        logs = [json.loads(line.replace('\n', '')) for line in in_file]
    logs.reverse()
    latest_image = None
    final_logs = []
    width = ''
    height = ''
    for row in logs:
        if row.get('photo'):
            row['photo_path'] = row['photo'][row['photo'].find('plant/') + 6:]
            if not latest_image:
                latest_image = '/static/img/plant/' + row['photo'][row['photo'].find('plant/') + 6:]
        if len(final_logs) < 5:
            final_logs.append(row)
    if not latest_image:
        latest_image = '/static/img/logo.png'
        width = '400'
        height = '400'
    return flask.render_template('home.html', HOST=HOST, logs=final_logs, latest_image=latest_image, width=width,
                                 height=height)


@webapp.route('/logs/text')
def text_logs():
    with open('logs/logs.json') as in_file:
        logs = [json.loads(line.replace('\n', '')) for line in in_file]
    logs.reverse()
    final_logs = []
    for row in logs:
        if row.get('photo'):
            row['photo_path'] = row['photo'][row['photo'].find('plant/') + 6:]
        final_logs.append(row)
    return flask.render_template('logs.html', HOST=HOST, logs=final_logs)


@webapp.route('/logs/photos')
def image_logs():
    with open('logs/logs.json') as in_file:
        logs = [json.loads(line.replace('\n', '')) for line in in_file]
    logs.reverse()
    photos = [[]]
    for row in logs:
        if row.get('photo'):
            photo = '/static/img/plant/' + row['photo'][row['photo'].find('plant/') + 6:]
            if len(photos[-1]) == 5:
                photos.append([])
            photos[-1].append(photo)
    return flask.render_template('photos.html', photos=photos)


@webapp.route('/settings', methods=['GET', 'POST'])
def settings():
    page = 'settings.html'
    if flask.request.method == 'POST':
        form = flask.request.form.to_dict()
        settings_dict = gardentools.form_to_dict(form)
        gardentools.settings_to_cron(settings_dict)
        settings_text = yaml.dump(settings_dict, default_flow_style=False)
        if os.path.exists('settings.yml'):
            shutil.move('settings.yml', 'settings.yml.old')
        with open('settings.yml', 'w') as output:
            output.write(settings_text)
        page = 'success.html'
    return flask.render_template(page, HOST=HOST)


@webapp.route('/api/img/<image>')
def serve_image(image):
    return flask.send_from_directory('static/img/plant', image)


if __name__ == '__main__':
    webapp.run(host=HOST.split(':')[0], port=HOST.split(':')[1])
