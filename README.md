# flask-app-folder
Here are two applications for backend server setup with flask and databases: mysql and redis both on docker service.

## 1. Flask+MySQL
This is an example of docker containers for flask and mysql connection. <br>
Please follow to the link and get more explanations:<br>
https://medium.com/@waynewu_25577/docker-flask-mysql-%E5%9F%BA%E6%9C%AC%E4%B8%B2%E6%8E%A5%E6%95%99%E5%AD%B8-77eff0871954

1. To use:
First open your terminal and locate in flask-mysql folder, then type in:
```
bash run.sh
```
It will start to build up every service. <br>

2. Then, open your browser and type in: 
```
http://0.0.0.0:5000/
```
You will first see an empty list for your current data, don't worry!!
You can start to interact with the database by adding, updating and deleting the data.
```
POST: (Add Information)
curl -i -H "Content-Type: application/json" -X POST -d '{"title":"Test", "notify":"xxxxxxxxx@gmail.com"}' http://0.0.0.0:5000/

PUT: (Update Information)
curl -i -H "Content-Type: application/json" -X PUT -d '{"title":"Update", "is_completed":1, "notify":"waynewu6250@gmail.com", "name":"Wayne"}' http://0.0.0.0:5000/<id>

GET: (Get Information)
curl -v http://0.0.0.0:5000/
curl -v http://0.0.0.0:5000/<id>

DELETE: (Delete Information)
curl -v -X DELETE http:/0.0.0.0:5000/
curl -v -X DELETE http:/0.0.0.0:5000/<id>
```
Then you can see some data on your browser. And also you can log in your database by typing in:
```
docker run -it --rm --network my-network mysql:5.7 sh -c 'exec mysql -h"mysql-server" -P"3306" -uroot -p"secret"'
```
We store our data in "mysql" database in docker container. 
<br><br>


## 2. Flask+RQ+redis
This is an example to send a request with some words to the server, and it will return a list of ten synonyms associated with those words. <br>
1. To use:
First open your terminal and locate in flask-redis folder, then type in:
```
bash startup.sh
```
It will start to build up every service. <br>

2. Then, open your browser and send a request by typing in: 
```
http://0.0.0.0:5000/get_synonym?word=[example]
```
Here \[example\], you can replace to any words you would like to search. <br>
For example, type http://0.0.0.0:5000/get_synonym?word=she will return in a sequence as follows: <br>
\["hers", "woman", "mother", "lady", "girl", "mom", "never", "him", "mama", "roxanne"\]
