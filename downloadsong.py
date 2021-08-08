import os
from youtube_dl import YoutubeDL
import youtubesearchpython
from youtubesearchpython.internal.constants import ResultMode


import subprocess
import shutil


def checkIfExists(filename: str) -> bool:
    '''Checks if the file is present in ./upload or not'''
    result = [filename for root, dir, files in os.walk('./upload')
              if filename in files]
    if len(result) > 0:
        return True
    else:
        return False


def decorateFilenameValue(title: str) -> str:
    '''removes illegal symbols from the song title '''
    title = title.translate(
        {ord(i): None for i in r'/\:*?"<>|'})

    return title


def searchSong(url: str):
    '''Searches the url and returns title, durationSeconds, thumbnail.
    Returns None if invalid url'''

    try:
        video = youtubesearchpython.Video.get(url, mode=ResultMode.dict)
        title = video["title"]
        thumbnail = video["thumbnails"][0]["url"]
        durationMs = video["streamingData"]["formats"][0]["approxDurationMs"]
        durationSeconds = round(int(durationMs)/1000)
    except:
        return None

    return title, durationSeconds, thumbnail


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
def subprocess_cm(args):
    pipe = subprocess.Popen(args,shell=True, stderr=subprocess.PIPE)
    text=pipe.communicate()
    return text

def download_url(url: str) -> tuple:
    """Downloads the mp3 file for the url passed and returns the filename,duration and thumbnail url"""

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
    try:
        os.chdir(f'./upload')
    except:
        pass
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

    songTitle = data['title']
    title = decorateFilenameValue(songTitle)

    os.rename(f"temp/{name[0]}", f'temp/{title}.mp3')

    path = os.getcwd()
    os.chdir(path)

    filename = title+'.mp3'
    return filename, data["duration"], data["thumbnails"][0]['url']


def delete_mp3file(file):
    location = os.getcwd()
    dir = r"upload\temp"
    path = os.path.join(location, dir)
    
    args=f'cd {path}'
    print(path)
    # b=subprocess_cm(args)

    # print(b)
    print(os.getcwd())
    path='upload/temp'
    os.chdir(path)
    print('workind dict',os.getcwd())
    b=subprocess_cm('ls')
    print(b)
    name = [filenames for root, dir, filenames in os.walk(
        f"upload") ]
    print(name)
    # try:
    # os.remove('C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\temp\sng')
    # except FileNotFoundError:
        # print('file not found')




if __name__ == '__main__':
    # filename = download_url('https://www.youtube.com/watch?v=LiaYDPRedWQ')
    # delete_mp3file(filename)  # Avril Lavigne - Hello Kitty.mp3
    # checkIfExists('Harry Styles - Watermelon Sugar (Official Video).mp3')
    a='Demon Slayer Kimetsu no Yaiba OP - Gurenge - LiSA - Cover (fingerstyle guitar) Anime.mp3'
    # delete_mp3file(a)
    # os.remove(r"C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\temp\Demon Slayer Kimetsu no Yaiba OP - Gurenge - LiSA - Cover (fingerstyle guitar) Anime.mp3")
    os.remove(r'C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\temp\Demon Slayer Kimetsu no Yaiba OP - Gurenge - LiSA - Cover (fingerstyle guitar) Anime.mp3')
    # shutil.rmtree(r'C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\temp\sng')

    '''
    To Do-
    Change file system from /temp/..mp3 to /temp/{filename[:5].remove('.')}/...mp3
    change os.remove to shutil.rmtree
    '''