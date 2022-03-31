from flask import Flask, render_template, request, jsonify
import nltk
from  model_tenserflow.MYBot  import get_responses, intents, predict_class

nltk.download('vader_lexicon')
app = Flask(__name__)

@app.route('/', methods=["GET"])
def index_get():
    return render_template('base.html')


@app.route("/predict", methods=["POST"])
def predict():   
    text = request.get_json().get("message")
    response = get_responses(predict_class(text), intents)
    message = {"answer": response}
    return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)
