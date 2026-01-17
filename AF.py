# Librerias
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Lectura de datos a los que se realizara AF:
Data = pd.read_excel('Data.xlsx', index_col=0)

# Para distribucion Normal:
# Calculo de promedio y desviacion estandar
mu = Data.mean().iloc[0]
sigma = Data.std().iloc[0]

# Para distribucion Log-Normal:
log_data = np.log(Data.iloc[:, 0]) #Esto cambiarlo si ingreso mas estaciones.
mu_log = log_data.mean()
sigma_log = log_data.std()

# Determinar probabilidad:
b = 3100.0
P_norm = stats.norm.sf(b, loc=mu, scale=sigma)
print('Resultados distribucion Normal:')
print(f'Pbb de excedencia: {P_norm:.4f}')
print(f'Periodo de retorno (años): {1/P_norm:.1f}')

P_lognorm = stats.lognorm.sf(b, s=sigma_log, scale=np.exp(mu_log))
print('\nResultados distribucion Log-Normal:')
print(f'Pbb de excedencia: {P_lognorm:.4f}')
print(f'Periodo de retorno (años): {1/P_lognorm:.1f}')

# Resultados de promedio y desviacion estandar calculados:
print('\nResultados de Promedio y Desviacion Estandar (calculo habitual):')
print(f'Promedio (no-fit): {mu:.2f}')
print(f'Desviacion estandar (no-fit): {sigma:.2f}')

# Resultados de metodo .fit() de scipy:
# Se calcula tamaño de la muestra:
n = len(Data.iloc[:, 0])

# 1) Distribucion Normal: 
mu_fit_norm, sigma_fit_mle_norm = stats.norm.fit(Data.iloc[:, 0])
sigma_fit_norm = sigma_fit_mle_norm * np.sqrt(n / (n - 1))  # Ajuste a ddof = 1
print('\nResultados metodo .fit() - Distribucion Normal:')
print(f'Promedio (fit-normal): {mu_fit_norm:.2f}')
print(f'Desviacion estandar (fit-normal): {sigma_fit_norm:.2f}')

"""
ddof: Delta Degrees of Freedom
- Data.std() calcula la desviacion estandar con ddof=1 (muestra).
- stats.norm.fit() calcula la desviacion estandar con ddof=0 (poblacion).

Para que la desviacion estándar calculado con el metodo .std() y el metodo .fit() sean comparables, 
se ajusta sigma_fit_mle multiplicandolo por sqrt(n/(n-1)), donde n es el tamaño de la muestra.

En resumen, con ddof=1 se obtiene la desviacion estandar de la muestra y con ddof=0 la desviacion estandar de la poblacion.
En hidorlogia tenemos que usar ddof=1 para obtener estimaciones insesgadas de la desviacion estandar a partir de datos muestrales.

"""

# 2) Distribucion Log-Normal: 
shape, loc, scale = stats.lognorm.fit(Data.iloc[:, 0], floc=0)  # floc=0 fija loc en 0
# Ajustar shape (sigma_log) de ddof=0 a ddof=1
sigma_log_fit = shape * np.sqrt(n / (n - 1))
mu_log_fit = np.log(scale)  # mu_log = ln(scale)

print('\nResultados metodo . fit() - Distribucion Log-Normal:')
print(f'mu_log (fit-lognormal): {mu_log_fit:.3f}')
print(f'sigma_log (fit-lognormal): {sigma_log_fit:.3f}')
print(f'Scale/Mediana (fit-lognormal): {scale:.2f}')

"""
En scipy.stats.lognorm, los parámetros tienen un significado diferente al de la distribución normal:
stats.lognorm.fit() devuelve 3 parámetros en este orden:

    1) s: sigma del log (desviación estándar de ln(X))
    2) loc: parámetro de localización (usualmente 0 para lognormal)
    3) scale: escala = exp(mu_log) = mediana

Nota: Usa floc=0 para fijar el parámetro de localización en 0, que es lo estándar para distribuciones lognormales en hidrología (sin desplazamiento).
"""

