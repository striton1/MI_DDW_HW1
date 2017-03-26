#!/usr/bin/python3

from sklearn.preprocessing import binarize
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import numpy as np
 
###### READ INPUTS ###### 
# pocet souboru s dotazy 
nrOfQueries=225

# pole s nactenymi zdrojovymi dokumenty
docs = []
for d in range(1400):
    f = open("./d/" + str(d + 1) + ".txt")
    docs.append(f.read())

# pole s nactenymi zdrojovymi dotazy
for q in range(nrOfQueries):
    f = open("./q/" + str(q + 1) + ".txt")
    docs.append(f.read())
    
# set id relevantnich dokumentu pro kazde id dotazu
relevances = []
for r in range(nrOfQueries):
    f = open("./r/" + str(r + 1) + ".txt")
    tmpset = set()
    # nacteni vsech radku 
    for line in f:
        tmpset.add(int(line))
    relevances.append(tmpset)
######  END READ INPUTS ######     


def calculate_f_measure(precision,recall):
    return (2*(precision*recall)/(precision + recall))

def calculate_cos_similarity(matrix):
    recall = 0.0
    precision = 0.0;
    docsLastPos = len(docs) - nrOfQueries
    for queryPos in range(docsLastPos, docsLastPos + nrOfQueries):
        similarity = np.array(cosine_similarity(matrix[queryPos], matrix[0:docsLastPos])[0])

        # serazeni a vyber deseti nejlepsich odzadu (dokumenty cislovane od 1)
        topTen = set(similarity.argsort()[-10:][::-1]+1)
        precision = precision + len(topTen & relevances[queryPos - docsLastPos]) / len(topTen)
        recall =         recall + len(topTen & relevances[queryPos - docsLastPos]) / len(relevances[queryPos - docsLastPos])
    
    precision = precision / nrOfQueries
    recall = recall / nrOfQueries      
    return recall, precision

def calculate_euclid_distances(matrix):
    recall = 0.0
    precision = 0.0;
    docsLastPos = len(docs) - nrOfQueries
    for queryPos in range(docsLastPos, docsLastPos + nrOfQueries):        
        similarity = np.array(euclidean_distances(matrix[queryPos], matrix[0:docsLastPos])[0])
        
        # prvnich 10
        topTen = set(similarity.argsort()[0:10]+1)
        precision = precision + len(topTen & relevances[queryPos - docsLastPos]) / len(topTen)
        recall =         recall + len(topTen & relevances[queryPos - docsLastPos]) / len(relevances[queryPos - docsLastPos])
    
    precision = precision / nrOfQueries
    recall = recall / nrOfQueries    
    return recall, precision

def separator():
    print("------------------------------------------")


count_vectorizer = CountVectorizer()
matrix_freq = count_vectorizer.fit_transform(docs)
matrix_bin = binarize(matrix_freq)
tfidf_vectorizer = TfidfVectorizer()
matrix_tfidf = tfidf_vectorizer.fit_transform(docs)

###########################################
recall, precision = calculate_cos_similarity(matrix_freq)
print("Term Frequency results x Cosine similarity measure")
print("Precision= " + str(precision))
print("Recall= " + str(recall))
print("F-measure= " + str( calculate_f_measure(precision, recall)))
separator();

recall, precision = calculate_euclid_distances(matrix_freq)
print("Term Frequency x Euclidean distance")
print("Precision= " + str(precision))
print("Recall= " + str(recall))
print("F-measure= " + str( calculate_f_measure(precision, recall)))
separator();

separator();
###########################################
recall, precision = calculate_cos_similarity(matrix_bin)
print("Boolean results x Cosine similarity measure")
print("Precision= " + str(precision))
print("Recall= " + str(recall))
print("F-measure= " + str( calculate_f_measure(precision, recall)))
separator();

recall, precision = calculate_euclid_distances(matrix_bin)
print("Boolean results x Euclidean distance")
print("Precision= " + str(precision))
print("Recall= " + str(recall))
print("F-measure= " + str( calculate_f_measure(precision, recall)))
separator();

separator();
###########################################
recall, precision = calculate_cos_similarity(matrix_tfidf)
print("TF-IDF results x Cosine similarity measure")
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F-measure: " + str( calculate_f_measure(precision, recall)))
separator();

recall, precision = calculate_euclid_distances(matrix_tfidf)
print("TF-IDF results x Euclidean distance")
print("Precision: " + str(precision))
print("Recall: " + str(recall))
print("F-measure: " + str( calculate_f_measure(precision, recall)))
separator();





