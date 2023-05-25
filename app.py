from flask import Flask,render_template,request,jsonify
# from chat import get_response
import pickle
import os                             # For protection of email and password while email automation and otp genration
from email.message import EmailMessage    # For email automation
import ssl
import smtplib
import random                           # for generating random nums for OTP
import numpy as np
from sklearn.preprocessing import StandardScaler
# from flask_sqlalchemy import SQLAlchemy
import pandas as pd


app = Flask(__name__)


# Loading the ML Models
dia_pred = pickle.load(open('models/dia_trained_model.pkl', 'rb'))
heart_pred = pickle.load(open('models/heart_trained_model1.pkl', 'rb'))
park_pred = pickle.load(open('models/park_trained_model.pkl', 'rb'))


# Creating a Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Creating About Page
@app.route('/about')
def about():
    return render_template('about.html')


# Creating Contact Page
@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact',  methods=["POST"])
def contact_us():

    # No need for OTP here, for appointment booking use OTP create a button confirm booking once clicked run the otp code



    mail_user = os.environ.get('TestUser')
    mail_pass = os.environ.get('TestUserPass')

    def GenEmail(email, name):
        subject = "Thank you for contacting us!"
        body = '''
        Dear {},
            Thank you for contacting us through our website's contact form. Our team has received your message and we will get back to you as soon as possible. We strive to provide prompt and helpful responses to all inquiries.
        Best regards,
        MultipleDiseasePredictionSystem
        '''.format(name)

        em = EmailMessage()
        em['From'] = mail_user
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(mail_user, email, em.as_string())

    name = request.form.get('name')
    email = request.form.get('email')
    query = request.form.get('Message')

    GenEmail(email, name)
    return render_template("contact.html", label=1)

# Creating Dpred Page
@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/diabetes', methods=['POST'])
def diabetes_result():
        scaler = StandardScaler()

        preg = request.form.get("pregnancies")
        glu = request.form.get("Glucose")
        bp = request.form.get("BP")
        stv = request.form.get("SkinThickness")
        insulin = request.form.get("Insulin")
        bmi = request.form.get("BMI")
        dpf = request.form.get("DPF")
        age = request.form.get("Age")

        input_data_dia = (preg, glu, bp, stv, insulin, bmi, dpf, age)

        # Transforming to Numpy Array
        input_data_to_numpy_array = np.asarray(input_data_dia)

        # Reshaping the Data of the Model for one instance
        input_dat_reshaped = input_data_to_numpy_array.reshape(1, -1)

        # Standardize the input_data
        scaler.fit(input_dat_reshaped)
        std_data = scaler.transform(input_dat_reshaped)
        # Using the obj of ML Model
        predict = dia_pred.predict(std_data)

        if predict[0] == 1:
            return render_template('diabetes.html', label=1)
        else:
            return render_template('diabetes.html', label=-1)

        return "Please Enter Correct Values ! "


@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/heart', methods=['POST'])
def heart_result():
        scaler = StandardScaler()

        age1 = request.form.get("age")
        sex = request.form.get("sex")
        cp = request.form.get("cp")
        RBP = request.form.get("RBP")
        chol = request.form.get("chol")
        FBS = request.form.get("FBS")
        RER = request.form.get("RER")
        thalach = request.form.get("thalach")
        ex = request.form.get("ex")
        sl = request.form.get("sl")
        op = request.form.get("op")
        ca = request.form.get("ca")
        thal = request.form.get("thal")

        input_data_heart = (age1, sex, cp, RBP, chol, FBS, RER, thalach, ex, sl, op, ca, thal)

        # Transforming to Numpy Array
        input_data_to_numpy_array_heart = np.asarray(input_data_heart)

        # Reshaping the Data of the Model for one instance
        input_dat_reshaped_heart = input_data_to_numpy_array_heart.reshape(1, -1)

        # Standardize the input_data
        scaler.fit(input_dat_reshaped_heart)
        std_data_heart = scaler.transform(input_dat_reshaped_heart)
        # Using the obj of ML Model
        predict_heart = heart_pred.predict(std_data_heart)

        if predict_heart[0] == 1:
            return render_template('heart.html', label=1)
        else:
            return render_template('heart.html', label=-1)

        return "Please Enter Correct Values ! "

@app.route('/parkinsons')
def parkinsons():
    return render_template('parkinsons.html')


