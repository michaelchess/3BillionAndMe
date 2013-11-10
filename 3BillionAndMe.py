from flask import Flask, request, Response, session, g, redirect, url_for, \
	abort, render_template, flash, send_from_directory, send_file
from werkzeug import secure_filename
import os
import StringIO
from datetime import datetime

DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
application = app
UPLOAD_FOLDER = os.getcwd()
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER#configuring file to save data
app.secret_key = 'HappyHalloween'


@app.route('/')
def initialize():
	#calls initial html
	if 'username' in session:
		return render_template('3BAMLoggedIn.html', genomeInfo = None, loggedInAs=session['username'])
	return render_template('3BAMMainPage.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
    	if request.form['username'] == '3BAMuser':
        	session['username'] = request.form['username']
        	return redirect(url_for('initialize'))
        else:
        	return '''
    			<p>Incorrect Username
        		<form action="" method="post">
        		    <p><input type=text name=username>
        		    <p><input type=submit value=Login>
        		</form>
        		'''
    return '''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('initialize'))

def allowedFile(filename):
	#checks if uploaded file is of the correct type
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def uploadGenome():
	if request.method == 'POST':
		userGenome = request.files['userGenome']
		if userGenome and allowedFile(userGenome.filename):
			dataName = secure_filename(userGenome.filename)
			userGenome.save(os.path.join(app.config['UPLOAD_FOLDER'], dataName))
		else:
			return "Your file was of an incorrect type, please change file type to .txt and try again."
		genomeFile = open(dataName, 'r')
		genomeInfo = genomeFile.read()
		return render_template('3BAMLoggedIn.html', genomeInfo = genomeInfo)

@app.route('/home')
def home():
	print 'Home'
	return render_template('3BAMLoggedIn.html')
	
@app.route('/healthVariants')
def healthVariants():
	print 'Health Variants'
	return render_template('3BAMLoggedIn.html')
	
@app.route('/otherRareVariants')
def otherRareVariants():
	print 'Other Rare Variants'
	return render_template('3BAMLoggedIn.html')
	
@app.route('/ethnicInfo')
def ethnicInfo():
	print 'Ethnic Info'
	return render_template('3BAMLoggedIn.html')
	
@app.route('/about')
def about():
	print 'About'
	return render_template('3BAMLoggedIn.html')
	
if __name__ == '__main__':
	app.run()