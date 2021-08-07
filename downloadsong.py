import os
from youtube_dl import YoutubeDL

import subprocess


'''os.system('mkdir temp')
    output on stdout:
    A subdirectory or file temp already exists.
    1
    
    Check docs on os.system(command) and subprocess to avoid this
    '''


'''
Example for using subprocess.Popen():

        args="mkdir upload"
        pipe = subprocess.Popen(args,shell=True, stderr=subprocess.PIPE)
        text=pipe.communicate() #type = tuple
        print(text[1].decode("utf-8"))    
'''


def download_url(url: str) -> str:
    """Downloads the mp3 file for the url passed and returns the filename"""

    # making a new folder and shifting the path to that path
    '''

    # cd doesnt work for some reason using Popen

    args = r'cd ./upload'
    pipe = subprocess.Popen(args, shell=True, stderr=subprocess.PIPE)
    text = pipe.communicate()

    args = r'mkdir temp'
    pipe = subprocess.Popen(args, shell=True, stderr=subprocess.PIPE)
    text = pipe.communicate()

    args = r'cd ./upload/temp'

    pipe = subprocess.Popen(args, shell=True, stderr=subprocess.PIPE)
    text = pipe.communicate()
    print(text)'''

    os.chdir(f'./upload')

    os.system(f'mkdir temp')

    # basically cd to temp
    os.chdir(f'./temp')

    type = "audio"
    if type == "audio":
        # format ydl request to download
        # check https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl and
        # https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312

        # need to change ydl_opts to add select quality feature 

        ydl_opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        # download song
        with YoutubeDL(ydl_opts) as ydl:
            data = ydl.extract_info(url)
    except:
        pass

    # rename the file

    os.chdir('./..')  # cd ..

    name = [f for root, dir, filenames in os.walk(
        f"temp") for f in filenames if os.path.splitext(f)[1] == '.mp3']

    title = data["title"].translate(
        {ord(i): None for i in r'/\:*?"<>|'})  # removes illegal symbols

    os.rename(f"temp/{name[0]}", f'temp/{title}.mp3')

    filename = title+'.mp3'
    return filename


def delete_mp3file(file):
    location = os.getcwd()
    dir = f"temp"
    path = os.path.join(location, dir)
    os.chdir(path)
    os.remove(file)


if __name__ == '__main__':
    filename = download_url('https://www.youtube.com/watch?v=LiaYDPRedWQ')
    delete_mp3file(filename)  # Avril Lavigne - Hello Kitty.mp3
