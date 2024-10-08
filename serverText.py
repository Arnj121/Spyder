from flask import Flask,request
from flask_cors import CORS
import random
import math
from db import *
from model import text

app=Flask(__name__)
CORS(app)
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
def detectText():
    print(request.form)
    if request.form.get('path')=='true':
        results=[]
        path = request.form.get('filepath')
        result = text.extract(path,True)
        results.append({path: result[0]})
        print(result[1])
        collection.insert_one({'filename': path, 'data': result[0], 'rawdata': result[1]})
        return {'response':results}
    else:
        files = list(request.files)
        results=[]
        for file in files:
            tmp=str(math.floor(random.random()*1000000))+'__'+ request.files[file].filename
            request.files[file].save('text/'+tmp)
            result = text.extract('text/'+tmp,False)
            os.remove('text/'+tmp)
            results.append({tmp:result[0]})
            print(result[0])
            collection.insert_one({'filename':tmp,'data':result[0],'rawdata':result[1]})

        return {'response':results}

app.run(host=host,port=textport)

