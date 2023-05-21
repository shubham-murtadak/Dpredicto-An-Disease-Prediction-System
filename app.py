from flask import Flask,render_template,request,jsonify
from chat import get_response
import pickle


app = Flask(__name__)


# Loading the ML Models
dia_pred = pickle.load(open('models/dia_trained_model.pkl', 'rb'))
heart_pred = pickle.load(open('models/heart_trained_model.pkl', 'rb'))
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


# Creating Dpred Page
@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')


@app.route('/diabetes_result', methods=['POST'])
def diabetes_result():
    preg = request.form.get("pregnancies")
    glu = request.form.get("Glucose")
    bp = request.form.get("BP")
    stv = request.form.get("SkinThickness")
    insulin = request.form.get("Insulin")
    bmi = request.form.get("BMI")
    dpf = request.form.get("DPF")
    age = request.form.get("Age")

    # Using the obj of ML Model
    predict = dia_pred.predict([[preg, glu, bp, stv, insulin, bmi, dpf, age]])

    if predict == 1:
        return render_template('diabetes.html', label=1)
    else:
        return render_template('diabetes.html', label=-1)

    return "Please Enter Correct Values ! "


@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/parkinsons')
def parkinsons():
    return render_template('parkinsons.html')

# @app.get("/chat")
#
# def index_get():
#     return render_template("cbase.html")


# Whats the use of this code ?
# @app.post("/predict")
# def predict():
#     text=request.get_json().get("message")
#     response=get_response(text)
#     message={"answer":response}
#     return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)
