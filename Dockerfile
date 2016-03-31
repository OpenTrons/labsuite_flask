FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask pyaml

# Install the LabSuite repo from Git.
RUN apt-get update
RUN apt-get install -y git
RUN pip3 install git+https://github.com/OpenTrons/labware.git

ENV APP_HOME /var/www/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Add the rest of our files to the app directory.
ADD . $APP_HOME

EXPOSE 8080
ENTRYPOINT python3 app.py