
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

# Chargement des fichiers de référence et prédits
ref_file = 'refDHT.rdf'
pred_file = 'finalFile.ttl'

# Chargement du fichier de résultats
result_file = 'result.csv'
results = pd.read_csv(result_file, header=None)

# Extraction des seuils et valeurs d'égalité à partir du fichier de résultats
thresholds = results.iloc[:, 0].values
equalities = results.iloc[:, 1].values

def fMesure(threshold, ref_file, pred_file):
    """
    Calcule la F-mesure pour un seuil donné et des fichiers d'alignement de référence et prédits.
    
    Args:
        threshold (float): seuil de similarité à utiliser pour l'alignement
        ref_file (str): chemin vers le fichier d'alignement de référence (au format RDF)
        pred_file (str): chemin vers le fichier d'alignement prédit (au format RDF ou TTL)
    
    Returns:
        float: la F-mesure pour le seuil donné et les fichiers d'alignement donnés
    """
    # Charger les graphes RDF à partir des fichiers
    g1 = rdflib.Graph()
    g1.parse(ref_file, format='xml')
    g2 = rdflib.Graph()
    g2.parse(pred_file, format=rdflib.util.guess_format(pred_file))
    
    # Extraire les alignements de référence et prédits
    reference_alignments = set((str(s), str(o)) for s, p, o in g1 if str(p) == "http://www.w3.org/2002/07/owl#sameAs" and str(o) != rdflib.term.URIRef(""))
    predicted_alignments = set((str(s), str(o)) for s, p, o in g2 if str(p) == "http://www.w3.org/2002/07/owl#sameAs" and str(o) != rdflib.term.URIRef("") and float(similarity(s, o)) >= threshold)
    
    # Calculer la F-mesure
    precision, recall, f_measure, _ = precision_recall_fscore_support(reference_alignments, predicted_alignments, average='binary')

# Calcul de la F-mesure pour chaque seuil
f_measures = []
for threshold in thresholds:
    predicted_file = f'finalFile_{threshold}.ttl'
    f_measure = calculate_f_measure(ref_file, predicted_file)
    f_measures.append(f_measure)

# Traçage de la courbe de F-mesure en fonction du seuil
plt.plot(thresholds, f_measures, label='F-mesure')
plt.xlabel('Seuil')
plt.ylabel('F-mesure')
plt.title('Courbe de F-mesure en fonction du seuil')
plt.legend()
plt.show()

