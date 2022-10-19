from flask import Flask, after_this_request
from flask import jsonify
app = Flask(__name__)

questionNumber = 0
questions = [{
        "id": 1,
        "sentence": "Ich gehe ___ Berliner Kirche",
        "answer": 1,
        "choices": ["ins", "in die", "auf der", "zum"]
    },
    {
        "id": 2,
        "sentence": "Ich bin stärker als meine Angst",
        "answer": 1,
        "choices": ["ins", "in die", "auf der", "zum"]
    }]



@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/question")
def getQuestion():
    @after_this_request
    def add_header(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    return jsonify(questions)

