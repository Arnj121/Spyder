from flask import Flask,request
import random
import math
from model import yolo
from db import *
app=Flask(__name__,static_folder='images')


@app.route('/',methods=['GET'])
def default():
    return {'response':'methods available: [POST]:/analyze | accepts: form/image files'}

@app.route('/analyze',methods=['POST'])
def detectImage():
    files = list(request.files)
    resultfilepath=[]
    for file in files:
        tmp='images/'+str(math.floor(random.random()*1000000))+ request.files[file].filename
        request.files[file].save(tmp)
        results=yolo.detectimage(tmp)
        resultfilepath.append(results[0])
        print(results[1])
        collection.insert_one({'filename':tmp,'data':results[1]})
    return {'filepath':resultfilepath}

app.run(host=host,port=imgport)