import pandas as pd
import glob

arquivos = glob.glob("./data/csv/*.csv")

df = pd.concat((pd.read_csv(arq) for arq in arquivos), ignore_index=True)
df.to_csv("data_final.csv", index=False)