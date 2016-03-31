FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask

# Install the LabSuite repo from Git.
# TODO: Replace with pip.
RUN apt-get update
RUN apt-get install -y git
RUN mkdir repos
WORKDIR repos
RUN git clone https://github.com/OpenTrons/labware.git
RUN python3 labware/setup.py install

ENV APP_HOME /var/www/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Add the rest of our files to the app directory.
ADD . $APP_HOME

EXPOSE 8080