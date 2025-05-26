import pandas as pd
import re


def removeText(lista):
    for i, item in enumerate(lista):
        numeros = re.findall(r'\d+', str(item))
        lista[i] = sum(int(n) for n in numeros)
    return lista


def extrairArmazenamento(lista):
    copyLista = lista.copy()
    for i, item in enumerate(copyLista):
        texto = str(item).upper()
        match = re.search(r'(\d+)\s*(T|G)B', texto)
        if match:
            valor = int(match.group(1))
            if match.group(2) == 'T':
                valor *= 1024
            copyLista[i] = valor
        else:
            copyLista[i] = None
    return copyLista






                
def formatterCSV(): 
    df = pd.read_csv("mobiles_dataset.csv", sep=",", decimal=",", encoding="latin1")
    print("Colunas encontradas:", df.columns.tolist())
    df['Launched Year'] = sorted(pd.to_numeric(df['Launched Year'])) 
    df['RAM'] = sorted(removeText(df['RAM']))
    df['Mobile Weight'] = removeText(df['Mobile Weight'])
    df['Back Camera'] = removeText(df["Back Camera"])
    df['Battery Capacity'] = removeText(df['Battery Capacity'])
    df['Screen Size'] = removeText(df['Screen Size'])
    df['Storage'] = extrairArmazenamento(df['Model Name'])
    return df