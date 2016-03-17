FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install flask

ENV APP_HOME /var/www/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Add the rest of our files to the app directory.
ADD . $APP_HOME

EXPOSE 8080

ENTRYPOINT python3 app.py