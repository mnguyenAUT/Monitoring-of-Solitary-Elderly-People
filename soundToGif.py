import pyaudio
import wave
from pydub import AudioSegment
import cv2
import numpy as np
from PIL import Image
import subprocess
import imageio

#subprocess.call(['ffmpeg', '-i', 'test.mp3', 'sound.wav'])

filename = 'audio.wav'
# convert wav to mp3                                                            
#sound = AudioSegment.from_mp3(filename)
#sound.export("sound.wav", format="wav")

images = []

ZISE = 256
SIZE = 32

# Set chunk size of 1024 samples per data frame
chunk = SIZE*ZISE  

# Open the sound file 
wf = wave.open(filename, 'rb')

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
Counter = wf.getsampwidth() * wf.getnchannels()

#print (p.get_format_from_width(wf.getsampwidth()))
#return 0

stream = p.open(format = p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = wf.getframerate(),
                output = True)

# Read data in chunks
data = wf.readframes(chunk)

# Play the sound by writing the audio data to the stream
counter = 0
while data != '':
    counter = counter + 1
    data = wf.readframes(chunk)
    #data = np.empty(512*512)
    #print(data)
    img = np.zeros((SIZE*Counter,ZISE), np.uint8) #with 3 chanels # img2 = img1.copy()
    if len(data) < SIZE*Counter*ZISE:
        break
    img.data = data 
    
    cv2.imshow("img", img)
    cv2.waitKey(1)
    #cv2.imwrite("test.png", img)
    #img=cv2.imread("test.png")
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    im = Image.fromarray(img)
    im.save("wav.png")    #use jpg to add noise
    img = Image.open("wav.png")  
    images.append(img)
    bigData = np.concatenate(np.asarray(img))
    
    #print(bigData)
    stream.write(bigData)
    
    #break
#images[0].save('audio.gif', save_all=True, append_images=images[1:])
imageio.mimsave('audio.gif', images, fps=2)  
# Close and terminate the stream
print(counter)
stream.close()
p.terminate()

