import pandas as pd
from xlsxwriter import *

data = pd.read_excel(r'C:\Users\Sabri.GASMI\Desktop\GEFCO\Data\Vision\ADMA00_General_report.xlsx')
result = pd.DataFrame(columns=["Matricule","Anomalies"])

result["Matricule"]=data["0-Matricule RH - Employé"]

def vide(colonne_source):
    for i,val in enumerate(data[colonne_source]):
        if pd.isna(val):
            if pd.notna(result.at[i,"Anomalies"]):
                result.at[i, "Anomalies"] = str(result.at[i, "Anomalies"]) + str(colonne_source) + " est vide/"

            if pd.isna(result.at[i,"Anomalies"]):
                result.at[i,"Anomalies"] = str(colonne_source) + " est vide/"

#   Appel de fonction

vide("Nom")
vide("Nationalité principale")
vide("Sexe")


# Export Excel

writer = pd.ExcelWriter(r'C:\Users\Sabri.GASMI\Desktop\Anomalie.xlsx',engine='xlsxwriter')
result.to_excel(writer, index=False)
writer.save()
