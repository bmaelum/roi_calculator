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

## Charts
labels = [
    'JAN', 'FEB', 'MAR', 'APR',
    'MAY', 'JUN', 'JUL', 'AUG',
    'SEP', 'OCT', 'NOV', 'DEC'
]

values = [
    967.67, 1190.89, 1079.75, 1349.19,
    2328.91, 2504.28, 2873.83, 4764.87,
    4349.29, 6458.30, 9907, 16297
]

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]



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

@app.route('/line')
def line():
    line_labels=labels
    line_values=values
    return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=line_labels, values=line_values)


if __name__ == "__main__":
    app.run(debug=True)