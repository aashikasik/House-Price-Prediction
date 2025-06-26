from flask import Flask, render_template, flash, request, session
import pickle
import mysql.connector
import sys
import numpy as np

app = Flask(__name__)
assert isinstance(app.config, object)
app.config['DEBUG']
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'




@app.route("/")
def home():

    return render_template('index.html')
@app.route("/Home")
def Home():
    return render_template('index.html')



@app.route("/UserLogin")
def UserLogin():
    return render_template('UserLogin.html')


@app.route("/NewUser")
def NewUser():
    return render_template('NewUser.html')


@app.route("/Predict")
def Predict():
    return render_template('Predict.html',price=00)



@app.route("/newproduct", methods=['GET', 'POST'])
def newproduct():
    if request.method == 'POST':
        area = request.form['area']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        stories = request.form['stories']
        mainroad = request.form['mainroad']
        guestroom = request.form['guestroom']
        basement = request.form['basement']
        hotwaterheating = request.form['hotwaterheating']
        airconditioning = request.form['airconditioning']
        parking = request.form['parking']
        prefarea = request.form['prefarea']
        furnished = request.form['furnished']
        Semifurnished = request.form['Semifurnished']



        filename = 'prediction-rfc-model.pkl'
        classifier = pickle.load(open(filename, 'rb'))

        data = np.array([[area, bedrooms, bathrooms, stories, mainroad, guestroom, basement, hotwaterheating, airconditioning, parking,prefarea,furnished,Semifurnished]])

        my_prediction = classifier.predict(data)

        print(my_prediction)

        print(my_prediction[0])
        price = int((my_prediction[0]) * 1000000)
        #price = my_prediction
        print(price)

    return render_template('Predict.html',price=price)




@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        mobile = request.form['mobile']

        email = request.form['email']

        address = request.form['address']

        uname = request.form['uname']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1housepricepy')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name + "','" + email + "','" + mobile + "','" + address + "','" + uname + "','" + password + "','" + gender + "')")
        conn.commit()
        conn.close()
        flash('User Register successfully')

    return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1housepricepy')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "'")
        data = cursor.fetchone()
        if data is None:

            flash('Username or Password is wrong')
            return render_template('UserLogin.html')
        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='1housepricepy')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb where username='" + username + "' and Password='" + password + "'")
            data = cur.fetchall()
            flash("Login successfully")

            return render_template('UserHome.html', data=data)


@app.route("/UserHome")
def UserHome(conn=None):
    uname = session['uname']
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE username = %s", (uname,))
    data = cur.fetchall()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='housepricey')
    conn.set_charset_collation('utf8')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb WHERE username = %s", (uname,))
    data = cur.fetchall()

    return render_template('UserHome.html', data=data)




if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
