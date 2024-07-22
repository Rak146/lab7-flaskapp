from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    err_msg = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for('secretPage'))
        else:
            err_msg = "Invalid credentials!"
    return render_template('signin.html', err_msg=err_msg)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    err_msg = None
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        
        if password != c_password:
            err_msg = "passwords do not match!"
        else:
            exist_usr = User.query.filter_by(email=email).first()
            if exist_usr:
                err_msg = "email address already used! Please use another email."
            else:
                new_user = User(first_name=first_name, last_name=last_name, email=email, password=password)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('thankyou'))
    return render_template('signup.html', err_msg=err_msg)

@app.route('/secretPage')
def secretPage():
    return render_template('secretPage.html')

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

if __name__ == '__main__':
    app.run(debug=True)
