# startup.sh: script to create docker containers to run this async task queue

# Create network
docker network create my-network-1

# Create container running redis
docker run --network my-network-1 --name some-redis -d redis redis-server --appendonly yes

# Build and create container running rq workers
pushd workerserver
docker build -t workerserver .
docker run --network my-network-1 --name some-workerserver -d workerserver
popd

# Build and create container for our definition webserver
pushd webserver
docker build -t webserver .
docker run --network my-network-1 --name some-webserver -d -e FLASK_APP=webserver.py -p 5000:5000 webserver
popd


# workerserver
# docker run --network my-network-1 --name some-workerserver --rm -v /Users/waynewu/Desktop/Boyu_Last_API/demo/workerserver:/app workerserver
# webserver
# docker run --network my-network-1 --name some-webserver --rm -v /Users/waynewu/Desktop/Boyu_Last_API/demo/webserver:/app -e FLASK_APP=webserver.py -p 5000:5000 webserver
