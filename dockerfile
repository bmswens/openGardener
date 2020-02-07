FROM raspbian/stretch

LABEL maintainer="Brandon Swenson (bmswens)" \
      version="1.0" \
      description="Docker container for running openGardener." \
      source="https://github.com/bmswens/openGardener"

EXPOSE 8080

RUN ["apt-get", "update"]
RUN ["useradd", "pi"]
RUN ["mkdir", "-p", "/opt/openGardener"]
RUN ["apt-get", "install", "-y", "curl", "python3.5", "python3-pip", "python3-venv", "unzip"]
RUN ["pip3", "install", "--upgrade", "pip"]
RUN ["ln", "-s", "/bin/python3.5", "/bin/python3"]
ADD static /opt/openGardener/static
ADD templates /opt/openGardener/templates
ADD system /opt/openGardener/system
ADD *.py /opt/openGardener/
ADD requirements.txt /opt/openGardener/requirements.txt
ADD README.md /opt/openGardener/README.md
ADD LICENSE.md /opt/openGardener/LICENSE.md
RUN ["bash", "/opt/openGardener/system/install.sh"]
ENTRYPOINT ["/opt/openGardener/venv/bin/python3", "/opt/openGardener/webapp.py"]