FROM python:3.7

ADD . /opt/cloud_mirror
WORKDIR /opt/cloud_mirror
ENV PYTHONPATH /opt/cloud_mirror

RUN curl --silent https://bootstrap.pypa.io/get-pip.py | python3.7
RUN pip3 install pipenv && set -ex && pipenv install

ENTRYPOINT pipenv run python ./core/run_fetchers.py