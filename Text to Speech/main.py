from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import requests
import json

app = Flask(__name__)
load_dotenv()
app.config['API_KEY'] = os.environ.get("API_KEY")
audio_api = "https://tmpfiles.org/api/v1/upload"
f = open("voices.json", 'r')
voices = json.loads(f.read())


@app.route('/', methods=['GET', 'POST'])
def text_to_audio():
    if request.method == 'POST':
        voice_chosen = request.form['voice_input']
        input_text = request.form['user_input']
        stability_input = request.form['stability_input']
        clarity_input = request.form['clarity_input']
        data = {
            "text": input_text,
            "voice_settings": {
                "stability": float((int(stability_input))/100),
                "similarity_boost": float((int(clarity_input))/100)
            }
        }
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voices[voice_chosen]}/stream"
        r = requests.post(url, headers={'xi-api-key': app.config['API_KEY']},
                          json=data)

        output_filename = "reply.mp3"
        with open(output_filename, "wb") as output:
            output.write(r.content)

        files = {
            'file': open('reply.mp3', 'rb'),
        }

        response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)

        audio_url = response.json()['data']['url']
        audio_url = audio_url.replace('https://tmpfiles.org', 'https://tmpfiles.org/dl')
        jsonify({'result': 'url'})
        return render_template("index.html", audio_link=audio_url)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
