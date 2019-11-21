#!/usr/bin/env bash
# get current directory and cd into openGardener directory
starting_directory=$(pwd)
directory="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd ${directory}
cd ..
mkdir logs
touch logs/logs.json
# setup python3 venv
python3 -m venv --system-site-packages venv
. venv/bin/activate
pip3 install -r requirements.txt
deactivate
# download and unpack boostrap, jquery, and popper
cd static
mkdir css js
curl -L https://github.com/twbs/bootstrap/releases/download/v4.0.0/bootstrap-4.0.0-dist.zip > bootstrap.zip
curl https://code.jquery.com/jquery-3.4.1.slim.min.js > js/jquery.slim.min.js
curl https://unpkg.com/popper.js@1.16.0/dist/umd/popper.min.js > js/popper.min.js
curl https://www.stickpng.com/assets/images/5847f98fcef1014c0b5e48c0.png > img/github.png
curl https://cdn.iconscout.com/icon/free/png-512/trello-1-432474.png > img/trello.png
unzip bootstrap.zip
cd ..
# finalize our service file and copy it to systemd
echo "WorkingDirectory=$(pwd)" >> system/openGardener.service
echo "ExecStart=$(pwd)/venv/bin/python3 $(pwd)/webapp.py" >> system/openGardener.service
cp system/openGardener.service /etc/systemd/system/openGardener.service
systemctl enable openGardener
systemctl start openGardener
# this was run as root, so let's give ownership back to pi
chown pi:pi -R .
cd ${starting_directory}