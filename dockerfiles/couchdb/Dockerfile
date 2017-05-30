FROM klaemo/couchdb:latest
RUN mv /etc/apt/sources.list.d/nodesource.list /etc/apt/sources.list.d/nodesource.list.disable
RUN apt-get update
RUN apt-get -y install apt-transport-https
RUN mv /etc/apt/sources.list.d/nodesource.list.disable /etc/apt/sources.list.d/nodesource.list
RUN apt-get  update
RUN curl -sL https://deb.nodesource.com/setup_7.x | bash -
RUN apt-get -y install nodejs
COPY local.ini /usr/local/etc/couchdb/local.d/
