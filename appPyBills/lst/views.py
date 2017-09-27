from appPyBills import app
from flask import render_template, redirect, flash, url_for, session, abort, request
from appPyBills.lst.form import SetupForm, BillForm
from appPyBills import db, uploads
from appPyBills.author.models import Author
from appPyBills.lst.models import Mailbox, Category, Bill
from appPyBills.author.decorators import login_required, auth_required
from appPyBills import bcrypt
from slugify import slugify

BILLS_MAX_PER_PAGE = 5


@app.route('/')
@app.route('/index')
@app.route('/index/<int:page>')
def index(page=1):
    mailbox_exists = Mailbox.query.first()
    if mailbox_exists:
        if session.get('username'):
            author = Author.query.filter_by(username=session.get('username')).first()
            mailbox = Mailbox.query.filter_by(admin=author.id).first()
            if not mailbox:
                flash('User has no mailboxes.')
                return redirect(url_for('setup'))
            bills = Bill.query.filter_by(paid=False, mailbox_id=mailbox.id).order_by(Bill.post_date.desc()).paginate(page, BILLS_MAX_PER_PAGE, False)  # False arg prevents 404
            return render_template('lst/index.html', mailbox=mailbox, bills=bills)
        return redirect(url_for('login'))
    return redirect(url_for('setup'))

@app.route('/admin')
@app.route('/admin/<int:page>')
@auth_required
def admin(page=1):
    if session.get('is_author'):
        author = Author.query.filter_by(username=session.get('username')).first()
        mailbox = Mailbox.query.filter_by(admin=author.id).first()
        if author and mailbox:
            bills = Bill.query.order_by(Bill.post_date.desc()).filter_by(mailbox_id=mailbox.id).paginate(page, BILLS_MAX_PER_PAGE, False)
            return render_template('lst/admin.html', bills=bills)
        else:
            flash('No mailbox for author.')
            return redirect(url_for('login'))
    else:
        abort(403)


@app.route('/setup', methods=("GET", "POST"))
def setup():
    form = SetupForm()  # DON'T FORGET THE FUCKING PARENTHESES
    error = ''
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        author = Author(  # Grab registration form entries.
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True  # Always admin, for now.
        )
        db.session.add(author)
        db.session.flush()  # A flush pushes a change to the database without committing.
        if author.id:  # id is primary key and auto incremented, created by necessity. If it didn't get created, error.
            box = Mailbox(
                form.name.data,
                author.id,  # Foreign key
                form.public.data  # Checkboxes return a bool in sqlalch/wtforms
            )
            db.session.add(box)
            db.session.flush()
        else:
            db.session.rollback()
            error = "Error creating user."
        if author.id and box.id:
            db.session.commit()
            flash('Mailbox created.')
            if box.is_public:
                flash('Public url will be: .../mailbox/%s' % box.public_slug)
            else:
                flash('This is a private mailbox.')
            return redirect(url_for('index'))
        else:
            db.session.rollback()
            error = "Error creating mailbox."

    return render_template('lst/setup.html', form=form, error=error)


@app.route('/post', methods=('GET', 'POST'))
@auth_required
def post():
    form = BillForm()
    if form.validate_on_submit():
        pdf = request.files['pdf']
        filename = None
        try:
            filename = uploads.save(pdf)
        except:
            flash('File could not be uploaded.')
        if form.new_category.data:  # If a new category specified...
            new_category = Category(form.new_category.data)
            db.session.add(new_category)
            db.session.flush()
            category = new_category
        elif form.cat_rel.data:  # Use an existing category
            category_id = form.cat_rel.get_pk(form.cat_rel.data)
            category = Category.query.filter_by(id=category_id).first()
        else:
            category = None  # You don't need one, it's just for filtering.
        author = Author.query.filter_by(username=session['username']).first()
        box = Mailbox.query.filter_by(admin=author.id).first()
        issuer = form.issuer.data
        due_date = form.due_date.data.strftime('%Y-%m-%d')  # only one bill/provider/day
        slug = slugify(issuer + ' ' + due_date + ' ' + author.username)
        amount = form.amount.data

        # TO BE ADDED: BPay interface... ideally you'd just punch in the code and the issuer would populate.

        bill = Bill(box, author, issuer, due_date, category, amount, pdf=filename, slug=slug)
        db.session.add(bill)
        db.session.commit()
        return redirect(url_for('view_bill', slug=slug))

    return render_template('lst/post.html', action="new", form=form)


@app.route('/viewbill/<slug>')
def view_bill(slug):
    view = Bill.query.filter_by(slug=slug).first_or_404()
    return render_template('lst/view.html', view=view)


@app.route('/delete/<int:bill_id>')
@auth_required
def delete(bill_id):
    author = Author.query.filter_by(username=session.get('username')).first()
    mailbox = Mailbox.query.filter_by(admin=author.id).first()
    if author and mailbox:
        bill = Bill.query.filter_by(id=bill_id).first_or_404()
        if bill.mailbox_id != mailbox.id:  # Shenanigans.
            abort(403)
        else:
            bill.paid = True
            db.session.commit()
            flash('Bill marked as paid.')
            return redirect(url_for('admin'))
    return redirect(url_for('login'))


@app.route('/edit/<int:bill_id>', methods=("GET", "POST"))
@auth_required
def edit(bill_id):
    author = Author.query.filter_by(username=session.get('username')).first()
    mailbox = Mailbox.query.filter_by(admin=author.id).first()
    bill = Bill.query.filter_by(id=bill_id).first_or_404()
    if bill.mailbox_id == mailbox.id:
        form = BillForm(obj=bill)
        if form.validate_on_submit():
            original_bill = bill.pdf
            form.populate_obj(bill)
            if form.pdf.has_file():
                pdf = request.files.get('pdf')
                try:
                    filename = uploads.save(pdf)
                except:
                    flash('Failed to upload new PDF.')
                if filename:
                    bill.pdf = filename
            else:
                bill.pdf = original_bill
            if form.new_category.data:
                new_category=Category(form.new_category.data)
                db.session.add(new_category)
                db.session.flush()
                bill.cat_rel=new_category
            db.session.commit()
            return redirect(url_for('view_bill', slug=bill.slug))

        return render_template('lst/post.html', form=form, bill=bill, action="edit")
    else:  # Shenanigans
        abort(403)


@app.route('/mailbox/<slug>/')  # Publicly available mailboxes
@app.route('/mailbox/<slug>/<int:page>')
def public(slug, page=1):
    box = Mailbox.query.filter_by(public_slug=str(slug), is_public=True).first_or_404()
    if box:
        bills = Bill.query.filter_by(paid=False, mailbox_id=box.id).order_by(Bill.post_date.desc()).paginate(page, BILLS_MAX_PER_PAGE, False)  # False arg prevents 404
        return render_template('lst/public.html', mailbox=box, bills=bills)
    return redirect(url_for('login'))
