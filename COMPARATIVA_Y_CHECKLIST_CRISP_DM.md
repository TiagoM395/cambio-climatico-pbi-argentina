# Comparativa y Checklist: Requerimientos de Cátedra vs. Estado del Proyecto

> **Proyecto:** Cambio climático en Argentina y su relación con el crecimiento económico (PBI)  
> **Cátedra:** Análisis y Exploración de Datos — Tecnicatura Superior en Ciencia de Datos e IA (Instituto 57)  
> **Docente:** Ibarra Martín | **Comisión:** 2.° año, Grupo 6  
> **Integrantes:** Elias Campos · Tiago Maidana · Rodrigo Bulggiani · Romina Guzman  
> **Documento de referencia de la cátedra:** `Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx`  
> **Fecha de entrega:** 30/11/2026 (Semana 11)  
> **Fecha de análisis:** 23/11/2026  

---

## 1. Resumen Ejecutivo de la Comparativa

El documento provisto por el profesor (`Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx`) establece dos dimensiones evaluativas:
1. **El seguimiento metodológico del ciclo de vida CRISP-DM** a través de sus 6 fases y 24 tareas formales.
2. **Los documentos obligatorios de entrega**:
   - **Plan de Proyecto** (actividades, objetivos de negocio y objetivos de explotación de datos).
   - **Informe Final** con 5 secciones temáticas obligatorias (recolección y métricas, preparación y transformaciones, selección de modelos y teoría, evaluación de resultados y conclusiones, y sugerencias de trabajo futuro).

### Veredicto Global
| Componente | Nivel de Cobertura | Estado | Observación Principal |
|---|:---:|:---:|---|
| **Fases CRISP-DM (1 a 6)** | **95 %** | ✅ Muy Alto | Todas las fases y tareas están contempladas en los documentos y en el código. |
| **Documento 1: Plan de Proyecto** | **100 %** | ✅ Completo | Cumple exhaustivamente con actividades, cronograma (11 semanas), riesgos, recursos y objetivos. |
| **Documento 2: Informe Final (5 secciones)** | **90 %** | ⚠️ Atención requerida | La estructura metodológica, teórica y de diseño está al 100 %. Sin embargo, el documento base fue formulado como *versión prospectiva* y los resultados numéricos finales fueron añadidos en notas al pie/revisión final. Conviene unificarlo como informe de resultados consolidados. |
| **Implementación / Despliegue** | **100 %** | ✅ Sobresaliente | Supera el requerimiento estándar: Streamlit interactivo de ~3.300 líneas con los 6 objetivos, `modelos.py` reproducible y trazabilidad total. |
| **Presentación Oral (Defensa)** | **75 %** | ⏳ En progreso | Esqueleto creado en `Presentacion_oral.pptx` (10–15 min), pendiente ensayo y pulido visual final. |

---

## 2. Comparativa Detallada por Fases de la Metodología CRISP-DM

### Fase 1: Comprensión del Negocio (Business Understanding)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Definir los objetivos del negocio:** situación actual de la organización, descripción del problema, objetivos del cliente y criterios de éxito. | Contextualización de la matriz productiva argentina, debate sobre crecimiento vs. emisiones, 3 objetivos de negocio claros y 5 criterios de éxito explícitos (admitiendo resultado negativo). | `Plan_de_Proyecto...CORREGIDO.docx` (Sec. 1 y 2)<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 1 y 2) | ✅ Cumplido |
| **2. Evaluar la situación:** inventario de recursos, lista de requerimientos, riesgos con planes de contingencia y análisis costo-beneficio. | Inventario de hardware/software/humano, matriz de 12 riesgos con probabilidad/impacto/contingencia, y análisis formal de costo-beneficio. | `Plan_de_Proyecto...CORREGIDO.docx` (Sec. 4 y 7) | ✅ Cumplido |
| **3. Determinar objetivos de la explotación de datos:** objetivos técnicos, resultados previstos y condiciones de aceptación. | 6 objetivos técnicos específicos (tendencias, correlación detrendizada, multicolinealidad VIF, estabilidad temporal Fisher/interacción, modelos OLS y RF, evaluación vs baseline). Criterios de aceptación numéricos fijados de antemano. | `Plan_de_Proyecto...CORREGIDO.docx` (Sec. 2.3)<br>`OBJETIVOS_del_proyecto.md` | ✅ Cumplido |
| **4. Desarrollar plan para el proyecto:** planificación de tareas, duraciones, hitos y recursos. | Cronograma de 11 semanas (14/09 al 30/11), desglose semanal, 8 hitos de control con compuertas de avance y 140 horas-persona presupuestadas. | `Plan_de_Proyecto...CORREGIDO.docx` (Sec. 6 y 12) | ✅ Cumplido |

