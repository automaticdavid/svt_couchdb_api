FROM 	python:3.6-alpine
ARG 	SERVICE_NAME
ARG 	SERVICE_VERSION
ENV 	SERVICE_NAME $SERVICE_NAME
ENV 	SERVICE_VERSION $SERVICE_VERSION
RUN	apk update && apk add curl && apk add bash
RUN 	mkdir /app
COPY 	. /app
RUN 	pip install -r /app/requirements.txt
RUN     pip install gunicorn
RUN	chmod 755 /app/boot.sh
WORKDIR	/app/app
CMD	["/app/boot.sh"]
