import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression

def classify_tfidf(text, model):
    """ Classifies text with a pretrained model"""

    vec_path = 'static/models/vectorizer_' + model + '.pickle'
    cla_path = 'static/models/classifier_' + model + '.pickle'
    vectorizer = pickle.load(open(vec_path, "rb"))
    classifier = pickle.load(open(cla_path, "rb"))

    exemplar = vectorizer.transform([text]) # example string
    category = classifier.predict(exemplar) # returns category
    probabilities = classifier.predict_proba(exemplar) # returns probability

    if probabilities[0][0] > probabilities[0][1]:
        class_prob = probabilities[0][0]
    else: class_prob = probabilities[0][1]

    return category, class_prob
    # print('This transcript was classified as ' + category + ', with a probability of ' + str(class_prob))
