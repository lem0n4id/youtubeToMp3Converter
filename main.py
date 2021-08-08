from flask import Flask, render_template, request, send_file , session
from downloadsong import *

app = Flask(__name__)
app.secret_key = "SOME SECRET KEY"

@app.route('/', methods=["GET"])
def main():
    '''main page: index.html'''

    # return render_template('music.html',page_title="App Name",video_title="Hello",video_duration="150",video_thumbnail="https://i.ytimg.com/vi/OxGsU8oIWjY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD2_XbqmOsuO-8PQKd9B7RFMW5m6w")
    return render_template('index.html')


@app.route('/music', methods=["GET", "POST"])
def my_form_post():
    '''It has three outputs. 
    1)If song requested is too large(>2400seconds) then it will render FileTooBig.html
    2)The download page
    3)Invalid url page
    '''
    if request.method == "POST":

        # retriving url
        text = request.form['url']
        url = text.strip('\n')
        data = searchSong(url)

        try:

            if data[1] >= 2400:  # max duration= 2400 seconds or 40 minutes

                return render_template('FileTooBig.html')
            else:

                songTitle = data[0]
                title = decorateFilenameValue(songTitle)
                filename = title+'.mp3'
                session['filename'] = filename

                bool = checkIfExists(filename)
                # If file exists then dont download
                if bool == False:
                    data = download_url(url,filename)
                else:
                    pass

                return render_template('music.html', page_title="App Name", video_title=title, video_duration=data[1], video_thumbnail=data[2])

        except TypeError:  # invalid url

            return render_template('InvalidUrl.html')

    # return render_template('music.html', page_title="App Name", video_title='sample', video_duration="150", video_thumbnail="https://i.ytimg.com/vi/OxGsU8oIWjY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD2_XbqmOsuO-8PQKd9B7RFMW5m6w")


@app.route('/dw', methods=["POST"])
def download_anchor():
    """Download Button"""


    # filename = 'sendfile.txt'  # need a way to get this from /music
    filename = session['filename']
    fileDirName = filename[:5].replace('.', '')

    base_path=os.getcwd() #C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload

    os.chdir(base_path)

    filepath = os.path.join(base_path , fileDirName) #C:\Users\Lemon\Documents\GitHub\youtubeToMp3Converter\upload\Demon

    # os.chdir(filepath)

    a=os.getcwd()
    with open('a.txt','w') as f:
        print(a,file=f)

    path = os.path.join(filepath , filename)    
    with open('path.txt','w') as f:
        print(path,file=f)

    # filepath = f"\{fileDirName}\\{filename}"
    # path=os.path.join(base_path,filepath)
    # path = r"upload/downloadFiles.txt"
    @app.teardown_request
    def delete(response):
        delete_mp3file(filename)
        return response
    return send_file(path, as_attachment=True)

    

if __name__ == '__main__':
    app.run()#debug=True)
