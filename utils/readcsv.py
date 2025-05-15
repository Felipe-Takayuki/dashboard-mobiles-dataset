import pandas as pd
import re


def removeText(lista):
    for i, item in enumerate(lista):
        numero = int(re.search(r'\d+', item).group())
        lista[i] = numero
    return lista

                
def formatterCSV(): 
    df = pd.read_csv("mobiles_dataset.csv", sep=",", decimal=",", encoding="latin1")
    print("Colunas encontradas:", df.columns.tolist())
    df['Launched Year'] = sorted(pd.to_numeric(df['Launched Year'])) 
    df['RAM'] = sorted(removeText(df['RAM']))
    df['Mobile Weight'] = removeText(df['Mobile Weight'])
    df['Battery Capacity'] = removeText(df['Battery Capacity'])
    df['Screen Size'] = removeText(df['Screen Size'])
    return df