from flask import Flask, request
from db import *
import json
from bson import json_util

app=Flask(__name__)

@app.get('/search')
def search():
    query=request.args.get('q')
    print(query)

    result = collection.find({
        'data':{
        '$regex':f"^{query}",'$options':"i"
        }
    },{'filename':1,'_id':0,'data':1,'rawdata':1})
    result=list(result)
    # json_data = json.dumps(result, default=json_util.default)
    print(result)
    return {'response':result}

app.run(host=host,port=searchport)



