#!/usr/bin/sh
# Construct a network
docker network create -d bridge my-network

# MYSQL server
# Pull mysql image from Docker Hub
docker pull mysql:5.7
# Run the mysql container
docker run -d --name mysql-server --network my-network -e MYSQL_ROOT_PASSWORD=secret mysql:5.7


# Flask server
# Build flask image
docker build -t flask-app .
# Run the flask server
docker run -p 5000:5000 --network my-network -v "$PWD":/app -d flask-app

# Common commands: 
# POST
# curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Test", "notify":"xxxxxx@gmail.com"}' http://0.0.0.0:5000/
# PUT
# curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Update", "is_completed":1, "notify":"xxxxxx@gmail.com", name:<Your Name>}' http://0.0.0.0:5000/<id>
# GET ALL
# curl -v http://0.0.0.0:5000/
# GET
# curl -v http://0.0.0.0:5000/<id>
# DELETE ALL
# curl -v -X DELETE http:/0.0.0.0:5000/
# DELETE
# curl -v -X DELETE http:/0.0.0.0:5000/<id>

# Enter Mysql
# docker run -it --rm --network my-network mysql:5.7 sh -c 'exec mysql -h"mysql-server" -P"3306" -uroot -p"secret"'