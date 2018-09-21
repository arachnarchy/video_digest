# function to use long-file transcription

def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types

    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        #encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code='en-US')

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    transcription_str = ''
    confidence_metric = 0
    for result in response.results:
        transcription_str += ' ' + format(result.alternatives[0].transcript)
        confidence_metric = format(result.alternatives[0].confidence)

    #for result in response.results:
        # The first alternative is the most likely one for this portion.
        #print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        #print('Confidence: {}'.format(result.alternatives[0].confidence))

    return transcription_str, confidence_metric
