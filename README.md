<img src="https://raw.githubusercontent.com/bmswens/openGardener/master/static/img/logo.png" alt="logo" width="200">

# openGardener

A project for automatically taking care of plants in your house.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

This project is designed to be run on a Raspberry Pi and uses Raspberry Pi specific modules like RPi.GPIO and picamera.
As such, it may not run correctly on other systems.

All Python requirements can be found in ```requirements.txt```, but do not have to be reinstalled.

### Currently Supported Components

* Moisture Sensor
* Water Pump
* Camera (plugged in via ribbon cable)

### Installing

#### Container

The container can be pulled directly from [docker hub](https://hub.docker.com/repository/docker/bmswens/opengardener)
or you can build it yourself using the supplied dockerfile.

Recommended docker use:
```
docker run \
-p 8080:8080 \
-v host/path/to/database.sqlite3:/opt/openGardener/opengardener.db \
-v host/path/to/picture_folder:/opt/openGardener/static/img/plant \
-d \
bmswens/opengardener
```


#### Direct Install

Installation is designed to be easy, but does require root access.

Before running anything as root, I recommend familiarizing yourself with the commands to be run.

##### Steps

openGardener can be installed anywhere, but ```/opt``` is a very good place for it.

```
cd /opt
git clone https://github.com/bmswens/openGardener.git
cd openGardener
```

Modify the HOST setting in webapp.py to match the IP and port that you wish to host on.
You may keep it as localhost if you only plan to access it locally, or are going to enable port forwarding. 

```
bash system/install.sh
```

After it finishes installing you will need to set up your configuration at ```http://ip:port/settings``` before
the system finishes setting up the cronjobs.

## Built With

* [Python](https://www.python.org/) - Primary language
* [Flask](https://www.palletsprojects.com/p/flask/) - The web framework used


## Authors

* **Brandon Swenson**- *Initial work* - [bmswens](https://github.com/bmswens)

## License

This project is licensed under the GNU GPLv3 - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* My wife, for forcing me to take care of her plants while she's away.
