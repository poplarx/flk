from flask import Flask,request,make_response,render_template
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app = Flask(__name__)
#manager = Manager(app)
bootstrap = Bootstrap(app)

class NameForm(Form):
    name = StringField('What is your name?',validators=[Required()])
    submit = SubmitField('Submit')

'''@app.route('/')
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html',form=form,name=name)'''

@app.route('/t')
def index():
    name = ''
    comments = ['HARRY','JANE','LILI']
    return render_template('test.html',name=name,comments=comments)

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

if __name__ == '__main__':
    app.run(debug=True)
