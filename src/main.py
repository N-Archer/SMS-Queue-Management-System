"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from datastructures import Queue
from sms import send_sms
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

q = Queue()
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/queue', methods=['GET'])
def get_queue():
    current_queue=q.get_queue()
    queue_length=q.size()

    response_body = {
        "Queue": current_queue,
        "# in Queue": f"There are {queue_length} in the queue.",
        # "first in Queue": q.get_queue([0]),
        "Next in Line":  f"Next is {current_queue[0]}." if queue_length else "empty queue"
    }

    return jsonify(response_body), 200

@app.route('/queue', methods=['POST'])
def post_queue():
    request_body=request.get_json()
    q.enqueue(request_body)
    queue_length=q.size()
    current_queue=q.get_queue()
    response_body = {
        "Added to Queue": f"{current_queue[-1]['name']} was added to the queue.",
        "Queue": q.get_queue(),
        "# in Queue": f"There are {queue_length} in the queue.",
        "Next in Line":  f"Next is {current_queue[0]}." if queue_length else "empty queue"
    }

    return jsonify(response_body), 200

@app.route('/queue', methods=['DELETE'])
def delete_from_queue():
    call_person = q.dequeue()
    queue_length=q.size()
    current_queue=q.get_queue()
    send_sms(body= f"Hi, {call_person['name']} your Table is Ready")

    response_body = {
        "Deleted from Queue": f"{call_person} was deleted from the queue.",
        "Queue": q.get_queue(),
        "# in Queue": f"There are {queue_length} in the queue.",
        "Next in Line":  f"Next is {current_queue[0]}." if queue_length else "empty queue"
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
