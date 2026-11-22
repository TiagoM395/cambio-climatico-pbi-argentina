# Objetivos 5 y 6 — Guía para entender y exponer el trabajo


## 1. En una frase

- **Objetivo 5:** construir modelos que predigan la anomalía de temperatura anual de Argentina a
  partir de variables económicas y climáticas, ajustarlos, diagnosticarlos y reportar la importancia
  de cada variable.
- **Objetivo 6:** evaluar si esos modelos sirven para algo, comparándolos contra un pronóstico
  trivial (el baseline) con una regla de decisión fijada **antes** de ver los resultados.

La conclusión es un **resultado negativo**: los dos modelos predefinidos no superan al baseline.
Ese resultado es el hallazgo, no un error de la práctica.

---

## 2. Qué predecimos y con qué datos

| Elemento | Definición |
|---|---|
| Variable respuesta (`y`) | `temp`: anomalía de temperatura media anual de Argentina, en °C (CIAM / SMN) |
| Predictoras (`X`) | `pbi` (crecimiento del PBI, %, Banco Mundial), `gei` (emisiones de gases de efecto invernadero, MtCO₂eq, OWID / Global Carbon Project), `lluvia` (anomalía de precipitación, %, CIAM / SMN) |
| Período | 1961–2024, 64 observaciones anuales completas. 2025 se descarta porque GEI y PBI per cápita están incompletos |
| Entrenamiento | 1961–2009 (n = 49) |
| Prueba | 2010–2024 (n = 15) |
| Partición | **Temporal**, nunca aleatoria: en series de tiempo mezclar años sería usar el futuro para predecir el pasado |
| Archivo | `data/processed/dataset_nacional.csv` |

La partición está implementada en `modelos.py:211-240` y en la app en `app.py:2402`.

---

## 3. Los modelos que usamos y por qué

### 3.1 Regresión Lineal Múltiple (OLS)

```
temp = β0 + β1·pbi + β2·gei + β3·lluvia + error
```

Es el punto de partida natural: es interpretable, permite testear cada coeficiente y muestra cuánto
aporta cada variable "manteniendo las demás constantes". Se ajusta por mínimos cuadrados con
`np.linalg.lstsq` (`modelos.py:87`, `app.py:462`).

**Qué reportamos:**
- Coeficientes, errores estándar, estadístico t, p-valores e intervalos del 95%.
- **Errores robustos HAC (Newey-West, 3 rezagos)**, el mismo criterio que el objetivo 1. Los usamos
  porque Shapiro-Wilk rechaza la normalidad de los residuos (p = 0,0188); son los p-valores que se
  leen en la tabla.
- R² = 0,1688, R² ajustado = 0,1133, F(3, 45) = 3,0453 (p = 0,0383).
- **Coeficientes estandarizados** para comparar pesos: GEI +0,3832, Lluvia −0,2059, PBI −0,0777.
- Diagnósticos: Shapiro (p = 0,0188 → se rechaza normalidad), Breusch-Pagan (p = 0,5316 → varianza
  constante), Durbin-Watson (2,1283 → sin autocorrelación) y VIF máximo 1,0397 (sin multicolinealidad).

**Resultado clave del ajuste:** dentro del entrenamiento el GEI es significativo incluso con HAC
(p = 0,0002), pero eso *no* significa que prediga: hay que ver si aguanta fuera de muestra.

### 3.2 Random Forest Regressor

- 500 árboles, semilla fija 42, `oob_score=True`, sin límite de profundidad y hoja mínima de 1
  (`modelos.py:344`, `app.py:2926`).
- Se eligió porque no impone linealidad y puede capturar interacciones; con pocas variables es barato
  y reproducible.
- **OOB R² = −0,1883**: ni siquiera internamente logra explicar la variación.
- Importancia Gini: GEI 0,4374 · Lluvia 0,3576 · PBI 0,2049.
- Importancia por **permutación sobre la prueba** (50 repeticiones): PBI +0,0055, Lluvia +0,0034,
  GEI −0,0090 (cambio en el RMSE al desordenar cada variable).

> La diferencia entre Gini y permutación es central: Gini dice "GEI es la variable más importante",
> pero al desordenar GEI en el bloque de prueba el RMSE **mejora** (−0,0090). Es decir: esa
> "importancia" es ajuste a los datos de entrenamiento, no capacidad predictiva.

### 3.3 Baseline naive de persistencia

```
temp(t) = temp(t-1)
```

No usa ninguna variable explicativa: simplemente repite el valor del año anterior. Es el piso que
cualquier modelo con pretensiones debe superar. Se definió en `OBJETIVOS_del_proyecto.md:90-98`,
antes de correr nada.

