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
                    data = download_url(url)
                else:
                    pass

                return render_template('music.html', page_title="App Name", video_title=title, video_duration=data[1], video_thumbnail=data[2])

        except TypeError:  # invalid url

            return render_template('InvalidUrl.html')

    # return render_template('music.html', page_title="App Name", video_title='sample', video_duration="150", video_thumbnail="https://i.ytimg.com/vi/OxGsU8oIWjY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD2_XbqmOsuO-8PQKd9B7RFMW5m6w")


@app.route('/dw', methods=["POST"])
def download_anchor():
    """Download Button"""
    try:

        # filename = 'sendfile.txt'  # need a way to get this from /music
        filename = session['filename']
        path = "upload/temp/"+filename
        # path = r"upload/downloadFiles.txt"
        return send_file(path, as_attachment=True)

    except:
        pass

@app.route('/about', methods=["GET","POST"])
def About():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
