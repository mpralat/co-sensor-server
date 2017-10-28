# CO Sensor [Raspberry Pi] + [Django Channels] Project - Server


# Getting started

## Virtual environment

#### Create virtual environment
`python -m venv ../server-env`
#### Activate virtual environemtn
`source ../server-env/bin/activate`
#### Install required python modules
`pip install -r requirements.txt`


## Server database

#### Migrate database
`python manage.py migrate`
#### Create admin user
`python manage.py createsuperuser`

## Redis
Server uses Redis for key-value storage.

#### Installation
There are many ways to install Redis and configure it for work.
This link shows one way to do it on Ubuntu: [How To Install and Configure Redis on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-redis-on-ubuntu-16-04)
#### Start Redis
`redis-server`

## Environment

#### Set environment variables
 * WEB_CONCURRENCY=2
###### Sendgrid credentials for mail server
 * SENDGRID_PASSWORD=[sendgrid-password]
 * SENDGRID_USERNAME=[sendgrid-username]
###### Redis URL as shown in `redis-server` output
 * REDIS_URL=[redis-urredis://localhost:6379l]
 
**If you are using Heroku save these environment variables in a new file `./env`**

## Run the server

#### Normal setup
`daphne co_sensor.asgi:channel_layer --port 5000 --bind 0.0.0.0 -v2 | python manage.py runworker -v2`

#### With Heroku
Processes that will run after this command are defined in `./Procfile`
`heroku local`
