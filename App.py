from flask import Flask, render_template, request, session, flash, send_file

import mysql.connector
import os
import pandas as pd
import numpy as np
import math
import datetime as dt
import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error, mean_absolute_error, explained_variance_score, r2_score
from sklearn.metrics import mean_poisson_deviance, mean_gamma_deviance, accuracy_score
from sklearn.preprocessing import MinMaxScaler

import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import LSTM

import matplotlib.pyplot as plt
from itertools import cycle
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio

pio.renderers.default = "browser"
# pio.renderers.default = 'png'
from plotly.subplots import make_subplots
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.graph_objects as go
import plotly.io as pio
import pytz
import yfinance as yf
import plotly.express as px
# Set the start and end date for the historical data
from datetime import datetime as dt
import pytz

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from requests import get
from bs4 import BeautifulSoup
import os
from flask import Flask, render_template, request, jsonify

english_bot = ChatBot('Bot',
                      storage_adapter='chatterbot.storage.SQLStorageAdapter',
                      logic_adapters=[
                          {
                              'import_path': 'chatterbot.logic.BestMatch'
                          },

                      ],
                      trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aaa'





@app.route('/')
def home():
    return render_template('index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/Chat')
def Chat():
    return render_template('chat.html')

@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewExpert')
def NewExpert():
    return render_template('NewExpert.html')


@app.route('/ExpertLogin')
def ExpertLogin():
    return render_template('ExpertLogin.html')


@app.route("/ask", methods=['GET', 'POST'])
def ask():
    message = str(request.form['messageText'])
    bott = ''
    bott1 = ''
    sresult1 = ''

    bot_response = english_bot.get_response(message)

    print(bot_response)
    conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')

    cur1 = conn1.cursor()
    cur1.execute(
        "SELECT  * from  chattb where Query='" + message + "'")
    data = cur1.fetchone()

    if data:
        bb = "Expert Name "+ str(data[1])
        bott ="Answer "+str(data[3])

        return jsonify({'status': 'OK', 'answer': bb + bott})

    while True:

        if bot_response.confidence > 0.5:

            bot_response = str(bot_response)
            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

        elif message == ("bye") or message == ("exit"):

            bot_response = 'Hope to see you soon' + '<a href="http://127.0.0.1:5000/UserHome">Exit</a>'

            print(bot_response)
            return jsonify({'status': 'OK', 'answer': bot_response})

            break



        else:

            try:
                url = "https://en.wikipedia.org/wiki/" + message
                page = get(url).text
                soup = BeautifulSoup(page, "html.parser")
                p = soup.find_all("p")
                return jsonify({'status': 'OK', 'answer': p[1].text})



            except IndexError as error:

                bot_response = 'Sorry i have no idea about that.'

                print(bot_response)
                return jsonify({'status': 'OK', 'answer': bot_response})

    # return render_template("index.html")




@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    error = None
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='2stocknew')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            return render_template('index.html', error=error)


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/ExpertInfo")
def ExpertInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM experttb")
    data = cur.fetchall()
    return render_template('ExpertInfo.html', data=data)


@app.route("/newex", methods=['GET', 'POST'])
def newex():
    if request.method == 'POST':
        name = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        uname = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO experttb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('New Expert  Register successfully')
    return render_template('ExpertLogin.html')


