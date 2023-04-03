import os

for sound in os.listdir():
    if sound.find(".wav") != -1:
        os.system("ffmpeg -y -i \".\\" + sound + "\" -vn -ar 48000 -ac 2 -b:a 320k \".\\" + sound.split(".wav")[0] + ".mp3\"")