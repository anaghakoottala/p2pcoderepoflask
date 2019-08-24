import os
import time
import datetime
import random
import subprocess
import hashlib
import shutil
import sys
from flask import Flask, render_template, redirect, url_for, request,send_from_directory
from werkzeug.utils import secure_filename
from os import path
from flask import send_from_directory
from flask import render_template
from os import path
from serverapp import pushf
from clientapp import pullf


p=os.getenv("HOME")
UPLOAD_FOLDER =p+'/dgit'+"/originalfiles"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','py','c'])

app = Flask(__name__)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def init():
	#path=os.getcwd()
	path=os.getenv("HOME")
	newpath=path+"/dgit"
	paths=path
	newpa=path+"/dgit/"+"/originalfiles"
	
	print("Initialized new dgit repository at" + path)
	if not os.path.exists(newpath):
		os.mkdir(newpath)
	if not os.path.exists(newpa):
		os.mkdir(newpa)
		


	

@app.route('/', methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['password'] != 'password' or request.form['username'] != 'admin':
			error="Invalid password! Try again"
		else:
			init()
			return render_template("base.html")
			
	return render_template("login.html")
	

@app.route('/add',methods=['GET','POST'])
def add():
	
	
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
       
		if file.filename == '':
			flash('No selected file')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			d=os.getenv("HOME")
			dirname=d+'/dgit/'+file.filename
			a=str(os.path.exists(dirname))
			
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
			
			
			
			paths=os.getenv("HOME")
			dirname=paths+'/dgit/'+filename;
			if(a=='False'):
				
				os.mkdir(dirname)
				f = open(os.path.join(dirname, 'record.txt'), 'w')
				f.close()
				
			
			return redirect(url_for('uploaded_file',filename=filename))
                                    

	return render_template("addfile.html")                        
	

	#if request.method == 'POST':
	#	return "Hello"

     #return "Hello"

@app.route('/uploads/<filename>')

def uploaded_file(filename):
	
   	return render_template("fileadded.html")
    	
@app.route('/lists')
def file_list():
	L=[]	
	path=os.getenv("HOME")
	path=path+'/dgit/originalfiles'
	for subdirs,dirs,files in os.walk(path):
		
		for file in files:
			L.append(file)
			
		
		
		
	return render_template('lists.html',list=L)
@app.route('/viewf/<filename>')
def viewf(filename):

	path=UPLOAD_FOLDER+'/'+filename
	with open(path,"r") as f:
		content=f.read()
		
		return render_template('viewf.html',content=content)
				
			# return send_from_directory(UPLOAD_FOLDER,
           #                    filename)


	
@app.route('/commit/<filename>')
def commit(filename):
	ts=time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
	path=os.getcwd()
	filen=path+'/'+filename
	s=os.listdir(path)
	
	mainpath=os.getenv("HOME")
	dirname=mainpath+'/dgit/'+filename
	orgfile=mainpath+'/dgit/originalfiles/'+filename
	new_path=""
	s1=st+'.txt'
	new_path=mainpath+'/dgit/'+s1
	rcrd_path=mainpath+'/dgit/'+filename+'/record.txt'
	f2=open(rcrd_path,"a")
	f2.write(s1)
	f2.write("\n")
	cmd='diff -u '+filename+' '+orgfile+'>'+new_path
	os.system(cmd)
	cmd1='patch -R '+orgfile+'< '+new_path
	os.system(cmd1)
	shutil.move(new_path,dirname)
	return render_template("commit.html")
@app.route('/logs/<filename>')
def log(filename):
	s=[]
	pa=os.getenv("HOME")
	path=pa+'/dgit/'+filename+'/record.txt'
	with open(path,"r") as f:
		line=f.read()
		s.append(line)
	f.close()	
	return render_template('log.html',list=s)


@app.route('/push/<filename>')
def push(filename):

	#os.system("python server0.py")
	mainpath=os.getenv("HOME")
	main_path=mainpath+'/dgit/originalfiles'
	
	pushf(main_path,filename)
	return render_template("push.html")

@app.route('/pull')	
def pull():
	pullf()
	return render_template("pull.html")
		
			

if(__name__=="__main__"):
			app.run(port=5000)

	
