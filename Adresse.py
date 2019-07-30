import pandas as pd
import re

def extract_adresse(source, destination):

    data = pd.read_excel(source)

    result = pd.DataFrame(columns=["Matricule", "Adresse initiale","Numéro dans la rue","Complément de numéro","Adresse (voie)","nb_char","Code postal","Pays" ,"Espace"])


    result[["Matricule","Adresse initiale","Code postal","Complément d'adresse","Pays"]] = data[["0-Matricule RH - Employé","Nom de voie","Code postal","Complément d'adresse","Pays"]]


    for i, val in enumerate(result["Adresse initiale"]):

        try:  #Extraction du numéro de rue
            num = re.findall(r'^\d+',val)
            result.at[i,"Numéro dans la rue"] = int(num[0])
        except:
            pass

        try: #Extraction complément de numéro une seule lettre collée
            complement = re.findall(r'^\S+', val)
            if re.findall(r'\d+',complement[0]):
                try:
                    complement = re.findall(r'[a-z]+|[A-Z]',complement[0])
                    result.at[i,"Complément de numéro"] = complement[0].upper()
                except:
                    pass
        except:
            pass

        try: #Extraction complément de numéro contenant BIS/TER
            complement = re.findall(r'(?i)BIS | (?i)BIS |(?i)TER | (?i)TER ', val)
            result.at[i, "Complément de numéro"] = complement[0].upper()
        except:
            pass

        try: #Extraction complément de numéro, une seule lettre après les chiffres 23 A rue
            complement = re.findall(r'\d\s[A-Z]\s', val)
            completement = re.findall(r'[A-Z]', complement[0])
            result.at[i, "Complément de numéro"] = complement[0].upper()
            result.at[i,"Espace"] = 1
        except:
            pass

    for i, val in enumerate(result["Adresse initiale"]):
        try:
            num_rue = str(result.at[i,"Numéro dans la rue"])
            compl = str(result.at[i, "Complément de numéro"])

            if num_rue == "nan":
                num_rue = ""
            if compl == "nan":
                compl = ""

            a = len(num_rue) + len(compl)

            if result.at[i, "Espace"]==1:
                b = len(str(result.at[i,"Adresse initiale"])) - a + 1
            else:
                b = len(str(result.at[i,"Adresse initiale"])) - a
            adresse = str(result.at[i,"Adresse initiale"])[-b:]

            adresse = re.findall(r'^\s*(.*)\s*$', adresse)
            adresse = re.findall(r'^(?i)[^a-z]*(.*)', adresse[0])

            result.at[i, "Adresse (voie)"] = adresse[0]


        except:
            pass



    for i, val in enumerate(result["Complément de numéro"]):
        try:
            a= re.findall(r'((?i)[a-z])', val)
            result.at[i,"Complément de numéro"] = a[0]
        except:
            pass

    for i, val in enumerate(result["Adresse (voie)"]):
        if val =="nan":
            result.at[i,"Adresse (voie)"] = ""

    for i, val in enumerate(result["Adresse initiale"]):
        try:
            result.at[i,"nb_char"] = len(result.at[i,"Adresse (voie)"])
        except:
            pass

    result = result.drop(columns=["Espace"])
    writer = pd.ExcelWriter(destination + "/Adresses_nouvelles.xlsx",engine='xlsxwriter')
    result.to_excel(writer, index=False)
    writer.save()
