# -*- coding: utf-8 -*-
import os
import zipfile
from flask import Flask, render_template,request,redirect,url_for,session
from flask_uploads import UploadSet, configure_uploads, IMAGES,TEXT, patch_request_class
from flask_wtf import FlaskForm
from werkzeug import secure_filename
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField,TextField,PasswordField,Form
from docker_container import container

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I have a dream'
ALLOWED_EXTENSIONS = set(['txt','py', 'pdf', 'png', 'zip','jpg', 'jpeg', 'gif'])
app.config['UPLOADED_PHOTOS_DEST'] = '/web/data'
class LoginForm(Form):
    username = TextField("username")
    password = PasswordField("password")
    submit = SubmitField(u'login')
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET','POST'])
def login():
	Form = LoginForm(request.form)
	if request.method=='POST':
		session['username']=request.form['username']
		session['password']=request.form['password']
		return redirect(url_for('upload_file'))
	return render_template('user.html',form=Form)
@app.route('/', methods=['GET','POST'])
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	if session.get('username')=='hydsoft' and session.get('password') == '1qaz@WSX':
		if request.method == 'POST':
			file = request.files['file']
			message = '请上传正确格式的文件'
			if file and allowed_file(file.filename):
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
				suffix = filename.rsplit('.', 1)[1]
				if suffix == 'py':
					container1 = container()
					container1.create_container(filename)
					return redirect(url_for('program_logs',filename=filename))
				elif suffix == 'zip':
					pakage_name = filename.rsplit('.', 1)[0]
					pakage = zipfile.ZipFile(app.config['UPLOADED_PHOTOS_DEST']+'/'+filename,'r')
					for p in pakage.namelist():
						pakage.extract(p,app.config['UPLOADED_PHOTOS_DEST']+'/'+pakage_name)
					pakage.close()
					os.remove(app.config['UPLOADED_PHOTOS_DEST']+'/'+filename)
					container2 = container()
					container2.create_container('main.py')
					return redirect(url_for('program_logs'))
					
			else:
				return render_template('upload.html',message=message)
		return render_template('upload.html')
	else:
		return redirect(url_for('login'))
@app.route('/logs')
def program_logs ():
	longline = ''
	message=open('/opt/logs', 'r').readlines()
	for line in message:
		longline +='<li>'+line.strip()+'</li>'
	return render_template('build_program.html',message=longline)
	
if __name__ == '__main__':
    app.run(host='0.0.0.0')
