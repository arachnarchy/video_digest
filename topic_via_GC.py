from google.cloud import language

def classify(text):
    """Classify the input text into categories. """

    language_client = language.LanguageServiceClient()

    document = language.types.Document(
        content=text,
        type=language.enums.Document.Type.PLAIN_TEXT)
    response = language_client.classify_text(document)
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence


    tags_found = list(result.keys())

    if len(tags_found) > 5:
        tags_found = tags_found[0:5]

    tf = []
    for topic in tags_found:
        topics = tf.append(topic.rsplit('/',1)[1])

    tags_conf = []
    for tag in tags_found:
        c = tags_conf.append(result[str(tag)])

    # tags_found = [s.strip('/') for s in tags_found]

    print("Topics analysis done")
    return tf, tags_conf
