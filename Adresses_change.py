from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
#from tkinter.filedialog import *
import tkinter
import pandas as pd
import json
from Adresse import extract_adresse

class Application(Tk):

    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent
        self.initialize()
        self.title("Transformation de données")
        self.resizable(width=False, height=False)
        self.load_data()
        self.mainloop()

    def initialize(self):
        self.control_menu = Frame(self)
        self.control_menu.pack()

        self.conf_menu = LabelFrame(self.control_menu, text="Configuation", width=430, height=300, labelanchor='n')
        self.conf_menu.grid(row=1, column=1, pady=10, padx=10)


        self.rep_source_affiche = StringVar()
        self.rep_cible_affiche = StringVar()

        self.entree_label = Label(self.conf_menu, text="Fichier source")
        self.entree_label.grid(row=1, column=1, padx=20,sticky=W)

        self.entree = Entry(self.conf_menu, textvariable=self.rep_source_affiche, width=50)
        self.entree.grid(row=1, column=2,sticky=W, padx=0)

        self.imp_Button = Button(self.conf_menu, text="Sélection...", command=self.import_file)
        self.imp_Button.grid(row=1, column=3, padx=15, pady=10,sticky=W)

        self.cible_label = Label(self.conf_menu, text="Répertoire cible")
        self.cible_label.grid(row=2,column=1, padx=20,sticky=W)

        self.cible_entree = Entry(self.conf_menu, textvariable=self.rep_cible_affiche, width=50)
        self.cible_entree.grid(row=2, column=2, sticky=W, padx=0)

        self.cible_Button = Button(self.conf_menu, text="Sélection...", command = self.rep_cible)
        self.cible_Button.grid(row=2, column=3, padx=15, pady=10,sticky=W)

        self.ex_menu = LabelFrame(self.control_menu, text="Execution", width=430, height=200, labelanchor='n')
        self.ex_menu.grid(row=1, column=2,padx=10, pady=10)

        self.ex_Button = Button(self.ex_menu, text="Executer", command = self.ex_programme,height = 1, width = 18)
        self.ex_Button.grid(row=3, column=1, padx=10, pady=10,sticky=W)

        self.quitButton = Button(self.ex_menu, text="Quitter", command=self.destroy,height = 1, width = 18)
        self.quitButton.grid(row=4, column=1, padx=10, pady=10,sticky=W)

    def import_file(self):
        rep = filedialog.askopenfilename(initialdir="/", title="Select file",
                                         filetypes=(("Excel files", "*.xlsx"), ("all files", "*.*")))
        if rep != "":
            self.rep_source_affiche.set(rep)
            try:
                self.save_data["source"] = rep
                with open('data.txt', 'w+') as outfile:
                    json.dump(self.save_data, outfile)
            except:
                self.save_data.update({"Source": rep})
                with open('data.txt', 'w+') as outfile:
                    json.dump(self.save_data, outfile)

    def rep_cible(self):

        self.rep_cible = filedialog.askdirectory()
        if self.rep_cible != "":
            self.rep_cible_affiche.set(self.rep_cible)

            try:
                self.save_data["cible"] = self.rep_cible
                with open('data.txt', 'w+') as outfile:
                    json.dump(self.save_data, outfile)
            except:
                self.save_data.update({"Cible": self.rep_cible })
                with open('data.txt', 'w+') as outfile:
                    json.dump(self.save_data, outfile)

    def ex_programme(self):

        if self.rep_source_affiche.get() == "":
            messagebox.showerror("Ficher source non sélectionné", "Veuillez sélectionner un fichier source")
        else:

            self.source = pd.read_excel(self.rep_source_affiche.get())

        if self.rep_cible_affiche.get() =="":
            messagebox.showerror("Répertoire source non sélectionné", "Veuillez sélectionner un répertoire source")

        if self.rep_source_affiche.get() != "" and self.rep_cible_affiche.get() != "":
            colonnes=[]
            colonnes = self.source.columns
            colonnes = list(colonnes)
            colonnes = str(colonnes)
            colonnes = colonnes[1:-1]


        if "Nom de voie" and "0-Matricule RH - Employé" and "Code postal" in colonnes:
            extract_adresse(self.rep_source_affiche.get(), self.rep_cible_affiche.get())
            messagebox.showinfo(title="Succès", message="Le fichier a bien été crée dans le répertoire suivant " + str(self.rep_cible_affiche.get()))
        else:
                print("cool")
                messagebox.showerror(title="Problème de colonnes", message="Le fichier doit contenir une colonne\
 intitulée Nom de voie contenant les adresses des collaborateurs")


    def load_data(self):
        try:
            with open('data.txt') as json_file:

                self.save_data = json.load(json_file)

            try:

                self.rep_cible_affiche.set(self.save_data["cible"])

            except:

                pass

            try:

                self.rep_source_affiche.set(self.save_data["source"])

            except:

                pass

        except:

            self.save_data={}

toto = Application(None)

toto.mainloop()