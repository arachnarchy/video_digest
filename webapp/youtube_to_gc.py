from pytube import YouTube
from pydub import AudioSegment
from google.cloud import storage

def youtube_to_gc(url):

    yt = YouTube(url)
    filename = 'yt3'
    yt.streams.filter(only_audio=True).first().download(filename=filename)

    clip =  AudioSegment.from_file(filename + ".mp4")
    clip = clip.set_channels(1) # convert to mono for GCS
    clip.export(filename + '.wav', format='wav')

    storage_client = storage.Client()
    bucket = storage_client.get_bucket('audio_a')
    blob = bucket.blob('tests/' + filename + '.wav')
    blob.upload_from_filename(filename + '.wav')
