from rdflib import *
from comparison import compare
import spacy
import time
import concurrent.futures

class AnalysableText:
    def __init__(self, text):
        self.text = text
        self.tokens = nlp(text)

    def __str__(self):
        return "Analyse Text : " + str(self.text)

class Syn_Exp:
    def getAllTitles(self, expression):
        req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT ?expression ?title
            WHERE {
                ?expression ecrm:P102_has_title ?title .
            }
        """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        for row in qres:
            result.append(str(row.title))

        return result;

    def getAllGenres(self, expression):
        req = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?genre
                    WHERE {
                      ?expression mus:U12_has_genre ?genre .
                      FILTER (isIRI(?genre))
                    }

                """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        req2 = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?genre
                    WHERE {
                      ?expression mus:U12_has_genre / ecrm:P1_is_identified_by ?genre .
                    }

                """

        qres2 = self.graph.query(req2, initBindings={'expression': expression})

        for row in qres:
            result.append(str(row.genre).split("/")[-1].replace("_", " "))

        for row in qres2:
            result.append(str(row.genre))

        return result;

    def getAllNotes(self, expression):
        req = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?note
                    WHERE {
                      ?expression ecrm:P3_has_note ?note .
                    }
                """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        for row in qres:
            result.append(str(row.note))

        return result;

    def getAllKey(self, expression):
        req = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?key
                    WHERE {
                      ?expression mus:U11_has_key ?key .
                      FILTER (isIRI(?key))
                    }
                """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        for row in qres:
            result.append(str(row.key))

        return result;

    def getAllOpus(self, expression):
        req = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?opus
                    WHERE {
                      ?expression mus:U17_has_opus_statement / mus:U42_has_opus_number ?opus .

                    }
                """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        for row in qres:
            result.append(str(row.opus))

        return result;

    #Can only return IRIs, so we use identity equals only
    def getAllComposer(self, expression):
        req = """
                    PREFIX mus: <http://data.doremus.org/ontology#>
                    PREFIX ecrm: <http://erlangen-crm.org/current/>
                    PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
                    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

                    SELECT ?expression ?composer
                    WHERE {
                      ?expression a efrbroo:F22_Self-Contained_Expression .
                      ?expCreation efrbroo:R17_created ?expression ;
                        ecrm:P9_consists_of / ecrm:P14_carried_out_by ?composer ;

                    }
                """

        qres = self.graph.query(req, initBindings={'expression': expression})
        result = []

        for row in qres:
            result.append(str(row.composer))

        return result;

    def __init__(self, graph, expression):
        self.graph = graph

        self.expression = expression
        self.title = [AnalysableText(text) for text in self.getAllTitles(expression)]
        self.note = [AnalysableText(text) for text in self.getAllNotes(expression)]
        self.composer = [AnalysableText(text) for text in self.getAllComposer(expression)]
        self.key = [AnalysableText(text) for text in self.getAllKey(expression)]
        self.opus = [AnalysableText(text) for text in self.getAllOpus(expression)]
        self.genre = [AnalysableText(text) for text in self.getAllGenres(expression)]

    def __str__(self):
        return "Expression : " + str(self.expression) + "\n\tTitle : " + str(self["title"]) + "\n\tGenre : " + str(
            self.genre) \
               + "\n\tNotes : " + str(self.note) + "\n\tComposer : " + str(self.composer) \
               + "\n\tKey : " + str(self.key) + "\n\tOpus : " + str(self.opus)

    def __getitem__(self, key):
        return getattr(self, key)

    def compare_type(self, exp2, type, identity=1, levenshteinBool=0, jaroBool=0, ngramBool=0, ngram_size=2, jaccardBool=0, monge_elkanBool=0):
        resultat = []
        for e1 in self[type]:
            for e2 in exp2[type]:
                resultat.append(compare(e1, e2, identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool))

        if len(resultat) > 0:
            return max(resultat)
        return 0

    def compare_expression(self, exp2, title=True, genre=True, note=True, composer=True, key=True, opus=True, identity=1, levenshteinBool=1, jaroBool=1, ngramBool=1, ngram_size=2, jaccardBool=1, monge_elkanBool=1):
        result = 0
        nbAttributes = title + genre + note + composer + key + opus

        if title:
            result += self.compare_type(exp2, "title", identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool)
        if genre:
            result += self.compare_type(exp2, "genre", identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool)
        if note:
            result += self.compare_type(exp2, "note", identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool)
        if composer:
            result += self.compare_type(exp2, "composer", identity=True)
        if key:
            result += self.compare_type(exp2, "key", identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool)
        if opus:
            result += self.compare_type(exp2, "opus", identity=identity, levenshteinBool=levenshteinBool, jaroBool=jaroBool, ngramBool=ngramBool, ngram_size=ngram_size, jaccardBool=jaccardBool, monge_elkanBool=monge_elkanBool)

        return result / nbAttributes


