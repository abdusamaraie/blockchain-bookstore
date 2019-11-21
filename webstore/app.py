
import db_init as db
import os
import uuid
from flask import Flask, render_template, request, g, json, redirect, session,jsonify, url_for
from werkzeug import generate_password_hash, check_password_hash
from werkzeug.wsgi import LimitedStream
app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key?'
#database config

class StreamConsumingMiddleware(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        stream = LimitedStream (environ['wsgi.input'],int(environ.get('CONTENT_LENGTH') or 0) ) 
        environ['wsgi.input'] = stream
        app_iter = self.app(environ, start_response)
        try:
            stream.exhaust()
            for event in app_iter:
                yield event
        finally:
            if hasattr(app_iter, 'close'):
                app_iter.close()

app.config['UPLOAD_FOLDER'] = 'static/Uploads'
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)



@app.route('/')
def main():
	
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showSignin')
def showSignin():
    return render_template('login.html')


@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        session['user'] = db.getUser(email)
        if db.userValidate(email,password):
        	return redirect('/userHome')
        else:
        	return render_template('error.html',error = 'Wrong Email address or Password.')

 
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
    	print("success signin")

@app.route('/signUp', methods = ['POST'])
def signUp():

	try:
		name = request.form['inputName']
		email = request.form['inputEmail']
		password = request.form['inputPassword']

			# validate the received values
		if name and email and password:
			if db.userValidate(email,password):
				print("error in render")
				return render_template('error.html',error = 'Email address already exists.')
			else:
				db.addUser(name,email, password)
				return json.dumps({'html':'<span>All fields good and user has been added !!</span>'})
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})

		
	except Exception as e:
		return json.dumps({'error':str(e)})
	finally:
		return redirect('/showSignin')




@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('dashboard.html')
	else:
		return render_template('error.html',error = 'Unauthorized Access')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')


@app.route('/showSell')
def showSell():
    return render_template('Sell.html')

@app.route('/addItem',methods=['POST'])
def addItem():
    try:
        if session.get('user'):
            name = request.form['inputTitle']
            disc = request.form['inputDescription']
            userId = session.get('user')

            if request.form.get('filePath') is None:
            	picURL = ''
            else:
            	picURL = request.form.get('filePath')

            db.add_item(userId,name,disc,picURL)
            item = db.get_items(userId)
            if len(item) is 0:
                return render_template('error.html',error = 'Item is not added!')
            else:
                return redirect('/showSell')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        return render_template('success.html', success = 'Item added')


@app.route('/getItems',methods=['GET'])
def getItems():
	try:
		if session.get('user'):
			userId = session.get('user')

			items = db.get_items(userId)
			items_dict = []

			for i in items:
				item_dict = {
				'Id': i[0],
				'Title': i[1],
				'Description': i[2],
				'FilePath': i[3]
				}
				items_dict.append(item_dict)
			return json.dumps(items_dict)
	except Exception as e:
		return render_template('error.html',error = str(e))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
    	file = request.files['file']
    	extension = os.path.splitext(file.filename)[1]
    	f_name = str(uuid.uuid4()) + extension
    	file.save(os.path.join(app.config['UPLOAD_FOLDER'], f_name))
    	return json.dumps({'filename':f_name})

if __name__ == "__main__":
	app.run(debug=True)



