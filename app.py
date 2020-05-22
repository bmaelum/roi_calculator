from flask import Flask, render_template, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(10)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    estateValue         = StringField('estateValue', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})

language = 'NO'

@app.route('/', methods=['GET', 'POST'])
def index():

        loanForm = MyForm()

        loanDict = dict()

        if loanForm.validate_on_submit():
                print('Validated.')
                print(loanDict)
                print(loanDict)
                loanDict['estateValue'] = int(loanForm.estateValue.data)
                loanDict['necessaryEquity'] = int(loanDict['estateValue'] * 0.15)
                loanDict['dokumentAvgift'] = int(loanDict['estateValue'] * 0.025)

                print(loanDict)
        
        else:
                print('Loan form not validated.')


        return render_template('index.html', loanForm=loanForm, loanDict=loanDict)

if __name__ == "__main__":
    app.run(debug=True)