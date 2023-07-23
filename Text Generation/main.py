import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import requests
from diffusers import StableDiffusionPipeline
import torch
from torch import autocast




app = Flask(__name__, static_url_path='/static', static_folder='static')
load_dotenv()
app.config['API_KEY_GEN'] = os.environ.get("API_KEY_GEN")

API_KEY_GEN = app.config['API_KEY_GEN']
openai.api_key = API_KEY_GEN
model_id = 'gpt-3.5-turbo'
conversation = []

app.config['API_KEY_SPEECH'] = os.environ.get("API_KEY_SPEECH")


@app.route("/")
def homepage():
    return render_template("index.html")


@app.route("/text-gen", methods=["GET", "POST"])
def predict():
    if request.method == "POST":
        input_str = request.form['user_input']
        token_input = request.form['token_input']
        temperature_input = request.form['temperature_input']
        n_input = request.form['n_input']
        stop_input = request.form['stop_input']
        conversation.append({"role": "user", "content": input_str})
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=conversation,
            max_tokens=int(token_input),
            temperature=float(temperature_input),
            n=int(n_input),
            stop=stop_input
        )
        reply = response['choices'][0]['message']['content']
        conversation.append({"role": "assistant", "content": reply})
        return reply
    return render_template("text-gen.html")





if __name__ == "__main__":
    app.run(debug=True)
