import requests
from flask import Flask,request
import random
import math
from model import yolo
from db import *

app=Flask(__name__)


if not os.path.isdir('videos'):
    try:
        os.mkdir('videos')
        print('creating directory videos')
    except Exception:
        print('error creating directory videos')
        exit(-1)
else:
    print('directory videos exists')


@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/video files'}

@app.route('/analyze',methods=['POST'])
def detectVideo():
    if request.form.get('path')=='true':
        results=[]
        path = request.form.get('filepath')
        result=yolo.detectvideo(path,True)
        results.append({path: result[1]})
        collection.insert_one({'filename': path, 'data': result[1]})
        return {'response':results}
    else:
        files = list(request.files)
        results=[]
        for file in files:
            tmp=str(math.floor(random.random()*1000000))+'__'+ request.files[file].filename
            request.files[file].save('videos/'+tmp)
            result = yolo.detectvideo('videos/'+tmp,False)
            os.remove('videos/'+tmp)
            results.append({tmp:result[1]})
            print(result[1])
            collection.insert_one({'filename':tmp,'data':result[1]})

        return {'response':results}

app.run(host=host,port=vidport)

