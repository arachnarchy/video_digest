from flask import Flask, render_template, request
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

@app.route('/start', methods=['POST'])
def get_data():
    # get url
    data = json.loads(request.data.decode())
    url = data["url"]
    youtube_id = crop_video_id(url)

    # Initiate queue #########
    #redis_conn = Redis()
    #q = Queue(connection=redis_conn)
    q = Queue(connection=conn)
    ##########################

    job = q.enqueue_call(func=scoop, args=(youtube_id,), result_ttl=5000)
    return job.get_id()


# @app.route('/outcomes', methods=['GET', 'POST'])
# def outcomes():
#     results = {}
#
#     return render_template('outcomes.html',
#                             youtube_id=youtube_id,
#                             results = results)


# outputs raw results on new page
@app.route("/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        return str(job.result), 200
    else:
        return "Nay!", 202


if __name__ == "__main__":
    app.run(debug=True)
