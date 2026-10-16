# Estado del proyecto — Snapshot 14/10/2026

Archivo generado el **14/10/2026**. Describe todo lo que hay en la carpeta
`C:\Cambio climatico trabajo` en este momento: qué está hecho, qué archivos existen,
qué datos hay y qué falta.

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
| Semana actual | **Semana 5 de 11** |

**Pregunta principal:** ¿Existe una relación entre el crecimiento económico (PBI) y el cambio climático
en Argentina entre 1961 y 2024, y es posible predecir la evolución de la temperatura a partir de las
variables económicas y climáticas?

---

## 2. Resumen ejecutivo

**Estado:** el proyecto tiene el **100 % de los datos descargados y procesados**, el **informe final
redactado** y una **interfaz web funcionando**. Objetivos 1 a 6 ya tienen resultados escritos y
verificados.

**Lo que ya está hecho:**

- Descarga y verificación de 13 fuentes oficiales y organismos internacionales.
- Construcción de 4 datasets processed (nacional, provincial, clima anual, tendencias).
- Análisis de los 6 objetivos específicos, con resultados numéricos documentados.
- Informe final en `.docx` (572 párrafos, 14 secciones).
- Plan de proyecto en `.docx`.
- App Streamlit con los objetivos 3 y 4, lista para proyectar.

**Lo que falta:**

- Actualizar el cronograma del plan (dice "Modeling: pendiente", pero los modelos ya se corrieron).
- No hay script reproducible de los objetivos 1, 2, 5 y 6 (solo `app.py` cubre el 3 y el 4).
- Presentación oral de 10–15 minutos.
- Revisión de los duplicados de documentos (ver sección 9).

---

## 3. Estructura de carpetas

```
C:\Cambio climatico trabajo\
│
├── app.py                                   ← aplicación Streamlit (1.175 líneas)
├── Levantar.bat                             ← doble clic para levantar la app
├── requirements.txt                         ← 6 librerías
├── README.md                                ← guía de uso (237 líneas)
├── ESTADO_PROYECTO.md                       ← este archivo
│
├── .streamlit/
│   └── config.toml                          ← tema claro, acento azul marino
│
├── data/
│   ├── sources.csv                          ← ficha de las 13 fuentes (14 columnas)
│   ├── raw/                                 ← 12 archivos originales
│   │   ├── geo_ign_provincias/               ← shapefile IGN (7 archivos)
│   │   └── ... (11 archivos de datos)
│   └── processed/                           ← 4 datasets derivados
│       ├── dataset_nacional.csv
│       ├── dataset_provincial.csv
│       ├── provincias_clima_anual.csv
│       └── provincias_tendencia.csv
│
├── Trabajo integrador y plan de proyecto/   ← copias de los 2 documentos finales
│   ├── Plan_de_Proyecto_..._CORREGIDO.docx
│   └── Trabajo_Integrador_..._CORREGIDO.docx
│
├── Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx   ← material de cátedra
│
└── _backup_*                                ← 4 respaldos (ver sección 9)
```

**No hay repositorio Git.** No hay `.venv`. No hay tests.

---

## 4. Inventario de archivos

### 4.1 Código y configuración

| Archivo | Fecha | Tamaño | Qué es |
|---|---|---|---|
| `app.py` | 14/10 16:27 | 50 KB | App Streamlit: objetivos 3 y 4 |
| `Levantar.bat` | 12/10 19:40 | 4,4 KB | Script de arranque en Windows |
| `requirements.txt` | 12/10 19:09 | 82 B | streamlit, pandas, numpy, scipy, statsmodels, plotly |
| `.streamlit/config.toml` | 12/10 19:26 | 705 B | Tema claro, `primaryColor #1E3A5F`, headless |
| `README.md` | 13/10 20:50 | 9 KB | Guía completa de instalación y uso |

### 4.2 Documentos