@app.route('/parkinsons', methods=['POST'])
def parkinsons_result():
        scaler = StandardScaler()

        age1 = request.form.get("age")
        sex = request.form.get("sex")
        cp = request.form.get("cp")
        RBP = request.form.get("RBP")
        chol = request.form.get("chol")
        FBS = request.form.get("FBS")
        RER = request.form.get("RER")
        thalach = request.form.get("thalach")
        ex = request.form.get("ex")
        sl = request.form.get("sl")
        op = request.form.get("op")
        ca = request.form.get("ca")
        thal = request.form.get("thal")

        input_data_heart = (age1, sex, cp, RBP, chol, FBS, RER, thalach, ex, sl, op, ca, thal)

        # Transforming to Numpy Array
        input_data_to_numpy_array_heart = np.asarray(input_data_heart)

        # Reshaping the Data of the Model for one instance
        input_dat_reshaped_heart = input_data_to_numpy_array_heart.reshape(1, -1)

        # Standardize the input_data
        scaler.fit(input_dat_reshaped_heart)
        std_data_heart = scaler.transform(input_dat_reshaped_heart)
        # Using the obj of ML Model
        predict = park_pred.predict(std_data_heart)

        if predict[0] == 1:
            return render_template('heart.html', label=1)
        else:
            return render_template('heart.html', label=-1)

        return "Please Enter Correct Values ! "

# @app.get("/chat")
# @app.get("/chat")
#
#
# def index_get():
#     return render_template("cbase.html")
#
#
# # Whats the use of this code ?
# @app.post("/predict")
# def predict():
#     text=request.get_json().get("message")
#     response=get_response(text)
#     message={"answer":response}
#     return jsonify(message)


# Working on Db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
# db = SQLAlchemy(app)

# class Appointment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     date = db.Column(db.String(10), nullable=False)
#     time = db.Column(db.String(8), nullable=False)
#     disease = db.Column(db.String(100), nullable=False)

# Create the database tables
# db.create_all()

@app.route('/a')
def appointment():
    return render_template("a.html")

@app.route('/a', methods=["POST"])
def appointment_booking():
    # No need for OTP here, for appointment booking use OTP create a button confirm booking once clicked run the otp code

    mail_user = os.environ.get('TestUser')
    mail_pass = os.environ.get('TestUserPass')

    def GenEmailA(email, name, date, time, disease):
        subject = "Appointment Confirmation!"
        body = '''
            Dear {},

            We are pleased to confirm your appointment for a medical consultation at our clinic. We appreciate your trust in our services and look forward to providing you with the best possible care. Please find the details of your appointment below:

            Patient's Name: {}
            Date: {}
            Time: {}
            Type of Disease: {}

            Please make sure to arrive at least 15 minutes before your scheduled appointment time to complete any necessary paperwork and to ensure a smooth check-in process.

            In case of any changes or if you need to reschedule your appointment, kindly notify us at least 24 hours in advance so that we can accommodate your request and offer the slot to another patient in need.

            For any questions or concerns, feel free to reach out to our clinic at dpredicto@gmail.com. Our team will be more than happy to assist you.

            We look forward to seeing you soon and working towards your well-being.
        '''.format(name, name, date, time, disease)

        em = EmailMessage()
        em['From'] = mail_user
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(mail_user, mail_pass)
            smtp.sendmail(mail_user, email, em.as_string())

    name = request.form.get('name')
    email = request.form.get('email')
    date = request.form.get('date')
    time = request.form.get('samay')
    disease = request.form.get('type')

    # # Adding the data to the DataBase
    # appointment = Appointment(name= name, email= email, date=date, time=time, disease=disease)
    # db.session.add(appointment)
    # db.session.commit()
    #
    #
    # # Retriving the data from the dataBase
    # appointment_list = Appointment.query.all()
    # df = pd.DataFrame(
    #     [(appointment.id, appointment.name, appointment.email, appointment.date, appointment.time, appointment.disease)
    #      for appointment in appointment_list],
    #     columns=['ID', 'Name', 'Email', 'Date', 'Time', 'Disease'])
    #
    # file_path = 'appointments.xlsx'
    # df.to_excel(file_path, index=False)


    GenEmailA(email, name, date, time, disease)
    return render_template("a.html", label=1)

# @app.route('/view_excel')
# def view_excel():
#     appointment_list = Appointment.query.all()
#     df = pd.DataFrame([(appointment.id, appointment.name, appointment.email, appointment.date, appointment.time, appointment.disease)
#                        for appointment in appointment_list],
#                       columns=['ID', 'Name', 'Email', 'Date', 'Time', 'Disease'])
#
#     return render_template('view_excel.html', data=df.to_html())


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

























