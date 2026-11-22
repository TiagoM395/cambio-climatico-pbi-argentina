# Estado del proyecto — Snapshot 22/11/2026

Archivo actualizado el **22/11/2026**. Describe el estado final de la carpeta del proyecto: qué está
hecho, qué archivos existen, qué datos hay, en qué estado está el repositorio Git y qué queda para la
entrega.

> Cambios principales respecto del snapshot del 19/10: se corrigieron los objetivos 5 y 6 (errores
> robustos HAC, baseline alternativo y análisis complementario con tendencia), se sincronizaron el
> informe `.docx`, el plan y el `README.md`, se crearon `README5y6.md`, `objetivos5y6.pdf` y el
> esqueleto `Presentacion_oral.pptx` para los 6 objetivos, y el PR #6 fue mergeado en `main`.
>
> El script reproducible `modelos.py` y la app Streamlit cubren los 6 objetivos (1 a 6). Ya no queda
> ningún objetivo fuera de la interfaz ni de la documentación.

---

## 1. Identificación

| Campo | Valor |
|---|---|
| Proyecto | Cambio climático en Argentina y su relación con el crecimiento económico (PBI) |
| Institución | Instituto 57 — Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial |
| Carrera / cátedra | Análisis y Exploración de Datos |
| Autores | Elias Campos · Tiago Maidana · Rodrigo Bulggiani · Romina Guzman |
| Docente | Ibarra Martín |
| Comisión | 2° año, grupo 6 |
| Metodología | CRISP-DM |
| Período analizado | 1961–2024 (64 observaciones anuales) |
| Inicio | 14/09/2026 |
| Entrega | 30/11/2026 |
| Duración estimada | 11 semanas |
| Semana actual | **Semana 11 de 11 — cierre para la entrega del 30/11/2026** |

**Pregunta principal:** ¿Existe una relación entre el crecimiento económico (PBI) y el cambio climático
en Argentina entre 1961 y 2024, y es posible predecir la evolución de la temperatura a partir de las
variables económicas y climáticas?

---

## 2. Resumen ejecutivo

**Estado:** el proyecto tiene el **100 % de los datos descargados y procesados**, el **informe final
redactado**, **repositorio Git activo** con historial de commits y una **interfaz web que cubre los
seis objetivos**. Los objetivos 1 a 6 ya tienen resultados escritos y verificados.

**Lo que ya está hecho:**

- Descarga y verificación de 13 fuentes oficiales y organismos internacionales.
- Construcción de 4 datasets processed (nacional, provincial, clima anual, tendencias).
- Análisis de los 6 objetivos específicos, con resultados numéricos documentados.
- Informe final y plan de proyecto en `.docx`, actualizados el 22/11.
- Script reproducible `modelos.py` para los objetivos 5 y 6.
- App Streamlit con los **seis objetivos (1 a 6)**, lista para proyectar.
- Repositorio Git con remoto en GitHub, ramas por integrante y 4 PRs mergeados.

**Lo que falta:**

- Completar el diseño visual y ensayar la presentación oral de 10–15 minutos; el esqueleto con
  contenido de los 6 objetivos ya está en `Presentacion_oral.pptx`.
- Nada bloqueante: el cronograma, el informe, el plan, el `README.md` y el repositorio están
  sincronizados (ver secciones 9 y 11).

---

## 3. Estructura de carpetas

