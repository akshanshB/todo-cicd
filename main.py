
from flask import Flask, render_template, Blueprint, send_from_directory
from flask_cors import CORS

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

app = Flask(__name__, template_folder='todo-list/dist/todo-list')
CORS(app)
from api import todo_entry

angular = Blueprint('todo-list', __name__,'todo-list/dist/todo-list' )
app.register_blueprint(angular)
app.register_blueprint(todo_entry,url_prefix="/api")

@app.route('/assets/<path:filename>')
def custom_static_for_assets(filename):
    return send_from_directory('todo-list/dist/todo-list/assets',filename)

@app.route('/<path:filename>')
def custom_static(filename):
    return send_from_directory('todo-list/dist/todo-list/',filename)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1',port=8008,debug=True)
