# Objetivos del proyecto

**Cambio climático en Argentina y su relación con el crecimiento económico (PBI)**
Instituto 57 — Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial
Análisis y Exploración de Datos — 2.º año, grupo 6
Docente: Ibarra Martín · Elías Campos · Tiago Maidana · Rodrigo Bulggiani · Romina Guzmán

---

## Objetivo general

Analizar la evolución histórica del cambio climático en Argentina entre 1961 y 2024 y su relación
con el crecimiento económico, y evaluar si es posible predecir la evolución de la temperatura a
partir de las variables económicas y climáticas disponibles, empleando la metodología CRISP-DM de
principio a fin.

### Pregunta de investigación que lo engloba

> ¿Existe una relación entre el crecimiento económico (PBI) y el cambio climático en Argentina entre
> 1961 y 2024, y es posible predecir la evolución de la temperatura a partir de las variables
> económicas y climáticas?

---

## Los 6 objetivos específicos

### 1. Descripción de cada variable
**Qué:** describir cómo cambió cada variable año por año —magnitud del cambio, tendencia y años
atípicos.

**Procedimiento:** gráfico de línea por variable, regresión lineal sobre el tiempo y detección de
atípicos por rango intercuartílico (IQR).

**Se acepta si:** se entrega el informe de tendencia con coeficiente, error estándar y p-valor de
cada variable.

---

### 2. Relación entre el PBI y el clima
**Qué:** evaluar si existe relación entre el PBI y las variables climáticas.

**Procedimiento:** matriz de correlación de Pearson con p-valor, complementada con análisis
detrendizado.

**Se acepta si:** se entrega la matriz completa y el contraste explícito entre la correlación en
niveles y la correlación sobre residuos de la tendencia.

> Importante: toda correlación se reporta **en niveles y detrendizada**. Si una correlación
> desaparece al quitar la tendencia, es espuria y no debe presentarse como hallazgo.

---

### 3. Multicolinealidad
**Qué:** verificar si el PBI, los GEI y la lluvia pueden usarse juntos en un mismo modelo sin que
una variable explique lo que explica otra.

**Procedimiento:** correlación por pares y Variance Inflation Factor (VIF) para cada variable
predictora.

**Se acepta si:** se entregan la tabla de pares y la tabla de VIF, con el umbral de referencia
declarado (VIF < 5 despreciable · 5 a 10 moderada · ≥ 10 severa).

---

### 4. Estabilidad temporal de la relación
**Qué:** determinar si la relación PBI–temperatura es estable a lo largo del tiempo.

**Procedimiento:** comparación de las correlaciones entre las dos mitades del período (1961–1992 y
1993–2024), test de Fisher y modelo con interacción `temp ~ pbi + post + pbi:post`.

**Se acepta si:** se reporta la comparación con su p-valor y el coeficiente de interacción.

---

### 5. Modelos predictivos
**Qué:** construir modelos que predigan la anomalía de temperatura a partir de las variables
económicas y climáticas.

**Procedimiento:** Regresión Lineal Múltiple y Random Forest Regressor, con partición temporal
—nunca aleatoria—: se entrena con los años más tempranos y se evalúa con los más recientes.

**Se acepta si:** los modelos quedan ajustados, diagnosticados y con la importancia de variables
reportada.

---

### 6. Evaluación frente al baseline
**Qué:** evaluar si los modelos aportan algo frente a no usar ningún modelo.

**Procedimiento:** comparación contra un baseline naive de **persistencia** (la temperatura de este
año es la del año anterior), mediante RMSE, MAE y R² sobre el mismo bloque de prueba.

**Se acepta si:** se entrega la tabla comparativa de métricas con una regla de decisión explícita.

> **Regla de decisión:** un modelo solo se considera útil si su RMSE es inferior al del baseline.
> Si ningún modelo lo supera, el objetivo se responde igualmente con un resultado negativo, y ese
> resultado se documenta igual que uno favorable. No se modifica la definición de baseline después
> de ver los resultados.

---

## Variables del estudio

| Variable | Tipo | Rol en el modelo | Unidad | Fuente |
|---|---|---|---|---|
| Anomalía de temperatura media | Cuantitativa continua | Variable respuesta | °C | CIAM / SMN |
| Crecimiento del PBI | Cuantitativa continua | Predictora | % anual | Banco Mundial |
| Emisiones de GEI | Cuantitativa continua | Predictora | MtCO₂eq | Global Carbon Project (OWID) |
| Anomalía de precipitación | Cuantitativa continua | Predictora | % | CIAM / SMN |
| Año | Cuantitativa discreta | Variable de tiempo | — | — |

Período: **1961–2024**, 64 observaciones anuales.

---

## Hipótesis de trabajo

| | Enunciado | Cómo se pone a prueba |
|---|---|---|
| **H1** | El PBI y las emisiones de GEI se correlacionan positivamente con la anomalía de temperatura; la precipitación se relaciona de forma negativa. | Correlación de Pearson entre pares, en niveles y sobre residuos de la tendencia |
| **H2** | Esa relación se mantiene o se fortalece con el tiempo. | Correlación por mitades, test de Fisher y coeficiente de interacción periodo × PBI |
| **H3** | Es posible construir un modelo predictivo de temperatura que supere a un baseline naive. | Comparación de RMSE contra el baseline naive de persistencia |

---

## Resumen en una línea por objetivo

1. **Tendencias** — cómo se movió cada variable en 64 años
2. **Correlación PBI ↔ clima** — con control de tendencia
3. **Multicolinealidad** — PBI, GEI y lluvia son independientes
4. **Estabilidad temporal** — ¿la relación cambió con los años?
5. **Modelos** — Regresión Lineal Múltiple + Random Forest
6. **Evaluación** — ¿superan al baseline de persistencia?

---

## Documentos del proyecto

- `Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx` — informe metodológico: cómo se
  recolectan, preparan, modelan y evalúan los datos
- `Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx` — plan de ejecución: actividades,
  cronograma, riesgos y recursos

Ambos están en la carpeta `Trabajo integrador y plan de proyecto`.
