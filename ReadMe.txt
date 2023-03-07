**************TP2 Traitement sémantique*****************

L’objectif de ce travail est de créer un outil d’intégration de données structurées sous la forme de graphes de connaissances.


Contenu:
  - Main.py: classe principale responsable du chargement des 
  ontologies, de leur analyse syntaxique, de la création d'un 
  graphe et de la transformation des données pour faciliter 
  leur accès lors de l'exécution
  
  - Comparaison.py: classe traitement regroupe l'ensemble des 
  fonctions de comparaison utilisées par l'algorithme, ainsi 
  qu'une fonction principale responsable de la pondération de 
  ces fonctions.
  
  - Interface.py: interface graphique qui permet de choisir
  les fichiers turtle source et target ainsi que les
  différentes fonctionnalités: algorithme de traitement, seuil
  et les mesures de similarité 

Avant de lancer l'interface:
  Installation des modules manquants: 
   - pip install rdflib
   - pip install py_stringmatching
   - pip install spacy

   
Lancement de l'interface:
  - python3 interface.py (ou python interface.py)
  
