#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple Flask App

from flask import *
import os
#from werkzeug.utils import secure_filename
app = Flask(__name__)

#searchword = request.args.get('q', '')

UPLOAD_FOLDER = '/media/glusterdata/upload_files'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    
    return "<h2>File Management App</h2><p><A HREF='/file'>Upload</A> | <A HREF='/lists'>List</A></p>"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/file', methods=['GET', 'POST'])
@app.route('/file/<pesan>', methods=['GET', 'POST'])
def upload_file(pesan=""):
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            #filename = secure_filename(file.filename)
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect("/file/File Berhasil di upload")
        else:
            return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>File Select Error!</h1>
            <a href="/file">file</a>
            <p>
            <A HREF='/'>Home</A> | <A HREF="/lists">List of Files</A>
            '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <h3>%s
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
     <p>
            <A HREF='/'>Home</A> | <A HREF="/lists">List of Files</A>
    '''%pesan

@app.route("/lists")
def lists_file():
    data = os.listdir(UPLOAD_FOLDER)
    items = ""
    for f in data:
         item = "<LI>%s</LI>"%f
         items = items + item
    content = "<UL>%s</UL>"%items
    return "<h3>List of Files</h3>%s <p><A HREF='/'>Home</A> | <A HREF='%s'>Upload file</A>"%(content,"/file")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000,debug=True)
