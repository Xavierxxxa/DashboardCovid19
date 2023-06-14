import pandas as pd

df = pd.read_csv("HIST_PAINEL_COVIDBR_2023.csv", sep=";")

df['data'] = pd.to_datetime(df['data'])

data_max = df['data'].max()
data_max = data_max.date()
data_max = str(data_max)

# df_muni = df[(~df["municipio"].isna()) & (df['data'] == data_max)]
# df_muni_v2 =df_muni[['estado', 'municipio', 'casosAcumulado','obitosAcumulado']]

# df_muni_v2.to_csv("df_muni.csv")


# Data Generation
df_states = df[(~df["estado"].isna()) & (df["codmun"].isna())]
df_brasil = df[df["regiao"] == "Brasil"]

df_states.to_csv("df_states.csv")
df_brasil.to_csv("df_brasil.csv")
