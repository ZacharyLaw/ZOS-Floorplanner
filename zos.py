'''
python3 ./hello.py
py -m pip install flask
'''
from flask import Flask, render_template, request,redirect,url_for
import sqlite3
app=Flask(__name__)
@app.route('/create')
def create():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("CREATE TABLE user(email TEXT PRIMARY KEY,password TEXT,json TEXT);")
    print('done')
@app.route('/')
def planner():
    return render_template('planner.html')
@app.route('/account/<email>')
def userplanner(email=None):
    return render_template('planner.html',email=email)
@app.route('/save', methods=['GET', 'POST'])
def save():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    c.execute("UPDATE user SET json = ? WHERE email = ?",(request.form['Json'],request.form['Email']))
    conn.commit()
    return render_template('planner.html',email=request.form['Email'],jsontxt=request.form['Json'])
@app.route('/account', methods=['GET', 'POST'])
def login():
    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    error = None
    if request.method == 'POST':
        c.execute("SELECT * FROM user WHERE email=?",(request.form['Email'],))
        result=c.fetchone()
        if len(request.form)==3:
            if request.form['Password']!=request.form['Confirm Password']:
                error = 'Invalid Confirm Password. Please try again.'
            elif c.fetchone():
                error = 'Account already made. Please try again.'
            else:
                c.execute("""INSERT INTO user VALUES (?,?,?)""",(request.form['Email'], request.form['Password'],None))
                conn.commit()
                return redirect(url_for('userplanner',email=request.form['Email']))
            return render_template('account.html', err=error)
        else:
            if not result:
                error = 'Email not found. Please try again.'
            elif result[1]!=request.form['Password']:
                error = 'Password incorrect. Please try again.'
            elif result[1]==request.form['Password']:
                return render_template('planner.html',email=request.form['Email'],jsontxt=result[2])
            return render_template('account.html', err2=error)
    return render_template('account.html')
if __name__=='__main__':
    app.debug=True
    app.run(host="0.0.0.0",port=8000)
