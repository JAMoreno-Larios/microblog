# Miguel Grinberg's Flask Mega-Tutorial 2024 edition
## Implemented by José Agustín Moreno

We develop a microblogging site using Flask as shown
in [Miguel Grinberg's Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) 

## Requirements
We have installed so far:
- Python
- Flask
- python-dotenv
- Flask-WTF
- WTForms
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Login
- Flask-Moment
- email-validator
- langdetect
- requests
- elasticsearch

## Installation

First, create a virtual environment in our main directory, and install
the necessary packages:
```bash
$ python -m venv venv
$ source venv/bin/activate
$ [venv] pip install -r requirements.txt
```

## Execution
Run `flask run` on the top-level directory


## Elasticsearch
To install the Elasticsearch engine in Docker:
```bash
$ sudo docker network create elastic
$ sudo docker pull docker.elastic.co/elasticsearch/elasticsearch:9.1.4
```

To start the Elasticsearch engine with Docker, run

```bash
$ sudo docker run --name elasticsearch --network elastic \
--rm -p 9200:9200 --memory 2GB -e discovery.type=single-node \
-e xpack.security.enabled=false \
-t docker.elastic.co/elasticsearch/elasticsearch:9.1.4

```

## Celery
We use Celery as our task queue. In addition to that, we need either a
Redis or Valkey server up and running.

To get our Celery worker started, we need to

```bash
$ celery -A microblog.celery_app worker --loglevel INFO
```
on our root directory.

## Deploying with Vagrant and Ubuntu Linux
To create the VM with the provided `Vagrantfile`:
```bash
$ vagrant up
```

We can start a SSH session with `$ vagrant ssh` and set up our environment.

Once inside the VM shell, we install the following packages:
```bash
$ sudo apt-get -y update
$ sudo apt-get -y install python3 python3-venv python3-dev
$ sudo apt-get -y install mysql-server postfix supervisor nginx git
```

Be sure to install Elasticsearch as you see fit, in my case I still used
the Docker container. Use the files found in `deployment` to configure
both supervisor and nginx.

Install as directed above, then add these additional packages.
```bash
[venv] $ pip install gunicorn pymysql cryptography
```

Configure the `.env` file
```bash
SECRET_KEY=52cb883e323b48d78a0a36e8e951ba4a
MAIL_SERVER=localhost
MAIL_PORT=25
DATABASE_URL=mysql+pymysql://microblog:<db-password>@localhost:3306/microblog
MS_TRANSLATOR_KEY=<your-translator-key-here>
```

We now compile the language translations
```bash
[venv] $ flask translate compile
```

To set up the MySQL server, supervisor and nginx, please
refer to [Miguel's tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux) 

# Next steps
I should figure out how to automate the app deployment, either to a
Linux box or using a multi-container solution such as Docker Compose.
