from flask import Flask, render_template, request, redirect, url_for
from rq import Connection, Queue
from rq.job import Job
import time
from redis import Redis
from string import Template
import requests
import argparse
import io
import json
import os
import numpy
import six

from scoop import scoop
from parse_yt_url import crop_video_id
from worker import conn


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# starts scoop function when url is entered
@app.route('/start', methods=['POST'])
def get_data():
    # get url
    data = json.loads(request.data.decode())
    url = data["url"]
    youtube_id = crop_video_id(url)

    q = Queue(connection=conn)

    job = q.enqueue_call(func=scoop, args=(youtube_id,), result_ttl=5000)
    return job.get_id()

# outputs raw results as string on new page when job is finished
@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202


if __name__ == "__main__":
    app.run(debug=True)
