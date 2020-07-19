from flask import Flask, render_template, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

import numpy as np

import datetime

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(10)
app.config['SECRET_KEY'] = SECRET_KEY

class MyForm(FlaskForm):
    estateValue         = StringField('estateValue', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    interestRate        = StringField('interestRate', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    numYears           = StringField('numYears', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})


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

def generate_chart(dataDict):

            # Generate labels
            now = datetime.datetime.now()
            labels = np.linspace(now.year, now.year+(dataDict['numYears']-1), num=dataDict['numYears'], endpoint=True)

            # Calculate values
            values = exponential(dataDict['estateValue'], dataDict['interestRate'], dataDict['numYears'])

            line_labels=labels
            line_values=values

            return line_labels, line_values

def exponential(start, base, num_samples):

    samples = [start]

    for i in range(0, num_samples):
        samples.append(int(samples[-1] * base))

    return samples

@app.route('/', methods=['GET', 'POST'])
def index():
        return render_template('index.html')

@app.route('/index2')
def index2():
        return render_template('index2.html')

        if loanForm.validate_on_submit():
                print('Validated.')

                loanDict['estateValue'] = int(loanForm.estateValue.data)
                loanDict ['numYears'] = int(loanForm.numYears.data)

                loanDict['necessaryEquity'] = int(loanDict['estateValue'] * 0.15)
                loanDict['dokumentAvgift'] = int(loanDict['estateValue'] * 0.025)

                loanDict['interestRate'] = float(loanForm.interestRate.data)


                line_labels, line_values = generate_chart(loanDict)

                return render_template('index.html', loanForm=loanForm, loanDict=loanDict, title='ROI per year', min=min(line_values), max=(max(line_values)-min(line_values)), labels=line_labels, values=line_values)
        
        else:
                print('Loan form not validated.')

        return render_template('index.html', loanForm=loanForm, loanDict=loanDict)

        return render_template('index3.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)