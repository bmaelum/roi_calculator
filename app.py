from flask import Flask, render_template, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(10)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    investment  = StringField('pclass', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/index2')
def index2():
        return render_template('index2.html')

@app.route('/index3', methods=['GET', 'POST'])
def index3():

        form = MyForm()

        if form.validate_on_submit():
                print('Validated.')
                investment = form.investment.data
                

        return render_template('index3.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)