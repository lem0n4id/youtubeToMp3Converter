from flask import Flask, request, render_template, send_file, redirect, abort
# ffmpeg==1.4

from flask.wrappers import Response
app = Flask(__name__)


@app.route('/')
def index() -> Response:
   return render_template('index.html')


@app.route('/download')
def download_anchor() -> Response:
	
	
   try:
      path = r"upload/downloadFile.txt"
      # path = r"upload/downloadFiles.txt"
      return send_file(path, as_attachment=True)
   except:
         return redirect('/downloadfailed')
      


@app.route('/downloadfailed')
def downloadFailed() -> Response:
   try:
      return render_template('fileError.html')
   except:
        abort(404)




if __name__ == '__main__':
   app.run(debug = True)