```
C:\Cambio climatico trabajo\
│
├── app.py                                   ← aplicación Streamlit (los 6 objetivos, ~3.100 líneas)
├── modelos.py                               ← script reproducible objetivos 5 y 6 (~536 líneas)
├── Levantar.bat                             ← doble clic para levantar la app
├── requirements.txt                         ← 7 librerías
├── README.md                                ← guía de uso (~478 líneas)
├── ESTADO_PROYECTO.md                       ← este archivo
├── .gitignore                               ← exclusiones (venv, cachés, backups, notas)
│
├── OBJETIVOS_del_proyecto.md / .pdf         ← definición de los 6 objetivos
├── README5y6.md                             ← guía de defensa de los objetivos 5 y 6
├── objetivos5y6.pdf                         ← versión PDF de esa guía
├── Presentacion_oral.pptx                   ← esqueleto de 10–15 min, cubre los 6 objetivos
├── Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx   ← material de cátedra
│
├── .streamlit/
│   └── config.toml                          ← tema oscuro azul noche, acento celeste
│
├── data/
│   ├── sources.csv                          ← ficha de las 13 fuentes (14 columnas)
│   ├── raw/                                 ← 12 ítems originales (incluye shapefile)
│   │   ├── geo_ign_provincias/               ← shapefile IGN (7 archivos)
│   │   └── ... (11 archivos de datos)
│   └── processed/                           ← 4 datasets derivados
│       ├── dataset_nacional.csv
│       ├── dataset_provincial.csv
│       ├── provincias_clima_anual.csv
│       └── provincias_tendencia.csv
│
├── Trabajo integrador y plan de proyecto/   ← documentos finales vigentes
│   ├── Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx
│   └── Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx
│
└── __pycache__/                             ← caché de Python (ignorada por Git)
```

**Sí hay repositorio Git** (ver sección 10). No hay `.venv` dentro de la carpeta del proyecto ni una
suite de tests automatizada.

---

## 4. Inventario de archivos

### 4.1 Código y configuración

| Archivo | Fecha | Tamaño | Qué es |
|---|---|---|---|
| `app.py` | 22/11 | ~152 KB | App Streamlit: los 6 objetivos (~3.312 líneas) |
| `modelos.py` | 22/11 | ~20 KB | Script reproducible de los objetivos 5 y 6 (536 líneas) |
| `Levantar.bat` | 12/10 19:40 | 4,4 KB | Script de arranque en Windows |
| `requirements.txt` | 19/10 | 106 B | streamlit, pandas, numpy, scipy, statsmodels, plotly, scikit-learn |
| `.streamlit/config.toml` | 12/10 19:26 | 705 B | Tema oscuro, `primaryColor #5B9BD5`, headless |
| `README.md` | 22/11 | ~24 KB | Guía de instalación y uso (~478 líneas) |
| `README5y6.md` | 22/11 | ~16 KB | Guía de defensa de los objetivos 5 y 6 (315 líneas) |
| `.gitignore` | 17/10 17:29 | 1,0 KB | Ignora venv, cachés y `_backup_*` |

> El `README.md` está sincronizado con este snapshot: navegación de los 6 objetivos, estado de Git y
> métricas de los objetivos 5 y 6.

### 4.2 Documentos

| Archivo | Fecha | Tamaño | Contenido |
|---|---|---|---|
| `Trabajo integrador y plan de proyecto\Trabajo_Integrador_..._CORREGIDO.docx` | **22/11** | ~65,6 KB | **Informe final vigente** (métricas y HAC sincronizados) |
| `Trabajo integrador y plan de proyecto\Plan_de_Proyecto_..._CORREGIDO.docx` | **22/11** | ~60,7 KB | Plan de proyecto vigente (cronograma actualizado) |
| `Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx` | 13/10 17:14 | 64,8 KB | Material de cátedra: fases CRISP-DM |
| `OBJETIVOS_del_proyecto.md` / `.pdf` | 16/10 14:22 | 6,3 KB / 94 KB | Definición de los 6 objetivos |
| `README5y6.md` | 22/11 | — | Guía de defensa de los objetivos 5 y 6 |
| `objetivos5y6.pdf` | 22/11 | 325 KB | Versión PDF de esa guía |
| `Presentacion_oral.pptx` | 22/11 | ~66 KB | Esqueleto de presentación de los 6 objetivos (10–15 min) |