def getAllExpressions(graph):
    req = """
            PREFIX mus: <http://data.doremus.org/ontology#>
            PREFIX ecrm: <http://erlangen-crm.org/current/>
            PREFIX efrbroo: <http://erlangen-crm.org/efrbroo/>
            PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

            SELECT DISTINCT ?expression
            WHERE {
              ?expression a efrbroo:F22_Self-Contained_Expression .
            }
            """

    qres = graph.query(req)
    print("Lecture d'un fichier ttl : " + str(len(qres)) + " entrées")

    return qres


def writeFile(file1, file2):
    finalFile = open("finalFile.ttl", "w", encoding="utf-8")
    f1 = open(file1, "r", encoding="utf-8")
    f2 = open(file2, "r", encoding="utf-8")

    #Add prefix at the beginning of the finalFile
    finalFile.write("@prefix owl: <http://www.w3.org/2002/07/owl#>.\n")

    #Add the content of file to compare
    for lines in f1:
        finalFile.write(lines)
    for lines2 in f2:
        finalFile.write(lines2)
    return finalFile

def addLineCsv(value):
    finalCsv = open("result.csv", "a", encoding="utf-8")
    finalCsv.write(str(value) + "\n")

def addRelation(entity1, entity2, file):
    fileFinal = open(file, "a",  encoding="utf-8")
    fileFinal.write("<" + entity1 + "> " + "owl:sameAs " + "<" + entity2 + "> .\n")

def threadCompare(exp1, result2, threshold, title, genre, note, composer, key, opus, identity, levenshteinBool, jaroBool, ngramBool, ngram_size, jaccardBool, monge_elkanBool):
    print("EXP1: " + str(exp1.expression))
    #TODO ADD PREFIX OWL
    for exp2 in result2:
        value = exp1.compare_expression(exp2, title, genre, note, composer, key, opus, identity, levenshteinBool, jaroBool, ngramBool, ngram_size, jaccardBool, monge_elkanBool)
        addLineCsv(value)
        if value > threshold:
            addRelation(exp1.expression, exp2.expression, "finalFile.ttl")
        # fileFinal.write("\t E2: " + str(y) + " SEUIL: " + str(exp1.compare(exp2, 0.25)))
        # y += 1
        # print(exp1.compare(exp2, 0.25))

def taskDone(arg):
     print("A task has finished")
     if(arg.exception() is not None):
         raise arg.exception()
         exit(1)

def main(threshold=0.5, title=True, genre=True, note=True, composer=True, key=True, opus=True, identity=1, levenshteinBool=1, jaroBool=1, ngramBool=1, ngram_size=2, jaccardBool=1, monge_elkanBool=1):
    print("Loading spacy")
    #Remove the exclude if we're using similarity or synonyms
    global nlp
    nlp = spacy.load("fr_core_news_sm", exclude=["parser", "tagger", "ner"])

    global result2

    g1 = Graph()
    g2 = Graph()
    g1.parse("./source.ttl")
    g2.parse("./target.ttl")

    fileFinal = "finalFile.ttl"
    fileFinal = open(fileFinal, "w", encoding="utf-8")
    open("result.csv", "w", encoding="utf-8")

    print("Starting tokenizer")
    start = time.time()
    result = [Syn_Exp(g1, expression[0]) for expression in getAllExpressions(g1)]
    result2 = [Syn_Exp(g2, expression[0]) for expression in getAllExpressions(g2)]
    end = time.time()
    print("Done in : " + str(round(end-start, 2)) + " seconds")

    print("Starting compare")
    start = time.time()

    futures = []
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for exp1 in result:
            future = executor.submit(threadCompare, exp1, result2, threshold, title, genre, note, composer, key, opus, identity, levenshteinBool, jaroBool, ngramBool, ngram_size, jaccardBool, monge_elkanBool)
            # future.add_done_callback(taskDone)
            futures.append(future)
        for future in futures:
            if future.exception() is not None:
                raise future.exception()
        # executor.map(threadCompare, result)

    end = time.time()
    print("Done in : " + str(round(end-start, 2)) + " seconds")


if __name__ == '__main__':
    main()
