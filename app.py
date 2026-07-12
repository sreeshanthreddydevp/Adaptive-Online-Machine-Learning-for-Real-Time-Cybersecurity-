import warnings
warnings.filterwarnings('ignore')

from flask import Flask, request, jsonify, render_template, redirect, url_for
import joblib
import pandas as pd
import numpy as np

from river.drift.binary import DDM, EDDM
from tqdm import tqdm


import re
import sqlite3

app = Flask(__name__)

# ---------------------------
# Load model + scaler
labels = ['BENIGN', 'Bot', 'BruteForce', 'DoS', 'Infiltration', 'PortScan', 'WebAttack']
online_model = joblib.load("Models/online_model.sav")


# ---


# ===========================
#  ROUTES
# ===========================

@app.route("/")
def index():
    return render_template("index.html")


# Offline Single Prediction
@app.route('/predict', methods=['POST'])
def predict():
    input_dict = {f"f{i+1}": float(request.form.get(f"f{i+1}", 0)) for i in range(20)}
    pred = online_model.predict_one(input_dict)
    if pred is None:
        pred = labels[0]
    elif isinstance(pred, int) or (isinstance(pred, str) and str(pred).isdigit()):
        pred = labels[int(pred)]
    else:
        pred = str(pred)
    return render_template('result.html', output=pred, confidence=None)


# CSV Upload Prediction
@app.route('/predict_csv', methods=['POST'])
def predict_csv():
    file = request.files.get('file')
    if not file:
        return "No file uploaded", 400

    df = pd.read_csv(file)
    records = df.to_dict(orient='records')
    preds = []
    for xi in records:
        y_pred = online_model.predict_one(xi)
        if y_pred is None:
            y_pred = labels[0]
        elif isinstance(y_pred, int) or (isinstance(y_pred, str) and str(y_pred).isdigit()):
            y_pred = labels[int(y_pred)]
        else:
            y_pred = str(y_pred)
        preds.append(y_pred)

    df['Predicted'] = preds

    output_path = 'static/predicted_output.csv'
    df.to_csv(output_path, index=False)

    table_html = df.to_html(classes='table table-bordered', index=False)


    X = df.drop('Predicted', axis=1)
    y = df['Predicted']
    ddm = DDM()
    eddm = EDDM()
    warnings_ddm = drifts_ddm = 0
    warnings_eddm = drifts_eddm = 0

    for xi, yi in tqdm(zip(X.to_dict(orient="records"), y), total=len(y)):

        # Convert ground truth to correct class name
        yi = str(yi)
        if yi.isdigit():
            yi = labels[int(yi)]

        # Predict
        y_pred = online_model.predict_one(xi)

        # Convert prediction to correct class name
        if y_pred is None:
            y_pred = labels[0]
        else:
            if isinstance(y_pred, int) or str(y_pred).isdigit():
                y_pred = labels[int(y_pred)]
            else:
                y_pred = str(y_pred)

        # Drift detection
        error = int(y_pred != yi)
        ddm.update(error)
        eddm.update(error)
        if ddm.warning_detected: warnings_ddm += 1
        if ddm.drift_detected: drifts_ddm += 1
        if eddm.warning_detected: warnings_eddm += 1
        if eddm.drift_detected: drifts_eddm += 1

        # Online learning
        online_model.learn_one(xi, yi)


    return render_template(
        "result_csv.html",
        table_html=table_html,
        download_link=output_path,
        warnings_ddm=warnings_ddm,
        drifts_ddm=drifts_ddm,
        warnings_eddm=warnings_eddm,
        drifts_eddm=drifts_eddm
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    else:
        username = request.form.get('user','')
        name = request.form.get('name','')
        email = request.form.get('email','')
        number = request.form.get('mobile','')
        password = request.form.get('password','')

        # Server-side validation
        username_pattern = r'^.{6,}$'
        name_pattern = r'^[A-Za-z ]{3,}$'
        email_pattern = r'^[a-z0-9._%+\-]+@[a-z0-9.\-]+\.[a-z]{2,}$'
        mobile_pattern = r'^[6-9][0-9]{9}$'
        password_pattern = r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$'

        if not re.match(username_pattern, username):
            return render_template("signup.html", message="Username must be at least 6 characters.")
        if not re.match(name_pattern, name):
            return render_template("signup.html", message="Full Name must be at least 3 letters, only letters and spaces allowed.")
        if not re.match(email_pattern, email):
            return render_template("signup.html", message="Enter a valid email address.")
        if not re.match(mobile_pattern, number):
            return render_template("signup.html", message="Mobile must start with 6-9 and be 10 digits.")
        if not re.match(password_pattern, password):
            return render_template("signup.html", message="Password must be at least 8 characters, with an uppercase letter, a number, and a lowercase letter.")

        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("SELECT 1 FROM info WHERE user = ?", (username,))
        if cur.fetchone():
            con.close()
            return render_template("signup.html", message="Username already exists. Please choose another.")
        
        cur.execute("insert into `info` (`user`,`name`, `email`,`mobile`,`password`) VALUES (?, ?, ?, ?, ?)",(username,name,email,number,password))
        con.commit()
        con.close()
        return redirect(url_for('login'))

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        mail1 = request.form.get('user','')
        password1 = request.form.get('password','')
        con = sqlite3.connect('signup.db')
        cur = con.cursor()
        cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
        data = cur.fetchone()

        if data == None:
            return render_template("signin.html", message="Invalid username or password.")    

        elif mail1 == 'admin' and password1 == 'admin':
            return render_template("home.html")

        elif mail1 == str(data[0]) and password1 == str(data[1]):
            return render_template("home.html")
        else:
            return render_template("signin.html", message="Invalid username or password.")


@app.route('/home')
def home():
	return render_template('home.html')


@app.route("/prediction")
def prediction():
    return render_template("prediction.html")

@app.route("/graphs1")
def graphs1():
    return render_template("graphs1.html")

@app.route("/graphs2")
def graphs2():
    return render_template("graphs2.html")

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')


if __name__ == "__main__":
    app.run(debug=True, port=5050)