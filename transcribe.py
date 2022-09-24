import whisper
import numpy as np
import torch

def trans():
    print("start transcribing")
    option = dict(language='Italian')
    model = whisper.load_model("small")
    result = model.transcribe("output.mp3", **option)
    print(result["text"])
    del(model)
    return result