@app.route("/exlogin", methods=['GET', 'POST'])
def exlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['ename'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute("SELECT * from experttb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('ExpertLogin.html')
        else:
            session['mob'] = data[4]
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='2stocknew')
            cur = conn.cursor()
            cur.execute("SELECT * FROM experttb where UserName='" + username + "' and password='" + password + "'")
            data = cur.fetchall()

            flash("you are successfully logged in")
            return render_template('ExpertHome.html', data=data)


@app.route('/ExpertHome')
def ExpertHome():
    uname = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM experttb where UserName='" + uname + "' ")
    data = cur.fetchall()
    return render_template('ExpertHome.html', data=data)


@app.route('/QueryInfo')
def QueryInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer ='' ")
    data = cur.fetchall()
    uname = session['ename']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer !=''  and ExpertName='" + uname + "' ")
    data1 = cur.fetchall()

    return render_template('QueryInfo.html', data=data, data1=data1)


@app.route("/ans")
def ans():
    id = request.args.get('id')
    session['id'] = id
    return render_template('Answer.html')

@app.route("/ChatTrain")
def ChatTrain():
    name = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM chattb where ExpertName='" + name + "' ")
    data = cur.fetchall()
    return render_template('ChatTrain.html', data=data)

@app.route("/chattrain", methods=['GET', 'POST'])
def chattrain():
    if request.method == 'POST':
        name = session['ename']
        Query = request.form['Query']
        Answer = request.form['Answer']
        import datetime
        date = datetime.datetime.now().strftime('%d-%b-%Y')

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO chattb VALUES ('','" + name + "','" + Query + "','" + Answer + "','" + date + "')")
        conn.commit()
        conn.close()
        flash('Chatbot train successfully')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM chattb where ExpertName='" + name + "' ")
    data = cur.fetchall()
    return render_template('ChatTrain.html', data=data)


@app.route("/Remove")
def Remove():
    id = request.args.get('id')
    name = session['ename']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cursor = conn.cursor()
    cursor.execute(
        "delete from  chattb  where id='" + id + "'")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM chattb where ExpertName='" + name + "' ")
    data = cur.fetchall()
    return render_template('ChatTrain.html', data=data)

@app.route("/answer", methods=['GET', 'POST'])
def answer():
    if request.method == 'POST':
        name = session['ename']
        id = session['id']
        Query = request.form['Query']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "update  Querytb set Answer='" + Query + "',ExpertName='" + name + "' where id='" + id + "'")
        conn.commit()
        conn.close()
        flash('Answer Info  Update successfully')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer ='' ")
    data = cur.fetchall()
    uname = session['ename']

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where Answer !=''  and ExpertName='" + uname + "' ")
    data1 = cur.fetchall()
    return render_template('QueryInfo.html', data=data, data1=data1)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        uname = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + name + "','" + email + "','" + mobile + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        flash('New User  Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:
            session['mob'] = data[4]
            conn = mysql.connector.connect(user='root', password='', host='localhost',
                                           database='2stocknew')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where UserName='" + username + "' and password='" + password + "'")
            data = cur.fetchall()

            flash("you are successfully logged in")
            return render_template('UserHome.html', data=data)


@app.route('/Search')
def Search():
    from gnewsclient import gnewsclient

    client = gnewsclient.NewsClient(language='english',
                                    location='india',
                                    topic='Business',
                                    max_results=20)

    news_list = client.get_news()

    return render_template('Search.html', data=news_list)

@app.route('/UserHome')
def UserHome():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost',
                                   database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where UserName='" + uname + "' ")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route('/Prediction')
def Prediction():
    return render_template('Prediction.html')


@app.route('/Limit')
def Limit():
    return render_template('Limit.html')



@app.route('/Expenses')
def Expenses():
    return render_template('Expenses.html')

@app.route("/setlimit", methods=['GET', 'POST'])
def setlimit():
    if request.method == 'POST':

        name1 = session['uname']
        mon = request.form['mon']
        yea = request.form['yea']
        amt = request.form['t2']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute("SELECT * from limtb where username='" + name1 + "' and mon='" + mon + "' and yea='" + yea + "'")
        data = cursor.fetchone()
        if data is None:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO limtb VALUES ('','" + name1 + "','" + mon + "','" + yea + "','" + amt + "')")
            conn.commit()
            conn.close()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            # cursor = conn.cursor()
            cur = conn.cursor()
            cur.execute("SELECT * FROM limtb where  username ='" + name1 + "' ")
            data = cur.fetchall()

            return render_template('Limit.html', data=data)



        else:

            flash('Already Set  Expense limit Remove And Set New!')
            return render_template('Limit.html')


@app.route("/dsearch", methods=['GET', 'POST'])
def dsearch():
    if request.method == 'POST':

        import datetime

        name1 = session['uname']
        type = request.form['c1']
        dat = request.form['t1']
        amt = request.form['t2']
        info = request.form['t3']

        file = request.files['fileupload']
        file.save('static/upload/'+file.filename)
        amt1 = 0


       

        if float(amt1) <= float(amt):
            date_object = datetime.datetime.strptime(dat, '%Y-%m-%d').date()

            mon = date_object.strftime("%m")
            yea = date_object.strftime("%Y")
            print(mon)
            print(yea)

            global lim1
            global lim2

            lim1 = 0
            lim2 = 0

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from limtb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "'")
            data = cursor.fetchone()
            if data is None:

                flash('Please Set Expense Limit')
                return render_template('Expenses.html')


            else:

                lim1 = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sum(Amount) as amt  from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "' ")
            data = cursor.fetchone()
            if data is None:
                lim2 = float(0.00)

                # alert = 'Please Set Expense Limit'
                # return render_template('goback.html', data=alert)


            else:

                lim2 = data[0]

            print(lim1)

            if lim2 is None:  # Checking if the variable is None

                lim2 = 0.00
            else:
                print("Not None")

            lim2 = float(lim2) + float(amt)

            if float(lim2) <= float(lim1):

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expensetb VALUES ('','" + name1 + "','" + type + "','" + dat + "','" + amt + "','" + info + "','" + file.filename + "','" +
                    date_object.strftime("%m") + "','" + date_object.strftime("%Y") + "')")
                conn.commit()
                conn.close()

                alert = 'New Expense Info Saved'
                flash('New Expense Info Saved')

                return render_template('Expenses.html',  result=amt)
            else:
                alert = 'Limit Above  Expense'
                msg = "Limit Amt:" + str(lim1) + " Above" + str(lim2)
                sendmsg(session['mob'], msg);
                flash('Limit Above  Expense' + session['mobile'])

                return render_template('Expenses.html',  result=amt)
        else:

            date_object = datetime.datetime.strptime(dat, '%Y-%m-%d').date()

            mon = date_object.strftime("%m")
            yea = date_object.strftime("%Y")
            print(mon)
            print(yea)

            lim1 = 0
            lim2 = 0

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * from limtb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "'")
            data = cursor.fetchone()
            if data is None:

                flash('Please Set Expense Limit')
                return render_template('Expenses.html')


            else:

                lim1 = data[4]

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cursor = conn.cursor()
            cursor.execute(
                "SELECT sum(Amount) as amt  from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + name1 + "' ")
            data = cursor.fetchone()
            if data is None:
                lim2 = float(0.00)

                # alert = 'Please Set Expense Limit'
                # return render_template('goback.html', data=alert)


            else:

                lim2 = data[0]

            print(lim1)

            if lim2 is None:  # Checking if the variable is None

                lim2 = 0.00
            else:
                print("Not None")

            lim2 = float(lim2) + float(amt1)

            if float(lim2) <= float(lim1):

                conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO expensetb VALUES ('','" + name1 + "','" + type + "','" + dat + "','" + str(
                        amt1) + "','" + info + "','" + file.filename + "','" +
                    date_object.strftime("%m") + "','" + date_object.strftime("%Y") + "')")
                conn.commit()
                conn.close()

                alert = 'New Expense Info Saved'
                flash('New Expense Info Saved')

                return render_template('Expenses.html', result=amt1)
            else:
                alert = 'Limit Above  Expense'
                msg = "Limit Amt:" + str(lim1) + " Above" + str(lim2)
                sendmsg(session['mob'], msg);
                flash('Limit Above  Expense' + session['mob'])

                return render_template('Expenses.html', result=amt1)



