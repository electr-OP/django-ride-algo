# Use an official Python runtime as a parent image
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup --system app && adduser --system --group app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat-openbsd
# install gdal
RUN apt-get install -y binutils gdal-bin libgdal-dev

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.prod.sh
COPY ./entrypoint.sh .

# copy project
COPY . $APP_HOME

RUN sed -i 's/\r$//g'  $APP_HOME/entrypoint.sh

RUN ["chmod", "+x", "/home/app/web/entrypoint.sh"]

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# Expose the port for Django ASGI application
EXPOSE 8060

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]

