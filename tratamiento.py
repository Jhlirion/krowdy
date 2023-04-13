#librerias empleadas
import pandas as pd
import re
import difflib
from pathlib import Path
import json
from funciones import subircsv
from funciones import mayus, busqueda
from collections import defaultdict

def trat_carg():
    #Extracción de datos
    ins_edu = pd.read_csv('2023-04-11T04-36-02-388Zinstituciones_educativas.csv')
    homolog = pd.read_json('https://krowdy.s3.us-east-1.amazonaws.com/ats/job/6434447e8e6c4c0008808420/opentest/2023-04-11T04-36-09-824ZUniversidades.json')

    #Pasamos los datos a Mayusculas para una mejor iteración de las palabras
    ins_edu['value_may'] = ins_edu['value'].apply(lambda x: mayus(x))
    homolog['value_may'] = homolog['Nombre '].apply(lambda x: mayus(x))

    '''
    Con este codigo se elimina los signos de puntuación que suelen poner al registrarse.
    ins_edu['siglas_may'] = ins_edu['value_may'].apply(lambda x: splitear(x))

    Con esto podemos hacer busqueda de los datos de las universidades obtenidos de los alumnos
    en los datos de la SUNEDU (sin limpieza de datos) con baja precisión
    ins_edu['universidad homologada'] = ins_edu['value'].apply(lambda x: busqueda(str(x),homolog, 'Nombre ', 0.5))

    '''

    nombre = list(homolog['Nombre '])
    sigla = list(homolog['Siglas '])

    #creamos diccionario para reemplazar los datos con siglas
    diccionario_siglas = defaultdict(list)
    prueba = {sigl:name for (sigl, name) in list(zip(sigla, nombre))}
    ins_edu.replace({'value_may': prueba}, inplace=True)

    #normalización de datos 
    ins_edu['value_may'] = ins_edu['value_may'].apply(lambda x: mayus(x))

    #Busqueda de los datos de las universidades obtenidos de los alumnos en los datos de la SUNEDU (limpieza)
    ins_edu['universidad homologada'] = ins_edu['value_may'].apply(lambda x: busqueda(x,homolog, 'value_may', 0.80))

    #eliminamos datos que no necesitamos
    ins_edu.drop(columns={'value_may'}, inplace=True)

    # subimos archivo homologado
    subircsv('Datos', 'universidad_homologada', ins_edu, '.csv')
    return ins_edu
    
    
    
def dic_json():
    ins_edu = trat_carg()
    prueba = ins_edu[['value','universidad homologada']]
    prueba = prueba.drop_duplicates()

    nombres = list(prueba['value']) #sinonimos
    homologados = list(prueba['universidad homologada']) #nombre_universidad
    
    my_dict = defaultdict(list)
    
    for indice, nombre in list(zip(homologados, nombres)):
        my_dict[indice].append(nombre)
        
    with open('Datos\sinonimos_universidade.json', 'w') as file:
        json.dump(my_dict, file, indent=4)
    
    
    
    
