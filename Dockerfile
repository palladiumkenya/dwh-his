# base image
FROM python:3.10
# setup environment variable
ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install dependencies
RUN pip install --upgrade pip
# copy whole project to your docker home directory.
COPY . $DockerHOME
RUN apt-get update -qq && \
apt-get install -y --no-install-recommends \
libmpc-dev \
libgmp-dev \
libmpfr-dev \
unixodbc-dev
# run this command to install all dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r requirements.txt
# port where the Django app runs
EXPOSE 8000
# start server
CMD python manage.py runserver