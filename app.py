from flask import Flask,render_template,request,jsonify
from chat import get_response
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/diabetes')
def diabetes():
    return render_template('diabetes.html')

@app.route('/heart')
def heart():
    return render_template('heart.html')

@app.route('/parkinsons')
def parkinsons():
    return render_template('parkinsons.html')

@app.get("/chat")

def index_get():
    return render_template("cbase.html")

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)
