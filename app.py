from flask import Flask,render_template,flash,request,redirect,url_for,session,logging
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt

app=Flask(__name__)

#config MySql
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='myflaskapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#initaialize mysql
mysql=MySQL(app)

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

class RegisterForm(Form):
	name=StringField('name',[validators.Length(min=1,max=50)])
	username=StringField('username',[validators.Length(min=4,max=25)])
	email=StringField('email',[validators.Length(min=6,max=50)])
	password=PasswordField('password',[validators.DataRequired(),validators.EqualTo('confirm',message='passwords do not match')])
	confirm=PasswordField('Confirm Password',[validators.DataRequired()])

@app.route('/register',methods=['GET','POST'])
def register():
	form=RegisterForm(request.form)
	if request.method=='POST' and form.validate():
		name=form.name.data
		email=form.email.data
		username=form.username.data
		password=sha256_crypt.encrypt(str(form.password.data))

		#create cursor 
		cur=mysql.connection.cursor()
		cur.execute("INSERT INTO users(name,email,username,password) VALUES(%s %s %s %s)",(name,email,username,password))
		#commit to the database
		mysql.connection.commit()

		#close connection
		cur.close()

		flash('You are now registerred','success')
		redirect(url_for('index'))

		return render_template('register.html',form=form)
	return render_template('register.html',form=form)


if __name__=='__main__':
	app.run(debug=True)