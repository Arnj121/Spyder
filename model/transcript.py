import whisper
from model.tokenizer import *
models={
    # 'medium': whisper.load_model("medium"),
    # 'base': whisper.load_model("base"),
    'small': whisper.load_model("small"),
    # 'large': whisper.load_model("large"),
}
def transcribe(audioPath,defaultModel='small'):
    audio = whisper.load_audio(audioPath)
    result = models[defaultModel].transcribe(audio)
    print(result)
    filtered_words = tokenize(result['text'])

    return [audioPath,filtered_words,result['text']]