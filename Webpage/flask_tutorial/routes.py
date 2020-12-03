import os
import secrets
from flask import *
import threading
from socket import *
from PIL import ImageGrab
import numpy as np
import math
import time

from flask import render_template, jsonify, url_for, flash, redirect,request
from flask_tutorial import app, db, bcrypt
from flask_tutorial.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_tutorial.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from flask_tutorial.forms import RegistrationForm, LoginForm






@app.route('/')         #app.route는 기호를 통하여 다른 페이지 정의


@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in ', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Login successful!' ,'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET','POST'])
@login_required
def account():
    form =UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.email.data=current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form = form)

@app.route("/controller")
@login_required
def controller():
    flash('12:07:47 GMT+0900 (대한민국 표준시) - connected!')
    return render_template('controller.html', title='Controller')

a=0
@app.route('/_stuff', methods = ['POST'])
def stuff():
    global a

    multiplier = request.form.get('multiplier')
    a = a + multiplier

    return jsonify(result=a)
# @app.route('/_stuff', methods = ['GET'])
# def stuff():
#     global msg
#     return jsonify(result=msg)


# @app.route('/robot_location')
# def robot_location():
#     global rob_loc
#     serverSocket = socket(AF_INET, SOCK_STREAM)
#     serverSocket.bind((TCP_IP_LOC,TCP_PORT_LOC))
#     serverSocket.listen(0)
#     connectionSocket, _ = serverSocket.accept()
   
#     while True:
#         data = connectionSocket.recv(8192)
#         rob_loc = eval(data.decode())
#         print(rob_loc)
#         connectionSocket.send('success'.encode())
#         serverSocket.close()
#     return "rob_loc"

# @app.route('/video_feed')
# def video_feed():
#     redirect(url_for('ordering'))
#     square = (348,194,1493,660)
#     return Response(gen_bboxed_frames(square),
#                     mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/TTS')
# def TTS():
#     TTS_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#     TTS_socket.connect('192.168.70.5',41000)
#     while True:
#         TTS_socket.send(TTS_text.encode())
#     return 'TTS'

# if __name__ == '__main__':
#     app.run(debug=True, port=12000, host = '172.22.77.52')       # flask run 커맨드를 해주지 않고도 flask server를 실행