---

### Fase 2: Entendiendo los Datos (Data Understanding)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Recolecta de datos:** obtención junto con un informe que describe la forma de obtención y problemas encontrados. | Ficha de 13 fuentes oficiales (CIAM, SMN, Banco Mundial, OWID, NASA POWER, IGN). Registro de problemas de acceso, discrepancias de cobertura y soluciones. | `data/sources.csv`<br>`data/raw/`<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 5.1–5.4) | ✅ Cumplido |
| **2. Descripción de datos:** tamaño, volumen, cantidad de registros y formato. | Detalle de las 64 observaciones anuales (1961–2024), 5 variables principales nacionales, extensión provincial a 24 jurisdicciones (1981–2024), tipos de archivos (.csv, shapefile). | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 3.4 y 5.2)<br>`app.py` | ✅ Cumplido |
| **3. Exploración de los datos:** variables clave, distribuciones, reporte inicial e impacto en el proyecto. | Objetivo 1 cubierto íntegramente: estadísticas descriptivas (min, max, media, mediana), tests de Shapiro-Wilk de normalidad, tendencias con OLS, gráficos de dispersión y series temporales. | `app.py` (Módulo Obj 1)<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 7.1) | ✅ Cumplido |
| **4. Verificación de datos:** calidad, detección de errores y soluciones. | Detección de atípicos por IQR contrastados con historia económica/climática, verificación de unicidad temporal, rangos y completitud sin nulos. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 5.6 y 6.2) | ✅ Cumplido |

---

### Fase 3: Preparación de los Datos (Data Preparation)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Selección de datos:** justificación de inclusión y exclusión de datos. | Justificación de las 4 predictoras y la variable objetivo; justificación de la exclusión de series alternativas cortas (inventario oficial nacional acotado) o modelos causales/GAM. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.1 y 8.7) | ✅ Cumplido |
| **2. Limpieza de datos:** nombres, normalización, tratamiento de nulos. | Tabla formal de 6 problemas y tratamientos previstos (nombres en minúsculas sin tildes, casteo de tipos, recorte al rango común 1961–2024). | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.2 y 6.3) | ✅ Cumplido |
| **3. Construcción de los datos:** atributos derivados, variables nuevas. | Detrendizado (residuos de regresión temporal), primeras diferencias ($\Delta$), variable binaria de período `post` (corte 1993) e interacción `pbi:post`. | `data/processed/`<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.3–6.4) | ✅ Cumplido |
| **4. Integración de los datos:** unión de tablas y nuevas estructuras. | Integración vía outer join por `anio` preservando trazabilidad. 4 datasets consolidados generados (`dataset_nacional.csv`, `dataset_provincial.csv`, `provincias_clima_anual.csv`, `provincias_tendencia.csv`). | `data/processed/`<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.5) | ✅ Cumplido |
| **5. Cambio de formato:** transformaciones por necesidades técnicas. | Agregación de NASA POWER mensual a anual por capital provincial; conversión de tipos float/int y matrices NumPy para modelado. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.3 y 10.2) | ✅ Cumplido |

---

