# This image must be built from the project root folder. In this case, use
# this script: docker build -t flakooo/myprojects:spotify-shuffler-db -f dev/db/Dockerfile .
FROM mariadb:10.6

COPY dev/db/*.sh dev/db/*.sql /
RUN chmod +x /*.sh