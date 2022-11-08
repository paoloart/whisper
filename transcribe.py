import whisper
import time 

def preload()->None:
    global model # get the global variable model
    model = whisper.load_model("large") #small, medium, large models are available
    return model

def trans(window, start,filepath="input.mp3")->None:
    """"
    This function transcribes the data from the whisper file to the console
    """
    global model
    print("start transcribing")
    option = dict(language='Italian') # option is a dictionary, with the language as key, and Italian as value
    # model = whisper.load_model("large") #small, medium, large models are available
    result = model.transcribe(filepath, **option) # transcribe the file input.mp3 to result (is a dictionary)
    print(result["text"])
    window["thought"].update(result["text"]) #show the result
    window["time"].update("Total time= %.2f sec" %((time.time() - start)))
    print("end transcribe{:.2f}".format(time.time()) , " , Total time={:.2f}".format(time.time()-start))
    # del(model) # delete the model from memory, otherwise it will be loaded in memory again and again for each call to this function
    #return result