Como control adicional (previsto en el informe) también calculamos el baseline de **último valor
constante**, que repite el último valor del entrenamiento. **No reemplaza al baseline oficial.**

---

## 4. Cómo se resolvió, paso a paso

1. **Cargar y recortar** el dataset a 1961–2024 y quitar filas incompletas (`cargar_datos`).
2. **Partir temporalmente** en entrenamiento y prueba y verificar que no se mezclen años.
3. **Ajustar el OLS** y calcular coeficientes, p-valores HAC, ajuste global y coeficientes estandarizados.
4. **Diagnosticar** supuestos (normalidad, varianza constante, autocorrelación, multicolinealidad).
5. **Ajustar el Random Forest** y reportar OOB + importance Gini + importance por permutación en prueba.
6. **Calcular el baseline** de persistencia (y el control constante).
7. **Comparar** RMSE, MAE y R² de los tres enfoques sobre el **mismo** bloque de prueba y aplicar la
   regla: un modelo sólo sirve si su RMSE es menor que el del baseline.
8. **Control de robustez:** validación cruzada temporal con `TimeSeriesSplit` de 5 cortes, sin usar
   años futuros para entrenar.
9. **Análisis complementario (revisión):** HAC, baseline constante y modelo con tendencia con
   sensibilidad por cortes móviles. No cambia la decisión oficial.

Todo esto se ejecuta con `python modelos.py` (secciones numeradas 1 a 8) y se visualiza en las
páginas "Objetivo 5" y "Objetivo 6" de la app Streamlit.

---

## 5. Resultados oficiales

| Modelo | RMSE | MAE | R² | ¿Supera al baseline? |
|---|---|---|---|---|
| **Baseline naive (persistencia)** | **0,3776** | 0,3100 | −1,1163 | — (referencia) |
| Regresión Lineal Múltiple | 0,3919 | 0,3234 | −1,2800 | No |
| Random Forest (500 árboles) | 0,4192 | 0,3514 | −1,6083 | No |

- El mejor de los dos modelos (regresión lineal) queda **0,0143 °C por encima** del baseline.
- El **R² negativo** de los tres enfoques indica que incluso la persistencia predice peor que la
  media del bloque de prueba; los modelos, peor todavía.
- En la validación cruzada temporal el RF promedia 0,3798 ± 0,0983 frente a 0,4133 ± 0,0513 de la
  persistencia. **No cambia el veredicto**: la regla se aplica al bloque 2010–2024 predefinido;
  cambiarla después de ver resultados sería modificar el criterio a medida.
- **H3 queda rechazada**: no es posible construir, con estas variables, un modelo que supere al
  baseline naive.

---

## 6. ¿Por qué no superan el baseline? (el corazón de la exposición)

### 6.1 La señal del GEI es espuria

El GEI parece importante dentro del entrenamiento (p HAC = 0,0002; mayor coeficiente estandarizado),
pero el objetivo 2 mostró que la correlación temperatura–GEI cae de **+0,600 en niveles a −0,165 al
quitar la tendencia** (p = 0,194). Ambas series suben con el tiempo, y eso crea una asociación
aparente. Cuando se evalúa fuera de muestra, desaparece: permutar GEI en la prueba no empeora el
RMSE, lo mejora.

### 6.2 PBI y lluvia no aportan

Con errores HAC, PBI tiene p = 0,5067 y lluvia p = 0,1496. El objetivo 4 mostró además que la
relación PBI–temperatura es débil y prácticamente idéntica en las dos mitades del período
(r = −0,169 vs −0,168; test de Fisher p ≈ 0,997). No hay relación que aprender.

### 6.3 El Random Forest sobreajusta

Con 49 observaciones y árboles sin podar, el bosque memoriza el entrenamiento. Prueba de eso:
OOB R² negativo (−0,1883) y una importancia Gini alta que no se confirma con permutación en prueba.
Más complejidad no compensa falta de señal.

### 6.4 La muestra es corta y la variable es ruidosa

64 años anuales, 49 para entrenar y 15 para probar. La anomalía de temperatura de un año está
dominada por oscilaciones interanuales que PBI, GEI y lluvia no explican. Con ese ruido, cualquier
ventaja de 0,01–0,02 °C es irrelevante frente a la incertidumbre muestral.

### 6.5 La persistencia es un piso duro… pero no es toda la explicación

