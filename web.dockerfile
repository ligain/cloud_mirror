FROM python:3.7

ADD . /opt/cloud_mirror
WORKDIR /opt/cloud_mirror

RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.7
RUN pip3 install pipenv && set -ex && pipenv install --deploy --system

EXPOSE 8080

ENTRYPOINT gunicorn -c ./config/gunicorn.py main:create_app

