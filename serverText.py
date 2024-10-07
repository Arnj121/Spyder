from flask import Flask,request
import random
import math
from model import yolo
from db import *

from model import text

app=Flask(__name__)

if not os.path.isdir('text'):
    try:
        os.mkdir('text')
        print('creating directory text')
    except Exception:
        print('error creating directory text')
        exit(-1)
else:
    print('directory text exists')


@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/text files'}

@app.route('/analyze',methods=['POST'])
def detectVideo():
    files = list(request.files)
    results=[]
    for file in files:
        tmp=str(math.floor(random.random()*1000000))+'__'+ request.files[file].filename
        request.files[file].save('text/'+tmp)
        results = text.extract(tmp)
        os.remove('text/'+tmp)
        results.append({tmp:results[0]})
        print(results[0])
        collection.insert_one({'filename':tmp,'data':results[0],'rawdata':results[1]})

    return {'response':results}

app.run(host=host,port=vidport)

