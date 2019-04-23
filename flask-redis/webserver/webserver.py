from flask import Flask, request, Response
import json
import logging
import time

from rq import Queue
from redis import Redis

app = Flask(__name__)
q = Queue(connection=Redis(host="some-redis", port=6379))
dictionary = {}

@app.route('/save_def', methods=["POST"])
def save_def():

    if request.headers['Content-Type'] == 'application/json':
        arguments = request.get_json()
        word = arguments.get("word")
        definition = arguments.get("definition")

        dictionary[word] = definition
        status_code = 200
        logging.info("Word {} with definition {} saved".format(word, definition))

        job = q.enqueue("taskrunner.send_email", "kay@ischool.berkeley.edu", "New Definition Saved", "word: {} with definition: {} was saved".format(word, definition))
    else:
        status_code = 400
        logging.warning("Invalid content type: only application/json is allowed")

    resp = Response('', status=status_code)
    return resp

@app.route('/get_def', methods=["GET"])
def get_def():
    # Note for GET Request, we get input parameters from URL, not
    # application/json nor applicaiton/x-www-form-urlencoded
    # request body
    word = request.args.get("word")

    if word not in dictionary:
        definition = "Not Found"
        status_code = 404
        logging.warning("{} not found in dictionary".format(word))
    else:
        definition = dictionary[word]
        status_code = 200

    job = q.enqueue("taskrunner.send_email", "kay@ischool.berkeley.edu", "New Definition requested", "word: {} with definition: {} was requested".format(word, definition))

    data = {"word": word, "definition": definition}
    resp = Response(json.dumps(data), status=status_code, mimetype='application/json')

    return resp


@app.route('/get_synonym', methods=["GET"])
def get_synonym():

    word = request.args.get("word")
    url = "https://api.datamuse.com/words?ml={}".format("+".join(word.split()))

    job = q.enqueue("taskrunner.get_synonym_words", url)
    time.sleep(5)
    resp = Response(json.dumps(job.result), status=200, mimetype='application/json')

    return resp



