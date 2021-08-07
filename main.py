from flask import Flask , render_template, request

app = Flask(__name__)

@app.route('/',methods =["GET"])
def main():

    # return render_template('music.html',page_title="App Name",video_title="Hello",video_duration="150",video_thumbnail="https://i.ytimg.com/vi/OxGsU8oIWjY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD2_XbqmOsuO-8PQKd9B7RFMW5m6w")
    return render_template('index.html')

@app.route('/ABC', methods =["GET", "POST"])
def my_form_post():
    if request.method == "POST":
        text = request.form['url']
        processed_text = text.upper()
        return render_template('music.html',page_title="App Name",video_title=processed_text,video_duration="150",video_thumbnail="https://i.ytimg.com/vi/OxGsU8oIWjY/hqdefault.jpg?sqp=-oaymwEcCNACELwBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLD2_XbqmOsuO-8PQKd9B7RFMW5m6w")

app.run(debug=True)
