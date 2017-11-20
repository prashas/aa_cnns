from __future__ import division
import numpy as np


__author__ = 'shrprasha'
import numpy as np
from collections import defaultdict
import csv
from textblob import TextBlob

def load_sentiwordnet(path):
    scores = defaultdict(list)
    with open(path, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter='\t', quotechar='"')
        for line in reader:
            # skip comments
            if line[0].startswith("#"):
                continue
            if len(line) == 1:
                continue
            POS, ID, PosScore, NegScore, SynsetTerms, Gloss = line
            if len(POS) == 0 or len(ID) == 0:
                continue
            # print POS,PosScore,NegScore,SynsetTerms
            for term in SynsetTerms.split(" "):
                # drop number at the end of every term
                term = term.split("#")[0]
                term = term.replace("-", " ").replace("_", " ")
                key = "%s/%s" % (POS, term.split("#")[0])
                scores[key].append((float(PosScore), float(NegScore)))
    for key, value in scores.iteritems():
        scores[key] = np.mean(value, axis=0)
    return scores


# REF Building Machine Learning Systems with Python Section Sentiment analysis
class SentiWordNetFeature():
    """
    Senti word net Feature estimator
    """
    def __init__(self):
        self.sentiwordnet = load_sentiwordnet('/Users/shrprasha/Projects/ghostwriting/resources/SentiWordNet_3.0.0_20130122.txt')

    def get_sentiments(self, d):
        untagged_sent = []
        tagged_sent = d
        pos_vals = []
        neg_vals = []
        nouns = 0.
        adjectives = 0.
        verbs = 0.
        adverbs = 0.
        for tag in tagged_sent.split():
            sent_len = 0
            p, t = tag.rsplit('/', 1)
            untagged_sent.append(p)
            # try:
            #     p, t = tag.rsplit('/')
            # except:
            #     print tag
            p_val, n_val = 0, 0
            sent_pos_type = None
            if t.startswith("NN"):
                sent_pos_type = "n"
                nouns += 1
            elif t.startswith("JJ"):
                sent_pos_type = "a"
                adjectives += 1
            elif t.startswith("VB"):
                sent_pos_type = "v"
                verbs += 1
            elif t.startswith("RB"):
                sent_pos_type = "r"
                adverbs += 1
            if sent_pos_type is not None:
                sent_word = "%s/%s" % (sent_pos_type, p.lower())
                if sent_word in self.sentiwordnet:
                    p_val, n_val = self.sentiwordnet[sent_word]
            pos_vals.append(p_val)
            neg_vals.append(n_val)
            sent_len += 1

        l = sent_len
        avg_pos_val = np.mean(pos_vals)
        avg_neg_val = np.mean(neg_vals)

        blob = TextBlob(" ".join(untagged_sent))
        blob_polarity = sum([sentence.sentiment.polarity for sentence in blob.sentences])
        print blob_polarity
        return np.array([1 - avg_pos_val - avg_neg_val, avg_pos_val, avg_neg_val, nouns / l, adjectives / l, verbs / l,
                adverbs / l, blob_polarity])
