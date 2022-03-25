from flask import Flask, render_template, request, jsonify
import nltk
import create_response
import fact_responses
from  bot  import respond

nltk.download('vader_lexicon')
app = Flask(__name__)

@app.route('/', methods=["GET"])
def index_get():
    return render_template('base.html')

@app.post("/predict")
def predict():   
    text = request.get_json().get("message")
    response = respond(text)
    message = {"answer": response}
    return jsonify(message)

if __name__ == '__main__':
    app.run(debug=True)