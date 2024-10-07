from model.tokenizer import *
from pypdf import PdfReader

def extract(textPath):
    if textPath.split('.')[-1] == 'pdf':
        data=''
        reader = PdfReader(textPath)
        for i in range(len(reader.pages)):
            data+=reader.pages[i].extract_text()

        filtered_words = tokenize(data)
        return [filtered_words, data]

    elif textPath.split('.')[-1] in ['txt']:
        with open(textPath,'r') as f:
            data=f.read()
            filtered_words = tokenize(data)
            return [filtered_words,data]