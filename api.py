import flask
from flask import request, jsonify
import MySQLdb
import random

app = flask.Flask(__name__)
app.config["DEBUG"] = True

# Create some test data for our catalog in the form of a list of dictionaries.
tasks = [
     {'id': 1, 'title': "Test Task 1", 'is_completed': 'true'},
     {'id': 2, 'title': "Test Task 2", 'is_completed': 'false'},
     {'id': 3, 'title': "Test Task 3", 'is_completed': 'false'}
]

# create new task and put it in mysql DB
@app.route('/', methods=["POST"])
def create_task():

    # check if new id exist in current ids
    current_id = []
    for task in tasks:
        current_id.append(task['id'])

    new_id = 1
    while new_id in current_id:
        new_id = random.randint(1,101)
    
    new_task = {'id': new_id}
    new_task['title'] = request.json['title']+" "+str(new_id)
    new_task['is_completed'] = request.json['is_completed']
    tasks.append(new_task)

    query = "INSERT INTO tasks(id, title, is_completed) VALUES (%s, '%s', %s)" % (new_task['id'], new_task['title'], new_task['is_completed'])
    db = MySQLdb.connect("mysql-server", "root", "secret", "testdb")
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    db.close()

    return jsonify(new_task), 201


# list all task
@app.route('/', methods=['GET'])
def list_all():
    # convert lists and dictionaries to JSON format
    return jsonify(tasks), 200


#"<>" syntax. This tells the function underneath to expect info from the url to be passed into its function
# get a specific task
@app.route('/<id>', methods=["GET"])
def get_task(id):
    response = []
    for task in tasks:
        if task['id'] == int(id):
            response.append(task)
        
    if response:
        return jsonify(response), 200
    else:
        return jsonify("error: There is no task at that id"), 404

# delete a specific task
@app.route('/<id>', methods=["DELETE"])
def delete_task(id):
    for task in tasks:
        if task['id'] == int(id):
            tasks.remove(task)
    return 204

    
# edit the task
@app.route('/<id>', methods=["PUT"])
def edit_task(id):

    current_id = []
    for task in tasks:
        current_id.append(task['id'])
    
    if int(id) not in current_id:
        return jsonify("error: There is no task at that id"), 404

    else:
        for task in tasks:
            if task['id'] == int(id):
                task['title'] = request.json['title']
                task['is_completed'] = request.json['is_completed']
        return 204


@app.route('/', methods=["DELETE"])
def bulk_delete_task():
    delete_list = request.json['tasks']
    delete_id = []
    for ids in delete_list:
        delete_id.append(ids['id'])
    
    for did in delete_id:
        for task in tasks:
            if task['id'] == did:
                tasks.remove(task)

    return 204

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')