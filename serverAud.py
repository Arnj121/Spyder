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
    if request.form.get('path')=='true':
        results = []
        path = request.form.get('filepath')
        result = transcript.transcribe(path, True)
        results.append({path: result[1]})
        collection.insert_one({'filename': path, 'data': result[1]})
        return {'response': results}
    else:
        files = list(request.files)
        results=[]
        for file in files:
            tmp=str(math.floor(random.random()*1000000))+ request.files[file].filename
            request.files[file].save('audios/'+tmp)
            result=transcript.transcribe('audios/'+tmp,False)
            os.remove('audios/'+tmp)
            results.append({tmp:result[1]})
            print(result[1])
            collection.insert_one({'filename':tmp,'data':result[1],'rawdata':result[2]})
        return {'response':results}

app.run(host=host,port=audport)