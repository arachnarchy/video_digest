from flask import Flask, render_template, request
from string import Template
import requests
# import functions from separate .py files in home dir
import topic_via_GC
import youtube_to_gc
import transcribe_gcs


app = Flask(__name__)

# this is a one-page app, so only one @app.route
@app.route('/', methods=['GET', 'POST'])
def index():
    youtube_id = []
    errors = []
    result = []
    partial_transcript = []

    if request.method == "POST":
        # get url that the user has entered
        try:
            youtube_id = request.form['ytID']
            print("ytID was:")
            print(youtube_id)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

        # download audio, make .wav, upload to GC bucket
        youtube_to_gc.youtube_to_gc('https://www.youtube.com/watch?v=' + youtube_id)

        # transcribe audio in GC bucket
        filename = 'yt3' + '.wav'
        audio_file = 'gs://audio_a/tests/' + filename
        t, c = transcribe_gcs.transcribe_gcs(audio_file)

        transcript = open("static/transcript3.txt", "w")
        transcript.write(t)
        transcript.close()

        # classify audio transcript
        with open('static/transcript3.txt', 'r') as myfile:
             transcript=myfile.read().replace('\n', '')

        partial_transcript = transcript[:280] + '...'
        result = topic_via_GC.classify(transcript)

    # render the actual page, passing the variable to the output in index.html
    return render_template('index.html',youtube_id=youtube_id, errors=errors, result=result, partial_transcript=partial_transcript)



if __name__ == "__main__":
    app.run(debug=True)
