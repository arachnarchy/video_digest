from pytube import YouTube
from pydub import AudioSegment
from google.cloud import storage
import os
from google.oauth2 import service_account
import json

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""

    storage_client = storage.Client()
    #storage_client = storage.Client.from_service_account_json("resources/wav/scratchlogs.json")
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    file_list = []
    for blob in blobs:
        file = blob.name
        file_list.append(file)

    return(file_list)


def youtube_to_gc(yt_id):
    """Downloads audio for youtube url, transforms to mono wave file, uploads to GC bucket"""

    url = 'https://www.youtube.com/watch?v=' + yt_id

    # Download
    yt = YouTube(url)
    filename = yt_id
    yt.streams.filter(only_audio=True).first().download(filename=filename)

    # Transform
    clip =  AudioSegment.from_file(filename + ".mp4")
    clip = clip.set_channels(1) # convert to mono for GCS
    clip.export(filename + '.wav', format='wav')

    # Upload
    storage_client = storage.Client()
    #storage_client = storage.Client.from_service_account_json("resources/wav/scratchlogs.json")
    bucket = storage_client.get_bucket('audio_a')
    blob = bucket.blob('tests/' + filename + '.wav')
    blob.upload_from_filename(filename + '.wav')

    # delete temp audio files
    mp4_file= filename + '.mp4'
    wav_file= filename + '.wav'

    ## If file exists, delete it ##
    if os.path.isfile(mp4_file):
        os.remove(mp4_file)
    else:    ## Show an error ##
        print("Error: %s file not found" % mp4_file)

    ## If file exists, delete it ##
    if os.path.isfile(wav_file):
        os.remove(wav_file)
    else:    ## Show an error ##
        print("Error: %s file not found" % wav_file)
