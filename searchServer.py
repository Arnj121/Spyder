from flask import Flask, request
from db import *

app=Flask(__name__)

@app.get('/search')
def search():
    query=request.args.get('q')
    result = collection.find({
        'data':{
        '$regex':f"^{query}",'$options':"i"
        }
    },{'filename':1,'_id':0,'data':1,'rawdata':1})
    result=list(result)
    return {'response':result}

@app.get('/getfiledata')
def getFileData():
    query=request.args.get('q')
    result = collection.find({
        'filename':{
            '$regex':f"{query}","$options":'i'
        }
    })
    return {'response':result}


app.run(host=host,port=searchport)



