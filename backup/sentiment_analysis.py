#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 17:22:23 2020

@author: trungminh

https://pythonprogramming.net/sentiment-analysis-python-textblob-vader/
"""


from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time

## VADER
analyzer = SentimentIntensityAnalyzer()

pos_count = 0
pos_correct = 0

with open("positive.txt", encoding="utf8", errors='ignore') as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['neg'] > 0.05:
            if vs['pos']-vs['neg'] > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("negative.txt", encoding="utf8", errors='ignore') as f:
    for line in f.read().split('\n'):
        vs = analyzer.polarity_scores(line)
        if not vs['pos'] > 0.05:
            if vs['pos']-vs['neg'] <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))


## TextBlob
from textblob import TextBlob

pos_count = 0
pos_correct = 0

with open("positive.txt", encoding="utf8", errors='ignore') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)

        if analysis.sentiment.polarity >= 0.001:
            if analysis.sentiment.polarity > 0:
                pos_correct += 1
            pos_count +=1


neg_count = 0
neg_correct = 0

with open("negative.txt", encoding="utf8", errors='ignore') as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        if analysis.sentiment.polarity <= -0.001:
            if analysis.sentiment.polarity <= 0:
                neg_correct += 1
            neg_count +=1

print("Positive accuracy = {}% via {} samples".format(pos_correct/pos_count*100.0, pos_count))
print("Negative accuracy = {}% via {} samples".format(neg_correct/neg_count*100.0, neg_count))