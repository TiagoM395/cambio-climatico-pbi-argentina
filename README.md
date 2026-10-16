# Cambio climático y PBI en Argentina (1961–2024)

Trabajo práctico de **Análisis y Exploración de Datos** sobre la relación entre el cambio climático
y el crecimiento económico en Argentina, desarrollado con metodología **CRISP-DM** de principio a fin.

La pregunta que guía el proyecto:

> ¿Existe una relación entre el crecimiento económico (PBI) y el cambio climático en Argentina entre
> 1961 y 2024, y es posible predecir la evolución de la temperatura a partir de las variables
> económicas y climáticas?

---

## Índice

1. [Equipo e institución](#equipo-e-institución)
2. [Qué hace el proyecto](#qué-hace-el-proyecto)
3. [Instalación](#instalación)
4. [Cómo levantar la aplicación](#cómo-levantar-la-aplicación)
5. [Estructura del proyecto](#estructura-del-proyecto)
6. [Los datos](#los-datos)
7. [Variables del estudio](#variables-del-estudio)
8. [Objetivos específicos](#objetivos-específicos)
9. [Resultados](#resultados)
10. [La aplicación](#la-aplicación)
11. [Limitaciones](#limitaciones)
12. [Solución de problemas](#solución-de-problemas)
13. [Estado del proyecto](#estado-del-proyecto)

---

## Equipo e institución

| Campo | Valor |
|---|---|
| **Proyecto** | Cambio climático en Argentina y su relación con el crecimiento económico (PBI) |
| **Institución** | Instituto 57 — Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial |
| **Cátedra** | Análisis y Exploración de Datos |
| **Curso** | 2.º año — grupo 6 |
| **Docente** | Ibarra Martín |
| **Autores** | Elías Campos · Tiago Maidana · Rodrigo Bulggiani · Romina Guzmán |
| **Metodología** | CRISP-DM |
| **Período analizado** | 1961–2024 (64 observaciones anuales) |
| **Inicio** | 14/09/2026 |
| **Entrega** | 30/11/2026 |

---

## Qué hace el proyecto

El proyecto recorre el ciclo **CRISP-DM** completo sobre un corpus de datos de clima y economía
argentinos. En concreto:

- **Reúne 13 fuentes oficiales** de organismos del Estado y de organismos internacionales
  (CIAM/SMN, Banco Mundial, CEPAL, INDEC, NASA POWER, IGN, Global Carbon Project, Secretaría de
  Agricultura, etc.) y documenta cada una en `data/sources.csv`.
- **Construye datasets derivados** combinando esas fuentes en cuatro tablas de análisis: una
  nacional anual (1961–2025) y tres provinciales.
- **Resuelve los 6 objetivos específicos** de la asignatura, aplicando técnicas de análisis
  exploratorio, correlación, multicolinealidad, estabilidad temporal y modelado predictivo.
- **Publica una interfaz web** en Streamlit con los objetivos, lista para proyectar en la
  defensa oral.

La conclusión central del trabajo es **negativa y está documentada como tal**: las correlaciones
aparentes entre PBI, emisiones y temperatura **desaparecen al detrendizar**, ningún modelo
predictivo supera al baseline naive, y la relación PBI–temperatura no cambió en 64 años. El valor
del proyecto está en haberlo demostrado con los procedimientos correctos, no en haber forzado una
relación.

---

## Instalación

### Requisitos

- **Python 3.10 o superior** (probado con 3.14.4)
- Conexión a internet solo la primera vez, para instalar las dependencias

### Dependencias

El proyecto usa 6 librerías, declaradas en `requirements.txt`:

```
streamlit>=1.30
pandas>=2.0
numpy>=1.24
scipy>=1.10
statsmodels>=0.14
plotly>=5.18
```

### Instalación manual

```bash
# Recomendado: usar un entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Cómo levantar la aplicación

### Opción rápida (Windows)

**Doble clic en `Levantar.bat`.** El script hace todo solo:

1. Detecta `.venv` si existe; si no, usa el Python del sistema.
2. Verifica que Python esté instalado y anotará su versión.
3. Comprueba las 6 dependencias y las instala si falta alguna.
4. Verifica que exista `data/processed/dataset_nacional.csv`.
5. Elige un puerto libre: **8501**, o **8502** si el 8501 está ocupado.
6. Abre el navegador y lanza Streamlit.

Para detener la aplicación, `Ctrl+C` en la ventana o cerrar la consola.

### Opción manual

```bash
streamlit run app.py
```

Después, abrir **http://localhost:8501**.

---

## Estructura del proyecto

```
C:\Cambio climatico trabajo\
│
├── app.py                                   ← aplicación Streamlit (1.227 líneas)
├── Levantar.bat                             ← lanzador con doble clic (Windows)
├── requirements.txt                         ← 6 dependencias
├── README.md                                ← este archivo
├── ESTADO_PROYECTO.md                       ← snapshot del estado del trabajo
│
├── .streamlit/
│   └── config.toml                          ← tema oscuro, acento celeste
│
├── data/
│   ├── sources.csv                          ← ficha de las 13 fuentes (14 columnas)
│   ├── raw/                                 ← datos originales, sin modificar
│   │   ├── geo_ign_provincias/               ← shapefile del IGN (7 archivos)
│   │   ├── ciam_anomalia_temp_precip_nacional.csv
│   │   ├── ciam_precipitacion_estaciones.csv
│   │   ├── owid_co2_data_argentina.csv
│   │   ├── owid_co2_data_mundial.csv
│   │   ├── nasa_power_temperatura_provincial.csv
│   │   ├── nasa_power_clima_mensual_provincial.csv
│   │   ├── banco_mundial_pbi_crecimiento.csv
│   │   ├── cepal_pbg_provincial.xlsx
│   │   ├── desagregacion-provincial_hasta_2022.xlsx
│   │   ├── inventario-nacional-gei-emisiones_hasta_2022.xlsx
│   │   ├── indec_poblacion_provincial_2010_2040.xls
│   │   └── magyp_estimaciones_agricolas.csv
│   └── processed/                           ← datasets derivados, listos para analizar
│       ├── dataset_nacional.csv             ← 65 filas · 12 cols · 1961–2025
│       ├── dataset_provincial.csv           ← 1.080 filas · 9 cols · 2004–2024
│       ├── provincias_clima_anual.csv       ← 1.032 filas · 5 cols
│       └── provincias_tendencia.csv         ← 24 filas · 13 cols
│
├── Trabajo integrador y plan de proyecto/
│   ├── Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx
│   ├── Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx
│   ├── OBJETIVOS_del_proyecto.md / .pdf
│   └── OBJETIVOS_WhatsApp.txt
│
├── Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx   ← material de cátedra
└── _backup_*                                ← respaldos de documentos y CSVs
```

> **Nota:** `data/processed/dataset_nacional.csv` es el único archivo que la app necesita para
> funcionar. Si se borra, la aplicación no arranca.

---

## Los datos

### Fuentes consultadas

Las 13 fuentes están documentadas una por una en **`data/sources.csv`**, que registra para cada una:
institución, URL, variable, unidad, cobertura temporal y geográfica, metodología, frecuencia,
fecha de consulta, limitaciones, y los campos *por qué* / *para qué* / *qué cuenta*.

| # | Fuente | Organismo | Cobertura |
|---|---|---|---|
| 1 | Anomalías climáticas anuales (temperatura y precipitación) | CIAM / Secretaría de Ambiente, sobre datos del SMN | 1961–2025, nacional |
| 2 | Precipitación por estación meteorológica | SMN, republicado vía CIAM | 2010–2024, 26 estaciones |
| 3 | Inventario Nacional de GEI — serie nacional | Secretaría de Ambiente (CMNUCC) | 1990–2022, nacional |
| 4 | Inventario Nacional de GEI — desagregación provincial | Secretaría de Ambiente | 2010–2022, 24 jurisdicciones |
| 5 | GEI y CO₂ (`owid-co2-data`) | Global Carbon Project / Our World in Data | 1850–2024, filtrado a Argentina |
| 6 | Crecimiento del PBI (anual %) | Banco Mundial | 1961–2025, nacional |
| 7 | Valor Agregado Bruto provincial (PBG) | CEPAL, sobre INDEC | 2004–2024, 24 jurisdicciones |
| 8 | PBI provincial (serie oficial **discontinuada**) | INDEC | 2006–2017 — no se usa |
| 9 | Temperatura a 2 m por punto geográfico | NASA POWER (MERRA-2) | 1981–2025, 24 puntos |
| 10 | Límites de provincias (shapefile) | Instituto Geográfico Nacional | 24 features, EPSG:4326 |
| 11 | Población y PBI (Maddison Project) | Bolt & van Zanden / Our World in Data | 1850–2024, nacional |
| 12 | Estimaciones agrícolas por cultivo, provincia y departamento | Secretaría de Agricultura | 1969–2025, 23 provincias |
| 13 | Población proyectada por provincia | INDEC | 2010–2040, 24 jurisdicciones |

### Datasets derivados

| Archivo | Filas | Cols | Cobertura | Estado |
|---|---|---|---|---|
| `dataset_nacional.csv` | 65 | 12 | 1961–2025, Argentina | **En uso por la app** |
| `dataset_provincial.csv` | 1.080 | 9 | 2004–2024, provincial | Derivado |
| `provincias_clima_anual.csv` | 1.032 | 5 | Provincial, clima mensual agregado | Derivado |
| `provincias_tendencia.csv` | 24 | 13 | Una fila por jurisdicción | Derivado |

### El dataset nacional

`data/processed/dataset_nacional.csv` tiene 65 filas (1961–2025) y 12 columnas. La app analiza
**1961–2024** porque el año 2025 está incompleto: no tiene registro de GEI ni de PBI per cápita,
e incluirlo recortaría la muestra de forma desigual entre variables.

| Columna normalizada | Columna original | Unidad | Nulos |
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

> **Por qué `gei` y no el inventario oficial.** La serie `emisiones_gei_co2eq` del Inventario Nacional
> solo cubre 1990–2022: 52 nulos sobre 65 filas. Con una muestra de 13 años el test de correlación
> solo detectaría relaciones de |r| ≥ 0,551. Por eso la variable principal es
> `emisiones_gei_no_uc_co2eq` del Global Carbon Project, que cubre los 64 años completos.

---

## Variables del estudio

| Variable | Tipo | Rol en el modelo | Unidad | Fuente |
|---|---|---|---|---|
| Anomalía de temperatura media | Cuantitativa continua | **Variable respuesta** | °C | CIAM / SMN |
| Crecimiento del PBI | Cuantitativa continua | Predictora | % anual | Banco Mundial |
| Emisiones de GEI | Cuantitativa continua | Predictora | MtCO₂eq | Global Carbon Project |
| Anomalía de precipitación | Cuantitativa continua | Predictora | % | CIAM / SMN |
| Año | Cuantitativa discreta | Variable de tiempo | — | — |

---

## Objetivos específicos

| # | Objetivo | Procedimiento | Criterio de aceptación |
|---|---|---|---|
| 1 | **Descripción de cada variable** | Gráfico de línea, regresión lineal sobre el tiempo, atípicos por IQR | Informe de tendencia con coeficiente, error estándar y p-valor |
| 2 | **Relación PBI ↔ clima** | Matriz de correlación de Pearson con p-valor + análisis detrendizado | Matriz completa y contraste explícito entre niveles y residuos |
| 3 | **Multicolinealidad** | Correlación por pares + VIF por variable | Tabla de pares y de VIF, con umbral declarado (VIF < 5 despreciable · 5–10 moderada · ≥ 10 severa) |
| 4 | **Estabilidad temporal** | Comparación de correlaciones por mitades, test de Fisher, modelo con interacción | Comparación con p-valor y coeficiente de interacción |
| 5 | **Modelos predictivos** | Regresión Lineal Múltiple y Random Forest Regressor, con partición **temporal** (nunca aleatoria) | Modelos ajustados, diagnosticados, con importancia de variables |
| 6 | **Evaluación frente al baseline** | RMSE, MAE y R² contra un baseline naive de **persistencia** | Tabla comparativa con regla de decisión explícita |

> **Regla de decisión declarada de antemano:** un modelo solo se considera útil si su RMSE es
> inferior al del baseline. Si ninguno lo supera, el objetivo se responde igual con el resultado
> negativo. La definición de baseline no se modifica después de ver los resultados.

### Hipótesis de trabajo

| | Enunciado | Cómo se pone a prueba |
|---|---|---|
| **H1** | El PBI y los GEI se correlacionan positivamente con la temperatura; la precipitación, de forma negativa | Correlación de Pearson por pares, en niveles y sobre residuos de la tendencia |
| **H2** | Esa relación se mantiene o se fortalece con el tiempo | Correlación por mitades, test de Fisher, coeficiente de interacción periodo × PBI |
| **H3** | Es posible construir un modelo predictivo que supere al baseline naive | RMSE contra el baseline de persistencia |

---

## Resultados

### Objetivo 1 — Tendencias ✅

- Temperatura: tendencia de **+0,013 °C/año** (p < 0,001). Año más cálido: **2023 (+0,83 °C)**.
- 1993–2024 es significativamente más cálido que 1961–1992: **+0,406 °C** (p < 0,001).

### Objetivo 2 — Relación PBI ↔ clima ✅

La correlación en niveles y la detrendizada cuentan historias distintas, y esa es la diferencia
entre un hallazgo y una correlación espuria:

| Relación | En niveles | Detrendizada | p |
|---|---|---|---|
| Temp ↔ GEI | **+0,60** | **−0,16** | 0,19 |
| Temp ↔ PBI | — | **−0,16** | 0,22 |
| Temp ↔ Lluvia | — | **−0,16** | 0,20 |

**Conclusión:** la correlación aparente es **espuria**, atribuible a la tendencia compartida de las
tres series.

### Objetivo 3 — Multicolinealidad ✅ *(implementado en la app)*

| Par | r | p |
|---|---|---|
| PBI ↔ GEI | −0,048 | 0,709 |
| PBI ↔ Lluvia | −0,150 | 0,236 |
| GEI ↔ Lluvia | +0,001 | 0,996 |

**VIF:** PBI 1,000 · GEI 1,025 · Lluvia 1,003 → **no hay multicolinealidad**. El resultado se
mantiene idéntico con las 3 series de emisiones disponibles (GEI total, CO₂ fósil, inventario).

### Objetivo 4 — Estabilidad temporal ✅ *(implementado en la app)*

| Período | r | p |
|---|---|---|
| 1961–1992 (n = 32) | −0,169 | 0,355 |
| 1993–2024 (n = 32) | −0,168 | 0,358 |

- Test de Fisher: p ≈ **0,997** → la diferencia entre mitades es compatible con el azar.
- Modelo `temp ~ pbi + post + pbi:post`: coeficiente `pbi:post` = **+0,0002** (p = 0,988).
- **La relación PBI–temperatura no cambió en 64 años.**

### Objetivo 5 — Modelos predictivos ✅

Regresión Lineal y Random Forest, entrenados con 1961–2009 y evaluados con 2010–2024.

### Objetivo 6 — Evaluación vs. baseline ✅

| Modelo | RMSE |
|---|---|
| **Baseline naive (persistencia)** | **0,378** |
| Regresión Lineal | 0,382 |
| Random Forest | 0,429 |

**Ningún modelo supera al baseline.** El R² en el conjunto de prueba es negativo.

### Veredicto de las hipótesis

| Hipótesis | Resultado | Veredicto |
|---|---|---|
| H1 — PBI y GEI correlacionan con la temperatura | La correlación aparente desaparece al detrendar | **Rechazada** |
| H2 — La relación se mantiene o se fortalece | r estable, p = 0,99 | **Rechazada** |
| H3 — Un modelo supera al baseline | Ninguno lo supera | **Rechazada** |

---

## La aplicación

`app.py` — interfaz Streamlit con tema oscuro y acento celeste, definida en
`.streamlit/config.toml`.

**Navegación (menú lateral):** Inicio · Objetivo 3 · Objetivo 4 · Metodología

| Sección | Contenido |
|---|---|
| **Inicio** | Encuadre, pregunta de investigación, variables, hallazgos principales, gráficos con media móvil y expander con los datos crudos |
| **Objetivo 3 · Multicolinealidad** | Selector de serie de emisiones · matriz de correlación · tests por par · VIF · dispersión · robustez con las 3 series · conclusión |
| **Objetivo 4 · Estabilidad temporal** | Corte temporal 1992 · comparación de correlaciones · dispersión con IC 95% · modelo con interacción · conclusión |
| **Metodología** | Fuentes, procedimientos estadísticos, estructura del proyecto, limitaciones y pasos para reproducir los resultados |

### Estructura del código

| Bloque | Qué hace |
|---|---|
| Configuración | Rutas, período 1961–2024, corte 1992, paleta de colores, etiquetas |
| CSS | Estilos de tarjetas, chips, callouts, tipografía Inter, sidebar |
| Carga de datos | `@st.cache_data`, renombrado de columnas, filtro 1961–2024 |
| Funciones estadísticas | `matriz_correlacion`, `pares_correlacion`, `vif`, `fisher_z`, `regresion_lineal` |
| Helpers gráficos | `_hex_a`, `plantilla_grafico` |
| Presentación | `tarjeta`, `fuerza` (clasifica la magnitud de una correlación) |

---

## Limitaciones

- **Correlación no implica causalidad.** Una correlación débil no descarta relaciones no lineales
  ni efectos con rezago — por ejemplo, de los GEI sobre la temperatura con años de atraso.
- **Agregación nacional.** La temperatura y la lluvia son promedios nacionales que ocultan
  contrastes regionales grandes.
- **Muestra corta.** 64 observaciones anuales es poco para inferencia: los intervalos de confianza
  son amplios y los p-valores hay que leerlos con cautela.
- **Variable económica volátil.** La relación se estima con el crecimiento anual del PBI, una serie
  muy inestable cuyo error de medición puede diluir correlaciones reales.
- **Sin cobertura temporal común total.** El Inventario Nacional de GEI oficial llega solo a 2022 y
  el PBI per cápita del Maddison Project a 2022.

---

## Solución de problemas

| Síntoma | Causa probable | Solución |
|---|---|---|
| `No se encontró Python en este equipo` | Python no está en el PATH | Instalar desde python.org marcando **Add Python to PATH**, reiniciar la terminal |
| `ModuleNotFoundError: streamlit` (u otro) | Faltan dependencias | `pip install -r requirements.txt` |
| `No se encontró el archivo de datos` | Falta el dataset processed | Verificar que exista `data/processed/dataset_nacional.csv` junto a `Levantar.bat` |
| `Address already in use` / puerto ocupado | Otra instancia de Streamlit corriendo | El `.bat` salta automáticamente al 8502; si no, cerrar la otra instancia |
| La app abre en blanco o con estilos raros | Caché de Streamlit desactualizada | Cerrar la app, borrar `~/.streamlit/cache` y relanzar |
| Cambios en los datos no se reflejan | Caché de datos activa | El decorador es `@st.cache_data`; relanzar la app recalcula todo |

---

## Estado del proyecto

**Avance:** semana 5 de 11.

### Hecho

- [x] Descarga y verificación de 13 fuentes oficiales
- [x] Construcción de los 4 datasets processed
- [x] Análisis y resultados de los 6 objetivos específicos
- [x] Informe final en `.docx`
- [x] Plan de proyecto en `.docx`
- [x] App Streamlit con los objetivos 3 y 4, lista para proyectar

### Pendiente

- [ ] Actualizar el cronograma del plan de proyecto (dice "Modeling: pendiente", pero los modelos
      ya se corrieron)
- [ ] Crear scripts reproducibles para los objetivos 1, 2, 5 y 6 (hoy sus resultados solo existen
      dentro del informe; `app.py` cubre el 3 y el 4)
- [ ] Extender la app con los objetivos 5 y 6
- [ ] Armar la presentación oral de 10–15 minutos
- [ ] Limpiar los duplicados y los `_backup_*` antes de la entrega
- [ ] Considerar inicializar Git para versionar el código

### Documentos de referencia

- `Trabajo_Integrador_Cambio_Climatico_Argentina_CORREGIDO.docx` — informe metodológico
- `Plan_de_Proyecto_Cambio_Climatico_Argentina_CORREGIDO.docx` — plan de ejecución
- `ESTADO_PROYECTO.md` — snapshot detallado del estado del trabajo
- `Trabajo integrador y plan de proyecto/OBJETIVOS_del_proyecto.md` — definición de los 6 objetivos
- `Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx` — material de cátedra