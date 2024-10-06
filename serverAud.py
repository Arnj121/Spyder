from flask import Flask,request
import random
import math
from model import transcript
from db import *

app=Flask(__name__)

@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/audio files'}

@app.route('/analyze',methods=['POST'])
def detectAudio():
    files = list(request.files)
    resultfilepath=[]
    for file in files:
        tmp='audios/'+str(math.floor(random.random()*1000000))+ request.files[file].filename
        request.files[file].save(tmp)
        results=transcript.transcribe(tmp)
        resultfilepath.append(results[0])
        print(results[1])
        collection.insert_one({'filename':tmp,'data':results[1],'rawdata':results[2]})
    return {'filepath':resultfilepath}

app.run(host=host,port=audport)