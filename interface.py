# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import *
from tkinter import filedialog as fd
from tkinter import ttk
from rdflib import *
from rdflib.namespace import RDF
import io
from main import main


def open_rdf_file():
    filetypes = (
        ('Turtle', '*.ttl'),
        ('XML/RDF', '*.rdf*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='.',
        filetypes=filetypes)

    print(filename)

    g = Graph()
    g.parse(filename)
    print(len(g))

    visualize(g)
    print("Oui")

    test_set = []

    # find all subjects of any type
    for s, p, o in g.triples((None, RDF.type, None)):
        # (f"{s} is a {o}")
        test_set.append(o)
    test_set = list(dict.fromkeys(test_set))

    for el in test_set:
        print(el)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    root.geometry('450x350')
    root.title("My Data Integration Tool")
  
    root.configure(bg="#FFFAF0")

    source1_button = ttk.Button(
        root,
        text="Select source",
        command=open_rdf_file,
        style="Bold.TButton"
    )

    source2_button = ttk.Button(
        root,
        text="Select target",
        command=open_rdf_file,
        style="Bold.TButton"
    )
    style = ttk.Style()
    style.configure("Bold.TButton", font=("Arial", 11, "bold"))

    source1_button.grid(column=0, row=0, padx=10, pady=10)
    source2_button.grid(column=2, row=0, padx=10, pady=10)

    def selectTitle(checked):
        print(not checked)

    def applied():
        print("Appliquer")
        jaroValue = float(jaroInput.get()) if jaro.get() else 0
        identityValue = float(identityInput.get()) if identity.get() else 0
        levenshteinValue = float(levenshteinInput.get()) if levenshtein.get() else 0
        if ngram.get():
            ngramValue = float(ngramInput.get())
            ngramSizeValue = int(sizeInput.get())
        else:
            ngramValue = 0
            ngramSizeValue = int(sizeInput.get())
        jacardValue = float(jaccardInput.get()) if jaccard.get() else 0
        monge_elkanValue = float(monge_elkanInput.get()) if monge_elkan.get() else 0

        main(threshold=float(e1.get()), title=title.get(), genre=genre.get(), note=notes.get(), composer=composer.get(), key=key.get(), opus=opus.get(), identity=identityValue, levenshteinBool=levenshteinValue, jaroBool=jaroValue, ngramBool=ngramValue, ngram_size=ngramSizeValue, jaccardBool=jacardValue, monge_elkanBool=monge_elkanValue)


    Label(root, text="Proprieties",bg='#ADD8E6').grid(row=2, column=0)

    title = BooleanVar()
    Checkbutton(root, text="Title", variable=title, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=3)
    title.set(True)
    composer = IntVar()
    Checkbutton(root, text="Composer", variable=composer, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=4)
    composer.set(True)
    notes = IntVar()
    Checkbutton(root, text="Notes", variable=notes, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=5)
    notes.set(True)
    genre = IntVar()
    Checkbutton(root, text="Gender", variable=genre, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=6)
    genre.set(True)
    key = IntVar()
    Checkbutton(root, text="Key", variable=key, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=7)
    key.set(True)
    opus = IntVar()
    Checkbutton(root, text="Opus", variable=opus, bg='#FFFFFF', highlightthickness=0).grid(column=0, row=8)
    opus.set(True)

    Label(root, text="Threshold", bg='#ADD8E6',width=12).grid(column=0,row=9)
    e1 = Entry(root, textvariable=DoubleVar(root, value=0.5),width=5)
    e1.grid(row=10, column=0, padx=25)

    Label(root, text="Algorithms", bg='#ADD8E6').grid(row=2, column=1)

    jaro = IntVar()
    Checkbutton(root, text="Jaro", variable=jaro, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=3, sticky="nsew")
    Label(root, text="Weighting", bg='#ADD8E6').grid(row=2, column=2)
    jaro.set(True)
    jaroInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    jaroInput.grid(row=3, column=2)

    identity = IntVar()
    Checkbutton(root, text="Identity", variable=identity, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=4, sticky="nsew")
    identity.set(True)
    
    identityInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    identityInput.grid(row=4, column=2)

    levenshtein = IntVar()
    Checkbutton(root, text="Levenshtein", variable=levenshtein, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=5, sticky="nsew")
    levenshtein.set(True)
    
    levenshteinInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    levenshteinInput.grid(row=5, column=2)

    ngram = IntVar()
    Checkbutton(root, text="Ngram", variable=ngram, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=6, sticky="nsew")
    ngram.set(True)
    
    ngramInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    ngramInput.grid(row=6, column=2)
    Label(root, text="Size", bg='#ADD8E6',width=12).grid(row=9, column=2)
    sizeInput = Entry(root, textvariable=IntVar(root, value=2),width=5)
    sizeInput.grid(row=10, column=2, padx=45)

    jaccard = IntVar()
    Checkbutton(root, text="Jaccard", variable=jaccard, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=7, sticky="nsew")
    jaccard.set(True)
    
    jaccardInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    jaccardInput.grid(row=7, column=2)

    monge_elkan = IntVar()
    Checkbutton(root, text="Monge Elkan", variable=monge_elkan, bg='#FFFFFF', highlightthickness=0).grid(column=1, row=8, sticky="nsew")
    monge_elkan.set(True)
    
    monge_elkanInput = Entry(root, textvariable=DoubleVar(root, value=1),width=5)
    monge_elkanInput.grid(row=8, column=2)

    
    
    Button(root, text="Applied", bg='#000080', fg='#ffffff', font=('Arial', 11,'bold'), command=applied, width=15).grid(row=11, column=1)

    root.mainloop()

    # Save un RDF file
    # g.serialize(destination="tbl.ttl")
