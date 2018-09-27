#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:20:25 2018

@author: daniel
"""

## IF-IDF Logistic regression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model.logistic import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score

# load dataset prepared in wrangle_news.py
news = pd.read_csv('news.csv', index_col=0)

# Split in train test (default 0.25 test)
X_train_raw, X_test_raw, y_train, y_test = train_test_split(news['content'],news['label'])

# Vectorize raw test data
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X_train_raw)

# Train LR classifier
classifier = LogisticRegression()
classifier.fit(X_train, y_train)

# Test model accuracy, 5x cross validation
x_test = vectorizer.transform(X_test_raw)
scores = cross_val_score(classifier, x_test, y_test, cv=5)
print(scores)

# Do predictions
predictions = classifier.predict(x_test)

print('Accuracy: ' + str(np.mean(scores)))

# Single prediction
exemplar = vectorizer.transform([X_test_raw[20980]]) # example string
classifier.predict(exemplar) # returns category
classifier.predict_proba(exemplar) # returns probability

## Save trained LR model
import pickle

file_Name = "classifier_pol_bias"

fileObject = open(file_Name,'wb') 
pickle.dump(classifier,fileObject)   
fileObject.close()

# tTo open the file for reading
fileObject = open(file_Name,'rb')
classifier_pol_bias = pickle.load(fileObject)  
fileObject.close()
