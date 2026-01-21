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

# 2) Distribucion Log-Normal: 
shape, loc, scale = stats.lognorm.fit(Data.iloc[:, 0], floc=0)  # floc=0 fija loc en 0
# Ajustar shape (sigma_log) de ddof=0 a ddof=1
sigma_log_fit = shape * np.sqrt(n / (n - 1))
mu_log_fit = np.log(scale)  # mu_log = ln(scale)

print('\nResultados metodo . fit() - Distribucion Log-Normal:')
print(f'mu_log (fit-lognormal): {mu_log_fit:.3f}')
print(f'sigma_log (fit-lognormal): {sigma_log_fit:.3f}')
print(f'Scale/Mediana (fit-lognormal): {scale:.2f}')

# 3) Distribucion Gumbel (Valores Extremos Tipo I):
# METODO DEL LIBRO:  Usando factores de frecuencia tabulados

# Tabla de factores de frecuencia de Gumbel (y_m y sigma_m)
# Fuente: Chow (1964), Aparicio Mijares, Ven Te Chow
gumbel_factors = {
    10: (0.49520, 0.94970),
    15: (0.51280, 1.02140),
    20: (0.52360, 1.06280),
    25: (0.53086, 1.09145),
    30: (0.53622, 1.11237),
    35: (0.54004, 1.12900),
    40: (0.54272, 1.14132),
    45: (0.54489, 1.15048),
    50: (0.54664, 1.15742),
    60: (0.54920, 1.16850),
    70: (0.55110, 1.17620),
    80: (0.55260, 1.18210),
    90: (0.55380, 1.18670),
    100: (0.55477, 1.19036)
}

# Obtener y_m y sigma_m para n=30
if n in gumbel_factors:
    y_m, sigma_m = gumbel_factors[n]
else:
    # Si n no está en la tabla, usar la aproximación
    y_m = 0.5772 + np.log(np.log(n / (n - 1)))
    sigma_m = 1.2825 / np.sqrt(np.log(n))
    print(f'\nAdvertencia: n={n} no está en la tabla.  Usando aproximación.')

print(f'\nFactores de Gumbel para n={n}:')
print(f'y_m = {y_m:.5f}')
print(f'sigma_m = {sigma_m:.5f}')

# Calcular variable reducida y para el valor b
y = y_m + sigma_m * (b - mu) / sigma

# Calcular probabilidad de no excedencia
F_gumbel = np.exp(-np.exp(-y))

# Calcular probabilidad de excedencia
P_gumbel = 1 - F_gumbel

# Periodo de retorno
T_gumbel = 1 / P_gumbel

print('\nResultados distribucion Gumbel (Metodo del libro):')
print(f'Variable reducida y:  {y:.4f}')
print(f'Pbb de excedencia: {P_gumbel:.4f}')
print(f'Periodo de retorno (años): {T_gumbel:.1f}')

# Comparacion con MLE (metodo fit de scipy):
loc_fit_gumbel, scale_fit_gumbel = stats.gumbel_r.fit(Data.iloc[:, 0])
P_gumbel_mle = stats.gumbel_r.sf(b, loc=loc_fit_gumbel, scale=scale_fit_gumbel)

print('\n' + '='*70)
print('COMPARACION:  Metodo del libro vs MLE')
print('='*70)
print(f'{"Método":<30} {"P(excedencia)":<20} {"T (años)":<15}')
print('-'*70)
print(f'{"Gumbel (libro, momentos)":<30} {P_gumbel: <20.4f} {T_gumbel:<15.1f}')
print(f'{"Gumbel (MLE, scipy. fit)":<30} {P_gumbel_mle:<20.4f} {1/P_gumbel_mle:<15.1f}')