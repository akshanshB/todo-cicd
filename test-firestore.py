
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import date, datetime


cred = credentials.Certificate('credentials.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
#add data
# data_point = {
#     'sno':1,
#     'title':'Create app',
#     'desc':'to complete app assignment',
#     'status':False,
#     'timestamp': datetime.now()
# }
# db.collection('todos').document('saksham').set(data_point)

#read data all
# result = db.collection('todos').get()
# result stores a reference

# for doc in result:
#     print(doc.to_dict())

# update data -known key
# db.collection('todos').document('LJ34uRqSP80iAHe3whlq').update({'Title':'Book reading'})
docs = db.collection('todos').where('todo_id','==','234ewd').get()
for doc in docs:
    key = doc.id
    db.collection('todos').document(key).delete()



