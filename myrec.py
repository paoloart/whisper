import pyaudio # library to record audio
import wave #library to save mp3 file

def onrec(window):

    chunk = 1024  # Record in chunks of 1024 samples, pieces of audio
    sample_format = pyaudio.paInt32  # 16 bits per sample, paInt32 stands for 32 bits, 16 bits is paInt16
    channels = 1 # 1 is mono, 2 is stereo
    fs = 44100  # Record at 44100 samples per second
    filename = "input.mp3"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')
    # open a new stream to write the audio data, which means we are recording!
    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames
    # Store data in chunks
    while True:
        data = stream.read(chunk)
        frames.append(data)
        event, values = window.read(timeout=1)
        if event == "stop":
            window["thought"].update("Recording stopped")
            break        

    print(len(frames))
    # Stop and close the stream , or stop recording
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb') # wb stands for write binary
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames)) # b stands for bytes. we use b because we are writing bytes
    wf.close()
    