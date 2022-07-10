import mysql.connector
import json
from flask import Flask, request
from flask_expects_json import expects_json

app = Flask(__name__)

docker_config = {
	"host": 'mysqldb',
	"database": 'apiflask',
	"user": 'root',
	"password": 'p@ss'
}

heroku_config = {
	"host": 'us-cdbr-east-06.cleardb.net',
	"database": 'heroku_c503db99b17ac2c',
	"user": 'b6a1fac7c54c61',
	"password": '7b1fd041'
}

schema = {
    'type': 'object',
    'properties': {
        'field_1': {'type': 'string'},
        'author': {'type': 'string'},
        'description': {'type': 'string'},
		'my_numeric_field': {'type': 'number'}
    }
}

def db_insert(f1, aut, des, num) -> int:
	mydb = mysql.connector.connect(
		host = heroku_config["host"],
		user = heroku_config["user"],
		password = heroku_config["password"],
		database = heroku_config["database"] )
	cursor = mydb.cursor()
	cursor.execute("INSERT INTO requests (field_1, author, description, my_numeric_field) VALUES (%s, %s, %s, %s)", (f1, aut, des, num))
	mydb.commit()
	cursor.execute("SELECT LAST_INSERT_ID()")
	id = cursor.fetchone()
	cursor.close()
	return id

@app.route('/')
def hello_world():
	return 'Server is up =D'

@app.route('/input/<string:field>', methods=['POST'])
@expects_json(schema)
def post_input(field):
	valid_fields = ["field_1", "author", "description"]
	if field not in valid_fields:
		return f"{field} no es un campo valido para convertir a mayuscula."
	post = request.get_json()
	field_1 = post.get("field_1")
	author = post.get("author")
	description = post.get("description")
	my_numeric_field = post.get("my_numeric_field")

	if field == "field_1":
		field_1 = field_1.upper()
	if field == "author":
		author = author.upper()
	if field == "description":
		description = description.upper()

	# print(request.json)
	id = db_insert(field_1, author, description, my_numeric_field)
	json_data = {"id": id}
	return json.dumps(json_data)

@app.route('/get_data/<int:id>')
def get_data(id):
	mydb = mysql.connector.connect(
		host = heroku_config["host"],
		user = heroku_config["user"],
		password = heroku_config["password"],
		database = heroku_config["database"] )
	cursor = mydb.cursor()

	cursor.execute("SELECT * FROM requests WHERE id = %s", (id,))
	row_headers=[x[0] for x in cursor.description] #this will extract row headers
	results = cursor.fetchall()
	
	json_data=[]
	for result in results:
		json_data.append(dict(zip(row_headers,result)))
	return json.dumps(json_data)

@app.route('/initdb')
def db_init():
	mydb = mysql.connector.connect(
		host = heroku_config["host"],
		user = heroku_config["user"],
		password = heroku_config["password"]
	)
	cursor = mydb.cursor()
	cursor.execute("DROP DATABASE IF EXISTS " + heroku_config["database"])
	cursor.execute("CREATE DATABASE " + heroku_config["database"])
	cursor.close()

	mydb = mysql.connector.connect(
		host = heroku_config["host"],
		user = heroku_config["user"],
		password = heroku_config["password"],
		database = heroku_config["database"]
	)
	cursor = mydb.cursor()
	cursor.execute("DROP TABLE IF EXISTS users")
	cursor.execute("CREATE TABLE users (name VARCHAR(255), password VARCHAR(255))")
	cursor.execute("INSERT INTO users VALUES ('apiadmin', 'asdf')")
	cursor.execute("DROP TABLE IF EXISTS requests")
	cursor.execute("""CREATE TABLE requests (
						id MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
						field_1 VARCHAR(255),
						author VARCHAR(255),
						description VARCHAR(255),
						my_numeric_field INT,
						PRIMARY KEY (id)
	)
	""")
	cursor.close()

	return 'DB Initialized'

if __name__ == "__main__":
	app.run(host ='0.0.0.0')