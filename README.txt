This is the repo for ScoopTube, a parenting tool to analyze YouTube content. Find the app at https://scooptube.herokuapp.com.

The app pulls audio, comments section, and some metadata from YouTube, and provides a content report. It uses pytube, pydub, ffmpeg, and Google Cloud Speech-to-text to create transcripts from audio. The transcript & comments are then analyzed for sentiment and topics using Google Cloud AI models, and content skew using custom classifiers. Content analyses look at two axes in the current version: "Seriousness", an axis from educational to shallow entertainment, and political bias. Content axis classifiers have been trained on YouTube transcripts from popular kid/teen educational channels and entertainment focused YouTubers, as well as news articles.

The Python app is deployed on Heroku using Flask, Redis, and AngularJS.

This project was created over 2 weeks as part of my Insight Data Science Fellowship Fall 2018.
