#---coding: utf8 ---#
import os
from flask import Flask,request,make_response,render_template,url_for,session,redirect,flash
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask.ext.moment import Moment
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy


base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the cup is blue'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(base_dir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField(u'什么鬼')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    users = db.relationship('User',backref='role')


    def __repr__(self):
        return '<Role: %s>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True,index=True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<Role: %s>' % self.username


@app.route('/',methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash("It seems that you changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html',form=form,name=session.get('name'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/cookie')
def cookie():
    r = make_response('Cookies will be set here.')
    r.set_cookie('answer','43')
    return r

@app.route('/tml1')
def template1():
    return render_template('index.html')

@app.route('/tml2/<name>')
def template2(name):
    return render_template('user.html',name=name)

@app.route('/show')
def show_page_urls():
    urls = [url_for('index',_external=True),url_for('user',name='BIGk',_external=True)]
    return render_template('urls.html',urls=urls)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    manager.run()
