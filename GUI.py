import PySimpleGUI as sg # pip install pysimplegui
from myrec import onrec # import onrec function from myrec.py
import transcribe #this is a local file called transcribe.py, we made it
import torch
import subprocess

sg.theme("DarkTeal2")
# in alto a destra c'e' il tasto per chiamare attenzione
# Layout of the graphical interface
layout = [[sg.Text("Record your thought")],
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
          [sg.Multiline("Your thought:", key="thought", size=(50,10),)],
          [sg.Button("save")],
          [sg.Button("close")]] # key is used to get the value of the element, and use later
              
    
print("Is GPU available?",torch.cuda.is_available()) #check if GPU is available
# Create the window
window = sg.Window("Demo", layout, margins=(300, 300))

# Create an event loop
while True:
    event, values = window.read() # Read the event that happened
    # if rec button is pressed
    if event == "rec":
        window["graph"].update(visible=True)
        window["thought"].update("Recording...")
        onrec(window)
        window["graph"].update(visible=False)
    if event=="save":
        print("save")
        with open("file.txt", "w") as f:
            f.write(window["thought"].get())
    if event == "transcribe":
        window["thought"].update("Transcribing, take a coffee...")
        window.refresh() # refresh the window to show the new text above
        result = transcribe.trans()
        window["thought"].update(result["text"])
        with open("file.txt", "w") as f:
            f.write(result["text"])
    if event == "Submit":
        result = transcribe.trans(values["-IN-"])
        window["thought"].update(result["text"])
        with open("file.txt", "w") as f:
            f.write(result["text"])
        print(values["-IN-"])
        
    
    # End program if user closes window or
    # presses the OK button
    if event == "close" or event == sg.WIN_CLOSED:
        break

window.close()