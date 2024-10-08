import whisper
from model.tokenizer import *
import requests
models={
    # 'medium': whisper.load_model("medium"),
    # 'base': whisper.load_model("base"),
    'small': whisper.load_model("small"),
    # 'large': whisper.load_model("large"),
}
def transcribe(audioPath,url,defaultModel='small'):
    if url:
        response = requests.get(audioPath)
        with open('audios/' + audioPath.split('/')[-1], 'wb') as f:
            f.write(response.content)
        audioPath='audios/'+ audioPath.split('/')[-1]
        audio = whisper.load_audio(audioPath)
        result = models[defaultModel].transcribe(audio)
        print(result)
        filtered_words = tokenize(result['text'])

        return [audioPath, filtered_words, result['text']]
    else:
        audio = whisper.load_audio(audioPath)
        result = models[defaultModel].transcribe(audio)
        print(result)
        filtered_words = tokenize(result['text'])

        return [audioPath,filtered_words,result['text']]