def sendmsg(targetno,message):
    import requests
    requests.post(
        "http://sms.creativepoint.in/api/push.json?apikey=6555c521622c1&route=transsms&sender=FSSMSS&mobileno=" + targetno + "&text=Dear customer your msg is " + message + "  Sent By FSMSG FSSMSS")

@app.route("/msearch", methods=['GET', 'POST'])
def msearch():
    if request.method == 'POST':
        if request.form["submit"] == "Search":

            mon = request.form['mon']
            yea = request.form['yea']
            uname = session['uname']

            import matplotlib.pyplot as plt

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')

            mycursor = conn.cursor()
            mycursor.execute(
                "select Type, sum(Amount) as MSales from expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + uname + "' group by Type ")
            result = mycursor.fetchall

            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in mycursor:
                Month.append(i[0])
                MSales.append(i[1])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Monthly Expenses")

            plt.show()


            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM expensetb where mon='" + mon + "' and yea='" + yea + "' and Username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('UReport.html', data=data)

        elif request.form["submit"] == "DSearch":
            d1 = request.form['d1']
            d2 = request.form['d2']
            uname = session['uname']

            import matplotlib.pyplot as plt


            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')

            mycursor = conn.cursor()
            mycursor.execute(
                "select Type, sum(Amount) as MSales,date from expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' group by Type ")
            result = mycursor.fetchall

            Month = []
            MSales = []
            Month.clear()
            MSales.clear()

            for i in mycursor:
                Month.append(i[0])
                MSales.append(i[1])

            print("Month = ", Month)
            print("Total Sales = ", MSales)

            # Visulizing Data using Matplotlib
            plt.bar(Month, MSales, color=['yellow', 'red', 'green', 'blue', 'cyan'])
            # plt.ylim(0, 5)
            plt.xlabel("Type")
            plt.ylabel("Total Expenses")
            plt.title("Date To Date  Expenses")
            plt.show()

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM expensetb where date between '" + d1 + "' and '" + d2 + "' and Username='" + uname + "' ")
            data = cur.fetchall()

            return render_template('UReport.html', data=data)

    return render_template('UReport.html')


@app.route("/Report")
def Report():
    name1 = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')

    cur = conn.cursor()
    cur.execute("SELECT * FROM expensetb where username='" + name1 + "' ")
    data = cur.fetchall()

    return render_template('UReport.html', data=data)

@app.route("/remove")
def remove():
    name1 = session['uname']

    did = request.args.get('did')

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cursor = conn.cursor()
    cursor.execute("delete from limtb  where Id='" + did + "' ")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    # cursor = conn.cursor()
    cur = conn.cursor()
    cur.execute("SELECT * FROM limtb where  username ='" + name1 + "' ")
    data = cur.fetchall()

    return render_template('Limit.html', data=data)





@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        ptdate = request.form['days']
        symbol = request.form['symbol']

        #tz = pytz.timezone("America/New_York")
        #start_date = tz.localize(dt(2022, 1, 1))
        #end_date = tz.localize(dt.today())


        #symbol = "AAPL"
        #print(start_date, end_date)

        #df1 = yf.download(symbol, start_date, end_date)
        #maindf = df1.reset_index()
        #maindf['symbol'] = symbol
        #print(maindf)

        import yfinance as yf
        from datetime import datetime as dt, timedelta

        # Define the date range
        start_date = dt(2024, 1, 1).strftime('%Y-%m-%d')
        end_date = (dt.today() - timedelta(days=1)).strftime('%Y-%m-%d')  # One day before today

        #symbol = symbol
        print(f"Start Date: {start_date}, End Date: {end_date}")

        # Download the data
        df1 = yf.download(symbol, start=start_date, end=end_date)

        # Check if data was retrieved
        if df1.empty:
            print(f"No data retrieved for {symbol} between {start_date} and {end_date}.")
        else:
            # Flatten the DataFrame (remove multi-level columns)
            df1.columns = df1.columns.droplevel(1)  # Drop the ticker symbol level
            df1 = df1.reset_index()  # Reset index to make 'Date' a column
            df1['symbol'] = symbol  # Add the symbol column

            # Rename columns to match the desired format
            df1 = df1.rename(columns={
                'Open': 'Open',
                'High': 'High',
                'Low': 'Low',
                'Close': 'Close',
                'Adj Close': 'Adj Close',
                'Volume': 'Volume'
            })

            # Print the DataFrame
            maindf = df1
            print(df1)






        hovertext = []
        for i in range(len(maindf['Open'])):
            hovertext.append('Open: ' + str(maindf['Open'][i]) + '<br>Close: ' + str(maindf['Close'][i]))
        pio.templates.default = "plotly_dark"
        fig = go.Figure(data=go.Candlestick(x=maindf['Date'],
                                            open=maindf['Open'],
                                            high=maindf['High'],
                                            low=maindf['Low'],
                                            close=maindf['Close'], text=hovertext,
                                            hoverinfo='text'))
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_layout(title_text="Stock history")
        fig.show()

        # maindf = pd.read_csv('Data/' + dateset + '.csv')
        print(maindf)

        print('Total number of days present in the dataset: ', maindf.shape[0])
        print('Total number of fields present in the dataset: ', maindf.shape[1])

        print(maindf.shape)

        sd = maindf.iloc[0][0]
        ed = maindf.iloc[-1][0]

        print('Starting Date', sd)
        print('Ending Date', ed)

        maindf['Date'] = pd.to_datetime(maindf['Date'], format='%Y-%m-%d')

        closedf = maindf[['Date', 'Close']]

        closedf = closedf[closedf['Date'] > '2024-02-02']
        close_stock = closedf.copy()
        print("Total data for prediction: ", closedf.shape[0])

        del closedf['Date']
        scaler = MinMaxScaler(feature_range=(0, 1))
        closedf = scaler.fit_transform(np.array(closedf).reshape(-1, 1))
        print(closedf.shape)

        training_size = int(len(closedf) * 0.60)
        test_size = len(closedf) - training_size
        train_data, test_data = closedf[0:training_size, :], closedf[training_size:len(closedf), :1]
        print("train_data: ", train_data.shape)
        print("test_data: ", test_data.shape)

        def create_dataset(dataset, time_step=1):
            dataX, dataY = [], []
            for i in range(len(dataset) - time_step - 1):
                a = dataset[i:(i + time_step), 0]  ###i=0, 0,1,2,3-----99   100
                dataX.append(a)
                dataY.append(dataset[i + time_step, 0])
            return np.array(dataX), np.array(dataY)

        time_step = 15
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, y_test = create_dataset(test_data, time_step)

        print("X_train: ", X_train.shape)
        print("y_train: ", y_train.shape)
        print("X_test: ", X_test.shape)
        print("y_test", y_test.shape)

        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
        X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

        print("X_train: ", X_train.shape)
        print("X_test: ", X_test.shape)

        model = Sequential()

        model.add(LSTM(10, input_shape=(None, 1), activation="relu"))

        model.add(Dense(1))

        model.compile(loss="mean_squared_error", optimizer="adam", metrics=['accuracy'])
        history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=200, batch_size=32, verbose=1)

        acc = history.history['accuracy']
        loss = history.history['loss']
        epochs = range(1, len(acc) + 1)

        acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        epochs = range(len(acc))

        plt.plot(epochs, acc, label='Training Accuracy')
        plt.plot(epochs, val_acc, label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.grid(True)
        # plt.show()

        # Plot Model Loss
        loss_train = history.history['loss']
        loss_val = history.history['val_loss']
        plt.plot(epochs, loss_train, label='Training Loss')
        plt.plot(epochs, loss_val, label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.grid(True)
        plt.show()

        train_predict = model.predict(X_train)
        test_predict = model.predict(X_test)
        train_predict.shape, test_predict.shape

        train_predict = scaler.inverse_transform(train_predict)
        test_predict = scaler.inverse_transform(test_predict)
        original_ytrain = scaler.inverse_transform(y_train.reshape(-1, 1))
        original_ytest = scaler.inverse_transform(y_test.reshape(-1, 1))

        print("Train data RMSE: ", math.sqrt(mean_squared_error(original_ytrain, train_predict)))
        print("Train data MSE: ", mean_squared_error(original_ytrain, train_predict))

        print("-------------------------------------------------------------------------------------")
        print("Test data RMSE: ", math.sqrt(mean_squared_error(original_ytest, test_predict)))
        print("Test data MSE: ", mean_squared_error(original_ytest, test_predict))

        print("Train data explained variance regression score:",
              explained_variance_score(original_ytrain, train_predict))
        print("Test data explained variance regression score:",
              explained_variance_score(original_ytest, test_predict))

        print("Train data R2 score:", r2_score(original_ytrain, train_predict))
        print("Test data R2 score:", r2_score(original_ytest, test_predict))

        look_back = time_step
        trainPredictPlot = np.empty_like(closedf)
        trainPredictPlot[:, :] = np.nan
        trainPredictPlot[look_back:len(train_predict) + look_back, :] = train_predict
        print("Train predicted data: ", trainPredictPlot.shape)

        # shift test predictions for plotting
        testPredictPlot = np.empty_like(closedf)
        testPredictPlot[:, :] = np.nan
        testPredictPlot[len(train_predict) + (look_back * 2) + 1:len(closedf) - 1, :] = test_predict
        print("Test predicted data: ", testPredictPlot.shape)

        names = cycle(['Original close price', 'Train predicted close price', 'Test predicted close price'])

        plotdf = pd.DataFrame({'date': close_stock['Date'],
                               'original_close': close_stock['Close'],
                               'train_predicted_close': trainPredictPlot.reshape(1, -1)[0].tolist(),
                               'test_predicted_close': testPredictPlot.reshape(1, -1)[0].tolist()})

        fig = px.line(plotdf, x=plotdf['date'], y=[plotdf['original_close'], plotdf['train_predicted_close'],
                                                   plotdf['test_predicted_close']],
                      labels={'value': 'Stock price', 'date': 'Date'})
        fig.update_layout(title_text='Comparison between original close price vs predicted close price',
                          plot_bgcolor='white', font_size=15, font_color='white', legend_title_text='Close Price')
        fig.for_each_trace(lambda t: t.update(name=next(names)))

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.show()

        # fig.write_image("images/fig31.png")
        # img = mpimg.imread('images/fig31.png')
        # imgplot = plt.imshow(img)
        # plt.show()

        x_input = test_data[len(test_data) - time_step:].reshape(1, -1)
        print(x_input)
        temp_input = list(x_input)
        temp_input = temp_input[0].tolist()

        lst_output = []
        n_steps = time_step
        i = 0

        pred_days = int(ptdate)

        while i < pred_days:

            if len(temp_input) > time_step:

                x_input = np.array(temp_input[1:])
                # print("{} day input {}".format(i,x_input))
                x_input = x_input.reshape(1, -1)
                x_input = x_input.reshape((1, n_steps, 1))

                yhat = model.predict(x_input, verbose=0)
                # print("{} day output {}".format(i,yhat))
                temp_input.extend(yhat[0].tolist())
                temp_input = temp_input[1:]
                # print(temp_input)

                lst_output.extend(yhat.tolist())
                i = i + 1

            else:

                x_input = x_input.reshape((1, n_steps, 1))
                yhat = model.predict(x_input, verbose=0)
                temp_input.extend(yhat[0].tolist())

                lst_output.extend(yhat.tolist())
                i = i + 1

        print("Output of predicted next days: ", len(lst_output))

        last_days = np.arange(1, time_step + 1)
        day_pred = np.arange(time_step + 1, time_step + pred_days + 1)
        print(last_days)
        print(day_pred)

        temp_mat = np.empty((len(last_days) + pred_days + 1, 1))
        temp_mat[:] = np.nan
        temp_mat = temp_mat.reshape(1, -1).tolist()[0]

        last_original_days_value = temp_mat
        next_predicted_days_value = temp_mat

        last_original_days_value[0:time_step + 1] = \
            scaler.inverse_transform(closedf[len(closedf) - time_step:]).reshape(1, -1).tolist()[0]
        next_predicted_days_value[time_step + 1:] = \
            scaler.inverse_transform(np.array(lst_output).reshape(-1, 1)).reshape(1, -1).tolist()[0]

        new_pred_plot = pd.DataFrame({
            'last_original_days_value': last_original_days_value,
            'next_predicted_days_value': next_predicted_days_value
        })

        names = cycle(['Last 15 days close price', 'Predicted next' + ptdate + 'days close price'])

        fig = px.line(new_pred_plot, x=new_pred_plot.index, y=[new_pred_plot['last_original_days_value'],
                                                               new_pred_plot['next_predicted_days_value']],
                      labels={'value': 'Stock price', 'index': 'Timestamp'})
        fig.update_layout(title_text='Compare last 15 days vs next ' + ptdate + ' days',
                          plot_bgcolor='white', font_size=15, font_color='white', legend_title_text='Close Price')

        fig.for_each_trace(lambda t: t.update(name=next(names)))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.show()

        # fig.write_image("images/fig19.png")
        # img = mpimg.imread('images/fig19.png')
        # imgplot = plt.imshow(img)
        # plt.show()

        lstmdf = closedf.tolist()
        lstmdf.extend((np.array(lst_output).reshape(-1, 1)).tolist())
        lstmdf = scaler.inverse_transform(lstmdf).reshape(1, -1).tolist()[0]

        names = cycle(['Close price'])

        fig = px.line(lstmdf, labels={'value': 'Stock price', 'index': 'Timestamp'})
        fig.update_layout(title_text='Plotting whole closing Stock price with prediction',
                          plot_bgcolor='white', font_size=15, font_color='white', legend_title_text='Stock Price')

        fig.for_each_trace(lambda t: t.update(name=next(names)))

        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.show()

        # fig.write_image("images/fig20.png")
        # img = mpimg.imread('images/fig20.png')
        # imgplot = plt.imshow(img)
        # plt.show()

        name = session['uname']
        import datetime
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO stocktb VALUES ('','" + name + "','" + symbol + "','" + date + "','1')")
        conn.commit()
        conn.close()
        return render_template('Prediction.html')

@app.route('/Target')
def Target():
    return render_template('Target.html')



@app.route("/predict1", methods=['GET', 'POST'])
def predict1():
    if request.method == 'POST':
        amount = request.form['amount']

        import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt
        from sklearn import metrics
        from sklearn.neural_network import MLPRegressor
        import datetime


        # Load dataset
        Stock = pd.read_csv('savings_jan_to_mar_2025.csv', index_col=0)
        df_Stock = Stock.rename(columns={'Amount': 'Amount'})
        print(df_Stock.head())
        print(df_Stock.tail(5))
        print(df_Stock.shape)
        print(df_Stock.columns)

        # Plot the original amount
        df_Stock['Amount'].plot(figsize=(10, 7))
        plt.title("Ex Amount", fontsize=17)
        plt.ylabel('Price', fontsize=14)
        plt.xlabel('Time', fontsize=14)
        plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
        plt.show()

        # Train/Validation/Test split function
        def create_train_test_set(df_Stock):
            features = df_Stock.drop(columns=['Category'], axis=1)
            target = df_Stock['Amount']

            data_len = df_Stock.shape[0]
            print('Historical Stock Data length is - ', str(data_len))

            train_split = int(data_len * 0.50)
            val_split = train_split + int(data_len * 0.3)

            print('Training Set length - ', str(train_split))
            print('Validation Set length - ', str(int(data_len * 0.3)))
            print('Test Set length - ', str(data_len - val_split))

            X_train, X_val, X_test = features[:train_split], features[train_split:val_split], features[val_split:]
            Y_train, Y_val, Y_test = target[:train_split], target[train_split:val_split], target[val_split:]

            print(X_train.shape, X_val.shape, X_test.shape)
            print(Y_train.shape, Y_val.shape, Y_test.shape)

            return X_train, X_val, X_test, Y_train, Y_val, Y_test

        X_train, X_val, X_test, Y_train, Y_val, Y_test = create_train_test_set(df_Stock)

        # Train MLP Regressor
        model = MLPRegressor(hidden_layer_sizes=(100, 50), activation="relu", solver="adam", max_iter=100,
                             random_state=2)
        model.fit(X_train, Y_train)

        # Evaluation
        Y_train_pred = model.predict(X_train)
        Y_val_pred = model.predict(X_val)
        Y_test_pred = model.predict(X_test)

        print("Training RMSE: ", round(np.sqrt(metrics.mean_squared_error(Y_train, Y_train_pred)), 2))
        print("Training MAE: ", round(metrics.mean_absolute_error(Y_train, Y_train_pred), 2))

        print("Test RMSE: ", round(np.sqrt(metrics.mean_squared_error(Y_test, Y_test_pred)), 2))
        print("Test MAE: ", round(metrics.mean_absolute_error(Y_test, Y_test_pred), 2))

        # Validation predictions DataFrame
        df_pred = pd.DataFrame(Y_val.values, columns=['Actual'], index=Y_val.index)
        df_pred['Predicted'] = abs(Y_val_pred)
        df_pred = df_pred.reset_index()
        df_pred.loc[:, 'Date'] = pd.to_datetime(df_pred['Date'])

        print(df_pred)

        # Plot actual vs predicted
        df_pred[['Actual', 'Predicted']].plot()
        plt.title("Actual vs Predicted (Validation Set)")
        plt.xlabel("Index")
        plt.ylabel("Amount")
        plt.grid(True)
        plt.show()

        # Continuous prediction until target is reached
        target_amount = float(amount)
        last_features = X_test.iloc[-1].copy()
        current_date = pd.to_datetime(df_Stock.index[-1])

        future_predictions = []

        while True:
            next_pred = model.predict([last_features])[0]

            # Append prediction
            current_date += datetime.timedelta(days=1)
            future_predictions.append({
                "Date": current_date,
                "Predicted_Amount": next_pred
            })

            # Stop when target is reached
            if next_pred >= target_amount:
                break

            # Update input with new predicted amount (if single feature)
            last_features['Amount'] = next_pred

        # Result DataFrame
        future_df = pd.DataFrame(future_predictions)
        print("\nFuture predictions:")
        print(future_df)

        # Show target hit
        target_row = future_df[future_df['Predicted_Amount'] >= target_amount].iloc[0]
        print(
            f"\n🎯 Target of {target_amount} predicted to be reached on: {target_row['Date'].date()} with amount: {round(target_row['Predicted_Amount'], 2)}")

        # Plot prediction path
        plt.plot(future_df['Date'], future_df['Predicted_Amount'], label="Predicted")
        plt.axhline(y=target_amount, color='red', linestyle='--', label='Target Amount')
        plt.title("Forecast Until Target is Reached")
        plt.xlabel("Date")
        plt.ylabel("Predicted Amount")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        return render_template('Target.html')


@app.route('/Query')
def Query():
    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' ")
    data = cur.fetchall()

    return render_template('NewQuery.html', data=data)


@app.route('/Recommend')
def Recommend():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT UserName,StockName,date, sum(coun) as count FROM stocktb group by UserName,StockName,date ")
    data = cur.fetchall()

    return render_template('Recommend.html', data=data)

@app.route("/newquery", methods=['GET', 'POST'])
def newquery():
    if request.method == 'POST':
        name = session['uname']
        Query = request.form['Query']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Querytb VALUES ('','" + name + "','" + Query + "','','')")
        conn.commit()
        conn.close()
        flash('New Query  Register successfully')

    uname = session['uname']
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='2stocknew')
    cur = conn.cursor()
    cur.execute("SELECT * FROM Querytb where UserName='" + uname + "' ")
    data = cur.fetchall()

    return render_template('NewQuery.html', data=data)


def sendmsg(targetno, message):
    import requests
    requests.post(
        "http://smsserver9.creativepoint.in/api.php?username=fantasy&password=596692&to=" + targetno + "&from=FSSMSS&message=Dear user  your msg is " + message + " Sent By FSMSG FSSMSS&PEID=1501563800000030506&templateid=1507162882948811640")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
