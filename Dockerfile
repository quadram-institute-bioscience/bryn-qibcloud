# pull official base image
FROM python:3.6-alpine

# set work directory
WORKDIR /usr/src/bryn

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/bryn/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/bryn/