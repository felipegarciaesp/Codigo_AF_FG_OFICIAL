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