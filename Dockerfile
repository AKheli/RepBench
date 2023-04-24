FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1


WORKDIR /usr/src/app
EXPOSE 8000

# Installing scipy
#RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.7.1
## Installing other slow packages
#RUN pip3 install --no-cache-dir \
#    pandas==1.3.5 \
#    numpy==1.21.4 \
#    psycopg2-binary==2.9.1 \
#    scikit-learn==1.0.2 \
#    matplotlib==3.5.1 \
#    scikit-optimize==0.9.0
#
#
#RUN pip3 install --no-cache-dir \
#    FLAML==1.1.3\
#    tsfresh==0.20.0

# Installing requirements
COPY ./frozen_requirements.txt /usr/src/app

RUN apt-get update && apt-get install -y build-essential

RUN pip install -r /usr/src/app/frozen_requirements.txt

# updated conflicting requierement
RUN pip install --upgrade protobuf

COPY . /usr/src/app




