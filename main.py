import pandas as pd

#Extracción de datos
ins_edu = pd.read_csv('2023-04-11T04-36-02-388Zinstituciones_educativas.csv')
homolog = pd.read_json('https://krowdy.s3.us-east-1.amazonaws.com/ats/job/6434447e8e6c4c0008808420/opentest/2023-04-11T04-36-09-824ZUniversidades.json')

print(homolog)