import os
from youtube_dl import YoutubeDL
import youtubesearchpython
from youtubesearchpython.internal.constants import ResultMode


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


def download_url(url: str, filename: str) -> tuple:
    """Downloads the mp3 file for the url passed and returns the filename,duration and thumbnail url"""

    fileDirName = filename[:5].replace('.', '')

    # making a new folder and shifting the path to that path     # basically os.chdir is cd (dirname)
    try:
        os.chdir(f'./upload')
    except:
        pass
    os.makedirs('temp', exist_ok=True)

    os.chdir(f'./temp')
    os.makedirs(fileDirName, exist_ok=True)

    os.chdir(f'./{fileDirName}')

    type = "audio"
    if type == "audio":

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

    # name = [f for root, dir, filenames in os.walk(
    #     f"temp/{fileDirName}") for f in filenames if os.path.splitext(f)[1] == '.mp3']

    name = url.split('=')[1]

    os.chdir("./..")

    # songTitle = filename.split()[0]

    # print(os.getcwd())

    # try: # for now fileDirName = 'abcm' , name='LiaYDPRedWQ' , filename='abc.mp3' os.system issue fixed- https://stackoverflow.com/a/47215478/12130497

    try:
        os.renames(f"temp/{fileDirName}/{name}.mp3",
                   f'temp/{fileDirName}/{filename}')
    except FileExistsError:
        pass

        # os.renames(r"C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\temp\abcm\LiaYDPRedWQ.mp3", f'temp/{fileDirName}/{filename}')

    # except FileNotFoundError:
    #     print('FileNotFoundError')

    path = os.getcwd()
    os.chdir(path)
    print(path)

    return filename, data["duration"], data["thumbnails"][0]['url']




if __name__ == '__main__':
    filename = download_url('https://www.youtube.com/watch?v=LiaYDPRedWQ','abc.mp3')
    print(filename)
