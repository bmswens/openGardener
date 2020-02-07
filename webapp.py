# standard
import shutil
import os

# custom
import gardentools

# third party
import flask
import yaml

webapp = flask.Flask(__name__)


@webapp.route('/')
def home():
    with gardentools.Logs('opengardener.db') as db:
        logs = db.get(5)
        latest_image = db.get_latest_image()
    height = ''
    width = ''
    if not latest_image or latest_image == '/static/img/plant/':
        latest_image = '/static/img/logo.png'
        width = '400'
        height = '400'
    return flask.render_template('home.html', logs=logs, latest_image=latest_image, width=width,
                                 height=height)


@webapp.route('/logs/text')
def text_logs():
    with gardentools.Logs() as db:
        logs = db.get()
    return flask.render_template('logs.html', logs=logs)


@webapp.route('/logs/photos')
def image_logs():
    with gardentools.Logs() as db:
        logs = db.get()
    logs = [log for log in logs if log.get('photo_path')]
    photos = [[]]
    for row in logs:
        if row.get('photo_path'):
            photo = row.get('photo_path')
            if len(photos[-1]) == 5:
                photos.append([])
            if photo != '/static/img/plant/':
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
    config = gardentools.get_config()
    if config and 'camera' in config:
        config['camera']['resolution'] = '{width}x{height}'.format(width=config['camera']['resolution'][0],
                                                                   height=config['camera']['resolution'][1])
    return flask.render_template(page, config=config)


@webapp.route('/api/img/<image>')
def serve_image(image):
    return flask.send_from_directory('static/img/plant', image)


@webapp.route('/about')
def about():
    return flask.render_template('about.html')


if __name__ == '__main__':
    if 'HOST' in os.environ:
        host = os.environ['HOST']
    else:
        host = '0.0.0.0'
    if 'PORT' in os.environ:
        port = os.environ['PORT']
    else:
        port = '8080'
    webapp.run(host=host, port=port)
