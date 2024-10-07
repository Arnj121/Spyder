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
    files = list(request.files)
    results=[]
    for file in files:
        tmp=str(math.floor(random.random()*1000000))+'__'+ request.files[file].filename
        request.files[file].save('videos/'+tmp)
        results = yolo.detectvideo(tmp)
        os.remove('videos/'+tmp)
        results.append({tmp:results[1]})
        print(results[1])
        collection.insert_one({'filename':tmp,'data':results[1]})

    return {'response':results}

app.run(host=host,port=vidport)

