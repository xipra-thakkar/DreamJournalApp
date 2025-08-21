from flask import Blueprint,render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

authorise=Blueprint('authorise',__name__)

@authorise.route('/sign-in', methods=['GET','POST'])
def signIn():
    if request.method=='POST':
        name=request.form.get('name')
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='error')
        elif not email or not name or not password1 or not password2:
            flash("All fields are required.", category='error')
        elif len(email) < 4:
            flash("Email must be greater than 4 characters.", category='error')
        elif len(name) < 2:
            flash("Name cannot be less than 2 characters.", category='error')
        elif password1 != password2:
            flash("Passwords don't match.", category='error')
        elif len(password1) < 8:
            flash("Password cannot be less than 8 characters.", category='error')
        else:
            new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Sign up successful",category='success')
            return redirect(url_for('views.notes'))
    if request.path == '/sign-in':
        return render_template('signin.html', user=current_user)
    else:
        return redirect(url_for('views.index'))

@authorise.route('/log-in', methods=['GET','POST'])
def logIn():
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.notes'))
            else:
                flash("Incorrect password", category='error')
        else:
            flash("Email does not exist", category='error')
        
    if request.path == '/log-in':
        return render_template('login.html', user=current_user)
    else:
        return redirect(url_for('views.index'))
    
@authorise.route('/log-out')
@login_required
def logOut():
    return redirect(url_for('views.index'))