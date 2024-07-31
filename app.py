from flask import Flask, render_template, request, redirect, url_for, session
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

WEBHOOK_URL = os.getenv('WEBHOOK_URL')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/california-management')
def california_management():
    return render_template('california_management.html')

@app.route('/california-roleplay')
def california_roleplay():
    return render_template('california_roleplay.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/appeal', methods=['GET', 'POST'])
def appeal():
    if request.method == 'POST':
        appeal_type = request.form['type']
        reason = request.form['reason']
        ban_reason = request.form['ban_reason']
        
        data = {
            "type": appeal_type,
            "reason": reason,
            "ban_reason": ban_reason
        }
        
        requests.post(WEBHOOK_URL, json=data)
        return redirect(url_for('index'))
    return render_template('appeal.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('admin_login.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' in session:
        return render_template('admin_dashboard.html')
    return redirect(url_for('admin_login'))

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
