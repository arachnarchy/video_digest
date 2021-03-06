def scoop(youtube_id):
    #import functions from separate .py files in home dir
    from string import Template
    import requests
    import argparse
    import io
    import json
    import os
    import numpy
    import six
    from google.cloud import storage
    from google.oauth2 import service_account

    import topic_via_GC
    from youtube_to_gc import youtube_to_gc, list_blobs
    from transcribe_gcs import transcribe_gcs
    from yt_video_data import get_video_data
    from GC_sentiment import analyze_sentiment
    from classify_tfidf import classify_tfidf
    from bad_word_finder import bad_word_finder
    from sentiment_plots import sentiment_plot, axis_plot

    results = {}
    results['youtube_id'] = youtube_id
    results['youtube_url'] = 'https://www.youtube.com/embed/' + youtube_id
    filename = youtube_id + '.wav'

    # If not already in bucket: download audio, make .wav, upload to GC
    gc_files = list_blobs('audio_a')
    if 'tests/' + filename not in gc_files:
        print("Downloading youtube audio.")
        youtube_to_gc(youtube_id)

    # If no local transcript available, transcribe audio in GC bucket
    #transcript_list = os.listdir('static/transcripts/')
    transcript_list = list_blobs('yt_transcripts')
    if youtube_id + '_t.txt' not in transcript_list:
        audio_file = 'gs://audio_a/tests/' + filename
        t, c = transcribe_gcs(audio_file)

        # save transcript to local file and push to GC
        transcript = open("static/transcripts/" + youtube_id + "_t.txt", "w")
        transcript.write(t)
        transcript.close()

        # Upload NEW
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('yt_transcripts')
        blob = bucket.blob(youtube_id + "_t.txt")
        blob.upload_from_filename("static/transcripts/" + youtube_id + "_t.txt")
        print("YouTube transcript uploaded")

    # CLASSIFY topic from transcript #######################################
    # Download NEW
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('yt_transcripts')
    blob = bucket.blob(youtube_id + "_t.txt")
    blob.download_to_filename("static/transcripts/" + youtube_id + "_t.txt")

    with open("static/transcripts/" + youtube_id + "_t.txt", 'r') as myfile:
         transcript=myfile.read().replace('\n', '')

    results['partial_transcript'] = transcript[:280] + '...'
    results['topics_found'], results['topics_conf'] = topic_via_GC.classify(transcript)

    # GET video data & comments ############################################
    vid_data = get_video_data(youtube_id)
    results['title'] = vid_data['title']

    # SENTIMENT on transcript ##############################################
    t_sentiment, t_magnitude = analyze_sentiment(transcript)
    t_magnitude_n = round(t_magnitude / len(transcript), 5)
    t_sentiment = round(t_sentiment, 3) + 0.0000001
    results['t_sentiment'] = t_sentiment

    # sentiment_plot(t_sentiment, t_magnitude_n, 'sentiment_t.png')

    # BADWORDS in transcript ###############################################
    bws, bwc, bwp = bad_word_finder(transcript)
    results['bw_result'] = 'Found ' + str(bwc) + ' bad words in transcript.'

    # SENTIMENT on comments ################################################
    c_sentiment, c_magnitude = analyze_sentiment(vid_data['comments'])
    c_magnitude_n = round(c_magnitude / len(vid_data['comments']), 5)
    c_sentiment = round(c_sentiment, 3) + 0.0000001
    results['c_sentiment'] = c_sentiment
    # sentiment_plot(c_sentiment, c_magnitude_n, 'sentiment_c.png')

    # TF-IDF on transcript #################################################
    cat_edu, prob_edu = classify_tfidf(transcript, 'edu')
    if cat_edu != 'edu':
        edu = prob_edu * (-1)
    else: edu = prob_edu
    results['edu'] = edu
    # axis_plot(edu, 'Info', 'Shallow', 'edu.png')

    cat_pol, prob_pol = classify_tfidf(transcript, 'pol')
    if cat_pol == 'left':
        pol = prob_pol * (-1)
    else: pol = prob_pol
    results['pol'] = pol
    # axis_plot(pol, 'Left', 'Right', 'pol.png')

    results = json.dumps(results)

    return results
