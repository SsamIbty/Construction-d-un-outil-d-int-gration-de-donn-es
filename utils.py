from sklearn.metrics import precision_recall_fscore_support

def calculate_f_measure(reference_alignments, predicted_alignments):
    precision, recall, f_measure, _ = precision_recall_fscore_support(reference_alignments, predicted_alignments, average='binary')
    return f_measure

