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

    GenEmail(email,name)
    return render_template(contact.html, label = 1)

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
        predict = heart_pred.predict(std_data)

        if predict[0] == 0:
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

        mdvpfo = request.form.get("mdvpfo")
        mdvpfh = request.form.get("mdvpfh")
        mdvpf1 = request.form.get("mdvpf1")
        mdvpj1 = request.form.get("mdvpj1")
        mdvpj2 = request.form.get("mdvpj2")
        mdvprap = request.form.get("mdvprap")
        mdvppq = request.form.get("mdvppq")
        jitterddp = request.form.get("jitterddp")
        mdvpshimner = request.form.get("mdvpshimner")
        mdvpshimner2 = request.form.get("mdvpshimner2")
        shimnerapq3 = request.form.get("shimnerapq3")
        shimnerapq5 = request.form.get("shimnerapq5")
        mdvpapq = request.form.get("mdvpapq")
        shimnerdda = request.form.get("shimnerdda")
        nhr = request.form.get("nhr")
        hnr = request.form.get("hnr")
        hs = request.form.get("hs")
        rdpe = request.form.get("rdpe")
        d2 = request.form.get("d2")
        dfa = request.form.get("dfa")
        spread1 = request.form.get("spread1")
        spread2 = request.form.get("spread2")
        ppe = request.form.get("ppe")


        input_data_park = (mdvpfo, mdvpfh, mdvpf1, mdvpj1, mdvpj2,
                           mdvprap, mdvppq, jitterddp, mdvpshimner, mdvpshimner2,
                           shimnerapq3, shimnerapq5, mdvpapq, shimnerdda,
                           nhr, hnr,hs, rdpe, d2, dfa,spread1, spread2, ppe)

        # Transforming to Numpy Array
        input_data_to_numpy_array_park = np.asarray(input_data_park)

        # Reshaping the Data of the Model for one instance
        input_dat_reshaped_park = input_data_to_numpy_array_park.reshape(1, -1)

        # Standardize the input_data
        scaler.fit(input_dat_reshaped_park)
        std_data_park = scaler.transform(input_dat_reshaped_park)
        # Using the obj of ML Model
        predict_park = park_pred.predict(std_data_park)

        if predict_park[0] == 1:
            return render_template('parkinsons.html', label=1)
        else:
            return render_template('parkinsons.html', label=-1)

        return "Please Enter Correct Values ! "

# @app.get("/chat")

# def index_get():
#     return render_template("cbase.html")


# # Whats the use of this code ?
# @app.post("/predict")
# def predict():
#     text=request.get_json().get("message")
#     response=get_response(text)
#     message={"answer":response}
#     return jsonify(message)



if __name__ == '__main__':
    app.run(debug=True)
