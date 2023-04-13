import pandas as pd
import re
import difflib
from pathlib import Path
from collections import defaultdict

#funciones
def mayus(pal):
    palabra = re.sub(r'[^\w\s\´]','',pal)
    palabra = palabra.upper()
    return palabra

def splitear(pal):
    palabra = re.sub(r'[^\w\s]','',pal)
    palabra = palabra.upper()
    palabras = palabra.split()   
    nueva_cadena = ""
    if len(pal) > 3:
        for p in palabras:
            if len(p) > 3:
                nueva_cadena = nueva_cadena + p[0]
    else: nueva_cadena = pal
    return nueva_cadena

def busqueda(palabra, df, columna, presicion):
    palabras_columna = df[columna].values
    palabras_similares = difflib.get_close_matches(palabra, palabras_columna, n=1, cutoff=presicion)
    if len(palabras_similares) == 0:
        palabras_similares = palabra
    return "".join(palabras_similares)

def subircsv(Nombre_Carpeta, Nombre_Archivo, df, extencion):
    filepath = Path(Nombre_Carpeta + '/', Nombre_Archivo + extencion)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)