
# base image
FROM python:3.10
# setup environment variable
#ENV DockerHOME=/home/project

# set work directory RUN mkdir -p $DockerHOME
RUN mkdir /project

# where your code lives  WORKDIR $DockerHOME
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD . /project/

# install dependencies
RUN pip install --upgrade pip

RUN apt-get update -qq && \
apt-get install -y --no-install-recommends \
libmpc-dev \
libgmp-dev \
libmpfr-dev \
unixodbc-dev
# run this command to install all dependencies
ADD requirements.txt /project
RUN pip install -r requirements.txt
RUN pip install mysqlclient
RUN pip install XlsxWriter

ADD entrypoint.sh /project
RUN chmod +x *.sh

# copy whole project to your docker home directory. COPY . $DockerHOME
COPY . /project
#RUN mkdir -p /tmp/app/webapp/mysqld && chmod -R 777 /tmp/app/webapp/mysqld
#ADD mfldbdump.sql /docker-entrypoint-initdb.d

ADD updated_db_data.json /project

# port where the Django app runs
EXPOSE 8000
# start server
#CMD python manage.py makemigrations
CMD python manage.py migrate
CMD python manage.py loaddata updated_db_data.json
CMD python manage.py runserver 0.0.0.0:8000

