from collections import Counter
from sklearn import metrics

__author__ = 'shrprasha'

def unqlist_inorder(l):
    seen = set()
    seen_add = seen.add
    return [x for x in l if not (x in seen or seen_add(x))]


"""
lines:
0              precision    recall  f1-score   support
1
2   111811642       0.43      0.60      0.50        10
...
52
53 avg / total       0.30      0.35      0.32       500
54
"""
def sort_classes_by_prediction_score(actual_Y, predicted_Y, target_names, n_top=None):
    report = metrics.classification_report(actual_Y, predicted_Y, target_names=target_names)
    lines = report.split("\n")
    result_lines = lines[2:len(lines)-3]
    fscore_by_class = {}
    for line in result_lines:
        class_label, precision, recall, fscore, support = line.split()
        fscore_by_class[class_label] = float(fscore)
    return Counter(fscore_by_class).most_common(n_top)

def display_top_scoring_authors(top_authors_scores):
    for author, score in top_authors_scores:
        print author, "\t", score




































