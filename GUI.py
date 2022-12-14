import PySimpleGUI as sg # pip install pysimplegui
from myrec import onrec # import onrec function from myrec.py
import transcribe #this is a local file called transcribe.py, we made it
import torch
import subprocess
import threading
import time
import multiprocessing




if __name__ == "__main__": 
    
   
    model = None
    # manager = multiprocessing.Manager()
    # return_dict = manager.dict()
    sg.theme("DarkTeal2")
    # in alto a destra c'e' il tasto per chiamare attenzione
    # Layout of the graphical interface
    layout = [[sg.Text('', size=(50, 1), relief='sunken', font=('Courier', 11),
               text_color='yellow', background_color='black',key='TEXT')],
            [sg.Text("Record your thought")],
            [sg.Graph(
                canvas_size=(20, 20),
                graph_bottom_left=(0, 0),
                graph_top_right=(20, 20),
                key="graph", 
                background_color="red",
                visible=False,
                ),sg.Button("rec"), sg.Button("stop"), sg.Button("transcribe")], 
            # add a separator in the gui
            [sg.Text("",size=(50,10))],
            [sg.Text("Choose from file")],
            
            [sg.Input(key="-IN2-" ,change_submits=True), sg.FileBrowse(key="-IN-")],
            [sg.Button("Submit")],
            [sg.Text("",size=(50,10))],
            [sg.Text("Time:", key="time", size=(30,1))],
            [sg.Multiline("Your thought:", key="thought", size=(50,10),)],
            [sg.Button("save")],
            [sg.Button("close")]] # key is used to get the value of the element, and use later
                
    print("Is GPU available?",torch.cuda.is_available()) #check if GPU is available
    x = threading.Thread(target=transcribe.preload, args=()) # create a thread
    # x = multiprocessing.Process(target=transcribe.preload, args=(return_dict,)) # create a process
    x.start()
    # Create the window
    window = sg.Window("Demo", layout, margins=(300, 300))
    text = window['TEXT']
    state = 0
    model_loaded = False
    # Create an event loop
    while True:
        event, values = window.read(timeout=140) # Read the event that happened
        # if state reach the max value, reset it
        if state < 50:
            state = (state+1)%51 
            text.update('???'*state)
        else:
            # make text green
            text.update("Model loaded in GPU, ready to transcribe or rec", text_color='green')
        # if rec button is pressed
        if event == "rec":
            window["graph"].update(visible=True)
            window["thought"].update("Recording...")
            onrec(window)
            window["graph"].update(visible=False)
        if event == "transcribe":
            if model_loaded == False:
                x.join()
                model_loaded = True
            start = time.time()
            # print start time formatted
            print("Start = {:.2f}".format(start))
            window["thought"].update("Transcribing, take a coffee...")
            window.refresh() # refresh the window to show the new text above
            q1 = threading.Thread(target=transcribe.trans, args=(window, start)).start() # create a thread
        if event == "Submit":
            if model_loaded == False:
                x.join()
                model_loaded = True
            start = time.time()
            print("Start = {:.2f}".format(start))
            q2 = threading.Thread(target=transcribe.trans, args=(window, start, values["-IN-"])).start() # create a thread
            
        
        if event=="save":
            print("save")
            with open("file.txt", "w") as f:
                f.write(window["thought"].get())
            
        # End program if user closes window or
        # presses the OK button
        if event == "close" or event == sg.WIN_CLOSED:
            break

    window.close()
    del(model)