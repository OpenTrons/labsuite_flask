FROM ubuntu:latest

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apk add py-pip
RUN pip install --upgrade pip
RUN pip install flask

ENV APP_HOME /var/www/
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

# Add the rest of our files to the app directory.
ADD . $APP_HOME

EXPOSE 8080

ENTRYPOINT python app.py