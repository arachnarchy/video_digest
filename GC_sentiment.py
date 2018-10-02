def analyze_sentiment(content):
    from google.cloud import language
    from google.cloud.language import enums
    from google.cloud.language import types
    import six
    import sys

    client = language.LanguageServiceClient()

    # content = 'Your text to analyze, e.g. Hello, world!'

    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment

    return sentiment.score, sentiment.magnitude