Copiar el año anterior funciona porque la temperatura tiene inercia. Sin embargo, en este bloque el
control con **último valor constante da RMSE 0,2685**, todavía mejor que la persistencia. Conviene
decirlo con precisión: lo que se sostiene no es "la temperatura tiene memoria y por eso ganamos",
sino **"ninguna de nuestras predictoras reduce el error por debajo de pronósticos triviales"**.

### 6.6 Cómo decirlo en una frase

> "El GEI parece significativo sólo porque comparte tendencia con la temperatura; al controlar la
> tendencia o al salir de muestra, la señal desaparece. El PBI y la lluvia nunca la tuvieron. Por eso
> nuestros modelos no bajan el error de repetir el último valor."

---

## 7. Lo que se agregó en la revisión (sin romper la regla)

Estos tres puntos están en el código y en la app, y conviene mencionarlos para mostrar que el
resultado se revisó críticamente:

1. **Inferencia HAC** en el OLS del objetivo 5, coherente con el objetivo 1.
2. **Baseline alternativo** de último valor constante: RMSE 0,2685, MAE 0,2287, R² −0,0700.
3. **Modelo complementario con tendencia** (`temp ~ anio + pbi + gei + lluvia`):

| Modelo | RMSE | MAE | R² | Δ vs persistencia |
|---|---|---|---|---|
| Persistencia (oficial) | 0,3776 | 0,3100 | −1,1163 | — |
| Tendencia (sola) | 0,3797 | 0,3212 | −1,1400 | +0,0021 |
| Tendencia + exógenas | 0,3326 | 0,2774 | −0,6421 | −0,0450 |

**Lectura correcta:** el modelo con tendencia baja el RMSE, pero **no se incorpora a la decisión
oficial** porque se propuso después de ver resultados. Además, la mejora **no viene de las
exógenas**: en entrenamiento r(año, GEI) = 0,9749 y al incluir la tendencia el GEI pasa a
p HAC = 0,698 (deja de ser significativo). Es extrapolación del calentamiento, no predicción
económica. El R² sigue siendo negativo (−0,64).

**Sensibilidad con 4 cortes móviles** (prueba de 5 años después de cada corte):

| Modelo | 1994 | 1999 | 2004 | 2009 | Media |
|---|---|---|---|---|---|
| Persistencia | 0,2700 | 0,3500 | 0,5679 | 0,2747 | 0,3656 |
| RF 500 | 0,4042 | 0,3064 | 0,3679 | 0,3710 | 0,3624 |
| Tendencia (sola) | 0,1921 | 0,2752 | 0,3330 | 0,3047 | **0,2763** |
| Tendencia + exógenas | 0,2555 | 0,2504 | 0,3343 | 0,3086 | 0,2872 |

Lo robusto es la tendencia: sumar exógenas ayuda en el bloque oficial pero **empeora en promedio**.
H3 sigue rechazada según la regla declarada de antemano.

---

## 8. La regla de decisión (y por qué no la cambiamos)

Del `OBJETIVOS_del_proyecto.md:95-98`:

> Un modelo solo se considera útil si su RMSE es inferior al del baseline. Si ningún modelo lo
> supera, el objetivo se responde igualmente con un resultado negativo, y ese resultado se documenta
> igual que uno favorable. No se modifica la definición de baseline después de ver los resultados.

Cambiar el baseline, usar la validación cruzada como criterio o sumar el modelo de tendencia a la
comparación **después** de haber visto los números sería *p-hacking*: elegir la regla que favorece al
resultado. Por eso mantenemos el veredicto y reportamos el resto como análisis complementario.

---

## 9. Cómo reproducirlo

```bash
python modelos.py
```

Imprime las 8 secciones con todos los números de este documento. Para verlo en la interfaz:

```bash
Levantar.bat
```

Luego entrar a las páginas **"Objetivo 5 · Modelos predictivos"** y
**"Objetivo 6 · Evaluacion vs baseline"**. En la página 5 hay sliders exploratorios (año de corte y
cantidad de árboles): si se mueven, la app avisa que se está viendo un **escenario exploratorio**; los
números oficiales son siempre con corte 2009 y 500 árboles. La página 6 usa siempre la configuración
oficial.

Dependencias: `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`, `plotly`, `streamlit`
(`requirements.txt`).

---

## 10. Dónde está cada cosa

