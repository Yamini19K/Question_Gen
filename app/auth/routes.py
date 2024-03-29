from flask import render_template, flash, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from app.auth.forms import RegistrationForm, LoginForm
from app.auth import authentication as at
from app.auth.models import User


@at.route('/register', methods=['GET', 'POST'])
def register_user():
    if current_user.is_authenticated:
        flash('You are already logged-in','info')
        return redirect(url_for('main.home'))

    form = RegistrationForm()

    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data)
        flash('Registration Successful', 'success')
        return redirect(url_for('authentication.my_login_user'))
    return render_template('registration.html', form=form)


@at.route('/login', methods=['GET', 'POST'])
def my_login_user():
    if current_user.is_authenticated:
        flash('You are already logged-in', 'info')
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()

        if not user or not user.check_password(form.password.data):
            flash('Invalid Credentials, Please try again', 'error')
            return redirect(url_for('authentication.do_the_login'))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for('main.home'))
    return render_template('login.html', form=form)


@at.route('/logout')
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for('main.home'))