### Fase 4: Modelado (Modeling)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Selección de las técnicas:** documentar qué técnicas se emplean y su justificación. | Regresión Lineal Múltiple (OLS) para interpretabilidad directa de coeficientes; Random Forest Regressor (500 árboles) como contraste no lineal de ensemble. Baseline naive de persistencia. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 8.1–8.4)<br>`modelos.py` | ✅ Cumplido |
| **2. Diseño de pruebas:** verificación de validez y partición de datos. | Partición temporal cronológica obligatoria (1961–2009 entrenamiento = 49 años; 2010–2024 prueba = 15 años). Validación cruzada con ventana deslizante/cortes móviles. No aleatoria para no filtrar futuro. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 6.7 y 9.1)<br>`modelos.py` | ✅ Cumplido |
| **3. Construcción del modelo:** aplicación de las técnicas sobre los datos. | Modelos entrenados y evaluados tanto en script batch (`modelos.py`) como en la aplicación interactiva (`app.py`), con semilla fija (`random_state=42`) para garantizar reproducibilidad exacta. | `modelos.py`<br>`app.py` | ✅ Cumplido |
| **4. Evaluación del modelado:** calidad técnica según criterios de éxito. | Diagnósticos completos: VIF (todos < 1.3, ausencia de multicolinealidad), Durbin-Watson, test de normalidad Shapiro-Wilk (p=0.0188), ajuste OLS con errores robustos HAC Newey-West (3 rezagos), importancias Gini en Random Forest. | `Trabajo_Integrador...CORREGIDO.docx` (Nota 22/11)<br>`modelos.py`<br>`app.py` | ✅ Cumplido |

---

### Fase 5: Evaluación (Evaluation)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Evaluación de resultados en función de negocio:** validez práctica respecto a las hipótesis. | **Hipótesis contrastadas:**<br>• **H1:** La correlación en niveles (r=0.45) desaparece al detrendar (r=0.08, p=0.55), demostrando correlación espuria.<br>• **H2:** Estabilidad temporal sostenida (Fisher p=0.46; interacción pbi:post p=0.74).<br>• **H3:** Rechazada formalmente con criterio científico riguroso: ningún modelo supera al baseline naive de persistencia (RMSE Persistencia = 0.3776 vs. OLS = 0.3919 vs. RF = 0.4192; $R^2$ de prueba negativos). | `Trabajo_Integrador...CORREGIDO.docx` (Notas finales)<br>`README5y6.md`<br>`modelos.py`<br>`app.py` | ✅ Cumplido |
| **2. Revisión del proceso:** detección de errores, problemas y lecciones metodológicas. | Detección del fenómeno de correlación espuria por no estacionariedad, problema de autocorrelación en residuos resuelto con estimador HAC Newey-West, análisis del sesgo por extrapolación de tendencia en modelos multivariados. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 4.3 y Nota 22/11)<br>`error_vif_objetivo3.md` | ✅ Cumplido |
| **3. Próximas etapas de actuación:** definir siguientes pasos o iteraciones. | Regla de decisión respetada: no se cambió el baseline post hoc; se añadieron dos análisis complementarios transparentes (baseline último valor y modelo con tendencia explícita) documentando sus implicancias. | `Trabajo_Integrador...CORREGIDO.docx` (Sec. 9.3 y 16) | ✅ Cumplido |

---

### Fase 6: Implementación (Deployment)

| Tarea exigida por el Profesor | Lo que tenemos en el proyecto | Documento / Archivo | Estado |
|---|---|---|:---:|
| **1. Planificación de la implementación:** plan para llevar a cabo el despliegue. | Despliegue interactivo local mediante Streamlit, documentado paso a paso con script directo `Levantar.bat` para ejecución en Windows con un solo clic. | `Levantar.bat`<br>`README.md`<br>`Trabajo_Integrador...CORREGIDO.docx` (Sec. 12) | ✅ Cumplido |
| **2. Monitoreo y mantenimiento:** plan ante cambios o actualizaciones en los datos. | Ficha de corte temporal de las 13 fuentes, procedimientos de actualización de series del Banco Mundial, CIAM y NASA POWER al publicarse nuevos años. | `data/sources.csv`<br>`Plan_de_Proyecto...CORREGIDO.docx` (Sec. 10) | ✅ Cumplido |
| **3. Elaboración de reporte final:** resumen del proyecto y resultados obtenidos. | Informes `.docx`, `.md`, `README.md`, `README5y6.md`, app interactiva y presentación en PowerPoint. | Todos los archivos del repositorio | ⚠️ Ver Sec. 4 |

---

## 3. Comparativa de los Documentos Obligatorios de Entrega

La consigna del docente en las líneas 35–43 del documento `Proyecto de Análisis y Exploración de datos - MetodologiaCRISP.docx` estipula:

### 3.1 Documento 1: Plan de Proyecto
> *"Plan de proyecto donde quede claro las actividades a desarrollar, los objetivos de negocio y los objetivos de explotación de los datos."*

