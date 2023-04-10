# This image must be built from the project root folder. In this case, use
# this script: docker build -t flakooo/myprojects:spotify-shuffler-webpack -f dev/webpack/Dockerfile .
FROM node:19-bullseye

# Copies files and sets permissions to be executable.
COPY dev/webpack/*.sh /
RUN chmod +x /*.sh

# Run a file script.
CMD /docker-start.sh
