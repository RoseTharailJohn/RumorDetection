#Training classifiers for Ranking
#1. SVM
import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import precision_recall_curve
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import classification_report
from collections import defaultdict

data_root='../Data/Phase2/'

#loading the dataset
'''
from sklearn import datasets
iris = datasets.make_hastie_10_2(n_samples=500, random_state=None)
X_train = iris[0][0:450]
Y_train = iris[1][0:450]
X_test = iris[0][450:]
Y_test = iris[1][450:]

Y_train = iris[1][0:450]
X_test = iris[0][450:]
Y_test = iris[1][450:]
'''

X_train = np.load(data_root+"X_train.npy")
Y_train = np.load(data_root+"Y_train.npy")
X_test = np.load(data_root+"X_test.npy")
Y_test = np.load(data_root+"Y_test.npy")

def dict_argmax(dct):
    """Return the key whose value is largest. In other words: argmax_k dct[k]"""
    return max(dct.iterkeys(), key=lambda k: dct[k][0])
                                                    
#hyperparameter optimization
kernels_to_try = ['rbf','poly']
Cs_to_try = [k for k in np.arange(0.01,5.5,0.15)]
prec_rec = defaultdict()
for kernel in kernels_to_try:
    for c in Cs_to_try:
        clf = SVC(C=c, kernel=kernel, probability=True)
        clf.fit(X_train, Y_train)
        Y_pred = clf.predict(X_train)
        precision, recall, thresholds, support = precision_recall_fscore_support(Y_train, Y_pred, pos_label=1,average='binary')
        prec_rec[(kernel,c)] = precision, recall
best_kernel, best_C = dict_argmax(prec_rec)
print ("Best kernel, BestC",(best_kernel, best_C))
print ("Precision, Recall",(prec_rec[(best_kernel, best_C)]))

#train classifier with best hyperparameters
clf = SVC(C=best_C, kernel=best_kernel, probability=True)
clf.fit(X_train, Y_train)
#test on test set
Y_pred = clf.predict(X_test)
Y_probs = clf.predict_proba(X_test)

#get final precision and recall
precision, recall, thresholds, support = precision_recall_fscore_support(Y_test, Y_pred, pos_label=1,average='binary')

# pick TOP n based on Y_proba[1] - ie sort based on the positive label's probability
# plot this - and precision/recall??

# DECISION TREES IMPLEMENTATION
# MAYBE LOOK INTO GRID SEARCH
