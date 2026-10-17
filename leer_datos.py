import pandas as pd

generales = pd.read_excel("informe_datos.xlsx", sheet_name="generales")
actividades = pd.read_excel("informe_datos.xlsx", sheet_name="actividades")

print(generales.iloc[0].to_dict())
print(actividades)