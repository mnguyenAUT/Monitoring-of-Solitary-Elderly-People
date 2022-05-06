from PIL import Image
from PIL import GifImagePlugin
from scipy.io.wavfile import write
import pyaudio
import wave
import numpy as np

chunk = 256*32  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
channels = 1
fs = 4000  # Record at 44100 samples per second
seconds = 60
filename = "gif2sound.wav"

p = pyaudio.PyAudio()  # Create an interface to PortAudio

print('Recording')

stream = p.open(format=sample_format,
                channels=channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames

imageObject = Image.open('audio.gif')
bigArray = []
for frame in range(0,imageObject.n_frames):
    imageObject.seek(frame)
    bigData = np.concatenate(np.asarray(imageObject))
    
    frames.append(bigData)

# Stop and close the stream 
stream.stop_stream()
stream.close()
# Terminate the PortAudio interface
p.terminate()

print('Finished recording')

# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()