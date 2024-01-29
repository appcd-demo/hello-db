import os
import sys
import json
import logging
import psycopg2
import pymongo
import pymysql
from flask import Flask, jsonify, request
from flask_cors import CORS

# set up logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# set up flask
app = Flask(__name__)
CORS(app)

# set up database connection
try:
    pg_host = os.environ['POSTGRES_HOST']
    pg_port = os.environ['POSTGRES_PORT']
    pg_name = os.environ['POSTGRES_NAME']
    pg_user = os.environ['POSTGRES_USER']
    pg_password = os.environ['POSTGRES_PASSWORD']

    mysql_host = os.environ['MYSQL_HOST']
    mysql_port = os.environ['MYSQL_PORT']
    mysql_name = os.environ['MYSQL_NAME']
    mysql_user = os.environ['MYSQL_USER']
    mysql_password = os.environ['MYSQL_PASSWORD']

    mongo_url = os.environ['MONGO_URL']
    
except KeyError as e:
    logger.error('Missing environment variable: {}'.format(e))
    sys.exit(1)


def get_pg_connection():
    try:
        conn = psycopg2.connect(host=pg_host, port=pg_port, dbname=pg_name, user=pg_user, password=pg_password)
        return conn
    except psycopg2.OperationalError as e:
        logger.error('Could not connect to database: {}'.format(e))
        sys.exit(1)

def get_mysql_connection():
    try:
        conn = pymysql.connect(host=mysql_host, port=int(mysql_port), db=mysql_name, user=mysql_user, passwd=mysql_password)
        return conn
    except pymysql.OperationalError as e:
        logger.error('Could not connect to database: {}'.format(e))
        sys.exit(1)

def get_mongo_connection():
    try:
        conn = pymongo.MongoClient(mongo_url, 27017)
        db = conn.test
        db.test.insert_one({'hello': 'world'})
        # print the connection string
        print(conn)
        return conn
    
    except pymongo.OperationalError as e:
        logger.error('Could not connect to database: {}'.format(e))
        sys.exit(1)

@app.route('/hello/pg', methods=['GET'])
def hello_pg():
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello, world!'")
    result = cur.fetchone()
    return jsonify("Hello, world!")


@app.route('/hello/mysql', methods=['GET'])
def hello_mysql():
    conn = get_mysql_connection()
    cur = conn.cursor()
    cur.execute("SELECT 'Hello, world!'")
    result = cur.fetchone()
    return jsonify(result)

@app.route('/hello/mongo', methods=['GET'])
def hello_mongo():
    conn = get_mongo_connection()
    db = conn.test
    result = db.test.find_one()
    return {"hello": result['hello']}

if __name__ == '__main__':
    app.run(host='localhost', port=5002, debug=True)