> Ya no hay `.docx` en la raíz: los dos documentos finales quedaron solo dentro de
> `Trabajo integrador y plan de proyecto\`, en su versión del 22/11.

### 4.3 Datos

**`data/raw/` — originales, sin modificar**

| Archivo | Tamaño | Organismo |
|---|---|---|
| `magyp_estimaciones_agricolas.csv` | 15 MB | Secretaría de Agricultura |
| `owid_co2_data_mundial.csv` | 33 MB | Global Carbon Project / OWID |
| `geo_ign_provincias/` (shapefile, 7 archivos) | 33 MB | Instituto Geográfico Nacional |
| `nasa_power_clima_mensual_provincial.csv` | 656 KB | NASA POWER |
| `cepal_pbg_provincial.xlsx` | 459 KB | CEPAL |
| `inventario-nacional-gei-emisiones_hasta_2022.xlsx` | 591 KB | Secretaría de Ambiente |
| `desagregacion-provincial_hasta_2022.xlsx` | 1,4 MB | Secretaría de Ambiente |
| `indec_poblacion_provincial_2010_2040.xls` | 207 KB | INDEC |
| `owid_co2_data_argentina.csv` | 180 KB | Global Carbon Project / OWID |
| `nasa_power_temperatura_provincial.csv` | 44 KB | NASA POWER |
| `ciam_precipitacion_estaciones.csv` | 3,4 KB | SMN / CIAM |
| `ciam_anomalia_temp_precip_nacional.csv` | 1,6 KB | SMN / CIAM |
| `banco_mundial_pbi_crecimiento.csv` | 1,6 KB | Banco Mundial |

**`data/processed/` — derivados, listos para analizar**

| Archivo | Filas | Cols | Cobertura |
|---|---|---|---|
| `dataset_nacional.csv` | 65 | 12 | 1961–2025, Argentina |
| `dataset_provincial.csv` | 1.080 | 9 | provincial, 2004–2024 |
| `provincias_clima_anual.csv` | 1.032 | 5 | provincial, clima mensual agregado |
| `provincias_tendencia.csv` | 24 | 13 | una fila por jurisdicción |
| `../sources.csv` | 13 | 14 | ficha de fuentes |

Los datasets procesados no cambiaron desde el 23–24/09, salvo `dataset_nacional.csv` (13/10).

---

## 5. Detalle de `app.py`

**~3.312 líneas**, ~152 KB. Entry point único. Contiene:

| Bloque | Líneas aprox. | Qué hace |
|---|---|---|
| Configuración y CSS | 1–233 | Rutas, período 1961–2024, cortes 1992/2009, tema oscuro azul noche, paleta celeste |
| Carga de datos | 234–252 | `@st.cache_data` + renombrado de columnas + filtro 1961–2024 |
| Funciones estadísticas | 255–414 | `matriz_correlacion`, `pares_correlacion`, `vif`, `tendencia`, `atipicos_iqr`, `detrendizar`, `matriz_r_p`, `fisher_z`, `regresion_lineal` |
| Helpers de modelos | 456–560 | `_ols_core`, `ajustar_ols`, `metricas_modelo`, `cv_rmse`, `cv_persistencia` |
| Helpers gráficos | 560–650 | `_hex_a`, `plantilla_grafico`, `tarjeta`, `que_demuestra`, `fuerza` |
| Sidebar | ~600 | Navegación (7 secciones) + datos crudos en expander |
| Página Inicio | — | Encuadre, pregunta, variables, hallazgos de los 6 objetivos, vista rápida |
| Objetivo 1 | — | Descripción de cada variable (6 subsecciones) |
| Objetivo 2 | — | Relación PBI ↔ clima (7 subsecciones) |
| Objetivo 3 | — | Multicolinealidad (6 subsecciones) |
| Objetivo 4 | — | Estabilidad temporal (5 subsecciones) |
| Objetivo 5 | — | Modelos predictivos (8 subsecciones) |
| Objetivo 6 | — | Evaluación frente al baseline (7 subsecciones) |
| Metodología | — | Datos, procedimientos, estructura, limitaciones, reproducir |

**Navegación (menú lateral):** Inicio · Objetivo 1 · Objetivo 2 · Objetivo 3 · Objetivo 4 ·
Objetivo 5 · Objetivo 6 · Metodología

**Subsecciones del objetivo 1:** informe de tendencia · evolución y recta · promedio por década y
distribución · magnitud del cambio año a año · resumen de atípicos · conclusión.

**Subsecciones del objetivo 2:** por qué quitar la tendencia · matriz de Pearson · originales vs sin
tendencia · dispersión de un par · robustez con primeras diferencias · crecimiento contra crecimiento ·
conclusión.

**Subsecciones del objetivo 3:** serie de emisiones · matriz de correlación · tests por par · VIF ·
dispersión · robustez con 3 series · conclusión.

**Subsecciones del objetivo 4:** corte temporal · comparación de correlaciones · dispersión e IC 95% ·
modelo con interacción · conclusión.

**Subsecciones del objetivo 5:** corte temporal · regresión lineal múltiple · diagnóstico de supuestos ·
Random Forest · baseline de persistencia · comparación sobre prueba · predicción vs observado ·
robustez (CV temporal) · conclusión.

**Subsecciones del objetivo 6:** regla de decisión · métricas con configuración oficial · tabla
comparativa · desglose del error por año · por qué gana el baseline · veredicto H3 · conclusión
(fase Evaluation).

Los **seis objetivos ya están en la app**; el objetivo 5 y el 6 además tienen su script reproducible
en `modelos.py`.

---

## 6. El dataset nacional

`data/processed/dataset_nacional.csv` — 65 filas (1961–2025), 12 columnas.
La app usa **1961–2024** porque el año 2025 está incompleto (sin GEI ni PBI per cápita).

| Columna normalizada | Columna original | Tipo | Nulos |
|---|---|---|---|
| `anio` | año | int | 0 |
| `jurisdiccion` | jurisdiccion | str | 0 |
| `tipo_jurisdiccion` | tipo_jurisdiccion | str | 0 |
| `temp` | anomalia_temperatura | °C | 0 |
| `lluvia` | anomalia_precipitacion_pct | % | 0 |
| `gei` | emisiones_gei_no_uc_co2eq | MtCO₂eq | 1 |
| `gei_inventario` | emisiones_gei_co2eq | MtCO₂eq | 52 |
| `co2` | emisiones_co2_fosil | Mt | 1 |
| `pbi` | pbi_crecimiento_pct | % anual | 0 |
| `poblacion` | poblacion | personas | 1 |
| `pib_per_capita` | pib_per_capita | USD int. 2011 | 3 |
| `pibpc` | pib_per_capita_crecimiento_pct | % anual | 3 |

**Nota:** el inventario oficial de GEI (52 nulos) solo cubre 1990–2022, por eso la variable principal
es `emisiones_gei_no_uc_co2eq` (Global Carbon Project), que cubre los 64 años.

---

## 7. Objetivos y resultados

### Objetivo 1 — Descripción de cada variable ✅ *(en la app)*
Gráfico de línea + regresión lineal (con Durbin-Watson y p robusto HAC) + atípicos por IQR.

- Temperatura: tendencia **+0,013 °C/año** (p < 0,001, R² = 0,42, DW = 1,90). Año más cálido: **2023 (+0,83 °C)**.
- Emisiones GEI: **+2,46 MtCO₂eq/año** (R² = 0,94, DW = 0,43 → autocorrelación fuerte).
- PBI y lluvia: sin tendencia significativa (p = 0,356 y p = 0,949).
- 1993–2024 es más cálido que 1961–1992: **+0,41 °C** (medias −0,32 vs +0,09 °C).
- Ningún año supera el criterio 1,5 × IQR; los atípicos aparecen en la **variación año a año** (crisis y rebotes).

### Objetivo 2 — Relación PBI ↔ clima ✅ *(en la app)*
Matriz de Pearson con p-valor + análisis detrendizado + primeras diferencias + Spearman.

| Par | En niveles | Sin tendencia | p (sin tend.) |
|---|---|---|---|
| Temp ↔ GEI | **+0,600** | −0,165 | 0,194 |
| Temp ↔ PBI | −0,156 | −0,105 | 0,407 |
| Temp ↔ Lluvia | −0,162 | −0,206 | 0,102 |
| **PBI ↔ GEI** | −0,048 | **+0,283** | **0,023** |

- El PBI **no** se relaciona con la temperatura (ni en niveles ni detrendizado).
- Pero **PBI ↔ GEI aparece sin tendencia** y se refuerza en primeras diferencias (**+0,431**, p < 0,001).
- **Conclusión actual de la app:** H1 no se confirma respecto de la temperatura; el PBI se relaciona con
  el cambio climático **a través de las emisiones** (cuando la economía crece, Argentina emite más).

### Objetivo 3 — Multicolinealidad ✅ *(en la app)*
| Par | r | p |
|---|---|---|
| PBI ↔ GEI | −0,048 | 0,709 |
| PBI ↔ Lluvia | −0,150 | 0,236 |
| GEI ↔ Lluvia | +0,001 | 0,996 |

VIF: PBI **1,025** · Lluvia 1,023 · GEI 1,002 → **no hay multicolinealidad**.
Robustez: con CO₂ fósil el máximo es 1,026; con el inventario oficial (n = 13) llega a 1,12. En ningún
caso se acerca al umbral de 5.

> Nota: la función `vif()` estuvo mal etiquetada en una revisión temprana y se corrigió; la conclusión
> no cambia.

### Objetivo 4 — Estabilidad temporal ✅ *(en la app)*
| Período | r | p |
|---|---|---|
| 1961–1992 (n = 32) | −0,169 | 0,355 |
| 1993–2024 (n = 32) | −0,168 | 0,358 |

- Test de Fisher: p ≈ **0,997** → diferencia compatible con el azar.
- Modelo `temp ~ pbi + post + pbi:post`: coeficiente `pbi:post` = **+0,0002** (p = 0,988).
- **La relación PBI–temperatura no cambió** en 64 años.

> Nota: se corrigieron un bug de etiquetado de leyenda, un semáforo de colores y erratas en la
> conclusión.

### Objetivo 5 — Modelos predictivos ✅ *(en la app y en `modelos.py`)*
Regresión Lineal y Random Forest, partición temporal 1961–2009 / 2010–2024. Diagnósticos (Shapiro-Wilk,
Breusch-Pagan, Durbin-Watson, VIF), p-valores robustos HAC (3 rezagos), importancia Gini y por
permutación.

### Objetivo 6 — Evaluación vs baseline ✅ *(en la app y en `modelos.py`)*
| Modelo | RMSE |
|---|---|
| Baseline naive (persistencia) | **0,3776** |
| Regresión Lineal | 0,3919 |
| Random Forest | 0,4192 |

**Ningún modelo supera al baseline.** R² negativo en el conjunto de prueba.

### Veredicto de hipótesis

| Hipótesis | Resultado | Veredicto |
|---|---|---|
| H1 — PBI y GEI correlacionan con temperatura | La correlación aparente desaparece al detrendar; el vínculo PBI–GEI sí sobrevive | **Rechazada** (respecto de la temperatura) |
| H2 — La relación se mantiene o fortalece | r estable, p = 0,99 | **Rechazada** |
| H3 — Un modelo supera al baseline | Ninguno lo supera | **Rechazada** |

---

## 8. Qué queremos predecir (objetivos 5 y 6)

**En una frase:** queremos predecir la **anomalía de temperatura media anual de Argentina** (en °C)
para un año del período, a partir de las variables económicas y climáticas de ese mismo año.

| Elemento | Definición |
|---|---|
| **Variable respuesta (`y`)** | Anomalía de temperatura media anual de Argentina — columna `temp` (`anomalia_temperatura`), en °C, fuente CIAM / SMN |
| **Predictoras (`X`)** | Crecimiento del PBI (`pbi`, % anual, Banco Mundial) · Emisiones de GEI (`gei`, MtCO₂eq, Global Carbon Project / OWID) · Anomalía de precipitación (`lluvia`, %, CIAM / SMN) |
| **Variable de tiempo** | Año |
| **Unidad de análisis** | País (Argentina), frecuencia anual |
| **Período** | 1961–2024 (64 observaciones) |

**Esquema de validación:** partición **temporal**, nunca aleatoria (se entrena con los años más
tempranos y se evalúa con los más recientes).

| Conjunto | Años | Observaciones |
|---|---|---|
| Entrenamiento | 1961–2009 | 49 |
| Prueba | 2010–2024 | 15 |

**Modelos a comparar:**

1. **Regresión Lineal Múltiple** — `temp ~ pbi + gei + lluvia`.
2. **Random Forest Regressor** — las mismas predictoras, sin supuestos de linealidad.
3. **Baseline naive de persistencia** — predice que la temperatura de este año es la del año anterior
   (`temp_t = temp_{t-1}`).

**Métrica y regla de decisión:** RMSE (y MAE, R²) sobre el bloque de prueba. Un modelo sirve **solo si
su RMSE es menor que el del baseline**. La definición del baseline no se modifica después de ver los
resultados.

**Resultado obtenido (en el informe):**

| Modelo | RMSE |
|---|---|
| Baseline naive (persistencia) | **0,3776** |
| Regresión Lineal | 0,3919 |
| Random Forest | 0,4192 |

**Ninguno de los dos modelos predefinidos supera al baseline.** Es coherente con lo hallado en el
objetivo 2: la temperatura está dominada por su propia tendencia, y el PBI y la lluvia no explican su
variación anual. Por eso el proyecto **sí define qué predecir** (la temperatura), pero su hallazgo es
que las variables económicas **no alcanzan para predecirla mejor que repetir el último valor**.

> **Actualización de la revisión (20/11/2026).** La inferencia del OLS usa errores robustos HAC
> (Newey-West, 3 rezagos) porque Shapiro-Wilk rechaza normalidad (p = 0,0188). Se agregaron dos
> controles que **no alteran la regla ni el veredicto H3**: el baseline alternativo «último valor
> constante» (previsto en el informe) da RMSE 0,2685, y un modelo con tendencia
> `temp ~ anio + pbi + gei + lluvia` da 0,3326 en el bloque oficial. Este último no estaba en la
> comparación predefinida: la mejora proviene de extrapolar la tendencia (r(año, GEI) = 0,975 en
> entrenamiento; al controlarla el GEI pasa a p HAC = 0,698), no de las variables económicas, y su R²
> de prueba sigue siendo negativo (−0,64). En 4 cortes móviles la tendencia sola promedia 0,2763
> frente a 0,3656 de la persistencia; tendencia + exógenas, 0,2872. Ambos análisis están reproducidos
> en `modelos.py` (sección 8) y en la app (objetivo 6, sección 7).

> **Alcance:** los objetivos 5 y 6 ya están implementados **en la app** (páginas "Objetivo 5 · Modelos
> predictivos" y "Objetivo 6 · Evaluacion vs baseline") y además tienen un **script reproducible**
> (`modelos.py`) que regenera todos sus números desde la consola.

---

## 9. Cronograma según el plan de proyecto

| Etapa CRISP-DM | Fechas | Estado en el plan | Estado real |
|---|---|---|---|
| Business Understanding | 14–20/09/2026 | Completada | Completada |
| Data Understanding | 21/09–11/10/2026 | Completada | Completada |
| Data Preparation | 12–25/10/2026 | En curso | Completada |
| Modeling | 26/10–01/11/2026 | Pendiente | **Ejecutada** (objetivos 1–5) |
| Evaluation | 02–08/11/2026 | Pendiente | **Ejecutada** (objetivo 6) |
| Deployment | 09–30/11/2026 | Pendiente | En curso (interfaz ya lista) |

> **Resuelto:** el cronograma del plan `.docx` ya refleja Modeling y Evaluation como «Ejecutada». Los
> objetivos 1 a 6 tienen resultados, están implementados en la app y los objetivos 5 y 6 también en
> `modelos.py`.

---

## 10. Repositorio Git

**Ya está inicializado** (el snapshot anterior decía que no existía).

| Dato | Valor |
|---|---|
| Remoto | `https://github.com/TiagoM395/cambio-climatico-pbi-argentina.git` |
| Rama de trabajo | `romy` → PR #6 mergeado en `main` (`6549de1`) |
| Ramas | `main`, `Tiago`, `elias`, `romy` (+ remotas `rodrigo`, `Romy`) |
| PRs mergeados | 4 (los últimos: #5 y #6) |
| Nota local | La rama `main` local está detrás de `origin/main`; actualizar con `git pull` |
| `.gitignore` | Ignora venv, cachés y `_backup_*` |

**Últimos commits relevantes:**

- `da30b38` — colores del Test de Fisher en el objetivo 4 + `.gitignore`.
- `269f297` — corrección del cálculo de VIF en el objetivo 3.
- `e7bcdcb` — Durbin-Watson, p robusto (HAC) y Spearman en los objetivos 1 y 2.
- `57ba439` / `878fc3b` — el objetivo 2 responde la pregunta central; cambios del PBI y la lluvia en puntos porcentuales.
- `1884ffc` — se agregaron los objetivos 1 y 2 a la app.

---

## 11. Duplicados, backups y notas de trabajo

- **Documentos finales:** quedan solo **2 `.docx`** vigentes (informe y plan) dentro de
  `Trabajo integrador y plan de proyecto\`.
- **Backups:** los `_backup_*.docx` se movieron fuera del repo; no quedan respaldos en la carpeta.
- **Notas de trabajo:** ya no se hace referencia a `analisis_objetivo4.md`, `error_vif_objetivo3.md`
  ni `EXPLICACION_OBJETIVOS_3_Y_4.md`; su contenido quedó consolidado en el informe, el plan,
  `README5y6.md` y `objetivos5y6.pdf`.

---

## 12. Cómo levantar la app

```bash
# Opción rápida
doble clic en Levantar.bat

# Opción manual
pip install -r requirements.txt
streamlit run app.py
```

http://localhost:8501 · El `.bat` detecta `.venv`, instala lo que falte y salta de puerto si el 8501
está ocupado.

---

## 13. Pendientes

- [x] Actualizar el cronograma del plan de proyecto (sección 9)
- [x] Armar el esqueleto de la presentación oral de 10–15 minutos (`Presentacion_oral.pptx`). Falta
      completar el diseño visual y ensayar.
- [x] Sincronizar `README.md` con el estado real (navegación, líneas de `app.py`, Git)
- [x] Limpiar duplicados y backups (sección 11)
- [x] Inicializar Git para versionar el código
- [x] Agregar los objetivos 1 y 2 a la app
- [x] Crear el script reproducible de los objetivos 5 y 6 (`modelos.py`)
- [x] Extender la app con los objetivos 5 y 6 (modelos y comparación con baseline)

---

## 14. Últimas versiones de datos clave

| Dato | Valor |
|---|---|
| Filas dataset nacional | 65 (1961–2025), la app usa 64 (1961–2024) |
| Observaciones completas | 64 años |
| **Variable a predecir** | **Anomalía de temperatura media anual de Argentina (°C)** |
| Predictoras del modelo | PBI (crecimiento %), GEI (MtCO₂eq), lluvia (anomalía %) |
| Partición de modelado | Entrenamiento 1961–2009 · Prueba 2010–2024 |
| Corte de mitades | 1992 |
| Fuentes documentadas | 13 |
| Objetivos específicos | 6 |
| Objetivos implementados en la app | 6 (1, 2, 3, 4, 5 y 6) |
| Líneas de `app.py` | ~3.100 |
| Líneas de `modelos.py` | 450 |
| Commits en Git | 11 |
| Líneas de trabajo futuro | 6 (ARIMA/Prophet, variables omitidas, rezagos, inventarios, provincial, GAM) |
