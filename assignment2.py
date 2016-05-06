from flask import Flask
from flask import render_template
import os
from flask import request
from flask import redirect


app = Flask(__name__)
app.debug = True


import sqlite3
from flask import g

DATABASE = './database.db'


def connect_to_database():
    db = sqlite3.connect(DATABASE)
    
    with db:
        db.execute('CREATE TABLE if not exists messages(pkey integer primary key, firstname,lastname,email,country,comment)')
    return db

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
@app.route('/Homepage.html')
def Homepage():
    return render_template('Homepage.html')


@app.route('/AboutMe.html')
def AboutMe():
    return render_template('AboutMe.html')

@app.route('/ContactUs.html', methods=['GET', 'POST'])
def ContactUs():
    
    if request.method == 'GET':
        return render_template('ContactUs.html')

    firstname = request.form['firstname']
    lastname = request.form['lastname']
    email = request.form['email']
    country = request.form['country']
    comment = request.form['comment']

    db = get_db()
    
    with db:
        db.execute('INSERT INTO messages(firstname,lastname,email,country,comment)VALUES(?,?,?,?,?)', (firstname,lastname,email,country,comment))

    return redirect('ContactUsThankYou.html')


@app.route('/ContactUsThankYou.html')
def ContactUsThankYou():
    return render_template('ContactUsThankYou.html')
@app.route('/Cv.html')
def Cv():
    return render_template('Cv.html')

@app.route('/Portfolio.html')
def Portfolio():
    return render_template('Portfolio.html')

@app.route('/Reflection.html')
def Reflection():
    return render_template('Reflection.html')






if __name__ == '__main__':
    # http://damyanon.net/getting-started-with-flask-on-cloud9/
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))




