import whisper

def trans(filepath="input.mp3")->None:
    """"
    This function transcribes the data from the whisper file to the console
    """
    print("start transcribing")
    option = dict(language='Italian') # option is a dictionary, with the language as key, and Italian as value
    model = whisper.load_model("large") #small, medium, large models are available
    result = model.transcribe(filepath, **option) # transcribe the file output.mp3 to result (is a dictionary)
    print(result["text"])
    
    del(model) # delete the model from memory, otherwise it will be loaded in memory again and again for each call to this function
    return result

