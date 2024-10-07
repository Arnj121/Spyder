import whisper
from tokenizer import *
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
    words = word_tokenize(result['text'])
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.lower() not in stop_words]

    return [audioPath,list(set(filtered_words)),result['text']]