| Requerimiento Específico | Estado | Cobertura en Nuestro Proyecto |
|---|:---:|---|
| **Actividades a desarrollar** | ✅ | Desglosadas en 11 semanas, 6 fases CRISP-DM, tareas individuales, roles y 8 hitos de control (`Plan_de_Proyecto...CORREGIDO.docx`, Sec. 6). |
| **Objetivos de negocio** | ✅ | 3 objetivos de negocio claros con impacto socioeconómico y criterios de éxito (`Plan_de_Proyecto...CORREGIDO.docx`, Sec. 2.2). |
| **Objetivos de explotación de datos** | ✅ | Los 6 objetivos técnicos especificados con procedimiento y condición de aceptación (`Plan_de_Proyecto...CORREGIDO.docx`, Sec. 2.3). |

---

### 3.2 Documento 2: Informe Final
> *"Informe final con las siguientes secciones:"*

#### Sección 1: Recolección de datos y análisis según métricas
> *"Explicar cómo se recolectaron los datos y el análisis de estos en función de las métricas a obtener."*
- **En el proyecto:**
  - Sección 5 del Trabajo Integrador (`Procedimiento de recolección de datos`, 5.1 a 5.6).
  - Ficha exhaustiva de 13 fuentes en `data/sources.csv` con URL, frecuencia, unidad y cobertura temporal.
  - Subsección 5.5 (`Métricas a obtener y procedimientos de cálculo`): define explícitamente coeficientes de tendencia, matriz de correlación en niveles y detrendizada, VIF, estadístico Z de Fisher, RMSE, MAE y $R^2$.
- **Estado:** ✅ **Completamente cubierto.**

#### Sección 2: Preparación de datos, problemas, soluciones y transformaciones
> *"Explicar y dar detalles de la preparación de los datos, cómo se realizó, que problemas tuvieron, como lo solucionaron, si se realizó alguna transformación de datos y con qué propósito."*
- **En el proyecto:**
  - Sección 6 del Trabajo Integrador (`Procedimiento de preparación de datos`).
  - **Tabla 6.2:** Problemas de calidad detectados (años incompletos, cobertura dispar, atípicos históricos, duplicados en claves, unidades heterogéneas, tipos de dato), cómo se detectaron, tratamiento aplicado y su propósito.
  - **Tabla 6.3:** 8 transformaciones realizadas (renombrado y normalización, casteo de tipos, filtrado territorial Argentina/provincias, agregación mensual a anual, detrendizado por regresión temporal, primeras diferencias, variable binaria de período y partición temporal disjunta) con su respectiva justificación técnica y propósito.
  - **Sección 6.4 y 6.5:** Procedimiento de integración mediante outer join y controles de calidad de 6 compuertas (unicidad, completitud, cobertura, consistencia, orden, trazabilidad).
- **Estado:** ✅ **Completamente cubierto.**

#### Sección 3: Selección de modelos y fundamento teórico
> *"Explicar porqué se seleccionó el o los modelos para este proyecto en particular y también explicar desde la teoría el modelo seleccionado."*
- **En el proyecto:**
  - Sección 8 del Trabajo Integrador (`Selección de modelos y fundamento teórico`).
  - **Criterios de selección:** interpretabilidad vs. flexibilidad, tipo de variable objetivo continua y comportamiento en extrapolación.
  - **Fundamento teórico de Regresión Lineal Múltiple (OLS):** formulación matricial, interpretación de coeficientes $\beta$, supuestos clásicos de Gauss-Markov y consecuencias de su incumplimiento en series temporales (autocorrelación de errores, colinealidad).
  - **Fundamento teórico de Random Forest Regressor:** ensembles bagging, árboles de decisión, no linealidad, ventaja frente a relaciones complejas y limitación crítica en series temporales (incapacidad de extrapolar tendencias crecientes).
  - **Fundamento teórico del Baseline Naive de Persistencia:** rol en series con inercia térmica y justificación como benchmark exigente.
  - **Fundamento teórico del Test de Fisher y modelo con interacción:** ecuaciones de $z = \operatorname{arctanh}(r)$ y especificación $Y = \beta_0 + \beta_1 X + \beta_2 \text{post} + \beta_3 (X \cdot \text{post}) + \varepsilon$.
  - **Modelos descartados con justificación:** ARIMA, GAM, PCA y Redes Neuronales.
