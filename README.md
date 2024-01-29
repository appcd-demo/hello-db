demo app that connects to pg, mongo, myqsl

## endpoints
- /hello/pg
- /hello/mysql
- /hello/mongo

## run the app with databases runnning in docker

```
docker run --name hello-db-pg -e POSTGRES_PASSWORD=my-secret-pw --publish 5432:5432 -d postgres:latest
docker run --name hello-db-mysql --publish 3306:3306 -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest
docker run --name hello-db-mongo --publish 27017:27017 -d mongo:latest
pip install -r requirements.txt 
python main.py
```