| Archivo | Fecha | Tamaño | Contenido |
|---|---|---|---|
| `Trabajo_Integrador_..._CORREGIDO.docx` (raíz) | **14/10 16:30** | 50 KB | **Informe final, versión más reciente** (572 párrafos, 14 secciones) |
| `Trabajo integrador y plan de proyecto\Trabajo_Integrador_..._CORREGIDO.docx` | 13/10 20:58 | 49 KB | Copia anterior (518 párrafos) |
| `Trabajo integrador y plan de proyecto\Plan_de_Proyecto_..._CORREGIDO.docx` | 13/10 20:58 | 41 KB | Plan de proyecto (290 párrafos) |
| `Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx` | 13/10 17:14 | 64 KB | Material de cátedra: fases CRISP-DM (43 párrafos) |

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

---

## 5. Detalle de `app.py`

**1.175 líneas.** Entry point único. Contiene:

| Bloque | Qué hace |
|---|---|
| Configuración (l. 24–75) | Rutas, período 1961–2024, corte 1992, paleta de colores, etiquetas |
| CSS (l. 77–157) | Estilos: tarjetas, chips, callouts, tipografía Inter, sidebar |
| Carga de datos (l. 160–181) | `@st.cache_data` + renombrado de columnas + filtro 1961–2024 |
| Funciones estadísticas (l. 184–244) | `matriz_correlacion`, `pares_correlacion`, `vif`, `fisher_z`, `regresion_lineal` |
| Helpers gráficos (l. 246–276) | `_hex_a`, `plantilla_grafico` |
| Presentación (l. 279–306) | `tarjeta`, `fuerza` (clasifica magnitud de r) |
| Sidebar (l. 322–349) | Navegación + datos crudos en expander |
| Página Inicio (l. 352–510) | Encuadre, variables, hallazgos, gráficos con media móvil |
| Objetivo 3 (l. 511–863) | 7 subsecciones |
| Objetivo 4 (l. 864–1098) | 5 subsecciones |
| Metodología (l. 1099–1175) | Fuentes, procedimientos, estructura, limitaciones |

**Navegación (menú lateral):** Inicio · Objetivo 3 · Objetivo 4 · Metodología

**Subsecciones del objetivo 3:** serie de emisiones · matriz de correlación · tests por par ·
VIF · dispersión · robustez con 3 series · conclusión

**Subsecciones del objetivo 4:** corte temporal · comparación de correlaciones · dispersión
e IC 95% · modelo con interacción · conclusión

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

**Nota:** el inventario oficial de GEI (52 nulos) solo cubre 1990–2022, por eso la variable
principal es `emisiones_gei_no_uc_co2eq` (Global Carbon Project), que cubre los 64 años.

---

## 7. Objetivos y resultados

### Objetivo 1 — Descripción de cada variable ✅
Gráfico de línea + regresión lineal + atípicos por IQR.
- Temperatura: tendencia **+0,013 °C/año** (p < 0,001). Año más cálido: **2023 (+0,83 °C)**.
- 1993–2024 es significativamente más cálido que 1961–1992 (+0,406 °C, p < 0,001).

### Objetivo 2 — Relación PBI ↔ clima ✅
Matriz de Pearson con p-valor + análisis detrendizado.
- En niveles: Temp–GEI r = **+0,60** (aparente).
- Detrendizado: Temp–GEI r = **−0,16** (p = 0,19) · Temp–PBI r = **−0,16** (p = 0,22) ·
  Temp–Lluvia r = **−0,16** (p = 0,20).
- Conclusión: la correlación aparente es **espuria**, atribuible a la tendencia compartida.

### Objetivo 3 — Multicolinealidad ✅ *(presentado en la app)*
| Par | r | p |
|---|---|---|
| PBI ↔ GEI | −0,048 | 0,709 |
| PBI ↔ Lluvia | −0,150 | 0,236 |
| GEI ↔ Lluvia | +0,001 | 0,996 |

VIF: PBI 1,000 · GEI 1,025 · Lluvia 1,003 → **no hay multicolinealidad**.
Robustez: resultado idéntico con las 3 series de emisiones (GEI total, CO₂ fósil, inventario).

### Objetivo 4 — Estabilidad temporal ✅ *(presentado en la app)*
| Período | r | p |
|---|---|---|
| 1961–1992 (n=32) | −0,169 | 0,355 |
| 1993–2024 (n=32) | −0,168 | 0,358 |