- **Estado:** ✅ **Completamente cubierto.**

#### Sección 4: Proceso de evaluación, resultados obtenidos y conclusiones
> *"Explicar el proceso de evaluación de los resultados, que se hizo, que se obtuvo y las conclusiones del trabajo realizado."*
- **En el proyecto:**
  - **Qué se hizo:** Sección 9 del Trabajo Integrador define el protocolo: partición temporal 1961–2009 (train) / 2010–2024 (test), métricas RMSE, MAE, $R^2$, regla de decisión anti-trampa previa, diagnósticos de residuos (Durbin-Watson, Shapiro-Wilk) y análisis de robustez.
  - **Qué se obtuvo:** Los números están calculados y comprobados en `modelos.py`, `app.py`, `README5y6.md` y en las notas de actualización al final del documento docx (Líneas 789–792):
    - RMSE Persistencia: **0,3776**
    - RMSE Regresión Lineal: **0,3919**
    - RMSE Random Forest: **0,4192**
    - Diagnóstico: Rechazo de normalidad de residuos ($p = 0,0188$), corrección vía errores robustos HAC Newey-West (3 rezagos) que revela que la relación con GEI no es significativa ($p_{\text{HAC}} = 0,698$).
  - **Conclusiones:** La hipótesis H3 se rechaza; el hallazgo negativo es el resultado científico válido (no hay capacidad predictiva económica sobre la anomalía de temperatura que supere la persistencia climática).
- **Estado:** ⚠️ **Atención:** En el `.docx` vigente, la Sección 9 describe el *procedimiento previsto*, y los resultados empíricos exactos están colocados como una *Nota de revisión* al final del texto. Si el profesor pide leer el informe como un trabajo ya ejecutado, es recomendable trasladar los resultados directamente a las secciones 7, 8 y 9 o presentar la sección de resultados como capítulo central.

#### Sección 5: Sugerencias para continuar con el análisis en el futuro
> *"Sugerencias para continuar con el análisis en el futuro."*
- **En el proyecto:**
  - Sección 16 del Trabajo Integrador (`Sugerencias para continuar con el análisis en el futuro`).
  - 7 propuestas detalladas y justificadas:
    1. Modelos de series temporales formales (ARIMA, SARIMAX, Prophet).
    2. Incorporación de variables omitidas (matriz energética, deforestación, uso del suelo, PBI sectorial).
    3. Modelado de rezagos dinámicos (efecto acumulativo de GEI a 10–30 años).
    4. Incorporación del inventario oficial de emisiones una vez que se amplíe su serie temporal.
    5. Análisis provincial cruzado con Producto Bruto Geográfico (PBG) homogéneo.
    6. Modelos aditivos generalizados (GAM).
    7. Análisis de sensibilidad respecto a la base de anomalía climática (1961–1990 vs 1991–2020).
- **Estado:** ✅ **Completamente cubierto.**

---

## 4. Brechas Detectadas y Aspectos a Perfeccionar

| # | Aspecto | Situación Actual | Riesgo / Observación con el Docente | Acción Recomendada |
|---|---|---|---|---|
| **1** | **Tiempo verbal del Informe Final** | El `.docx` dice *"Versión 2.0 — versión prospectiva"* e *"Informe metodológico — procedimiento previsto..."*. | El profesor podría interpretarlo como una propuesta de trabajo antes de ejecutarse, en lugar de un informe final de resultados. | En la carátula y presentación, aclarar que el informe metodológico fijó las hipótesis y reglas pre-registro para evitar sesgos, y consolidar los resultados obtenidos dentro del cuerpo del texto. |
| **2** | **Integración de resultados en el cuerpo del .docx** | Los valores numéricos finales (0.3776 vs 0.3919 vs 0.4192, HAC p=0.698) están en las Notas al pie del final (pág. final) y en `README5y6.md`. | Si el docente lee únicamente el cuerpo principal del `.docx`, verá fórmulas pero no las tablas de resultados llenas. | Verificar si se debe exportar una versión final con las tablas de resultados insertadas directamente en la sección 7 y 9 del informe. |
| **3** | **Defensa Oral (Presentación)** | `Presentacion_oral.pptx` contiene el esqueleto conceptual para los 6 objetivos. | La cátedra suele evaluar la defensa oral de 10–15 min de forma determinante. | Ensayar los tiempos por integrante, verificar que los gráficos de Streamlit se visualicen claramente y practicar la explicación de por qué un resultado negativo es un éxito metodológico. |

