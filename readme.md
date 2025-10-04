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
Pending

# Execution
Run `flask run` on the top-level directory


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
