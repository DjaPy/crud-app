from flask_login import login_user, logout_user, current_user, login_required

from flask import render_template, flash, redirect, url_for, request
from werkzeug.urls import url_parse

from config import connex_app, db
from forms import LoginForm, RegistrationForm
from models import Admin

connex_app.add_api('swagger.yml')


@connex_app.route('/')
@connex_app.route('/index')
@login_required
def index():
    return render_template('home.html')


@connex_app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(login=form.login.data).first()
        if admin is None or not admin.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(admin, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@connex_app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@connex_app.route('/registration', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Admin(login=form.login.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)


if __name__ == "__main__":
    connex_app.run(host='0.0.0.0', port=5000, debug=True)

