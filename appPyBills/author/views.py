from appPyBills import app
from flask import render_template, redirect, url_for, session, request, flash
from appPyBills.author.form import RegisterForm, LoginForm
from appPyBills.author.models import Author
from appPyBills.author.decorators import login_required
from appPyBills import bcrypt


@app.route('/login', methods=('GET', 'POST'))
def login():
    if not session.get('username'):
        form = LoginForm()
        error = ''
        if request.method == 'GET' and request.args.get('next'):  # request.args.get will get a URL parameter.
            session['next'] = request.args.get('next')  # This block will only execute on a redirect with 'next' parameter.

        if form.validate_on_submit(): # Won't execute immediately after a redirect - only when form has been submitted.
            author = Author.query.filter_by(  # SELECT * FROM author WHERE...
                username=form.username.data,
                # password=form.password.data  This is how you did it before you learned how to hash.
            ).first()
            if author:
                if bcrypt.check_password_hash(author.password, form.password.data):
                    session['username'] = form.username.data
                    session['is_author'] = author.is_auth
                    flash('User %s logged in.' % form.username.data)
                    if 'next' in session:  # Only if a permissions based redirect has occurred.
                        next = session.get('next')  # next is a python keyword, it works but naughty, remember for next time
                        session.pop('next')  # We don't want to keep redirecting, get the redirect out of the sess. cookie
                        return redirect(next)  # next is a string.
                    else:
                        return redirect(url_for('index'))
                else:
                    error = 'Invalid username/password.'
            else:
                error = 'Invalid username/password.'
        return render_template('author/login.html', form=form, error=error)
    else:
        flash('Logout before logging in again.')
        return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('username')
    session.pop('is_author')
    flash('User logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        return redirect(url_for('reg_successful'))
    return render_template('author/register.html', form=form)


@app.route('/success')
def reg_successful():
    return 'Registration successful.'
