
from datetime import  datetime
from functools import wraps
from multiprocessing import AuthenticationError
import traceback

from flask import Blueprint, render_template, abort,request
import json


from uid import get_uid

from firebase_admin import firestore,auth


db = firestore.client()

def checkToken(f):
    @wraps(f)
    def decorated_function(*args,**kws):
        if not 'Authorization' in request.headers:
            abort(401,{'message':'Unauth caller'})
        user =None
        try:
            data = request.headers['Authorization']
            header_token = str(data)
            token = header_token.split(" ")[-1]
            user = auth.verify_id_token(token)
            kws['uid'] = user['uid']
            kws['email'] = user['email']
        except Exception:
            traceback.print_exc()
            abort(401)        


        return f(*args,**kws)
    return decorated_function    


todo_entry = Blueprint('todo_entry', __name__,)

@todo_entry.route('/todo-entry', methods=['POST'])
@checkToken
def store_todo(*args,**kwargs):
    print(request.json)
    
    todo = request.json
    
    
    data_point = {
        'todo_id':get_uid(),
        'title': todo['title'],
        'desc': todo['desc'],
        'status': False,
        'timestamp': datetime.now()
    }
    print(data_point['todo_id'])

    
    db.collection('todos').add(data_point)
    return json.dumps({
        'status':'OK'

    })

# read data from firestore
@todo_entry.route('/get-todos',methods=['GET']) 
@checkToken
def get_todos(*args,**kwargs):
    result = db.collection('todos').get()
    data = [ doc.to_dict() for doc in result]
    return json.dumps({
        'status':'ok',
        'data':data
    },default=str)

#delete data from firestore
@todo_entry.route('/delete-todo',methods=['POST'])
@checkToken
def delete_todo(*args,**kwargs):
    todo = request.json
    
    docs = db.collection('todos').where('todo_id','==',todo['todo_id']).get()
    for doc in docs:
        key = doc.id
        db.collection('todos').document(key).delete()
@todo_entry.route('/toggle-status',methods=['POST'])
@checkToken
def toggle_todo_status(*args,**kwargs):
    todo = request.json
    docs = db.collection('todos').where('todo_id','==',todo['todo_id']).get()   
    curr_status = docs[0].to_dict()['status']
    
    curr_status = not curr_status    
    for doc in docs:
        key = doc.id
        db.collection('todos').document(key).update({'status':curr_status})