- Test de Fisher: p ≈ **0,997** → diferencia compatible con el azar.
- Modelo `temp ~ pbi + post + pbi:post`: coeficiente `pbi:post` = **+0,0002** (p = 0,988).
- **La relación PBI–temperatura no cambió** en 64 años.

### Objetivo 5 — Modelos predictivos ✅
Regresión Lineal y Random Forest, partición temporal 1961–2009 / 2010–2024.

### Objetivo 6 — Evaluación vs baseline ✅
| Modelo | RMSE |
|---|---|
| Baseline naive (persistencia) | **0,378** |
| Regresión Lineal | 0,382 |
| Random Forest | 0,429 |

**Ningún modelo supera al baseline.** R² negativo en el conjunto de prueba.

### Veredicto de hipótesis

| Hipótesis | Resultado | Veredicto |
|---|---|---|
| H1 — PBI y GEI correlacionan con temperatura | La correlación aparente desaparece al detrendar | **Rechazada** |
| H2 — La relación se mantiene o fortalece | r estable, p = 0,99 | **Rechazada** |
| H3 — Un modelo supera al baseline | Ninguno lo supera | **Rechazada** |

---

## 8. Cronograma según el plan de proyecto

| Etapa CRISP-DM | Fechas | Estado en el plan |
|---|---|---|
| Business Understanding | 14–20/09/2026 | Completada |
| Data Understanding | 21/09–11/10/2026 | Completada |
| Data Preparation | 12–25/10/2026 | En curso |
| Modeling | 26/10–01/11/2026 | Pendiente |
| Evaluation | 02–08/11/2026 | Pendiente |
| Deployment | 09–30/11/2026 | Pendiente |

> ⚠️ **Discrepancia:** el cronograma del plan no está actualizado. Los objetivos 5 y 6 ya tienen
> resultados escritos en el informe final (sección 5.5), y el objetivo 3 ya está implementado en la
> app. El plan debería reflejar que Modeling y Evaluation ya se ejecutaron.

---

## 9. Duplicados y respaldos

Hay **3 copias del informe integrador** y **2 del plan**. La de la raíz (14/10 16:30) es la más nueva.

| Archivo | Fecha | Párrafos | Estado |
|---|---|---|---|
| `Trabajo_Integrador_..._CORREGIDO.docx` (raíz) | 14/10 16:30 | 572 | **Actual** |
| `Trabajo integrador y plan de proyecto\Trabajo_Integrador...` | 13/10 20:58 | 518 | Anterior |
| `_backup_integrador.docx` | 12/10 20:18 | 518 | Backup |
| `Plan_de_Proyecto_..._CORREGIDO.docx` | 13/10 20:58 | 290 | **Actual** |
| `_backup_plan.docx` | 12/10 20:17 | 290 | Backup |
| `_backup_dataset_nacional.csv` | 24/09 20:09 | — | Backup |
| `_backup_sources.csv` | 25/09 22:38 | — | Backup |

**Sugerencia:** consolidar en una sola carpeta y borrar los `_backup_*` antes de la entrega.

---

## 10. Cómo levantar la app

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

## 11. Pendientes

- [ ] Actualizar el cronograma del plan de proyecto (sección 8)
- [ ] Crear script reproducible para objetivos 1, 2, 5 y 6 (hoy solo existen resultados en el informe)
- [ ] Extender la app con los objetivos 5 y 6 (modelos y comparación con baseline)
- [ ] Armar la presentación oral de 10–15 minutos
- [ ] Limpiar duplicados y backups (sección 9)
- [ ] Considerar inicializar Git para versionar el código

---

## 12. Últimas versiones de datos clave

| Dato | Valor |
|---|---|
| Filas dataset nacional | 65 (1961–2025), la app usa 64 (1961–2024) |
| Observaciones completas | 64 años |
| Corte de mitades | 1992 |
| Fuentes documentadas | 13 |
| Objetivos específicos | 6 |
| Objetivos implementados en la app | 2 (el 3 y el 4) |
| Líneas de trabajo futuro | 6 (ARIMA/Prophet, variables omitidas, rezagos, inventarios, provincial, GAM) |