FROM python:3.7

WORKDIR /usr/src/app

# https://ruddra.com/docker-reduce-build-time-for-data-science-packages/
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Installing scipy
RUN pip3 install --no-cache-dir --disable-pip-version-check scipy==1.3.1

# Installing
RUN pip3 install --no-cache-dir \
    pandas==0.25.2 \
    numpy==1.17.3 \
    psycopg2==2.8.4 \
    scikit-learn==0.21.3 \
    matplotlib==3.1.1 \
    scikit-optimize




COPY ./requirements.txt /usr/src/app
RUN pip3 install -r requirements.txt

# copy project
COPY . /usr/src/app

COPY ./entrypoint.sh /usr/src/app
ENTRYPOINT ["sh", "/usr/src/app/entrypoint.sh"]
