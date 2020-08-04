from flask import Flask, render_template, url_for, request, redirect

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired

import pandas as pd
import numpy as np
import json
import plotly
import plotly.graph_objs as go

import matplotlib.pyplot as plt

import datetime

app = Flask(__name__)

import os
SECRET_KEY = os.urandom(10)
app.config['SECRET_KEY'] = SECRET_KEY

class loanFormClass(FlaskForm):
    estateValue         = StringField('estateValue', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    interestRate        = StringField('interestRate', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    numYears            = StringField('numYears', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})

class fundSavingsFormClass(FlaskForm):
    startingEquity                  = StringField('startingEquity', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    interestRatePercent             = StringField('interestRatePercent', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    numYears                        = StringField('numYears', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    savingsPerMonth                 = StringField('savingsPerMonth', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    costOfFund                      = StringField('costOfFund', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})
    taxRate                         = StringField('taxRate', validators=[DataRequired()], render_kw={"placeholder": "Write a number..."})

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

def create_plot(df_data):

    data = [
        go.Line(
            x=df_data['month'], # assign x as the dataframe column 'x'
            y=df_data['sum_with_return'],
            title = 'Return per Month'
        )
    ]

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def generate_roi_chart(dataDict):

            # Generate labels
            now = datetime.datetime.now()
            labels = np.linspace(now.year, now.year+(dataDict['numYears']-1), num=dataDict['numYears'], endpoint=True)

            # Calculate values
            values = exponential(dataDict['estateValue'], dataDict['interestRate'], dataDict['numYears'])

            line_labels=labels
            line_values=values

            return line_labels, line_values

def generate_fundsavings_chart(dataDict):

            # Generate labels
            now = datetime.datetime.now()
            labels = np.linspace(now.year, now.year+(dataDict['numYears']-1), num=dataDict['numYears'], endpoint=True)

            # Calculate values
            values = exponential(dataDict['startingEquity'], dataDict['interestRate'], dataDict['numYears'])

            line_labels=labels
            line_values=values

            return line_labels, line_values

def exponential(start, base, num_samples):

    samples = [start]

    for i in range(0, num_samples):
        samples.append(int(samples[-1] * base))

    return samples

def fundSavingsROI(dataDict):
    sum_input = dataDict['startingEquity']
    sum_with_return = dataDict['startingEquity']
    MoM_return = dataDict['interestRateMoM']
    cost_of_fund = dataDict['costOfFund']
    tax_rate = dataDict['taxRate']
    num_years = dataDict['numYears']
    accumulated_cost_of_fund = 0

    data_list = []

    year = 1

    for i in range(1, dataDict['numMonths']):
        print('--- Month ' + str(i) + '---')
        sum_input += dataDict['savingsPerMonth']
        sum_with_return += dataDict['savingsPerMonth']
        sum_with_return = int(sum_with_return * (MoM_return))
        print('Accumulated savings:  ' + str(sum_input) + ',-')
        print('With return:          ' + str(sum_with_return) + ',-')
        if i % 12 == 0:
            print('\n- Year ' + str(int(i / 12)) + ' -')
            year += 1
            sum_with_return = int(sum_with_return * (1 - cost_of_fund))
            current_cost_of_fund = int(sum_with_return * cost_of_fund)
            accumulated_cost_of_fund += current_cost_of_fund
            print('Yearly cost of fund = ' + str(round(current_cost_of_fund)) + ',-')
            print('Sum after yearly cost deducted from overall sum = ' + str(sum_with_return) + ',-')
            print('-------------------------\n')

        data_list.append([i, year, sum_input, sum_with_return])
        
    df_data = pd.DataFrame(columns=['month', 'year', 'sum_input', 'sum_with_return'], data=data_list)

    dataDict['accumulated_savings'] = round(sum_input,2)
    dataDict['accumulated_savings_with_return'] = round(sum_with_return,2)
    dataDict['accumulated_cost_of_fund'] = accumulated_cost_of_fund

    total_gain = sum_with_return - sum_input 
    dataDict['total_gain'] = round(total_gain,2)

    gain_after_tax = total_gain * (1 - (tax_rate))
    tax_deduction = total_gain * tax_rate
    print('Tax = ' + str(tax_deduction) + ',-')
    print('Actual gain after ' + str(num_years) + ' years = ' + str(gain_after_tax) + ',-')
    dataDict['tax'] = round(tax_deduction,2)

    total_fund_cost = dataDict['accumulated_cost_of_fund'] + tax_deduction
    print('Total cost of fund = ' + str(total_fund_cost))
    dataDict['total_cost_of_fund'] = round(total_fund_cost)

    dataDict['actual_gain_at_withdraw'] = round(gain_after_tax,2)
    dataDict['actual_gain_at_withdraw']

    dataDict['fortune'] = dataDict['accumulated_savings'] + dataDict['actual_gain_at_withdraw']
    dataDict['fortune']

    return dataDict, df_data

@app.route('/', methods=['GET', 'POST'])
def index():

        loanForm = loanFormClass()

        loanDict = dict()

        if loanForm.validate_on_submit():
                print('Validated.')

                loanDict['estateValue'] = int(loanForm.estateValue.data)
                loanDict ['numYears'] = int(loanForm.numYears.data)

                loanDict['necessaryEquity'] = int(loanDict['estateValue'] * 0.15)
                loanDict['dokumentAvgift'] = int(loanDict['estateValue'] * 0.025)

                loanDict['interestRate'] = float(loanForm.interestRate.data)


                line_labels, line_values = generate_roi_chart(loanDict)

                return render_template('index.html', loanForm=loanForm, loanDict=loanDict, title='ROI per year', min=min(line_values), max=(max(line_values)-min(line_values)), labels=line_labels, values=line_values)
        
        else:
                print('Loan form not validated.')

        return render_template('index.html', loanForm=loanForm, loanDict=loanDict)

@app.route('/fund_savings', methods=['GET', 'POST'])
def fund_savings():
        
    fundSavingsForm = fundSavingsFormClass()

    fundSavingsDict = dict()

    if fundSavingsForm.validate_on_submit():
        print('Validated.')

        fundSavingsDict['startingEquity']       = int(fundSavingsForm.startingEquity.data)
        fundSavingsDict ['numYears']            = int(fundSavingsForm.numYears.data)
        fundSavingsDict ['numMonths']           = int(fundSavingsForm.numYears.data) * 12


        fundSavingsDict['interestRatePercent']  = float(fundSavingsForm.interestRatePercent.data)
        fundSavingsDict['interestRate']         = (fundSavingsDict['interestRatePercent']  / 100) + 1
        fundSavingsDict['interestRateMoM']      = round(fundSavingsDict['interestRate'] ** (1 / 12),4)

        fundSavingsDict['savingsPerMonth']      = int(fundSavingsForm.savingsPerMonth.data)
        fundSavingsDict['costOfFund']           = float(fundSavingsForm.costOfFund.data) / 100
        fundSavingsDict['taxRate']              = float(fundSavingsForm.taxRate.data) / 100

        fundSavingsDict, df_fundsavings = fundSavingsROI(fundSavingsDict)

        print(fundSavingsDict)
        print(df_fundsavings)

        line_labels, line_values = generate_fundsavings_chart(fundSavingsDict)

        bar_plot = create_plot(df_fundsavings)

        return render_template('fund_savings.html', plot=bar_plot, fundSavingsForm=fundSavingsForm, fundSavingsDict=fundSavingsDict, title='ROI per year', min=min(line_values), max=(max(line_values)-min(line_values)), labels=line_labels, values=line_values)
    
    else:
        print('Fund savings form not validated.')

    return render_template('fund_savings.html', fundSavingsForm=fundSavingsForm, fundSavingsDict=fundSavingsDict)

if __name__ == "__main__":
    app.run(debug=True)