import flask
from flask import request, jsonify
import MySQLdb
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def query_handle(query):
    db = MySQLdb.connect("mysql-server", "root", "secret", "testdb")
    cursor = db.cursor()
    cursor.execute(query)
    return db, cursor


# create new task and put it in mysql DB
@app.route('/', methods=["POST"])
def create_task():
    
    query =  "SELECT * FROM tasks"
    db, cursor = query_handle(query)
    results = cursor.fetchall()
    current_id = [row[0] for row in results]
    db.close()

    new_id = 1
    while new_id in current_id:
        new_id = random.randint(1,101)
    
    new_task = {'id': new_id}
    new_task['title'] = request.json['title']+" "+str(new_id)
    new_task['is_completed'] = request.json['is_completed']

    query = "INSERT INTO tasks(id, title, is_completed) VALUES (%s, '%s', %s)" % (new_task['id'], new_task['title'], new_task['is_completed'])
    db, cursor = query_handle(query)
    db.commit()
    db.close()

    return jsonify(new_task), 201


# list all task
@app.route('/', methods=['GET'])
def list_all():

    tasks = []
    query =  "SELECT * FROM tasks"
    db, cursor = query_handle(query)
    results = cursor.fetchall()
    for row in results:
        task = {'id': row[0]}
        task['title'] = row[1]
        task['is_completed'] = row[2]
        tasks.append(task)
    db.close()

    return jsonify(tasks), 200


#"<>" syntax. This tells the function underneath to expect info from the url to be passed into its function
# get a specific task
@app.route('/<id>', methods=["GET"])
def get_task(id):
    response = []
    query =  "SELECT * FROM tasks"
    db, cursor = query_handle(query)
    results = cursor.fetchall()
    for row in results:
        if row[0] == int(id):
            response.append({'id': row[0], 'title': row[1], 'is_completed': row[2]})
            break
    db.close()
        
    if response:
        return jsonify(response), 200
    else:
        return jsonify("error: There is no task at that id"), 404
    
# edit the task
@app.route('/<id>', methods=["PUT"])
def edit_task(id):

    new_task = {'id': id}
    new_task['title'] = request.json['title']+" "+str(id)
    new_task['is_completed'] = request.json['is_completed']
    
    flag = False
    query =  "SELECT * FROM tasks"
    db, cursor = query_handle(query)
    results = cursor.fetchall()
    for row in results:
        if row[0] == int(id):
            query = "UPDATE tasks SET title = '%s', is_completed = %s WHERE id = %s" % (new_task['title'], new_task['is_completed'], new_task['id'])
            cursor.execute(query)
            db.commit()
            flag = True
            break
    db.close()
    
    if not flag:
        return jsonify("error: There is no task at that id"), 404
    else:
        return jsonify(new_task), 204

# delete a specific task
@app.route('/<id>', methods=["DELETE"])
def delete_task(id):
    flag = False
    query =  "SELECT * FROM tasks"
    db, cursor = query_handle(query)
    results = cursor.fetchall()
    for row in results:
        if row[0] == int(id):
            cursor.execute("DELETE FROM tasks WHERE id = %s" % id)
            db.commit()
            flag = True
            break
    db.close()
    
    if not flag:
        return jsonify("error: There is no task at that id"), 404
    else:
        return '204'

@app.route('/', methods=["DELETE"])
def bulk_delete_task():
    query =  "DELETE FROM tasks"
    db, _ = query_handle(query)
    db.commit()
    db.close()

    return '204'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')