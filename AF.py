# Librerias
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Lectura de datos a los que se realizara AF:
Data = pd.read_excel('Data.xlsx', index_col=0)

# Calculo de promedio y desviacion estandar
mu = Data.mean().iloc[0]
sigma = Data.std().iloc[0]

# Determinar probabilidad:
b = 3100.0
P = stats.norm.sf(b, loc=mu, scale=sigma)
print('Pbb de excedencia:', P)
print('Periodo de retorno (años):', 1/P)
