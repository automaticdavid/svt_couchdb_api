FROM 	python:3.6-alpine
RUN	mkdir /base
COPY	. /base
RUN	apk update "$(< /base/apk.txt)"
RUN 	pip install -r /base/requirements.txt