---

## 5. Checklists de Tareas a Completar

### Checklist 1: Documentación Escrita (.docx y .md)
- [x] **Plan de Proyecto (`Plan_de_Proyecto...CORREGIDO.docx`):**
  - [x] Objetivos de negocio y técnicos alineados.
  - [x] Cronograma de 11 semanas completo.
  - [x] Matriz de riesgos y análisis costo-beneficio presentes.
- [ ] **Informe Final (`Trabajo_Integrador...CORREGIDO.docx`):**
  - [x] Sección 1: Recolección y métricas explicadas.
  - [x] Sección 2: Preparación, problemas, soluciones y transformaciones detalladas.
  - [x] Sección 3: Fundamento teórico de OLS, Random Forest y Baseline Naive.
  - [ ] **Integrar resultados numéricos en el cuerpo:** Trasladar los valores de la Nota de Revisión del 22/11 (RMSE, MAE, $R^2$, p-valores HAC) a las tablas de la Sección 7 y 9 para que no queden solo al final.
  - [ ] **Actualizar carátula:** Cambiar la leyenda *"versión prospectiva"* a *"Versión Final — Resultados y Conclusiones"*.
  - [x] Sección 5: Sugerencias futuras documentadas (7 líneas de trabajo).

### Checklist 2: Datos, Modelos y Reproducibilidad
- [x] **Datos crudos y procesados:**
  - [x] 13 fuentes en `data/raw/` y metadatos en `data/sources.csv`.
  - [x] 4 datasets derivados limpios en `data/processed/`.
  - [x] Verificación de ausencia de nulos y duplicados en el rango 1961–2024.
- [x] **Scripts de modelado:**
  - [x] `modelos.py` ejecutable de punta a punta con `random_state=42`.
  - [x] Cálculo de errores robustos HAC Newey-West implementado.
  - [x] Baseline alternativo (último valor constante) y modelo con tendencia incorporados.

### Checklist 3: Aplicación Interactiva y Despliegue (Streamlit)
- [x] Módulo del Objetivo 1: Tendencias, IQR, atípicos y tests de normalidad.
- [x] Módulo del Objetivo 2: Matriz en niveles vs. detrendizada (demostración de correlación espuria).
- [x] Módulo del Objetivo 3: VIF (< 1.3) y dispersión por pares.
- [x] Módulo del Objetivo 4: Test de Fisher y modelo de interacción temporal.
- [x] Módulo del Objetivo 5: Regresión OLS y Random Forest con feature importance.
- [x] Módulo del Objetivo 6: Tabla comparativa de métricas vs. persistencia naive.
- [x] Extensión Provincial: Mapa interactivo y proyecciones NASA POWER 2030/2040.
- [x] Acceso rápido: `Levantar.bat` verificado y funcional en Windows.

### Checklist 4: Presentación Oral y Cierre de Entrega (30/11/2026)
- [ ] **Presentación oral (`Presentacion_oral.pptx`):**
  - [ ] Revisar diseño visual de las diapositivas (colores, fuentes legibles, capturas de gráficos).
  - [ ] Asignar diapositivas a cada uno de los 4 integrantes (Elías, Tiago, Rodrigo, Romina).
  - [ ] Cronometrar la exposición completa para no exceder los 10–15 minutos reglamentarios.
  - [ ] Preparar respuestas a preguntas típicas de la cátedra:
    - *¿Por qué un R² negativo en el bloque de prueba no significa que el trabajo esté mal hecho?*
    - *¿Por qué no se usó partición aleatoria train_test_split?*
    - *¿Por qué la correlación entre PBI y temperatura era espuria?*
- [ ] **Repositorio Git y Entrega:**
  - [x] Repositorio limpio con `.gitignore` (sin carpetas pesadas innecesarias).
  - [x] `README.md` sincronizado con las instrucciones de instalación y reproducción.
  - [ ] Empaquetado o enlace de entrega según la modalidad requerida por el profesor Martín Ibarra.