| Qué | Dónde |
|---|---|
| Definición de los objetivos 5 y 6 y regla de decisión | `OBJETIVOS_del_proyecto.md:75-98` |
| Script reproducible con todos los números | `modelos.py` (`cargar_datos` :76, `ols_ajustar` :87, `main` :211, sección 8 :471) |
| Página visual del objetivo 5 | `app.py:2402` |
| Página visual del objetivo 6 | `app.py:2888` |
| Helpers de modelos (OLS, métricas, CV) | `app.py:462-569` |
| Resultados y hipótesis | `README.md` y `ESTADO_PROYECTO.md` |
| Informe metodológico | `Trabajo integrador y plan de proyecto/Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx` (secciones 7.5, 7.6, 9.2, 9.3 y notas finales) |

---

## 11. Glosario express

| Término | Significado |
|---|---|
| **RMSE** | Raíz del error cuadrático medio, en °C. Penaliza más los errores grandes. Es nuestra métrica principal |
| **MAE** | Error absoluto medio, en °C. Más intuitivo: error típico sin penalizar tanto los outliers |
| **R²** | Mejora sobre predecir siempre la media. Negativo = peor que la media |
| **Baseline** | Pronóstico trivial de referencia. Acá: repetir el valor del año anterior |
| **HAC / Newey-West** | Corrección de errores estándar para que los p-valores sean válidos aunque haya dependencia en el tiempo |
| **OOB** | Error estimado con las muestras que cada árbol no usó al entrenar (validación interna del Random Forest) |
| **Importancia por permutación** | Cuánto empeora el error al desordenar una variable: mide si realmente aporta en prueba |
| **Gini** | Importancia interna del bosque; tiende a inflar variables continuas con muchos valores distintos |
| **VIF** | Mide multicolinealidad entre predictoras; cerca de 1 es bueno |
| **Overfitting** | Ajustar el ruido del entrenamiento en vez de la señal; se detecta con OOB negativo y permutación nula |

---

## 12. Guion sugerido para exponer (≈2 minutos)

1. *"Nos tocó los objetivos 5 y 6: predecir la anomalía de temperatura con PBI, emisiones y lluvia, y
   ver si eso servía para algo."*
2. *"Usamos dos modelos: una regresión lineal múltiple, interpretable, y un Random Forest de 500
   árboles, para capturar posibles no linealidades. Entrenamos con 1961–2009 y evaluamos con
   2010–2024, sin mezclar años."*
3. *"La regla estaba fijada antes: un modelo sirve sólo si baja el RMSE de repetir el valor del año
   anterior."*
4. *"Resultado: persistencia 0,3776; regresión 0,3919; Random Forest 0,4192. Ninguno gana, y el R² es
   negativo."*
5. *"¿Por qué? Porque la aparente influencia de las emisiones es una correlación espuria: comparte
   tendencia con la temperatura y desaparece al detrendizar o al salir de muestra. La permutación en
   prueba lo confirma: desordenar GEI no empeora el error. El bosque, además, sobreajusta."*
6. *"Hicimos una revisión: errores HAC, un baseline alternativo y un modelo con tendencia. La tendencia
   sí baja el RMSE a 0,3326, pero no la sumamos a la decisión porque se propuso después de ver
   resultados y la mejora viene de extrapolar el calentamiento, no del PBI ni del GEI."*
7. *"Conclusión: el resultado negativo es el hallazgo. Con los datos disponibles no se puede predecir
   mejor que un pronóstico trivial, y lo demostramos con la validación y la regla correctas."*

---

## 13. Preguntas frecuentes y respuestas cortas

**¿Por qué no probaron ARIMA o redes neuronales?**
Con 64 observaciones anuales, modelos con muchos parámetros sobreajustan. El informe (sección 8.7)
los evaluó y los descartó por falta de datos; la prioridad fue un procedimiento correcto y auditable.

**¿Por qué el Random Forest es peor que la regresión lineal?**
Porque no hay señal no lineal que aprovechar: con 49 filas y árboles sin podar, memoriza el
entrenamiento (OOB R² = −0,1883) y su importancia Gini no se confirma en prueba.

**¿Si el GEI es significativo, por qué dicen que no sirve?**
Porque la significancia es dentro del entrenamiento y está dominada por la tendencia compartida.
Fuera de muestra, permutar GEI *reduce* el RMSE en 0,0090. Significancia ≠ capacidad predictiva.

**¿Por qué no cambian el baseline si el modelo con tendencia da 0,3326?**
Porque la regla se fijó antes de ver resultados y cambiarla sería elegir el criterio después. Se
reporta como análisis complementario, con su propia sensibilidad, y H3 sigue rechazada.

**¿Entonces el proyecto "falló"?**
No. Los objetivos 1 a 4 ya mostraban que la correlación era espuria y que la relación era débil y
estable. El resultado negativo es la consecuencia lógica y verificable de esos hallazgos.
