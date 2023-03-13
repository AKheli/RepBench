FROM python:3.9-slim

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1


#EXPOSE 8000

# Installing scipy
RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.7.1

# Installing other slow packages
RUN pip3 install --no-cache-dir \
    pandas==1.3.5 \
    numpy==1.21.4 \
    psycopg2-binary==2.9.1 \
    scikit-learn==1.0.2 \
    matplotlib==3.5.1 \
    scikit-optimize==0.9.0

# Installing requirements
COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

#RUN mkdir -p /vol/web/static && \
#    mkdir -p /vol/web/media && \
#    chown -R app:app /vol && \
#    chmod -R 755 /vol

COPY . /usr/src/app

#sudo docker-compose build --no-cache web
#sudo docker-compose up web
