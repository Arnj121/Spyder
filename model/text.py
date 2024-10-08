import os
from model.tokenizer import *
from pypdf import PdfReader
import requests

def extract(textPath,url):
    if textPath.split('.')[-1] == 'pdf':
        if url:
            response = requests.get(textPath)
            content = response.content
            with open('text/'+textPath.split('/')[-1],'wb') as f:
                f.write(content)
        data = ''
        reader = PdfReader('text/'+textPath.split('/')[-1])
        for i in range(len(reader.pages)):
            data += reader.pages[i].extract_text()
        os.remove('text/'+textPath.split('/')[-1])
        filtered_words = tokenize(data)
        return [filtered_words, data]

    elif textPath.split('.')[-1] in ['txt'] or len(textPath.split('.')) == 1:
        if url:
            response = requests.get(textPath)
            content = response.text
            filtered_words = tokenize(content)
            return [filtered_words, content]
        else:
            with open(textPath, 'r') as f:
                data = f.read()
                filtered_words = tokenize(data)
                return [filtered_words, data]
