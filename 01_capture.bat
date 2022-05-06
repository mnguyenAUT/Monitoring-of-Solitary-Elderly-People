del video.mp4
ffmpeg -f dshow -i video="j5create 360 Meeting Webcam":audio="Microphone (j5create Meeting Mic)" -to 60 video.mp4
del *.wav
ffmpeg -i video.mp4 audio_orig.wav
ffmpeg -i audio_orig.wav -ar 4000 -ac 1 audio.wav