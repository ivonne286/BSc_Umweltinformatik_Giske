# Code zur Erstellung der Tabelle 7: Alle Fehlerkombinatinen und ihre Häufigkeit
import pandas as pd

RELATIVE_PATH_IN = "../input/cross.csv"
RELATIVE_PATH_OUT = "../output/kreuztabelle.csv"

# Import csv Tabelle mit Daten
df = pd.read_csv(RELATIVE_PATH_IN, delimiter=";")
# Dictionary of Lists
data_dict = {}
data_dict["Fehlertyp"] = df["Fehlertyp"]
data_dict["Kategorie"] = df["Kategorie"]
data_dict["Anzahl"] = [1] * 238

df_cross = pd.DataFrame(data_dict)
# Verwendung der Kreuztabelle mit Aggregation
tabelle = pd.crosstab(
    df_cross["Fehlertyp"],
    df_cross["Kategorie"],
    values=df_cross["Anzahl"],
    aggfunc="sum",
)
tabelle = pd.crosstab(df_cross["Fehlertyp"], df_cross["Kategorie"])
print(tabelle)

tabelle.to_csv(RELATIVE_PATH_OUT, sep=";")
