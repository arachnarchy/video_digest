from flask import Flask, render_template, request
from string import Template
import requests
import argparse
import io
import json
import os
import numpy
import six

# import functions from separate .py files in home dir
import topic_via_GC
from youtube_to_gc import youtube_to_gc, list_blobs
from transcribe_gcs import transcribe_gcs
from yt_video_data import get_video_data
from GC_sentiment import analyze_sentiment
from classify_tfidf import classify_tfidf
from parse_yt_url import crop_video_id
from bad_word_finder import bad_word_finder
from sentiment_plots import sentiment_plot


app = Flask(__name__)

# this is a one-page app, so only one @app.route
@app.route('/', methods=['GET', 'POST'])
def index():
    youtube_id = []
    errors = []
    topic_result = []
    partial_transcript = []
    views = []
    t_sentiment = []
    t_magnitude_n = []
    c_sentiment = []
    c_magnitude_n = []
    bw_result = []
    results = {}

    if request.method == "POST":
        # get url that the user has entered
        try:
            url_entry = request.form['ytID']
            youtube_id = crop_video_id(url_entry)
            print("ytID was:")
            print(youtube_id)
        except:
            errors.append(
                "Unable to get URL. Please make sure it's valid and try again."
            )

        filename = youtube_id + '.wav'

        # If not already in bucket: download audio, make .wav, upload to GC
        gc_files = list_blobs('audio_a')
        if 'tests/' + filename not in gc_files:
            youtube_to_gc(youtube_id)

        # If no local transcript available, transcribe audio in GC bucket
        static_list = os.listdir('static/')
        if youtube_id + '_t.txt' not in static_list:
            audio_file = 'gs://audio_a/tests/' + filename
            t, c = transcribe_gcs(audio_file)

            # save transcript to file (should be SQL)
            transcript = open("static/" + youtube_id + "_t.txt", "w")
            transcript.write(t)
            transcript.close()

        # CLASSIFY topic from transcript #######################################
        with open("static/" + youtube_id + "_t.txt", 'r') as myfile:
             transcript=myfile.read().replace('\n', '')

        partial_transcript = transcript[:280] + '...'
        results['topics_found'], results['topics_conf'] = topic_via_GC.classify(transcript)

        # GET video data & comments ############################################
        vid_data = get_video_data(youtube_id)

        # SENTIMENT on transcript ##############################################
        t_sentiment, t_magnitude = analyze_sentiment(transcript)
        t_magnitude_n = round(t_magnitude / len(transcript), 5)
        t_sentiment = round(t_sentiment, 3)

        sentiment_plot(t_sentiment, t_magnitude_n, 'sentiment_t.png')

        # BADWORDS in transcript ###############################################
        bws, bwc, bwp = bad_word_finder(transcript)
        bw_result = 'Found ' + str(bwc) + ' bad words in transcript.'

        # SENTIMENT on comments ################################################
        c_sentiment, c_magnitude = analyze_sentiment(vid_data['comments'])
        c_magnitude_n = round(c_magnitude / len(vid_data['comments']), 5)
        c_sentiment = round(c_sentiment, 3)

        # TF-IDF on transcript #################################################
        cat_edu, prob_edu = classify_tfidf(transcript, 'edu')
        if cat_edu == 'edu':
            edu = prob_edu * (-100)
        else: edu = prob_edu * 100
        results['edu'] = edu
        # edu_result = 'This transcript was classified as ' + cat_edu + ', with a probability of ' + str(prob_edu)

        cat_pol, prob_pol = classify_tfidf(transcript, 'pol')
        if cat_pol == 'left':
            pol = prob_pol * (-100)
        else: pol = prob_pol * 100
        results['pol'] = pol
        # pol_result = 'This transcript was classified as ' + cat_pol + ', with a probability of ' + str(prob_pol)

    # render the actual page, passing the variable to the output in index.html
    return render_template('index.html',
                            youtube_id=youtube_id,
                            errors=errors,
                            topic_result=topic_result,
                            partial_transcript=partial_transcript,
                            views = views,
                            t_sentiment = t_sentiment,
                            t_magnitude_n = t_magnitude_n,
                            c_sentiment = c_sentiment,
                            c_magnitude_n = c_magnitude_n,
                            results = results,
                            bw_result = bw_result)



if __name__ == "__main__":
    app.run(debug=True)
