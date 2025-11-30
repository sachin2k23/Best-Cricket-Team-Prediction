from flask import Flask, render_template, url_for, request
import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib 
from odibat import *
from odibowl import *
from t20bat import *
from t20bowl import *
from testbat import *
from testbowl import *

connection = sqlite3.connect('user_data.db')
cursor = connection.cursor()

command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('userlog.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT name, password FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchall()

        if len(result) == 0:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')
        else:
            return render_template('userlog.html')

    return render_template('index.html')


@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        command = """CREATE TABLE IF NOT EXISTS user(name TEXT, password TEXT, mobile TEXT, email TEXT)"""
        cursor.execute(command)

        cursor.execute("INSERT INTO user VALUES ('"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        mode = request.form['mode']
        bat = int(request.form['bat'])
        bowl = int(request.form['bowl'])
        name = request.form['name']
        oname = request.form['oname']
        total = bat + bowl
        if total == 11:
            print(mode, bat, bowl, name)
            a = False
            if mode == 'ODI':
                try:
                    bt = custom_ODI_bats(bat, name, oname)
                    bts = []
                    bl = custom_ODI_bowl(bowl, name, oname)
                    bls = []
                    for index, row in bt.iterrows():
                        bts.append([row['Player'], row['Mat'], row['Ave'], row['Runs']])
                    a = True

                    
                    for index, row in bl.iterrows():
                        bls.append([row['Player'], row['Mat'], row['Mdns'], row['Ave'], row['Econ']])
                except:
                    if a:
                        return render_template('userlog.html', msg=bl)
                    else:
                        return render_template('userlog.html', msg=bt)

            if mode == 'T20':
                try:
                    bt = custom_T20_bats(bat, name, oname)
                    bts = []
                    bl = custom_T20_bowl(bowl, name, oname)
                    bls = []
                    for index, row in bt.iterrows():
                        bts.append([row['Player'], row['Mat'], row['Ave'], row['Runs']])
                    a = True

                    
                    for index, row in bl.iterrows():
                        bls.append([row['Player'], row['Mat'], row['Mdns'], row['Ave'], row['Econ']])
                except:
                    if a:
                        return render_template('userlog.html', msg=bl)
                    else:
                        return render_template('userlog.html', msg=bt)

            if mode == 'TEST':
                try:
                    bt = custom_test_bats(bat, name, oname)
                    bts = []
                    bl = custom_ODI_bowl(bowl, name, oname)
                    bls = []
                    for index, row in bt.iterrows():
                        bts.append([row['Player'], row['Mat'], row['Ave'], row['Runs']])
                    a = True

                    
                    for index, row in bl.iterrows():
                        bls.append([row['Player'], row['Mat'], row['Mdns'], row['Ave'], row['Econ']])
                except:
                    if a:
                        return render_template('userlog.html', msg=bl)
                    else:
                        return render_template('userlog.html', msg=bt)

            return render_template('userlog.html', bts=bts, bls=bls)    
        else:
            return render_template('userlog.html', msg="Error: sum of batsmen and bowlers should be equal to 11")   
    return render_template('userlog.html')

@app.route('/logout')
def logout():
    return render_template('index.html')

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

