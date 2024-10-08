from flask import Flask,request
import random
import math
from model import yolo
from db import *
app=Flask(__name__,static_folder='images')


if not os.path.isdir('images'):
    try:
        os.mkdir('images')
        print('creating directory images')
    except Exception:
        print('error creating directory images')
        exit(-1)
else:
    print('directory images exists')


@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/image files'}

@app.route('/analyze',methods=['POST'])
def detectImage():
    if request.form.get('path')=='true':
        results=[]
        path = request.form.get('filepath')
        result=yolo.detectimage(path,True)
        results.append({path: result[1]})
        print(result[1])
        collection.insert_one({'filename': path, 'data': result[1]})
        return {'response': results}
    else:
        files = list(request.files)
        results=[]
        for file in files:
            tmp=str(math.floor(random.random()*1000000))+ request.files[file].filename
            request.files[file].save('images/'+tmp)
            result=yolo.detectimage('images/'+tmp,False)
            os.remove('images/'+tmp)
            results.append({tmp:result[1]})
            print(result[1])
            collection.insert_one({'filename':tmp,'data':result[1]})
        return {'response':results}

app.run(host=host,port=imgport)