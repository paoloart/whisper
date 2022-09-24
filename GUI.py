import myrec
import PySimpleGUI as sg
from myrec import onrec
import transcribe

layout = [[sg.Text("Record your thought")],
          [sg.Button("rec")], 
          [sg.Button("stop")],
          [sg.Button("transcribe")], 
          [sg.Button("close")],
          [sg.Text("Your thought:", key="thought")]]

# add to sg.Text("Your thought are good")
    

# Create the window
window = sg.Window("Demo", layout, margins=(300, 300))

# Create an event loop
while True:
    event, values = window.read()
    # if rec button is pressed
    if event == "rec":
        window["thought"].update("Recording...")
        onrec(window)
    if event == "transcribe":
        window["thought"].update("Transcribing, take a coffee...")
        window.refresh()
        result = transcribe.trans()
        window["thought"].update(result["text"])
    
    # End program if user closes window or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break

window.close()