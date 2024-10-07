from tokenizer import *

def extract(textPath):
    with open(textPath,'r') as f:
        data=f.read()
        words = word_tokenize(data)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if word.lower() not in stop_words]
        return [filtered_words,data]