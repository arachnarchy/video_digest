# function to use long-file transcription
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from google.oauth2 import service_account
import os
import json

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    #client = speech.SpeechClient.()
    client = speech.SpeechClient.from_service_account_json("resources/wav/scratchlogs.json")

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    response = operation.result(timeout=90)

    transcription_str = ''
    confidence_metric = 0
    for result in response.results:
        transcription_str += ' ' + format(result.alternatives[0].transcript)
        confidence_metric = format(result.alternatives[0].confidence)

    return transcription_str, confidence_metric
