from flask import Flask,request
import random
import math
from model import transcript
from db import *

app=Flask(__name__)

if not os.path.isdir('audios'):
    try:
        os.mkdir('audios')
        print('creating directory audios')
    except Exception:
        print('error creating directory audios')
        exit(-1)
else:
    print('directory audios exists')

@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/audio files'}

@app.route('/analyze',methods=['POST'])
def detectAudio():
    files = list(request.files)
    results=[]
    for file in files:
        tmp=str(math.floor(random.random()*1000000))+ request.files[file].filename
        request.files[file].save('audios/'+tmp)
        results=transcript.transcribe(tmp)
        os.remove('audios/'+tmp)
        results.append({tmp:results[1]})
        print(results[1])
        collection.insert_one({'filename':tmp,'data':results[1],'rawdata':results[2]})
    return {'response':results}

app.run(host=host,port=audport)