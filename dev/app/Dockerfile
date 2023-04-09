# This image must be built from the project root folder. In this case, use
# this script: docker build -t flakooo/myprojects:spotify-shuffler-app -f dev/app/Dockerfile .
FROM python:3.12-rc-bullseye
RUN mkdir /opt/spotify-shuffler
WORKDIR /opt/spotify-shuffler

# Copies and installs requirements.txt
COPY requirements.txt .
RUN pip3 install -r requirements.txt


# Copies files and sets permissions to be executable.
COPY dev/app/*.sh /
RUN chmod +x /*.sh

# Run a file script.
CMD /docker-start.sh