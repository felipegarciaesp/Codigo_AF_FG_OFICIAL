# Codigo_AF_FG_OFICIAL
Codigo Oficial en trabajo para calcular AF, realizado integramente por Felipe Garcia


## Diferencia entre gumbel_r y gumbel_l

- **`gumbel_r`** (right-skewed o máximos): Distribución Gumbel para **valores máximos**
  - Usada para modelar eventos extremos máximos (crecidas, lluvias máximas, etc.)
  - Esta es la más común en hidrología

- **`gumbel_l`** (left-skewed o mínimos): Distribución Gumbel para **valores mínimos**
  - Usada para modelar eventos extremos mínimos (sequías, caudales mínimos, etc.)

## Fórmulas de la Distribución Gumbel

La función de distribución acumulada (CDF) es:

```
F(x) = exp(-exp(-(x-μ)/β))
```

**Donde:**
- **μ (mu)** = parámetro de ubicación (`loc` en scipy)
- **β (beta)** = parámetro de escala (`scale` en scipy)

**Para el período de retorno T:**
```
P(X ≤ x) = 1 - 1/T
x_T = μ - β × ln(-ln(1 - 1/T))
```

## Uso en Hidrología Aplicada

**Para hidrología aplicada, usa `scipy.stats.gumbel_r` para:**
- Crecidas máximas
- Precipitaciones máximas
- Caudales máximos

**Usa `scipy.stats.gumbel_l` solo para:**
- Caudales mínimos
- Sequías

## ddof: Delta Degrees of Freedom

- `Data.std()` calcula la desviación estándar con **`ddof=1`** (muestra)
- `stats.norm.fit()` calcula la desviación estándar con **`ddof=0`** (población)

Para que la desviación estándar calculada con el método `.std()` y el método `.fit()` sean comparables, se ajusta `sigma_fit_mle` multiplicándolo por `sqrt(n/(n-1))`, donde `n` es el tamaño de la muestra.

**En resumen:**
- Con **`ddof=1`** se obtiene la desviación estándar de la **muestra**
- Con **`ddof=0`** se obtiene la desviación estándar de la **población**

> ⚠️ **Importante en Hidrología:** Tenemos que usar `ddof=1` para obtener estimaciones insesgadas de la desviación estándar a partir de datos muestrales.

## Distribución Lognormal en scipy

En `scipy.stats.lognorm`, los parámetros tienen un significado diferente al de la distribución normal. 

`stats.lognorm.fit()` devuelve **3 parámetros** en este orden:

1. **`s`**: sigma del log (desviación estándar de ln(X))
2. **`loc`**: parámetro de localización (usualmente 0 para lognormal)
3. **`scale`**: escala = exp(mu_log) = mediana

> 📌 **Nota:** Usa `floc=0` para fijar el parámetro de localización en 0, que es lo estándar para distribuciones lognormales en hidrología (sin desplazamiento).

**Ejemplo:**
```python
from scipy import stats
import numpy as np

# Datos de caudales
caudales = np.array([45, 67
