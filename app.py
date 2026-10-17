# -*- coding: utf-8 -*-
"""
Cambio climatico en Argentina y su relacion con el crecimiento economico (PBI)
Interfaz Streamlit - Objetivos 1, 3 y 4

Objetivo 1: Descripcion de cada variable (tendencia lineal y atipicos por IQR)
Objetivo 3: Multicolinealidad (PBI, GEI, Lluvia sin temperatura)
Objetivo 4: Estabilidad temporal de la relacion PBI - Temperatura (1961-1992 vs 1993-2024)
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor

# ----------------------------------------------------------------------------
# CONFIGURACION
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "dataset_nacional.csv"

ANIO_MIN, ANIO_MAX = 1961, 2024
MITAD_CORTE = 1992

# Sistema de color: tema oscuro azul noche, acento celeste.
# Paleta de datos: tonos luminosos sobre fondo oscuro para mantener el contraste.
ACENTO = "#5B9BD5"          # celeste - color de marca de la interfaz
ACENTO_CLARO = "#1E2E40"    # variante oscura del acento, para superficies

# Superficies (alineadas con .streamlit/config.toml)
FONDO = "#0D1520"           # fondo de la aplicacion
FONDO_2 = "#16212F"         # tarjetas, sidebar, bloques
FONDO_3 = "#111C29"         # superficies intermedias

# Texto: la escala baja la luminancia para sostener la jerarquia sobre fondo oscuro.
TEXTO = "#E6EDF5"
TEXTO_2 = "#A9B6C6"
TEXTO_3 = "#7C8A9B"

BORDE = "#24334A"           # separadores y contornos

COLORES = {
    "pbi": "#5B9BD5",       # celeste
    "gei": "#C3A98C",       # arena - industrial
    "lluvia": "#45B3C9",    # teal - agua
    "temp": "#E8896A",      # terracota - calor
    "h1": "#5B9BD5",        # celeste
    "h2": "#E8896A",        # terracota
    "neutro": "#8A93A0",
}

# Semantica (chips, callouts, estados). Fondo oscuro, texto claro.
SEM = {
    "ok": "#7ED9A4",
    "ok_bg": "#132A1D",
    "ok_bd": "#245039",
    "warn": "#E8C46A",
    "warn_bg": "#2A2415",
    "warn_bd": "#4A3E1C",
    "bad": "#F2857A",
    "bad_bg": "#2C1815",
    "bad_bd": "#4E2A24",
}

# Tokens de los graficos Plotly.
GRAF = {
    "titulo": TEXTO,        # titulo del grafico
    "texto": TEXTO_2,       # ejes, ticks, leyenda
    "linea": BORDE,         # eje y marco de la celda
    "grid": "#1B2736",      # grilla horizontal
    "ref": "#3D4C61",       # lineas de referencia (vline, hline)
    "ajuste": "#8A99AB",    # recta de ajuste OLS
    "surf": FONDO_2,        # fondo del area de trazado
}

VARS_ESTUDIO = ["temp", "pbi", "gei", "lluvia"]

# Unidad del nivel, unidad de la pendiente y decimales para mostrar cada variable.
UNIDADES = {
    "temp": ("°C", "°C/año", 3),
    "pbi": ("%", "pp/año", 3),
    "gei": ("MtCO2eq", "MtCO2eq/año", 2),
    "lluvia": ("%", "pp/año", 3),
}

ETIQUETAS = {
    "pbi": "PBI (crecimiento %)",
    "gei": "GEI total (MtCO2eq)",
    "gei_inventario": "GEI inventario (MtCO2eq)",
    "co2": "CO2 fosil (Mt)",
    "lluvia": "Lluvia (anomalia %)",
    "temp": "Temperatura (anomalia C)",
}

st.set_page_config(
    page_title="Cambio climatico y PBI en Argentina",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------------
# CSS
# ----------------------------------------------------------------------------
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    :root {
        --fondo:      #0D1520;
        --fondo-2:    #16212F;
        --fondo-3:    #111C29;
        --acento:     #5B9BD5;
        --borde:      #24334A;
        --texto:      #E6EDF5;
        --texto-2:    #A9B6C6;
        --texto-3:    #7C8A9B;
    }

    html, body, [class*="css"] { font-family: 'Inter', -apple-system, sans-serif; }

    .block-container { padding-top: 2.6rem; padding-bottom: 5rem; max-width: 1280px; }

    /* Tipografia */
    h1 { font-weight: 600; letter-spacing: -0.022em; font-size: 1.95rem; margin-bottom: .25rem; color: var(--texto); }
    h2 { font-weight: 600; letter-spacing: -0.014em; font-size: 1.28rem; margin-top: 2.2rem;
         padding-bottom: .5rem; border-bottom: 1px solid var(--borde); color: var(--texto); }
    h3 { font-weight: 600; font-size: .98rem; margin-top: .4rem; color: var(--texto-2); }
    p, li, .stMarkdown { color: var(--texto-2); line-height: 1.65; }
    a { color: var(--acento); }

    /* Etiqueta superior */
    .eyebrow {
        font-size: .68rem; font-weight: 600; letter-spacing: .16em;
        text-transform: uppercase; color: var(--acento); opacity: .85; margin-bottom: .4rem;
    }

    /* Tarjetas */
    .card {
        background: var(--fondo-2); border: 1px solid var(--borde); border-radius: 10px;
        padding: 1.05rem 1.15rem; margin-bottom: .7rem;
        border-top: 2px solid var(--acento);
    }
    .card-titulo {
        font-size: .68rem; font-weight: 600; letter-spacing: .09em;
        text-transform: uppercase; color: var(--texto-3); margin-bottom: .4rem;
    }
    .card-valor { font-size: 1.8rem; font-weight: 600; letter-spacing: -0.025em; line-height: 1.15; color: var(--texto); }
    .card-nota { font-size: .8rem; color: var(--texto-3); margin-top: .3rem; line-height: 1.5; }

    /* Chips */
    .chip {
        display: inline-block; padding: .22rem .62rem; border-radius: 4px;
        font-size: .73rem; font-weight: 600; margin-right: .35rem; margin-top: .25rem;
        letter-spacing: .01em;
    }
    .chip-ok   { background: #132A1D; color: #7ED9A4; border: 1px solid #245039; }
    .chip-warn { background: #2A2415; color: #E8C46A; border: 1px solid #4A3E1C; }
    .chip-bad  { background: #2C1815; color: #F2857A; border: 1px solid #4E2A24; }
    .chip-info { background: #16283A; color: #7FB4E4; border: 1px solid #2A4568; }

    /* Callout */
    .callout {
        border-left: 3px solid var(--acento); background: var(--fondo-2);
        padding: .9rem 1.1rem; border-radius: 0 8px 8px 0; margin: .9rem 0;
        font-size: .92rem; line-height: 1.65; color: var(--texto-2);
    }
    .callout strong { color: var(--texto); font-weight: 600; }
    .callout em { color: var(--texto-3); }
    .callout-ok   { border-left-color: #7ED9A4; background: #12251B; }
    .callout-warn { border-left-color: #E8C46A; background: #241F13; }
    .callout-bad  { border-left-color: #F2857A; background: #271715; }

    /* Lectura de un grafico: que demuestra */
    .lectura {
        background: var(--fondo-3); border: 1px solid var(--borde); border-radius: 8px;
        padding: .8rem 1rem; margin: -.3rem 0 1.3rem; font-size: .88rem; line-height: 1.6;
        color: var(--texto-2);
    }
    .lectura-titulo {
        font-size: .66rem; font-weight: 600; letter-spacing: .14em; text-transform: uppercase;
        color: var(--acento); margin-bottom: .35rem;
    }
    .lectura-leer { color: var(--texto-3); font-size: .82rem; margin-bottom: .45rem; }
    .lectura strong { color: var(--texto); font-weight: 600; }

    /* Sidebar */
    section[data-testid="stSidebar"] { background: var(--fondo-3); border-right: 1px solid var(--borde); }
    section[data-testid="stSidebar"] .block-container { padding-top: 1.4rem; }
    section[data-testid="stSidebar"] .stRadio label { font-size: .89rem; font-weight: 500; color: var(--texto); }
    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p { color: var(--texto-3); font-size: .84rem; }
    section[data-testid="stSidebar"] hr { border-color: var(--borde); }

    /* Widgets nativos sobre fondo oscuro */
    .stSlider [data-baseweb="slider"] div[role="slider"] { border-color: var(--acento); }
    .stRadio [role="radiogroup"] label { color: var(--texto); }
    .stRadio [aria-checked="true"] p { color: var(--acento); }
    .stExpander summary { color: var(--texto-2); }
    .stExpander summary:hover { color: var(--texto); }

    /* Tablas y separadores */
    .stDataFrame { border: 1px solid var(--borde); border-radius: 8px; overflow: hidden; }
    hr { margin: 2.4rem 0; border-color: var(--borde); }

    /* Refuerza fondo oscuro en todos los contenedores, incluidos los que
       Streamlit crea para el encabezado y los bloques de componentes. */
    html, body, [data-testid="stAppViewContainer"],
    .stApp, section.main, [data-testid="stMain"],
    [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stVerticalBlock"] {
        background-color: var(--fondo);
        color: var(--texto);
    }
    [data-testid="stAppViewContainer"] > .main { background-color: var(--fondo); }
    </style>
""",
    unsafe_allow_html=True,
)


# ----------------------------------------------------------------------------
# CARGA DE DATOS
# ----------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def cargar_datos() -> pd.DataFrame:
    """Carga el dataset nacional y normaliza los nombres de columna."""
    df = pd.read_csv(DATA_PATH, encoding="utf-8")
    df = df.rename(
        columns={
            "año": "anio",
            "anomalia_temperatura": "temp",
            "anomalia_precipitacion_pct": "lluvia",
            "emisiones_gei_co2eq": "gei_inventario",
            "emisiones_gei_no_uc_co2eq": "gei",
            "emisiones_co2_fosil": "co2",
            "pbi_crecimiento_pct": "pbi",
            "pib_per_capita_crecimiento_pct": "pibpc",
        }
    )
    # El proyecto trabaja 1961-2024: 2025 es un dato incompleto (sin emisiones).
    df = df[(df["anio"] >= ANIO_MIN) & (df["anio"] <= ANIO_MAX)].copy()
    return df.sort_values("anio").reset_index(drop=True)


@st.cache_data(show_spinner=False)
def matriz_correlacion(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Matriz de correlacion de Pearson."""
    return df[cols].corr()


def pares_correlacion(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Devuelve r, p-valor y n para cada par de variables."""
    filas = []
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            sub = df[[a, b]].dropna()
            r, p = stats.pearsonr(sub[a], sub[b])
            filas.append(
                {
                    "Par": f"{ETIQUETAS[a].split(' (')[0]}  ↔  {ETIQUETAS[b].split(' (')[0]}",
                    "r": r,
                    "r_abs": abs(r),
                    "p_valor": p,
                    "n": len(sub),
                    "Interpretacion": "Relacionado" if p < 0.05 else "No relacionado",
                    "Significativo": p < 0.05,
                }
            )
    return pd.DataFrame(filas)


def vif(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Variance Inflation Factor para cada variable."""
    X = sm.add_constant(df[cols].dropna())
    filas = []
    for c in cols:
        # Se busca la posicion por nombre: add_constant inserta 'const' en la columna 0.
        v = variance_inflation_factor(X.values, X.columns.get_loc(c))
        filas.append({"Variable": ETIQUETAS[c], "VIF": v})
    return pd.DataFrame(filas).sort_values("VIF", ascending=False)


def tendencia(df: pd.DataFrame, var: str) -> dict:
    """Regresion lineal de una variable sobre el año, con banda de confianza al 95%."""
    sub = df[["anio", var]].dropna()
    X = sm.add_constant(sub["anio"])
    modelo = sm.OLS(sub[var], X).fit()
    frame = modelo.get_prediction(X).summary_frame(alpha=0.05)
    b = float(modelo.params["anio"])
    return {
        "sub": sub,
        "modelo": modelo,
        "b": b,
        "ee": float(modelo.bse["anio"]),
        "t": float(modelo.tvalues["anio"]),
        "p": float(modelo.pvalues["anio"]),
        "r2": float(modelo.rsquared),
        "cambio": b * (sub["anio"].max() - sub["anio"].min()),
        "yhat": frame["mean"].values,
        "ic_inf": frame["mean_ci_lower"].values,
        "ic_sup": frame["mean_ci_upper"].values,
    }


def atipicos_iqr(serie: pd.Series, k: float = 1.5) -> tuple[pd.Series, float, float]:
    """Marca los valores fuera de [Q1 - k·IQR, Q3 + k·IQR]. Devuelve (mascara, limite inf, limite sup)."""
    q1, q3 = serie.quantile([0.25, 0.75])
    iqr = q3 - q1
    inf, sup = q1 - k * iqr, q3 + k * iqr
    return (serie < inf) | (serie > sup), float(inf), float(sup)


def detrendizar(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Reemplaza cada variable por el residuo de su regresion lineal sobre el año."""
    out = df[["anio"]].copy()
    X = sm.add_constant(df["anio"])
    for c in cols:
        out[c] = sm.OLS(df[c], X).fit().resid
    return out


def matriz_r_p(df: pd.DataFrame, cols: list[str]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Matrices de r de Pearson y de p-valores."""
    R = pd.DataFrame(np.eye(len(cols)), index=cols, columns=cols)
    P = pd.DataFrame(np.zeros((len(cols), len(cols))), index=cols, columns=cols)
    for i, a in enumerate(cols):
        for b in cols[i + 1 :]:
            r, p = stats.pearsonr(df[a], df[b])
            R.loc[a, b] = R.loc[b, a] = r
            P.loc[a, b] = P.loc[b, a] = p
    return R, P


def heatmap_correlacion(R: pd.DataFrame, P: pd.DataFrame, titulo: str, lim: float = 0.7) -> go.Figure:
    """Heatmap de correlacion con r y p en cada celda; la diagonal se enmascara."""
    etiquetas = [ETIQUETAS[c].split(" (")[0] for c in R.columns]
    Z = R.values.copy()
    np.fill_diagonal(Z, np.nan)
    fig = go.Figure(
        go.Heatmap(
            z=Z, x=etiquetas, y=etiquetas, zmin=-lim, zmax=lim,
            colorscale=[
                [0.00, "#7FB4E4"],
                [0.25, "#2E6FA8"],
                [0.50, "#1A2637"],
                [0.75, "#C2714F"],
                [1.00, "#E8896A"],
            ],
            xgap=2, ygap=2, hoverongaps=False, showscale=False,
            hovertemplate="%{y} ↔ %{x}<br/>r = %{z:+.3f}<extra></extra>",
        )
    )
    for i in range(len(Z)):
        for j in range(len(Z)):
            if i == j:
                continue
            v, p = Z[i, j], P.values[i, j]
            fig.add_annotation(
                x=etiquetas[j], y=etiquetas[i],
                text=f"<b>{v:+.2f}</b><br><span style='font-size:10px'>p {fmt_p(p)}</span>"
                + (" ★" if p < 0.05 else ""),
                showarrow=False,
                font=dict(size=13, color=TEXTO if abs(v) / lim < 0.6 else FONDO),
            )
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=14, color=GRAF["titulo"]), x=0.01, xanchor="left"),
        height=380, margin=dict(l=100, r=15, t=80, b=20),
        paper_bgcolor=FONDO, plot_bgcolor=FONDO,
        font=dict(family="Inter, sans-serif", size=12, color=GRAF["texto"]),
    )
    fig.update_xaxes(showgrid=False, side="top", ticks="", linecolor=GRAF["linea"])
    fig.update_yaxes(showgrid=False, autorange="reversed", ticks="", linecolor=GRAF["linea"])
    return fig


def fmt_p(p: float) -> str:
    """p-valor legible: por debajo de 0,001 no aporta mostrar mas decimales."""
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def fisher_z(r1: float, n1: int, r2: float, n2: int) -> tuple[float, float]:
    """Test de Fisher para comparar dos correlaciones independientes."""
    z1, z2 = np.arctanh(r1), np.arctanh(r2)
    se = np.sqrt(1 / (n1 - 3) + 1 / (n2 - 3))
    z = (z1 - z2) / se
    p = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p


def regresion_lineal(x: np.ndarray, y: np.ndarray) -> dict:
    """OLS simple: devuelve coeficientes, ajuste y banda de confianza al 95%."""
    X = sm.add_constant(x)
    modelo = sm.OLS(y, X).fit()
    grid = np.linspace(x.min() - 2, x.max() + 2, 120)
    pred = modelo.get_prediction(sm.add_constant(grid, has_constant="add"))
    frame = pred.summary_frame(alpha=0.05)
    return {
        "modelo": modelo,
        "grid": grid,
        "yhat": frame["mean"].values,
        "ic_inf": frame["mean_ci_lower"].values,
        "ic_sup": frame["mean_ci_upper"].values,
    }


def _hex_a(hex_color: str, alpha: float) -> str:
    """Convierte un color '#RRGGBB' en 'rgba(r, g, b, alpha)'."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def plantilla_grafico(fig: go.Figure, titulo: str = "", alto: int = 420) -> go.Figure:
    """Aplica un estilo limpio y consistente a los graficos Plotly (fondo oscuro)."""
    fig.update_layout(
        title=dict(text=titulo, font=dict(size=14, color=GRAF["titulo"]), x=0.01, xanchor="left", y=0.97)
        if titulo
        else None,
        height=alto,
        margin=dict(l=62, r=26, t=58 if titulo else 26, b=56),
        paper_bgcolor=FONDO,
        plot_bgcolor=FONDO,
        font=dict(family="Inter, -apple-system, sans-serif", size=12, color=GRAF["texto"]),
        colorway=list(COLORES.values()),
        hoverlabel=dict(bgcolor=FONDO_2, font=dict(size=12, color=TEXTO),
                        bordercolor=BORDE, font_family="Inter, sans-serif"),
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="right", x=1,
                    font=dict(size=11, color=GRAF["texto"])),
    )
    fig.update_xaxes(showgrid=False, linecolor=GRAF["linea"], linewidth=1,
                     zeroline=False, ticks="outside", ticklen=4, tickcolor=GRAF["linea"],
                     title_font=dict(size=11, color=TEXTO_3), tickfont=dict(size=11, color=GRAF["texto"]))
    fig.update_yaxes(gridcolor=GRAF["grid"], linecolor=GRAF["linea"], linewidth=1,
                     zeroline=False, ticks="outside", ticklen=4, tickcolor=GRAF["linea"],
                     title_font=dict(size=11, color=TEXTO_3), tickfont=dict(size=11, color=GRAF["texto"]))
    return fig


# ----------------------------------------------------------------------------
# HELPERS DE PRESENTACION
# ----------------------------------------------------------------------------
def tarjeta(valor: str, titulo: str, nota: str = "", color: str = TEXTO) -> None:
    st.markdown(
        f"""
        <div class="card">
            <div class="card-titulo">{titulo}</div>
            <div class="card-valor" style="color:{color}">{valor}</div>
            {f'<div class="card-nota">{nota}</div>' if nota else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def que_demuestra(texto: str, como_leer: str = "") -> None:
    """Recuadro debajo de un grafico: como se lee y que demuestra."""
    # "p < 0.001" debe mostrarse como texto, no interpretarse como etiqueta HTML.
    texto = texto.replace("= < ", "< ").replace("< ", "&lt; ")
    como_leer = como_leer.replace("< ", "&lt; ")
    leer = f'<div class="lectura-leer"><strong>Cómo leerlo.</strong> {como_leer}</div>' if como_leer else ""
    st.markdown(
        f'<div class="lectura"><div class="lectura-titulo">Qué demuestra este gráfico</div>'
        f"{leer}<div>{texto}</div></div>",
        unsafe_allow_html=True,
    )


def fuerza(r: float) -> tuple[str, str]:
    """Clasifica la magnitud de una correlacion. Devuelve (chip, descripcion)."""
    a = abs(r)
    if a < 0.10:
        return "chip-ok", "Despreciable"
    if a < 0.30:
        return "chip-ok", "Debil"
    if a < 0.50:
        return "chip-warn", "Moderada"
    if a < 0.70:
        return "chip-warn", "Fuerte"
    return "chip-bad", "Muy fuerte"


# ----------------------------------------------------------------------------
# DATOS
# ----------------------------------------------------------------------------
df = cargar_datos()

OBJ3_COLS = ["pbi", "gei", "lluvia"]
VARS4 = ["pbi", "temp"]

datos_completos = df.dropna(subset=OBJ3_COLS + ["temp"]).copy()

mitad1 = datos_completos[datos_completos["anio"] <= MITAD_CORTE]
mitad2 = datos_completos[datos_completos["anio"] > MITAD_CORTE]

# ----------------------------------------------------------------------------
# SIDEBAR
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="eyebrow">Trabajo academico</div>'
        '<div style="font-size:1.15rem;font-weight:700;letter-spacing:-.02em;line-height:1.3">'
        "Cambio climatico y PBI<br/>Argentina 1961–2024</div>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown('<div class="card-titulo">Navegacion</div>', unsafe_allow_html=True)

    pagina = st.radio(
        "Seccion",
        ["Inicio", "Objetivo 1 · Descripcion de variables", "Objetivo 2 · Relacion PBI y clima",
         "Objetivo 3 · Multicolinealidad", "Objetivo 4 · Estabilidad temporal", "Metodologia"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown('<div class="card-titulo">Datos</div>', unsafe_allow_html=True)
    st.caption(f"Periodo analizado: **{ANIO_MIN}–{ANIO_MAX}**")
    st.caption(f"Observaciones completas: **{len(datos_completos)} años**")
    st.caption("Fuente: `dataset_nacional.csv`")

    st.markdown("---")
    with st.expander("Datos crudos"):
        st.dataframe(df, width="stretch", hide_index=True, height=320)


# ----------------------------------------------------------------------------
# PAGINA: INICIO
# ----------------------------------------------------------------------------
if pagina == "Inicio":
    st.markdown('<div class="eyebrow">Presentacion</div>', unsafe_allow_html=True)
    st.markdown("# Cambio climatico y crecimiento economico en Argentina")

    st.markdown(
        '<div class="callout">'
        "<strong>Pregunta principal.</strong> ¿Existe una relacion entre el crecimiento economico (PBI) "
        "y el cambio climatico en Argentina entre 1961 y 2024, y es posible predecir la evolucion de la "
        "temperatura a partir de las variables economicas y climaticas?<br/><br/>"
        "<strong>Esta interfaz presenta los objetivos 1 a 4.</strong> Los objetivos 5 y 6 (modelos "
        "predictivos y evaluacion frente al baseline) quedan fuera de alcance."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## Pregunta de investigacion y objetivos")
    st.markdown(
        '<div class="eyebrow">Encuadre teorico</div>',
        unsafe_allow_html=True,
    )

    col = st.columns(2, gap="large")

    with col[0]:
        st.markdown(
            """
            **Objetivo 1 — Descripcion de cada variable**

            Describir como cambio cada variable año por año: magnitud del cambio, tendencia y años
            atipicos.

            *Se mide con:* grafico de linea, regresion lineal sobre el tiempo y atipicos por IQR.
            """
        )
        st.markdown(
            """
            **Objetivo 2 — Relacion entre el PBI y el clima**

            Evaluar si el PBI se relaciona con las variables climaticas, distinguiendo una relacion
            real de una que solo aparece porque las series comparten tendencia.

            *Se mide con:* matriz de Pearson con p-valor, con los datos originales y sin tendencia.
            """
        )
        st.markdown(
            """
            **Objetivo 3 — Multicolinealidad**

            Verificar que el PBI, los GEI y la lluvia no se pisen entre si. Si dos variables se movieran
            siempre juntas estarian diciendo lo mismo, y en un modelo de regresion no se podria separar
            el efecto de cada una.

            *Se mide con:* matriz de correlacion de Pearson, p-valores y el VIF.
            """
        )
        st.markdown(
            f"""
            **Objetivo 4 — Estabilidad temporal**

            Comprobar si la relacion entre PBI y temperatura se modifico a lo largo del periodo,
            partiendo los 64 años en dos mitades (1961–1992 / 1993–2024).

            *Se mide con:* correlacion por subperiodo, test de Fisher y comparacion de rectas de ajuste.
            """
        )

    with col[1]:
        st.markdown("### Variables del estudio")
        st.markdown(
            f"""
            | Variable | Descripcion | Unidad |
            |---|---|---|
            | Temperatura | Anomalia termica media nacional | °C |
            | PBI | Crecimiento del producto bruto interno | % anual |
            | GEI | Emisiones de gases de efecto invernadero, en CO2 equivalente | MtCO2eq |
            | Lluvia | Anomalia de precipitacion nacional | % |
            """
        )
        st.markdown(
            '<div class="callout callout-warn">'
            "<strong>Nota sobre la ventana temporal.</strong> El archivo original incluye el año 2025, "
            "pero sin dato de GEI y con cobertura incompleta de PBI per capita. Se trabaja "
            f"<strong>1961–2024</strong> para mantener las {len(datos_completos)} observaciones "
            "comparables entre todas las variables."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")

    st.markdown("### Hallazgos de los cuatro objetivos")

    t_temp, t_gei = tendencia(df, "temp"), tendencia(df, "gei")
    base_ini = df.dropna(subset=VARS_ESTUDIO)
    R_n, _ = matriz_r_p(base_ini, VARS_ESTUDIO)
    R_d, P_d = matriz_r_p(detrendizar(base_ini, VARS_ESTUDIO), VARS_ESTUDIO)

    c1, c2 = st.columns(2, gap="large")
    with c1:
        tarjeta(
            f"{t_temp['b']:+.3f} °C/año",
            "Objetivo 1 · Descripcion de variables",
            f"La temperatura sube {t_temp['cambio']:+.2f} °C en el periodo (p {fmt_p(t_temp['p'])}) "
            f"y los GEI {t_gei['b']:+.2f} MtCO2eq/año. PBI y lluvia no tienen tendencia.",
            color=COLORES["temp"],
        )
        st.markdown(
            '<span class="chip chip-info">Temperatura y GEI con tendencia</span>'
            '<span class="chip chip-warn">Ningun valor anual atipico</span>',
            unsafe_allow_html=True,
        )
    with c2:
        r_tasa_ini = stats.pearsonr(base_ini["pbi"].iloc[1:], (base_ini["gei"].pct_change() * 100).iloc[1:])[0]
        tarjeta(
            "Si, a traves del GEI",
            "Objetivo 2 · Relacion PBI y clima",
            f"PBI–GEI: {R_d.loc['pbi', 'gei']:+.2f} sin tendencia (p = {fmt_p(P_d.loc['pbi', 'gei'])}) y "
            f"{r_tasa_ini:+.2f} comparando crecimiento con crecimiento. Con la temperatura "
            f"({R_d.loc['pbi', 'temp']:+.2f}) y las precipitaciones ({R_d.loc['pbi', 'lluvia']:+.2f}) no hay "
            f"relacion. Temperatura–GEI ({R_n.loc['temp', 'gei']:+.2f} → {R_d.loc['temp', 'gei']:+.2f}) es espuria.",
            color=SEM["ok"],
        )
        st.markdown(
            '<span class="chip chip-ok">PBI se relaciona con el GEI</span>'
            '<span class="chip chip-warn">Sin relacion con temperatura ni lluvia</span>'
            '<span class="chip chip-bad">Correlacion Temp–GEI espuria</span>',
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")

    # Pre-calculos para las tarjetas
    pares = pares_correlacion(datos_completos, OBJ3_COLS)
    r_max = float(pares["r_abs"].max())
    vifs = vif(datos_completos, OBJ3_COLS)
    vif_max = float(vifs["VIF"].max())

    r1, p1 = stats.pearsonr(mitad1["pbi"], mitad1["temp"])
    r2, p2 = stats.pearsonr(mitad2["pbi"], mitad2["temp"])
    z_f, p_f = fisher_z(r1, len(mitad1), r2, len(mitad2))

    with c1:
        tarjeta(
            "Independientes",
            "Objetivo 3 · Multicolinealidad",
            f"La correlacion mas fuerte entre pares es {r_max:.3f}. "
            f"VIF maximo {vif_max:.2f} (umbral 5). Ningun par es significativo al 5%.",
            color=SEM["ok"],
        )
        st.markdown(
            '<span class="chip chip-ok">Sin multicolinealidad</span>'
            '<span class="chip chip-info">Las 3 variables se pueden usar juntas</span>',
            unsafe_allow_html=True,
        )

    with c2:
        tarjeta(
            f"{r1:.2f}  /  {r2:.2f}",
            "Objetivo 4 · Estabilidad temporal",
            f"PBI–Temperatura en 1961–1992 y en 1993–2024. "
            f"Diferencia no significativa (p = {p_f:.3f}). La relacion no cambio.",
            color=SEM["bad"],
        )
        st.markdown(
            '<span class="chip chip-bad">Relacion debil</span>'
            '<span class="chip chip-warn">p > 0,05 en ambas mitades</span>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### Vista rapida de las cuatro variables")
    st.caption("Graficos de linea, 1961–2024. Suavizado opcional con media movil de 5 anos.")

    ventana = st.slider("Ventana de la media movil", 1, 11, 5, step=2,
                        help="1 = sin suavizado. Un valor mayor reduce el ruido de corto plazo.")

    cols_t = st.columns(4, gap="medium")
    for c, var in zip(cols_t, ["temp", "pbi", "gei", "lluvia"]):
        sub = df[["anio", var]].dropna()
        color = COLORES[var]
        f = go.Figure()
        if ventana > 1:
            # Serie anual: tenue y fina, al fondo
            f.add_trace(
                go.Scatter(
                    x=sub["anio"], y=sub[var], mode="lines",
                    line=dict(color=color, width=1, shape="spline", smoothing=0.6),
                    opacity=0.28, name="Anual",
                    hovertemplate="Anio %{x}<br/>%{y:.2f}<extra>Anual</extra>",
                )
            )
            f.add_trace(
                go.Scatter(
                    x=sub["anio"], y=sub[var].rolling(ventana, min_periods=1).mean(),
                    mode="lines", line=dict(color=color, width=2.5, shape="spline", smoothing=0.6),
                    name=f"Media movil {ventana}",
                    hovertemplate="Anio %{x}<br/>%{y:.2f}<extra>Media movil</extra>",
                )
            )
        else:
            f.add_trace(
                go.Scatter(
                    x=sub["anio"], y=sub[var], mode="lines",
                    line=dict(color=color, width=2, shape="spline", smoothing=0.6),
                    name=ETIQUETAS[var], hovertemplate="Anio %{x}<br/>%{y:.2f}<extra></extra>",
                )
            )
        f = plantilla_grafico(f, ETIQUETAS[var], alto=270)
        f.update_layout(margin=dict(l=45, r=12, t=48, b=40), showlegend=ventana > 1)
        f.update_yaxes(title=None, tickfont=dict(size=10))
        f.update_xaxes(title=None, tickfont=dict(size=10), dtick=10)
        with c:
            st.plotly_chart(f, width="stretch", config={"displayModeBar": False})


# ----------------------------------------------------------------------------
# PAGINA: OBJETIVO 1
# ----------------------------------------------------------------------------
elif pagina == "Objetivo 1 · Descripcion de variables":

    def u_cambio(v: str) -> str:
        """Unidad de un cambio: el de una variable ya expresada en % se mide en puntos porcentuales."""
        return "pp" if UNIDADES[v][0] == "%" else UNIDADES[v][0]

    st.markdown('<div class="eyebrow">Objetivo especifico 1</div>', unsafe_allow_html=True)
    st.markdown("# Descripción de cada variable")
    st.markdown(
        '<div class="callout">'
        "<strong>Qué se busca.</strong> Antes de relacionar variables entre sí hay que conocer cada una "
        "por separado: cuánto cambió en 64 años, si tiene una tendencia sostenida o solo oscila, y qué "
        "años se salen de lo normal. Para eso se ajusta una regresión lineal de cada variable sobre el "
        "tiempo y se buscan atípicos con el rango intercuartílico (IQR)."
        "</div>",
        unsafe_allow_html=True,
    )

    tends = {v: tendencia(df, v) for v in VARS_ESTUDIO}

    # --- 1. Informe de tendencia ---
    st.markdown("## 1. Informe de tendencia")
    st.caption(
        "Modelo: variable = a + b · año. La pendiente b es el cambio promedio por año. "
        "H0: b = 0 (no hay tendencia). Si el p-valor es menor a 0,05 la tendencia se considera real."
    )

    cols_k = st.columns(4, gap="medium")
    for c, v in zip(cols_k, VARS_ESTUDIO):
        t = tends[v]
        _, u_pend, dec = UNIDADES[v]
        with c:
            tarjeta(
                f"{t['b']:+.{dec}f}",
                ETIQUETAS[v].split(" (")[0],
                f"{u_pend} · p = {fmt_p(t['p'])} · R² = {t['r2']:.2f}",
                color=COLORES[v],
            )
            st.markdown(
                '<span class="chip chip-info">Con tendencia</span>' if t["p"] < 0.05
                else '<span class="chip chip-warn">Sin tendencia</span>',
                unsafe_allow_html=True,
            )

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

    # Control de autocorrelacion de los residuos: Durbin-Watson (ideal cerca de 2) y p-valor de la
    # pendiente con errores robustos HAC (Newey-West, 3 rezagos), que corrigen esa dependencia.
    control = {}
    for v in VARS_ESTUDIO:
        e = tends[v]["modelo"].resid.values
        robusto = tends[v]["modelo"].get_robustcov_results(cov_type="HAC", maxlags=3)
        control[v] = (float(np.sum(np.diff(e) ** 2) / np.sum(e ** 2)), float(robusto.pvalues[1]))

    filas_t = []
    for v in VARS_ESTUDIO:
        t = tends[v]
        u_nivel, u_pend, dec = UNIDADES[v]
        dw, p_hac = control[v]
        filas_t.append(
            {
                "Variable": ETIQUETAS[v],
                "Pendiente (b)": f"{t['b']:+.{dec + 1}f} {u_pend}",
                "Error estándar": f"{t['ee']:.{dec + 1}f}",
                "t": f"{t['t']:+.2f}",
                "p-valor": fmt_p(t["p"]),
                "R²": f"{t['r2']:.3f}",
                f"Cambio {ANIO_MIN}–{ANIO_MAX}": f"{t['cambio']:+.{dec - 1 if dec > 2 else 1}f} {u_cambio(v)}",
                "n": len(t["sub"]),
                "Durbin-Watson": f"{dw:.2f}",
                "p robusto (HAC)": fmt_p(p_hac),
                "Tendencia": "Significativa" if t["p"] < 0.05 else "No significativa",
            }
        )
    st.dataframe(
        pd.DataFrame(filas_t).style.map(
            lambda v: (
                "background-color:#16283A; color:#7FB4E4"
                if v == "Significativa"
                else f"background-color:{SEM['warn_bg']}; color:{SEM['warn']}"
            ),
            subset=["Tendencia"],
        ),
        width="stretch",
        hide_index=True,
    )

    con_tend = [ETIQUETAS[v].split(" (")[0] for v in VARS_ESTUDIO if tends[v]["p"] < 0.05]
    sin_tend = [ETIQUETAS[v].split(" (")[0] for v in VARS_ESTUDIO if tends[v]["p"] >= 0.05]
    st.markdown(
        '<div class="callout">'
        f"<strong>Dos comportamientos distintos.</strong> {' y '.join(con_tend)} tienen una tendencia "
        f"creciente clara (p < 0,05). {' y '.join(sin_tend)} no: oscilan alrededor de su promedio sin "
        "subir ni bajar de forma sostenida. Esta diferencia es clave para el objetivo 2, porque dos "
        "series que crecen juntas en el tiempo aparecen correlacionadas aunque no tengan relación real."
        "</div>",
        unsafe_allow_html=True,
    )

    dependientes = [f"{ETIQUETAS[v].split(' (')[0]} ({control[v][0]:.2f})"
                    for v in VARS_ESTUDIO if control[v][0] < 1.5]
    coinciden = all((tends[v]["p"] < 0.05) == (control[v][1] < 0.05) for v in VARS_ESTUDIO)
    st.markdown(
        '<div class="callout">'
        "<strong>Control de la recta: Durbin-Watson y p robusto.</strong> La recta supone que el desvío "
        "de un año respecto de la tendencia no depende del año anterior. <strong>Durbin-Watson</strong> "
        "lo revisa: cerca de 2 está bien; cuanto más cerca de 0, más dependencia hay. "
        + (
            f"Hay dependencia en {' y '.join(dependientes)}. "
            if dependientes
            else "Ninguna variable muestra una dependencia fuerte. "
        )
        + "El <strong>p robusto (HAC)</strong> recalcula la significancia corrigiendo esa dependencia. "
        + (
            "Las cuatro conclusiones se mantienen: las variables con tendencia la siguen teniendo y las "
            "que no la tenían tampoco la ganan."
            if coinciden
            else "Al menos una conclusión cambia con el p robusto; hay que revisarla."
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    # --- 2. Evolucion de una variable ---
    st.markdown("## 2. Evolución y recta de tendencia")
    st.caption("Elegí una variable para ver su detalle. La selección aplica a las secciones 2, 3 y 4.")

    nombres = {ETIQUETAS[v].split(" (")[0]: v for v in VARS_ESTUDIO}
    elegida = st.radio("Variable", list(nombres), horizontal=True, label_visibility="collapsed")
    var = nombres[elegida]
    t = tends[var]
    sub = t["sub"]
    color = COLORES[var]
    u_nivel, u_pend, dec = UNIDADES[var]
    u_cam = u_cambio(var)

    i_max, i_min = sub[var].idxmax(), sub[var].idxmin()
    a, b_, c, d = st.columns(4, gap="medium")
    with a:
        tarjeta(f"{sub[var].iloc[0]:+.{dec - 1}f}", f"Valor en {int(sub['anio'].iloc[0])}", u_nivel, color=TEXTO_2)
    with b_:
        tarjeta(f"{sub[var].iloc[-1]:+.{dec - 1}f}", f"Valor en {int(sub['anio'].iloc[-1])}", u_nivel, color=color)
    with c:
        tarjeta(f"{sub.loc[i_max, var]:+.{dec - 1}f}", "Máximo",
                f"Año {int(sub.loc[i_max, 'anio'])} · {u_nivel}", color=TEXTO)
    with d:
        tarjeta(f"{sub.loc[i_min, var]:+.{dec - 1}f}", "Mínimo",
                f"Año {int(sub.loc[i_min, 'anio'])} · {u_nivel}", color=TEXTO)

    mask_niv, inf_niv, sup_niv = atipicos_iqr(sub[var])

    fig_t = go.Figure()
    fig_t.add_trace(
        go.Scatter(
            x=np.concatenate([sub["anio"], sub["anio"][::-1]]),
            y=np.concatenate([t["ic_sup"], t["ic_inf"][::-1]]),
            fill="toself", fillcolor=_hex_a(GRAF["ajuste"], 0.12),
            line=dict(width=0), hoverinfo="skip", showlegend=False,
        )
    )
    fig_t.add_trace(
        go.Scatter(
            x=sub["anio"], y=sub[var], mode="lines+markers", name="Serie anual",
            line=dict(color=color, width=1.8), marker=dict(size=5, color=color),
            hovertemplate="Año %{x}<br/>%{y:.2f} " + u_nivel + "<extra></extra>",
        )
    )
    fig_t.add_trace(
        go.Scatter(
            x=sub["anio"], y=t["yhat"], mode="lines", name=f"Tendencia ({t['b']:+.{dec}f} {u_pend})",
            line=dict(color=GRAF["ajuste"], width=2, dash="dash"), hoverinfo="skip",
        )
    )
    if mask_niv.any():
        fig_t.add_trace(
            go.Scatter(
                x=sub.loc[mask_niv, "anio"], y=sub.loc[mask_niv, var], mode="markers", name="Atípico (IQR)",
                marker=dict(size=11, color=SEM["bad"], line=dict(width=1, color=FONDO)),
                hovertemplate="Atípico %{x}<br/>%{y:.2f}<extra></extra>",
            )
        )
    for idx, txt in [(i_max, "Máx"), (i_min, "Mín")]:
        fig_t.add_annotation(
            x=sub.loc[idx, "anio"], y=sub.loc[idx, var],
            text=f"{txt} {int(sub.loc[idx, 'anio'])}", showarrow=True, arrowhead=0,
            arrowcolor=GRAF["ref"], ax=0, ay=-26 if txt == "Máx" else 26,
            font=dict(size=10, color=TEXTO_2),
        )
    if var != "gei":
        fig_t.add_hline(y=0, line=dict(color=GRAF["ref"], width=1, dash="dot"))
    fig_t.update_xaxes(title="Año", dtick=5)
    fig_t.update_yaxes(title=ETIQUETAS[var])
    fig_t = plantilla_grafico(
        fig_t,
        f"{ETIQUETAS[var]}   ·   b = {t['b']:+.{dec + 1}f} {u_pend}, p = {fmt_p(t['p'])}, R² = {t['r2']:.3f}",
        alto=440,
    )
    st.plotly_chart(fig_t, width="stretch", config={"displayModeBar": False})

    ic_inf_b, ic_sup_b = (float(x) for x in t["modelo"].conf_int().loc["anio"])
    nom_art = {"temp": "la temperatura", "pbi": "el crecimiento del PBI",
               "gei": "las emisiones de GEI", "lluvia": "la lluvia"}[var]
    verbo = "tienen" if var == "gei" else "tiene"
    lecturas = {
        "temp": (
            f"La temperatura sube {t['b']:+.3f} °C por año, unos <strong>{t['cambio']:+.2f} °C</strong> "
            f"en todo el período. El año más cálido es {int(sub.loc[i_max, 'anio'])} "
            f"({sub.loc[i_max, var]:+.2f} °C). Es la tendencia que da sentido al estudio: el calentamiento "
            "en Argentina es real y sostenido."
        ),
        "pbi": (
            f"Oscila alrededor de un "
            f"promedio de {sub[var].mean():.2f}% anual con un desvío de {sub[var].std():.2f} puntos: su "
            "comportamiento lo dominan los ciclos y las crisis, no una dirección de largo plazo."
        ),
        "gei": (
            f"Las emisiones crecen {t['b']:+.2f} MtCO2eq por año (R² = {t['r2']:.2f}). Pasaron de "
            f"{sub[var].iloc[0]:.0f} a {sub[var].iloc[-1]:.0f} MtCO2eq: el año explica casi toda su "
            "variación. Es la serie con la tendencia más marcada."
        ),
        "lluvia": (
            f"Alterna años secos y húmedos entre "
            f"{sub[var].min():+.1f}% y {sub[var].max():+.1f}% sin un patrón de largo plazo a escala nacional."
        ),
    }
    if t["p"] < 0.05:
        demuestra_t = (
            f"<strong>Que {nom_art} {verbo} una tendencia real.</strong> Toda la banda gris está "
            "inclinada: ni siquiera la recta más plana compatible con los datos es horizontal. Con 95% de "
            f"confianza, el cambio por año está entre {ic_inf_b:+.{dec + 1}f} y {ic_sup_b:+.{dec + 1}f} "
            f"{u_pend}; el intervalo no incluye el cero, por eso p = {fmt_p(t['p'])}. "
        )
    else:
        demuestra_t = (
            f"<strong>Que {nom_art} no {verbo} tendencia.</strong> La recta es casi plana y dentro "
            "de la banda gris caben rectas que suben, que bajan y horizontales: con 95% de confianza el "
            f"cambio por año está entre {ic_inf_b:+.{dec + 1}f} y {ic_sup_b:+.{dec + 1}f} {u_pend}, un "
            f"intervalo que incluye el cero (p = {fmt_p(t['p'])}). "
        )
    que_demuestra(
        demuestra_t + lecturas[var],
        como_leer="Cada punto es un año. La línea gris punteada es la recta de tendencia y la banda gris "
        "sombreada es su intervalo de confianza del 95%: el rango donde está la recta verdadera.",
    )

    # --- 3. Promedio por decada y distribucion ---
    st.markdown("## 3. Promedio por década y distribución")
    st.caption("Dos formas de resumir los 64 años: por décadas y como reparto de los valores anuales.")

    dec_df = sub.assign(decada=(sub["anio"] // 10) * 10).groupby("decada")[var].mean().reset_index()
    d_ini, d_fin = dec_df.iloc[0], dec_df.iloc[-1]
    n_ult = int((sub["anio"] >= d_fin["decada"]).sum())
    c1, c2 = st.columns([1.6, 1], gap="medium")
    with c1:
        fig_d = go.Figure(
            go.Bar(
                x=[f"{int(x)}s" for x in dec_df["decada"]], y=dec_df[var],
                marker=dict(color=[_hex_a(color, 0.45 + 0.55 * i / (len(dec_df) - 1)) for i in range(len(dec_df))],
                            line=dict(width=0)),
                text=[f"{y:+.{dec - 1}f}" for y in dec_df[var]], textposition="outside",
                textfont=dict(size=12, color=TEXTO_2),
                hovertemplate="Década %{x}<br/>Promedio %{y:.2f}<extra></extra>",
            )
        )
        if var != "gei":
            fig_d.add_hline(y=0, line=dict(color=GRAF["ref"], width=1))
        rango = dec_df[var].abs().max() * 1.25
        fig_d.update_yaxes(title=u_nivel, range=[0, rango] if var == "gei" else [-rango, rango])
        fig_d = plantilla_grafico(fig_d, "Promedio por década", alto=340)
        fig_d.update_layout(showlegend=False, bargap=0.35)
        st.plotly_chart(fig_d, width="stretch", config={"displayModeBar": False})
        tramo = (
            f"de {d_ini[var]:+.{dec - 1}f} en los {int(d_ini['decada'])}s a {d_fin[var]:+.{dec - 1}f} "
            f"en los {int(d_fin['decada'])}s"
        )
        que_demuestra(
            (
                f"<strong>Que el cambio es de fondo, no de un año suelto.</strong> Al promediar cada "
                "década se borra el ruido de los años individuales y queda el movimiento de largo plazo, "
                f"que va {tramo}. Es la misma tendencia de la sección 2, vista sin el ruido."
                if t["p"] < 0.05
                else f"<strong>Que no hay movimiento de fondo.</strong> Aun promediando por década, las "
                f"barras suben y bajan sin un orden ({tramo}): no hay una dirección de largo plazo. Es la "
                "misma conclusión de la sección 2, vista sin el ruido de cada año."
            )
            + f" <em>La década de {int(d_fin['decada'])} tiene solo {n_ult} años.</em>",
            como_leer="Cada barra es el promedio de los diez años de esa década. Las barras más intensas "
            "son las más recientes.",
        )
    with c2:
        fig_b = go.Figure(
            go.Box(
                y=sub[var], name=elegida, boxpoints="all", jitter=0.45, pointpos=0,
                marker=dict(color=color, size=5, opacity=0.65),
                line=dict(color=color, width=1.5), fillcolor=_hex_a(color, 0.15),
                customdata=sub["anio"],
                hovertemplate="Año %{customdata}<br/>%{y:.2f}<extra></extra>",
            )
        )
        fig_b.update_yaxes(title=u_nivel)
        fig_b = plantilla_grafico(fig_b, "Distribución anual", alto=340)
        fig_b.update_layout(showlegend=False)
        st.plotly_chart(fig_b, width="stretch", config={"displayModeBar": False})
        que_demuestra(
            (
                "<strong>Que ningún año supera el criterio de 1,5 × IQR.</strong> Todos quedan dentro de "
                f"los bigotes, entre {inf_niv:.2f} y {sup_niv:.2f} {u_nivel}. Incluso el máximo "
                f"({int(sub.loc[i_max, 'anio'])}) y el mínimo ({int(sub.loc[i_min, 'anio'])}) de la serie "
                "están dentro de ese límite."
                if not mask_niv.any()
                else f"<strong>Que hay {int(mask_niv.sum())} valores anuales atípicos</strong>, fuera "
                f"de {inf_niv:.2f} a {sup_niv:.2f} {u_nivel}."
            ),
            como_leer="Cada punto es un año. La caja contiene al 50% central de los años (de Q1 a Q3) y "
            "la línea interior es la mediana. Los bigotes llegan hasta 1,5 × IQR: un punto afuera sería "
            "atípico.",
        )

    # --- 4. Variacion interanual y atipicos ---
    st.markdown("## 4. Magnitud del cambio año a año")
    st.caption(
        "Se aplica el mismo criterio IQR, pero a los cambios de un año al siguiente en lugar de a los "
        "valores."
    )

    var_ia = sub.set_index("anio")[var].diff().dropna()
    mask_ia, inf_ia, sup_ia = atipicos_iqr(var_ia)

    fig_ia = go.Figure(
        go.Bar(
            x=var_ia.index, y=var_ia.values,
            marker=dict(
                color=[SEM["bad"] if m else _hex_a(color, 0.6) for m in mask_ia],
                line=dict(width=0),
            ),
            hovertemplate="Año %{x}<br/>Cambio %{y:+.2f} " + u_cam + "<extra></extra>",
        )
    )
    for y, lab in [(sup_ia, "Límite superior IQR"), (inf_ia, "Límite inferior IQR")]:
        fig_ia.add_hline(y=y, line=dict(color=SEM["bad"], width=1, dash="dash"),
                         annotation_text=f"{lab} ({y:+.2f})", annotation_position="top left",
                         annotation_font=dict(size=10, color=TEXTO_3))
    fig_ia.add_hline(y=0, line=dict(color=GRAF["ref"], width=1))
    fig_ia.update_xaxes(title="Año", dtick=5)
    fig_ia.update_yaxes(title=f"Cambio interanual ({u_cam})")
    fig_ia = plantilla_grafico(fig_ia, f"Variación interanual · {ETIQUETAS[var]}", alto=360)
    fig_ia.update_layout(showlegend=False, bargap=0.25)
    st.plotly_chart(fig_ia, width="stretch", config={"displayModeBar": False})
    saltos = ", ".join(f"{int(an)} ({vl:+.2f})" for an, vl in var_ia[mask_ia].items())
    que_demuestra(
        f"<strong>Cuánto se {'mueven' if var == 'gei' else 'mueve'} {nom_art} de un año al otro y qué "
        f"saltos son anormales.</strong> En promedio "
        f"{'cambian' if var == 'gei' else 'cambia'} {var_ia.abs().mean():.2f} "
        f"{u_cam} por año, en una u otra dirección. "
        + (
            f"{'Hay ' + str(int(mask_ia.sum())) + ' saltos' if mask_ia.sum() > 1 else 'Hay un salto'} "
            f"fuera de los límites, en rojo: {saltos}. Son quiebres bruscos, no errores de medición."
            if mask_ia.any()
            else "Ningún salto supera los límites: los cambios de un año al otro son graduales."
        ),
        como_leer="Cada barra es el cambio respecto del año anterior: hacia arriba subió y hacia abajo "
        "bajó. Las líneas rojas punteadas son los límites de 1,5 × IQR calculados sobre estos cambios.",
    )

    a, b_, c = st.columns(3, gap="medium")
    with a:
        tarjeta(f"{var_ia.abs().mean():.2f}", "Cambio medio absoluto",
                f"{u_cam} por año", color=color)
    with b_:
        tarjeta(str(int(mask_niv.sum())), "Atípicos en el valor anual",
                f"Fuera de [{inf_niv:.2f}, {sup_niv:.2f}]", color=TEXTO_2)
    with c:
        tarjeta(str(int(mask_ia.sum())), "Atípicos en la variación",
                f"Fuera de [{inf_ia:.2f}, {sup_ia:.2f}]",
                color=SEM["bad"] if mask_ia.any() else TEXTO_2)

    if mask_ia.any():
        st.markdown(
            "".join(
                f'<span class="chip chip-bad">{int(anio)} · {val:+.2f}</span>'
                for anio, val in var_ia[mask_ia].items()
            ),
            unsafe_allow_html=True,
        )

    contexto = {
        "pbi": "Los saltos coinciden con rebotes posteriores a crisis: 2003 tras la caída de 2001–2002 "
               "y 2021 tras la pandemia de 2020.",
        "gei": "La caída de 2020 refleja la menor actividad durante la pandemia, y 2021 el rebote posterior.",
    }
    # Control: el mismo criterio aplicado a cada año contra su tendencia (residuos de la recta).
    mask_res, _, _ = atipicos_iqr(t["modelo"].resid)
    st.markdown(
        '<div class="callout callout-warn">'
        "<strong>Por qué hay atípicos en la variación y no en el valor anual.</strong> Ningún valor anual cae "
        "fuera del rango 1,5 · IQR"
        + (", ni siquiera midiendo cada año contra su tendencia" if not mask_res.any() else "")
        + ". Pero algunos cambios de un año al siguiente sí lo superan. Un atípico en la variación marca un quiebre brusco, no un dato erróneo, "
        "por eso se conservan en el análisis. "
        + (contexto.get(var, "") if mask_ia.any() else "")
        + "</div>"
        if not mask_niv.any()
        else '<div class="callout callout-warn"><strong>Atípicos en el valor anual.</strong> '
        f"Hay {int(mask_niv.sum())} años fuera del rango 1,5 · IQR. Se marcan en rojo en el gráfico "
        "de la sección 2 y se conservan: reflejan eventos reales, no errores de medición.</div>",
        unsafe_allow_html=True,
    )

    # --- 5. Resumen de atipicos ---
    st.markdown("## 5. Resumen de atípicos por variable")
    filas_a = []
    for v in VARS_ESTUDIO:
        s = tends[v]["sub"].set_index("anio")[v]
        m_niv, _, _ = atipicos_iqr(s)
        dv = s.diff().dropna()
        m_ia, _, _ = atipicos_iqr(dv)
        filas_a.append(
            {
                "Variable": ETIQUETAS[v],
                "Atípicos en el valor anual": int(m_niv.sum()),
                "Atípicos en la variación": int(m_ia.sum()),
                "Años con salto atípico": ", ".join(str(int(x)) for x in dv[m_ia].index) or "—",
            }
        )
    st.dataframe(pd.DataFrame(filas_a), width="stretch", hide_index=True)

    # --- 6. Conclusion ---
    tt, tg = tends["temp"], tends["gei"]
    st.markdown("## 6. Conclusión del objetivo")
    st.markdown(
        '<div class="callout callout-ok">'
        f"<strong>Temperatura y emisiones suben; PBI y lluvia no tienen dirección.</strong> La temperatura "
        f"aumenta {tt['b']:+.3f} °C por año (p {fmt_p(tt['p'])}), cerca de {tt['cambio']:+.2f} °C en el "
        f"período, y las emisiones {tg['b']:+.2f} MtCO2eq por año. El crecimiento del PBI y la lluvia "
        "fluctúan sin tendencia significativa. Ningún valor anual supera el criterio de 1,5 × IQR; los saltos atípicos "
        "año a año corresponden a crisis y rebotes conocidos. Como temperatura y emisiones comparten una "
        "tendencia, en el objetivo 2 la correlación debe calcularse también sobre series sin tendencia."
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# PAGINA: OBJETIVO 2
# ----------------------------------------------------------------------------
elif pagina == "Objetivo 2 · Relacion PBI y clima":
    st.markdown('<div class="eyebrow">Objetivo especifico 2</div>', unsafe_allow_html=True)
    st.markdown("# Relación entre el PBI y el clima")
    st.markdown(
        '<div class="callout">'
        "<strong>Qué se busca.</strong> Evaluar si el crecimiento económico se relaciona con el cambio "
        "climático, medido con sus tres indicadores: <strong>temperatura, precipitaciones y emisiones de "
        "GEI</strong>. Toda correlación se reporta dos veces: <strong>con los datos originales</strong> "
        "(tal como vienen) y <strong>sin tendencia</strong> (después de quitarle a cada serie su "
        "subida o bajada de largo plazo; el nombre técnico es <em>detrendizar</em>). Si una correlación desaparece al quitar la tendencia, es espuria y no se "
        "presenta como hallazgo."
        "</div>",
        unsafe_allow_html=True,
    )

    base = df.dropna(subset=VARS_ESTUDIO).copy()
    resid = detrendizar(base, VARS_ESTUDIO)
    R_niv, P_niv = matriz_r_p(base, VARS_ESTUDIO)
    R_det, P_det = matriz_r_p(resid, VARS_ESTUDIO)

    # --- 1. Por que detrendizar ---
    st.markdown("## 1. Por qué hay que quitar la tendencia")
    st.caption(
        "El mismo par, temperatura y GEI, antes y después de quitarles la tendencia."
    )

    def _z(s: pd.Series) -> pd.Series:
        return (s - s.mean()) / s.std()

    leer_z = (
        "Las dos series están estandarizadas: 0 es el promedio de cada una y cada unidad es un desvío "
        "estándar. Así se pueden dibujar juntas aunque una esté en °C y la otra en millones de toneladas."
    )
    textos_s1 = [
        f"<strong>Que con los datos originales las dos series parecen ir juntas</strong> "
        f"(r = {R_niv.loc['temp', 'gei']:+.2f}, p = {fmt_p(P_niv.loc['temp', 'gei'])}). Las dos empiezan "
        "abajo y terminan arriba. Pero lo que comparten es la subida con los años, no lo que pasa en cada "
        "año: con dos series que crecen en el tiempo, la correlación sale alta aunque no tengan relación.",
        f"<strong>Que sin la tendencia las dos series dejan de acompañarse</strong> "
        f"(r = {R_det.loc['temp', 'gei']:+.2f}, p = {fmt_p(P_det.loc['temp', 'gei'])}). Cada una oscila "
        "por su lado: los años más cálidos de lo esperado para su época no coinciden con los años de más "
        "emisiones de lo esperado. La correlación de la izquierda era <strong>espuria</strong>: la "
        "producía el paso del tiempo.",
    ]
    c1, c2 = st.columns(2, gap="medium")
    for c, datos, tit, texto in [
        (c1, base, f"Datos originales · r = {R_niv.loc['temp', 'gei']:+.2f}", textos_s1[0]),
        (c2, resid, f"Sin tendencia · r = {R_det.loc['temp', 'gei']:+.2f}", textos_s1[1]),
    ]:
        f = go.Figure()
        for v in ["temp", "gei"]:
            f.add_trace(
                go.Scatter(
                    x=datos["anio"], y=_z(datos[v]), mode="lines", name=ETIQUETAS[v].split(" (")[0],
                    line=dict(color=COLORES[v], width=2),
                    hovertemplate="Año %{x}<br/>%{y:+.2f} desvíos<extra>" + ETIQUETAS[v].split(" (")[0] + "</extra>",
                )
            )
        f.add_hline(y=0, line=dict(color=GRAF["ref"], width=1, dash="dot"))
        f.update_yaxes(title="Desvíos estándar")
        f.update_xaxes(dtick=10)
        f = plantilla_grafico(f, "Temperatura y GEI · " + tit, alto=330)
        with c:
            st.plotly_chart(f, width="stretch", config={"displayModeBar": False})
            que_demuestra(texto, como_leer=leer_z)

    # --- 2. Matrices ---
    st.markdown("## 2. Matriz de correlación de Pearson")
    st.caption(
        "Cada celda muestra r y su p-valor. H0: no hay relación lineal. La estrella (★) marca los "
        "pares significativos al 5%. La diagonal se omite porque siempre vale 1."
    )
    def _pares_sig(R: pd.DataFrame, P: pd.DataFrame) -> list[str]:
        return [
            f"{ETIQUETAS[a].split(' (')[0]}–{ETIQUETAS[b].split(' (')[0]} ({R.loc[a, b]:+.2f})"
            for i, a in enumerate(VARS_ESTUDIO) for b in VARS_ESTUDIO[i + 1 :] if P.loc[a, b] < 0.05
        ]

    def _lista(items: list[str]) -> str:
        return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " y " + items[-1]

    sig_niv, sig_det = _pares_sig(R_niv, P_niv), _pares_sig(R_det, P_det)
    leer_hm = (
        "Cada celda cruza dos variables: el número grande es r y debajo está el p-valor. La ★ marca "
        "p < 0,05. Terracota = relación positiva, azul = negativa, oscuro = cercana a cero."
    )
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.plotly_chart(heatmap_correlacion(R_niv, P_niv, "Datos originales"),
                        width="stretch", config={"displayModeBar": False})
        que_demuestra(
            f"<strong>Que con los datos originales solo {_lista(sig_niv) if sig_niv else 'ningún par'} "
            f"{'es significativa' if len(sig_niv) == 1 else 'son significativas'}.</strong> El PBI no se "
            f"relaciona con la temperatura ({R_niv.loc['pbi', 'temp']:+.2f}) ni con la lluvia "
            f"({R_niv.loc['pbi', 'lluvia']:+.2f}): sus celdas están oscuras y sin estrella. La única celda "
            "intensa une a las dos variables que suben con los años.",
            como_leer=leer_hm,
        )
    with c2:
        st.plotly_chart(heatmap_correlacion(R_det, P_det, "Sin tendencia (cada año contra lo esperado para su época)"),
                        width="stretch", config={"displayModeBar": False})
        que_demuestra(
            "<strong>Que al quitar la tendencia el mapa cambia.</strong> Temperatura–GEI pasa de "
            f"{R_niv.loc['temp', 'gei']:+.2f} a {R_det.loc['temp', 'gei']:+.2f} y pierde la estrella: era "
            f"espuria. Ahora lo significativo es {_lista(sig_det) if sig_det else 'ningún par'}, una "
            "relación que la tendencia de las emisiones tapaba. El PBI sigue sin relación con la "
            f"temperatura ({R_det.loc['pbi', 'temp']:+.2f}) ni con la lluvia "
            f"({R_det.loc['pbi', 'lluvia']:+.2f}).",
            como_leer=leer_hm,
        )

    # --- 3. Contraste ---
    st.markdown("## 3. Comparación: datos originales vs sin tendencia")
    st.caption(
        "Se compara cada par en las dos versiones. El veredicto sigue la regla del trabajo: solo cuenta "
        "como hallazgo una relación que es significativa una vez quitada la tendencia."
    )

    def veredicto(p_n: float, p_d: float) -> str:
        if p_n < 0.05 and p_d >= 0.05:
            return "Espuria"
        if p_d < 0.05 and p_n >= 0.05:
            return "Aparece sin tendencia"
        if p_d < 0.05:
            return "Se mantiene"
        return "Sin relación"

    filas_c = []
    for i, a in enumerate(VARS_ESTUDIO):
        for b in VARS_ESTUDIO[i + 1 :]:
            filas_c.append(
                {
                    "Par": f"{ETIQUETAS[a].split(' (')[0]}  ↔  {ETIQUETAS[b].split(' (')[0]}",
                    "PBI": "pbi" in (a, b),
                    "r originales": R_niv.loc[a, b],
                    "p originales": P_niv.loc[a, b],
                    "r sin tendencia": R_det.loc[a, b],
                    "p sin tendencia": P_det.loc[a, b],
                    "Veredicto": veredicto(P_niv.loc[a, b], P_det.loc[a, b]),
                }
            )
    contraste = pd.DataFrame(filas_c).sort_values("PBI", ascending=False, kind="stable")

    chip_ver = {
        "Espuria": "chip-bad",
        "Aparece sin tendencia": "chip-info",
        "Se mantiene": "chip-ok",
        "Sin relación": "chip-warn",
    }
    h = st.columns([3, 1.4, 1.4, 2.2], gap="medium")
    for col_h, txt in zip(h, ["Par", "Datos originales", "Sin tendencia", "Veredicto"]):
        col_h.markdown(f'<div class="card-titulo">{txt}</div>', unsafe_allow_html=True)
    for _, row in contraste.iterrows():
        c1, c2, c3, c4 = st.columns([3, 1.4, 1.4, 2.2], gap="medium")
        with c1:
            st.markdown(f"**{row['Par']}**" if row["PBI"] else row["Par"])
        for c, r, p in [(c2, row["r originales"], row["p originales"]),
                        (c3, row["r sin tendencia"], row["p sin tendencia"])]:
            with c:
                st.markdown(
                    f'<div style="font-size:1.15rem;font-weight:600;color:{ACENTO if p < 0.05 else TEXTO_2}">'
                    f'{r:+.3f}</div><div class="card-nota" style="margin-top:0">p = {fmt_p(p)}</div>',
                    unsafe_allow_html=True,
                )
        with c4:
            st.markdown(f'<span class="chip {chip_ver[row["Veredicto"]]}">{row["Veredicto"]}</span>',
                        unsafe_allow_html=True)
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
    st.caption("En negrita, los pares que involucran al PBI (el foco del objetivo).")

    # --- 4. Dispersion por par ---
    st.markdown("## 4. Dispersión de un par, antes y después")
    pares_op = list(contraste["Par"])
    par = st.selectbox("Par de variables", pares_op, index=pares_op.index(
        f"{ETIQUETAS['temp'].split(' (')[0]}  ↔  {ETIQUETAS['pbi'].split(' (')[0]}"))
    fila = contraste[contraste["Par"] == par].iloc[0]
    inv = {ETIQUETAS[v].split(" (")[0]: v for v in VARS_ESTUDIO}
    va, vb = (inv[x.strip()] for x in par.split("↔"))

    # Si las dos variables del par tienen tendencia, la inclinacion de la nube la ordena el tiempo.
    ambas_tend = all(stats.pearsonr(base[v], base["anio"])[1] < 0.05 for v in (va, vb))
    r_o, p_o = fila["r originales"], fila["p originales"]
    r_s, p_s = fila["r sin tendencia"], fila["p sin tendencia"]
    if p_o < 0.05:
        txt_orig = (
            f"<strong>Que con los datos originales hay una relación aparente</strong> (r = {r_o:+.3f}, "
            f"p = {fmt_p(p_o)}): la nube está inclinada. "
            + (
                "Fijate en el color: los años viejos (oscuros) quedan en una punta y los recientes "
                "(claros) en la otra. Lo que ordena la nube es el tiempo, porque las dos variables "
                "suben con los años."
                if ambas_tend
                else "Hay que ver si sobrevive al quitar la tendencia (gráfico de la derecha)."
            )
        )
    else:
        txt_orig = (
            f"<strong>Que con los datos originales no hay relación</strong> (r = {r_o:+.3f}, "
            f"p = {fmt_p(p_o)}): la nube no tiene una inclinación clara y la recta gris es casi plana."
        )
    txt_sin = {
        "Espuria": (
            f"<strong>Que la relación era espuria.</strong> Sin la tendencia los colores se mezclan, la "
            f"nube queda redonda y r cae a {r_s:+.3f} (p = {fmt_p(p_s)}). Lo que se veía a la izquierda "
            "era solo que las dos variables suben con el tiempo."
        ),
        "Aparece sin tendencia": (
            f"<strong>Que al quitar la tendencia aparece una relación que estaba tapada</strong> "
            f"(r = {r_s:+.3f}, p = {fmt_p(p_s)}). La nube se inclina: los años en que una variable "
            "estuvo por encima de lo esperado para su época, la otra también tendió a estarlo."
        ),
        "Se mantiene": (
            f"<strong>Que la relación resiste el control.</strong> Sin la tendencia la nube sigue "
            f"inclinada (r = {r_s:+.3f}, p = {fmt_p(p_s)}): no era un efecto del paso del tiempo."
        ),
        "Sin relación": (
            f"<strong>Que tampoco sin tendencia hay relación</strong> (r = {r_s:+.3f}, "
            f"p = {fmt_p(p_s)}). La nube sigue sin forma: saber cómo fue un año en una variable no ayuda "
            "a adivinar cómo fue en la otra."
        ),
    }[fila["Veredicto"]]
    leer_sc = (
        "Cada punto es un año. El color va de azul apagado (1961) a celeste intenso (2024). La línea "
        "gris es la recta que mejor se ajusta a la nube: cuanto más inclinada, más fuerte la relación."
    )

    escala_año = [[0.0, "#2A4568"], [0.5, "#4A7FB0"], [1.0, "#9CCBEE"]]
    c1, c2 = st.columns(2, gap="medium")
    for c, datos, r, p, tit, suf, texto in [
        (c1, base, r_o, p_o, "Datos originales", "", txt_orig),
        (c2, resid, r_s, p_s, "Sin tendencia", " · residuo", txt_sin),
    ]:
        aj = sm.OLS(datos[va], sm.add_constant(datos[vb])).fit()
        xs = np.linspace(datos[vb].min(), datos[vb].max(), 50)
        f = go.Figure()
        f.add_trace(
            go.Scatter(
                x=datos[vb], y=datos[va], mode="markers",
                marker=dict(size=8, color=datos["anio"], colorscale=escala_año, opacity=0.9,
                            line=dict(width=0.5, color=FONDO)),
                customdata=datos["anio"],
                hovertemplate="Año %{customdata}<br/>x %{x:.2f}<br/>y %{y:.2f}<extra></extra>",
            )
        )
        f.add_trace(
            go.Scatter(x=xs, y=aj.params.iloc[0] + aj.params.iloc[1] * xs, mode="lines",
                       line=dict(color=GRAF["ajuste"], width=2), hoverinfo="skip")
        )
        f.update_xaxes(title=ETIQUETAS[vb] + suf)
        f.update_yaxes(title=ETIQUETAS[va] + suf)
        f = plantilla_grafico(f, f"{tit}   ·   r = {r:+.3f}, p = {fmt_p(p)}", alto=360)
        f.update_layout(showlegend=False)
        with c:
            st.plotly_chart(f, width="stretch", config={"displayModeBar": False})
            que_demuestra(texto, como_leer=leer_sc)

    # --- 5. Robustez ---
    st.markdown("## 5. Robustez: primeras diferencias")
    st.caption(
        "Otra forma de quitar la tendencia es trabajar con el cambio de un año al siguiente. "
        "Si las conclusiones coinciden con la recta de tendencia, son confiables. La columna Spearman "
        "repite la comparación sin tendencia, pero ordenando los años de menor a mayor en lugar de usar "
        "los valores: así los años extremos, como las crisis, no pesan de más."
    )
    dif = base[VARS_ESTUDIO].diff().dropna()
    R_dif, P_dif = matriz_r_p(dif, VARS_ESTUDIO)
    rob = []
    for i, a in enumerate(VARS_ESTUDIO):
        for b in VARS_ESTUDIO[i + 1 :]:
            # Spearman: misma comparacion sin tendencia, pero por orden (ranking) y no por valores.
            rho, p_rho = stats.spearmanr(resid[a], resid[b])
            rob.append(
                {
                    "Par": f"{ETIQUETAS[a].split(' (')[0]}  ↔  {ETIQUETAS[b].split(' (')[0]}",
                    "r originales": f"{R_niv.loc[a, b]:+.3f}",
                    "r sin tendencia": f"{R_det.loc[a, b]:+.3f}",
                    "Spearman sin tendencia": f"{rho:+.3f} (p = {fmt_p(p_rho)})",
                    "r primeras diferencias": f"{R_dif.loc[a, b]:+.3f}",
                    "p primeras diferencias": fmt_p(P_dif.loc[a, b]),
                    "Significativa": "Sí" if P_dif.loc[a, b] < 0.05 else "No",
                }
            )
    st.dataframe(
        pd.DataFrame(rob).style.map(
            lambda v: (
                "background-color:#16283A; color:#7FB4E4" if v == "Sí"
                else f"color:{TEXTO_3}"
            ),
            subset=["Significativa"],
        ),
        width="stretch",
        hide_index=True,
    )

    rho_pt, p_pt = stats.spearmanr(resid["pbi"], resid["temp"])
    rho_pl, p_pl = stats.spearmanr(resid["pbi"], resid["lluvia"])
    rho_pg, p_pg = stats.spearmanr(resid["pbi"], resid["gei"])
    st.markdown(
        '<div class="callout">'
        "<strong>Qué agrega Spearman.</strong> Confirma que el PBI no se relaciona con la temperatura "
        f"({rho_pt:+.2f}, p = {fmt_p(p_pt)}) ni con las precipitaciones ({rho_pl:+.2f}, p = {fmt_p(p_pl)}): "
        "no depende de los años extremos. Para PBI–GEI sin tendencia da "
        f"{rho_pg:+.2f} (p = {fmt_p(p_pg)})"
        + (
            ", más débil que con Pearson. Por eso esa relación se confirma con dos métodos más: primeras "
            "diferencias (esta tabla) y crecimiento contra crecimiento (sección 6)."
            if p_pg >= 0.05
            else ", igual que con Pearson."
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    # --- 6. Crecimiento contra crecimiento ---
    st.markdown("## 6. Crecimiento contra crecimiento: PBI y emisiones")
    st.caption(
        "El PBI está medido como crecimiento (% respecto del año anterior) y los GEI como cantidad "
        "(millones de toneladas). Para comparar lo mismo con lo mismo, los GEI se pasan también a "
        "crecimiento: cuánto más o menos se emitió que el año anterior, en %."
    )
    tasa = pd.DataFrame(
        {"anio": base["anio"], "pbi": base["pbi"], "gei_pct": base["gei"].pct_change() * 100}
    ).dropna()
    r_tasa, p_tasa = stats.pearsonr(tasa["pbi"], tasa["gei_pct"])

    a, b_, c = st.columns(3, gap="medium")
    with a:
        tarjeta(f"{r_tasa:+.2f}", "Crecimiento contra crecimiento",
                f"PBI vs cambio % de los GEI · p = {fmt_p(p_tasa)}", color=SEM["ok"])
    with b_:
        tarjeta(f"{R_det.loc['pbi', 'gei']:+.2f}", "Sin tendencia",
                f"PBI vs residuos de los GEI · p = {fmt_p(P_det.loc['pbi', 'gei'])}", color=TEXTO_2)
    with c:
        tarjeta(f"{R_dif.loc['pbi', 'gei']:+.2f}", "Primeras diferencias",
                f"Cambio del PBI vs cambio de los GEI · p = {fmt_p(P_dif.loc['pbi', 'gei'])}", color=TEXTO_2)

    fig_tasa = go.Figure()
    for col, nombre, color in [("pbi", "Crecimiento del PBI (%)", COLORES["pbi"]),
                               ("gei_pct", "Crecimiento de los GEI (%)", COLORES["gei"])]:
        fig_tasa.add_trace(
            go.Scatter(
                x=tasa["anio"], y=tasa[col], mode="lines+markers", name=nombre,
                line=dict(color=color, width=2), marker=dict(size=4, color=color),
                hovertemplate="Año %{x}<br/>%{y:+.2f} %<extra>" + nombre + "</extra>",
            )
        )
    fig_tasa.add_hline(y=0, line=dict(color=GRAF["ref"], width=1, dash="dot"))
    fig_tasa.update_xaxes(title="Año", dtick=5)
    fig_tasa.update_yaxes(title="Crecimiento respecto del año anterior (%)")
    fig_tasa = plantilla_grafico(
        fig_tasa, f"PBI y emisiones de GEI, año a año   ·   r = {r_tasa:+.3f}, p = {fmt_p(p_tasa)}", alto=400
    )
    st.plotly_chart(fig_tasa, width="stretch", config={"displayModeBar": False})

    ej = tasa.set_index("anio")
    ejemplos = ", ".join(
        f"{a_} (PBI {ej.loc[a_, 'pbi']:+.1f} %, GEI {ej.loc[a_, 'gei_pct']:+.1f} %)"
        for a_ in (2002, 2020, 2021) if a_ in ej.index
    )
    que_demuestra(
        "<strong>Que el PBI y las emisiones se mueven juntos.</strong> Cuando la economía crece, las "
        "emisiones crecen; cuando cae, las emisiones caen. Por ejemplo: "
        f"{ejemplos}. Comparando crecimiento con crecimiento, la relación es "
        f"<strong>r = {r_tasa:+.2f}</strong> (p = {fmt_p(p_tasa)}): es la forma más clara de ver la "
        "relación PBI–GEI, que sin tendencia y en primeras diferencias ya aparecía, más débil.",
        como_leer="Cada línea muestra cuánto creció (arriba del cero) o cayó (abajo del cero) cada serie "
        "respecto del año anterior. Si las dos líneas suben y bajan a la vez, se mueven juntas.",
    )

    # --- 7. Conclusion ---
    st.markdown("## 7. Conclusión del objetivo")
    st.markdown(
        '<div class="callout callout-ok">'
        "<strong>Respuesta: sí, el PBI se relaciona con el cambio climático, a través de las emisiones de "
        "GEI.</strong> Con los datos originales la relación no se ve "
        f"({R_niv.loc['pbi', 'gei']:+.2f}), porque la tendencia de las emisiones la tapa. Aparece sin "
        f"tendencia ({R_det.loc['pbi', 'gei']:+.2f}, p = {fmt_p(P_det.loc['pbi', 'gei'])}), en primeras "
        f"diferencias ({R_dif.loc['pbi', 'gei']:+.2f}, p = {fmt_p(P_dif.loc['pbi', 'gei'])}) y, con más "
        f"claridad, comparando crecimiento con crecimiento ({r_tasa:+.2f}, p = {fmt_p(p_tasa)}): en los "
        "años en que la economía crece, Argentina emite más gases de efecto invernadero, y en las crisis "
        "emite menos."
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="callout">'
        "<strong>Con los otros dos indicadores no hay relación.</strong> PBI–temperatura es "
        f"{R_niv.loc['pbi', 'temp']:+.2f} con los datos originales (p = {fmt_p(P_niv.loc['pbi', 'temp'])}) y "
        f"{R_det.loc['pbi', 'temp']:+.2f} sin tendencia (p = {fmt_p(P_det.loc['pbi', 'temp'])}); "
        "PBI–precipitaciones tampoco es significativa en ninguna versión. Además, la correlación "
        f"temperatura–GEI ({R_niv.loc['temp', 'gei']:+.2f} con los datos originales) cae a "
        f"{R_det.loc['temp', 'gei']:+.2f} (p = {fmt_p(P_det.loc['temp', 'gei'])}) al quitar la tendencia: "
        "es <strong>espuria</strong>, producto de que ambas series crecen en el tiempo. "
        "<em>La hipótesis H1 no se confirma: ni el PBI ni las emisiones muestran una relación lineal real "
        "con la temperatura anual.</em>"
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# PAGINA: OBJETIVO 3
# ----------------------------------------------------------------------------
elif pagina == "Objetivo 3 · Multicolinealidad":
    st.markdown('<div class="eyebrow">Objetivo especifico 3</div>', unsafe_allow_html=True)
    st.markdown("# Revision de multicolinealidad")
    st.markdown(
        '<div class="callout">'
        "<strong>Que se busca.</strong> Cruzar el PBI, los GEI y la lluvia entre si, sin incluir la "
        "temperatura. Si dos variables se movieran siempre juntas estarian emitiendo la misma señal, y "
        "en el modelo del objetivo 5 no se sabria cual de las dos influye de verdad. Antes de armar ese "
        "modelo hay que descartar este problema."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## 0. Serie de emisiones utilizada")
    st.caption(
        "El objetivo menciona GEI, y el dataset ofrece tres series de emisiones distintas. Se puede "
        "cambiar entre ellas para comprobar que la conclusión no depende de cuál se elija."
    )

    serie_emis = st.radio(
        "Serie de emisiones",
        ["GEI (total GHG sin cambio de uso del suelo)", "CO₂ fósil (combustión fósil)"],
        index=0,
        horizontal=True,
        label_visibility="collapsed",
    )
    var_emis = "gei" if serie_emis.startswith("GEI") else "co2"
    ETIQUETAS.setdefault("co2", "CO2 fosil (Mt)")
    COLORES.setdefault("co2", COLORES["gei"])

    cols_obj3 = ["pbi", var_emis, "lluvia"]
    datos_obj3 = df.dropna(subset=cols_obj3 + ["temp"]).copy()

    # Serie oficial del inventario argentino: cobertura 2010-2022 (13 años).
    if "gei_inventario" in df.columns:
        datos_inv = df.dropna(subset=["pbi", "gei_inventario", "lluvia", "temp"]).copy()

    t1, t2, t3 = st.columns(3)
    with t1:
        tarjeta(str(len(datos_obj3)), "Observaciones disponibles",
                f"{int(datos_obj3['anio'].min())}–{int(datos_obj3['anio'].max())}", color=ACENTO)
    with t2:
        z = stats.norm.ppf(1 - 0.05 / 2)
        r_min = float(np.tanh(z / np.sqrt(len(datos_obj3) - 3)))
        tarjeta(f"{r_min:.3f}", "Menor |r| detectable",
                "Por debajo de este valor el test no alcanza potencia", color=ACENTO)
    with t3:
        tarjeta(str(len(datos_completos)), "Cobertura del período",
                "Años con las cuatro variables completas", color=ACENTO)

    if var_emis == "gei":
        st.markdown(
            '<div class="callout callout-info">'
            "<strong>Por qué se elige el GEI y no el inventario oficial.</strong> El objetivo está escrito "
            "con GEI, así que se usa la serie de GEI. El inventario oficial argentino cubre solo 2010–2022 "
            f"(13 de 65 años), que no alcanza para un análisis estadístico: con n=13 el test solo detecta "
            "correlaciones de |r| ≥ 0,551. La serie elegida cubre los 64 años completos."
            "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("## 1. Matriz de correlacion de Pearson")

    st.caption(
        "La temperatura se deja fuera del calculo a proposito: el objetivo es comprobar que las tres "
        "variables predictoras no estan midiendo lo mismo."
    )

    M = matriz_correlacion(datos_obj3, cols_obj3)
    etiquetas = [ETIQUETAS[c].split(" (")[0] for c in cols_obj3]

    # Reescalado: con el rango completo (-1 a 1) toda la matriz se veria casi
    # blanca, porque las correlaciones reales van de -0,15 a 0,02. Se ajusta el
    # limite a los valores observados para que las diferencias se distingan.
    max_off = float(np.abs(M.values - np.eye(len(M))).max())
    lim = max(0.20, max_off * 1.15)

    # La diagonal se enmascara: la correlacion de una variable consigo misma
    # es siempre 1. Si se deja visible, tres celdas saturadas dominan el grafico
    # y sugieren relaciones fuertes que en realidad no existen.
    Z = M.values.copy()
    np.fill_diagonal(Z, np.nan)

    fig = go.Figure(
        go.Heatmap(
            z=Z,
            x=etiquetas,
            y=etiquetas,
            zmin=-lim,
            zmax=lim,
            # Escala divergente sobre fondo oscuro: el cero se funde con la
            # superficie y los dos extremos resaltan. La direccion se mantiene
            # (negativo = azul, positivo = terracota) para no cambiar la lectura.
            colorscale=[
                [0.00, "#7FB4E4"],
                [0.25, "#2E6FA8"],
                [0.50, "#1A2637"],
                [0.75, "#C2714F"],
                [1.00, "#E8896A"],
            ],
            xgap=2,
            ygap=2,
            hoverongaps=False,
            colorbar=dict(
                title=dict(text="r", font=dict(size=12, color=GRAF["texto"])),
                thickness=12,
                len=0.75,
                tickfont=dict(size=10, color=GRAF["texto"]),
                outlinewidth=0,
                tickvals=[-lim, 0, lim],
                ticktext=[f"{-lim:.2f}", "0", f"{lim:.2f}"],
            ),
        )
    )

    # El valor va como anotacion y no como text del heatmap porque
    # heatmap.textfont.color no admite una matriz: hace falta un color
    # distinto por celda para mantener el contraste (texto oscuro sobre las
    # celdas brillantes de los extremos, texto claro sobre las celdas
    # apagadas cercanas al cero).
    for i, fila in enumerate(Z):
        for j, v in enumerate(fila):
            if np.isnan(v):
                continue
            fig.add_annotation(
                x=etiquetas[j],
                y=etiquetas[i],
                text=f"{v:.3f}",
                showarrow=False,
                font=dict(size=15, color=TEXTO if abs(v) / lim < 0.6 else FONDO),
            )
    fig.update_layout(
        height=380, margin=dict(l=115, r=25, t=30, b=70),
        paper_bgcolor=FONDO, plot_bgcolor=FONDO,
        font=dict(family="Inter, sans-serif", size=13, color=GRAF["texto"]),
    )
    fig.update_xaxes(showgrid=False, side="top", linecolor=GRAF["linea"], ticks="")
    fig.update_yaxes(showgrid=False, autorange="reversed", linecolor=GRAF["linea"], ticks="")
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    st.caption(
        f"Escala ampliada a ±{lim:.2f} para que se aprecien las diferencias entre pares. "
        "La diagonal queda vacia: la correlacion de una variable consigo misma es "
        "siempre 1 y no aporta informacion. Solo interesan los seis valores fuera de la diagonal."
    )

    st.markdown("## 2. Tests de significancia por par")
    st.caption(
        "H0: no existe relacion lineal entre las variables. "
        "Si el p-valor es menor a 0,05 se rechaza H0 y la relacion se considera real."
    )

    tabla = pares_correlacion(datos_obj3, cols_obj3)

    for _, row in tabla.iterrows():
        chip, desc = fuerza(row["r"])
        c1, c2, c3, c4 = st.columns([3, 1.3, 1.3, 2.2], gap="medium")
        with c1:
            st.markdown(f"**{row['Par']}**")
        with c2:
            st.markdown(
                f'<div style="font-size:1.3rem;font-weight:600;color:{ACENTO}">{row["r"]:+.3f}</div>',
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(
                f'<div style="font-size:1.3rem;font-weight:600;color:{TEXTO_2}">{row["p_valor"]:.3f}</div>',
                unsafe_allow_html=True,
            )
        with c4:
            st.markdown(
                f'<span class="chip {chip}">{desc}</span>'
                f'<span class="chip {"chip-bad" if row["Significativo"] else "chip-ok"}">'
                f'{"Significativo" if row["Significativo"] else "No significativo"}</span>',
                unsafe_allow_html=True,
            )
        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    n_sig = int(tabla["Significativo"].sum())
    st.markdown(
        f'<div class="callout {"callout-ok" if n_sig == 0 else "callout-bad"}">'
        f"<strong>Resultado.</strong> De los {len(tabla)} pares evaluados, "
        f"<strong>{n_sig}</strong> resultan significativos al 5%. "
        + (
            "Ninguna variable esta relacionada con otra: las tres son estadisticamente independientes "
            "y cada una aporta informacion propia."
            if n_sig == 0
            else "Existe al menos un par redundante que deberia revisarse."
        )
        + "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## 3. Variance Inflation Factor (VIF)")
    st.caption(
        "El VIF estima cuanto se infla el error de un coeficiente al incluir las demas variables. "
        "Regla practica: por debajo de 5 no hay problema; por encima de 10 es multicolinealidad severa."
    )

    v = vif(datos_obj3, cols_obj3)

    fig_v = go.Figure(
        go.Bar(
            x=v["VIF"], y=v["Variable"], orientation="h",
            marker=dict(
                color=[ACENTO if x < 5 else SEM["bad"] for x in v["VIF"]],
                line=dict(width=0),
            ),
            text=[f"{x:.3f}" for x in v["VIF"]],
            textposition="outside",
            textfont=dict(size=13, color=TEXTO_2),
            hovertemplate="%{y}<br/>VIF = %{x:.3f}<extra></extra>",
        )
    )
    fig_v.add_vline(x=5, line=dict(color=SEM["bad"], width=1.5, dash="dash"),
                    annotation_text="Umbral 5", annotation_position="top")
    fig_v.add_vline(x=1, line=dict(color=GRAF["ref"], width=1, dash="dot"))
    fig_v.update_xaxes(range=[0, max(5.6, float(v["VIF"].max()) * 1.35)], title="VIF")
    fig_v.update_yaxes(autorange="reversed")
    fig_v = plantilla_grafico(fig_v, "VIF por variable", alto=260)
    fig_v.update_layout(margin=dict(l=150, r=70, t=55, b=50), showlegend=False)
    st.plotly_chart(fig_v, width="stretch", config={"displayModeBar": False})

    st.markdown(
        f'<div class="callout callout-ok">'
        f"<strong>Resultado.</strong> Todos los VIF estan muy cerca de 1, que es el valor teorico "
        f"minimo. Cuanto mas se alejan de 1, mas correlacion hay entre las variables. "
        f"El maximo es <strong>{v['VIF'].max():.3f}</strong>, muy por debajo de 5."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## 4. Dispersion de cada par")
    st.caption(
        "Cada punto es un ano. El color va de azul apagado a celeste intenso segun avanza el "
        "tiempo, lo que permite ver si la relacion cambio a lo largo del periodo."
    )

    # Escala monocroma azul, coherente con el acento y legible sobre fondo oscuro.
    # Se sustituye Viridis, que introduce otros tonos (verde, amarillo) y rompe la paleta.
    escala_año = [[0.0, "#2A4568"], [0.5, "#4A7FB0"], [1.0, "#9CCBEE"]]

    fig_pairs = px.scatter(
        datos_obj3,
        x="pbi", y=var_emis,
        color="anio", color_continuous_scale=escala_año,
        hover_data={"anio": True, "pbi": ":.2f", var_emis: ":.1f"},
        labels={"pbi": ETIQUETAS["pbi"], var_emis: ETIQUETAS[var_emis]},
        trendline="ols",
    )
    fig_pairs = plantilla_grafico(
        fig_pairs,
        f"PBI vs {ETIQUETAS[var_emis].split(' (')[0]}   ·   "
        f"r = {tabla.iloc[0]['r']:+.3f}, p = {tabla.iloc[0]['p_valor']:.3f}",
        alto=380,
    )
    fig_pairs.update_layout(margin=dict(l=65, r=25, t=60, b=55))
    fig_pairs.update_coloraxes(colorbar=dict(title=dict(text="Año", side="right", font=dict(size=11, color=GRAF["texto"])),
                                           thickness=10, len=0.6, outlinewidth=0,
                                           tickfont=dict(size=10, color=GRAF["texto"])))
    fig_pairs.data[1].line.color = GRAF["ajuste"]
    fig_pairs.data[1].line.width = 2
    st.plotly_chart(fig_pairs, width="stretch", config={"displayModeBar": False})

    c1, c2 = st.columns(2, gap="medium")
    for c, (x, y, i) in zip(
        [c1, c2],
        [("pbi", "lluvia", 1), (var_emis, "lluvia", 2)],
    ):
        f = px.scatter(
            datos_obj3, x=x, y=y, color="anio", color_continuous_scale=escala_año,
            hover_data={"anio": True},
            labels={x: ETIQUETAS[x], y: ETIQUETAS[y]},
            trendline="ols",
        )
        f = plantilla_grafico(
            f,
            f"{ETIQUETAS[x].split(' (')[0]} vs {ETIQUETAS[y].split(' (')[0]}"
            f"   ·   r = {tabla.iloc[i]['r']:+.3f}, p = {tabla.iloc[i]['p_valor']:.3f}",
            alto=330,
        )
        f.update_layout(margin=dict(l=60, r=20, t=58, b=50), showlegend=False)
        f.data[1].line.color = GRAF["ajuste"]
        f.data[1].line.width = 2
        f.update_coloraxes(showscale=False)
        with c:
            st.plotly_chart(f, width="stretch", config={"displayModeBar": False})

    st.caption(
        "La linea gris es el ajuste por minimos cuadrados. En los tres graficos las pendientes son "
        "apenas inclinadas: eso es la multicolinealidad ausente hecha visible."
    )

    # --- Comparacion entre series de emisiones ---
    series_cmp = []
    for vcol, nombre in [("gei", "GEI (total GHG sin cambio de uso del suelo)"),
                         ("co2", "CO2 fosil (combustion fosil)")] + (
                        [("gei_inventario", "GEI inventario oficial")] if "gei_inventario" in df.columns else []):
        if vcol not in df.columns:
            continue
        dd = df.dropna(subset=["pbi", vcol, "lluvia", "temp"])
        vv = vif(dd, ["pbi", vcol, "lluvia"])
        zc = stats.norm.ppf(1 - 0.05 / 2)
        series_cmp.append({
            "Serie de emisiones": nombre,
            "n": len(dd),
            "Periodo": f"{int(dd['anio'].min())}–{int(dd['anio'].max())}",
            "VIF max": float(vv["VIF"].max()),
            "|r| min detectable": float(np.tanh(zc / np.sqrt(len(dd) - 3))),
            "Veredicto": "Sin multicolinealidad" if vv["VIF"].max() < 5 else "Con multicolinealidad",
        })

    st.markdown("## 5. Robustez: el resultado no depende de la serie elegida")
    st.caption(
        "El objetivo esta escrito con GEI, pero el dataset ofrece tres series de emisiones. Si la "
        "conclusion fuera sensible a esa eleccion, el hallazgo no seria confiable."
    )
    st.dataframe(
        pd.DataFrame(series_cmp).style.format(
            {
                "VIF max": "{:.3f}",
                "|r| min detectable": "{:.3f}",
                "Veredicto": lambda v: (
                    f"background-color:{SEM['ok_bg']}; color:{SEM['ok']}"
                    if v == "Sin multicolinealidad"
                    else f"background-color:{SEM['bad_bg']}; color:{SEM['bad']}"
                ),
            },
            na_rep="—",
        ),
        width="stretch",
        hide_index=True,
    )
    st.markdown(
        '<div class="callout callout-ok">'
        "<strong>Las tres series dan el mismo veredicto: no hay multicolinealidad.</strong> "
        "Los VIF maximos se mantienen entre 1,03 y 1,12, muy por debajo del umbral de 5. La conclusion "
        "del objetivo 3 es robusta: no depende de cual serie de emisiones se utilice."
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown("## 6. Conclusion del objetivo")
    st.markdown(
        '<div class="callout callout-ok">'
        "<strong>Las tres variables son independientes.</strong> Ninguna correlacion alcanza "
        "significacion estadistica y todos los VIF son practicamente 1. Esto habilita su uso conjunto "
        "en el modelo de prediccion del objetivo 5: el PBI, las emisiones y la lluvia pueden entrar al "
        "mismo modelo sin que una variable este robando la explicacion de otra."
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# PAGINA: OBJETIVO 4
# ----------------------------------------------------------------------------
elif pagina == "Objetivo 4 · Estabilidad temporal":
    st.markdown('<div class="eyebrow">Objetivo especifico 4</div>', unsafe_allow_html=True)
    st.markdown("# Estabilidad de la relacion en el tiempo")

    st.markdown(
        '<div class="callout">'
        "<strong>Que se busca.</strong> La hipotesis del trabajo planteaba que la relacion entre PBI y "
        "temperatura se fortaleceria con el correr de los años. Para comprobarlo se parte el periodo en "
        "dos mitades y se compara la correlacion de cada una. Si el numero cambia mucho, la relacion "
        "cambio; si se mantiene, fue estable."
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Corte configurable ---
    st.markdown("## 0. Corte temporal")

    corte = st.slider(
        "Ultimo ano de la primera mitad",
        min_value=1970, max_value=2005, value=MITAD_CORTE, step=1,
        help="Con el valor por defecto el corte es 1992, que divide 1961-2024 en dos bloques de 32 anos.",
    )

    m1 = datos_completos[datos_completos["anio"] <= corte]
    m2 = datos_completos[datos_completos["anio"] > corte]

    if len(m1) < 10 or len(m2) < 10:
        st.warning("El corte elegido deja menos de 10 observaciones en alguna mitad. Ajustalo para un analisis valido.")
        st.stop()

    r1, p1 = stats.pearsonr(m1["pbi"], m1["temp"])
    r2, p2 = stats.pearsonr(m2["pbi"], m2["temp"])
    z_f, p_f = fisher_z(r1, len(m1), r2, len(m2))
    delta = r2 - r1

    k1, _ = fuerza(r1)
    k2, _ = fuerza(r2)

    # --- Tarjetas ---
    a, b, c, d = st.columns(4, gap="medium")
    with a:
        tarjeta(f"{r1:+.3f}", f"Primera mitad · {m1['anio'].min()}–{m1['anio'].max()}",
                f"n = {len(m1)} observaciones<br/>p-valor = {p1:.3f}", color=COLORES["h1"])
    with b:
        tarjeta(f"{r2:+.3f}", f"Segunda mitad · {m2['anio'].min()}–{m2['anio'].max()}",
                f"n = {len(m2)} observaciones<br/>p-valor = {p2:.3f}", color=COLORES["h2"])
    with c:
        tarjeta(f"{delta:+.3f}", "Cambio en la correlacion",
                f"Diferencia bruta entre mitades", color=TEXTO_2)
    with d:
        tarjeta(f"{p_f:.3f}", "Test de Fisher",
                f"z = {z_f:.3f} · diferencia significativa al 5%: "
                f'{"Si" if p_f < 0.05 else "No"}',
                color=SEM["bad"] if p_f >= 0.05 else SEM["ok"])

    # --- Grafico comparativo de barras ---
    st.markdown("## 1. Comparacion de las dos correlaciones")

    fig_bar = go.Figure()
    for r, p, x, lab, color in [
        (r1, p1, f"{m1['anio'].min()}–{m1['anio'].max()}", "Primera mitad", COLORES["h1"]),
        (r2, p2, f"{m2['anio'].min()}–{m2['anio'].max()}", "Segunda mitad", COLORES["h2"]),
    ]:
        fig_bar.add_trace(
            go.Bar(
                x=[r], y=[f"{lab}\n({x})"], orientation="h",
                marker=dict(color=color, line=dict(width=0)),
                width=0.5,
                text=[f"r = {r:+.3f}"], textposition="outside",
                textfont=dict(size=15, color=TEXTO_2),
                hovertemplate=f"{lab} ({x})<br/>r = {r:+.4f}<br/>p = {p:.4f}<extra></extra>",
                name=lab,
            )
        )

    fig_bar.add_vline(x=0, line=dict(color=GRAF["ref"], width=1.5))
    fig_bar.add_vline(x=-0.30, line=dict(color=GRAF["linea"], width=1, dash="dash"))
    fig_bar.add_vline(x=0.30, line=dict(color=GRAF["linea"], width=1, dash="dash"))
    fig_bar.add_annotation(
        x=0.30, y=1.0, xref="x", yref="paper", yanchor="bottom", xanchor="left",
        text="Umbral |r| = 0,30", showarrow=False,
        font=dict(size=10, color=TEXTO_3), xshift=4,
    )
    fig_bar.update_xaxes(range=[-0.62, 0.62], title="Correlacion de Pearson (r)")
    fig_bar = plantilla_grafico(fig_bar, "Correlacion PBI – Temperatura por mitad del periodo", alto=300)
    fig_bar.update_layout(margin=dict(l=140, r=30, t=62, b=50), showlegend=False, bargap=0.55)
    st.plotly_chart(fig_bar, width="stretch", config={"displayModeBar": False})

    if p_f >= 0.05:
        st.markdown(
            '<div class="callout callout-ok">'
            f"<strong>La relacion no cambio.</strong> El test de Fisher da p = {p_f:.3f}, muy por encima "
            f"de 0,05: la diferencia entre las dos mitades ({delta:+.3f}) es compatible con el azar. "
            "Ademas ninguna de las dos correlaciones es significativa por separado, asi que la relacion "
            "PBI–temperatura es debil y ademas constante en todo el periodo."
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="callout callout-bad">'
            f"<strong>La relacion cambio con el tiempo.</strong> El test de Fisher da p = {p_f:.4f}, "
            f"por debajo de 0,05: la diferencia entre mitades ({delta:+.3f}) no puede atribuirse al azar."
            "</div>",
            unsafe_allow_html=True,
        )

    # --- Dispersion por mitad ---
    st.markdown("## 2. Dispersion y recta de ajuste por mitad")
    st.caption(
        "La banda sombreada es el intervalo de confianza al 95% del valor medio predicho. "
        "Si las rectas se superponen, la relacion es la misma en ambas epocas."
    )

    fig_sc = go.Figure()

    for sub, r, p, color, lab in [
        (m1, r1, p1, COLORES["h1"], f"Primera mitad ({m1['anio'].min()}–{m1['anio'].max()})"),
        (m2, r2, p2, COLORES["h2"], f"Segunda mitad ({m2['anio'].min()}–{m2['anio'].max()})"),
    ]:
        aj = regresion_lineal(sub["pbi"].values, sub["temp"].values)

        fig_sc.add_trace(
            go.Scatter(x=sub["pbi"], y=sub["temp"], mode="markers", name=lab,
                       marker=dict(color=color, size=8, opacity=0.75,
                                   line=dict(width=0.6, color=FONDO)),
                       customdata=sub["anio"],
                       hovertemplate=lab + "<br/>Anio %{customdata}<br/>PBI %{x:.2f}%<br/>Temp %{y:+.2f} °C<extra></extra>")
        )
        fig_sc.add_trace(
            go.Scatter(x=aj["grid"], y=aj["yhat"], mode="lines", name=f"Ajuste {lab.split(' ')[1]}",
                       line=dict(color=color, width=2.5), hoverinfo="skip")
        )
        fig_sc.add_trace(
            go.Scatter(x=np.concatenate([aj["grid"], aj["grid"][::-1]]),
                       y=np.concatenate([aj["ic_sup"], aj["ic_inf"][::-1]]),
                       fill="toself", fillcolor=_hex_a(color, 0.10),
                       line=dict(width=0), hoverinfo="skip", showlegend=False)
        )

    fig_sc.add_hline(y=0, line=dict(color=GRAF["linea"], width=1, dash="dash"))
    fig_sc.add_hline(y=datos_completos["temp"].mean(),
                     line=dict(color=GRAF["ref"], width=1, dash="dot"),
                     annotation_text=f"Media global {datos_completos['temp'].mean():+.2f} °C",
                     annotation_position="top left")
    fig_sc.update_xaxes(title=ETIQUETAS["pbi"])
    fig_sc.update_yaxes(title=ETIQUETAS["temp"])
    fig_sc = plantilla_grafico(fig_sc, "PBI vs Temperatura, dos subperiodos", alto=470)
    fig_sc.update_layout(margin=dict(l=65, r=25, t=60, b=55))
    st.plotly_chart(fig_sc, width="stretch", config={"displayModeBar": False})

    # --- Test de interaccion ---
    st.markdown("## 3. Formalizacion: interaccion periodo × PBI")

    st.caption(
        "Ademas de comparar dos numeros por separado, se ajusta un unico modelo que incluye el periodo "
        "y su interaccion con el PBI. Si el coeficiente de la interaccion es distinto de cero, "
        "la relacion entre PBI y temperatura es distinta en cada mitad."
    )

    d_int = pd.concat(
        [m1.assign(periodo="Primera"), m2.assign(periodo="Segunda")], ignore_index=True
    )
    d_int = d_int.assign(post=(d_int["periodo"] == "Segunda").astype(int))
    modelo_int = smf.ols("temp ~ pbi + post + pbi:post", data=d_int).fit()

    filas_int = []
    for nombre in ["Intercept", "pbi", "post", "pbi:post"]:
        if nombre in modelo_int.params.index:
            filas_int.append(
                {
                    "Termino": {"Intercept": "Constante", "pbi": "PBI",
                                "post": "Cambio de periodo", "pbi:post": "PBI × Periodo"}[nombre],
                    "Coeficiente": modelo_int.params[nombre],
                    "Error estandar": modelo_int.bse[nombre],
                    "t": modelo_int.tvalues[nombre],
                    "p-valor": modelo_int.pvalues[nombre],
                    "Significativo": "Si" if modelo_int.pvalues[nombre] < 0.05 else "No",
                }
            )

    st.dataframe(
        pd.DataFrame(filas_int).style.format(
            {
                "Coeficiente": "{:+.4f}",
                "Error estandar": "{:.4f}",
                "t": "{:+.3f}",
                "p-valor": "{:.4f}",
                "Significativo": lambda v: (
                    f"background-color:{SEM['bad_bg']}; color:{SEM['bad']}"
                    if v == "Si"
                    else f"background-color:{SEM['ok_bg']}; color:{SEM['ok']}"
                ),
            }
        ),
        width="stretch",
        hide_index=True,
    )

    coef_int = modelo_int.params.get("pbi:post", 0.0)
    p_int = modelo_int.pvalues.get("pbi:post", 1.0)

    st.markdown(
        f'<div class="callout {"callout-ok" if p_int >= 0.05 else "callout-bad"}">'
        f"<strong>El coeficiente de interaccion es {coef_int:+.4f} (p = {p_int:.3f}).</strong> "
        + (
            "No es significativamente distinto de cero, de modo que la pendiente del PBI es la misma en "
            "las dos mitades. No hay evidencia de que la relacion se haya fortalecido con el tiempo, "
            "lo que contradice la hipotesis inicial."
            if p_int >= 0.05
            else "Es significativamente distinto de cero: la pendiente del PBI difiere entre las dos mitades."
        )
        + f"<br/><br/><em>R² del modelo = {modelo_int.rsquared:.4f} · R² ajustado = "
        f"{modelo_int.rsquared_adj:.4f} · n = {int(modelo_int.nobs)}</em>"
        "</div>",
        unsafe_allow_html=True,
    )

    # --- Conclusion ---
    st.markdown("## 4. Conclusion del objetivo")
    st.markdown(
        '<div class="callout callout-bad">'
        "<strong>La relacion se mantuvo estable y sigo siendo debil.</strong> El valor Practicamente "
        f"identico en ambas mitades ({r1:.2f} y {r2:.2f}) muestra que la relacion PBI–temperatura no "
        "cambio con el tiempo. Sumado a que ninguno de los dos coeficientes alcanza significacion "
        "estadistica, la conclusion es que el crecimiento economico argentino no tiene una relacion "
        "lineal detectable con la temperatura nacional. Este resultado es coherente con el objetivo 2, "
        "donde la correlacion PBI–temperatura tambien resulto no significativa."
        "</div>",
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# PAGINA: METODOLOGIA
# ----------------------------------------------------------------------------
else:
    st.markdown('<div class="eyebrow">Anexo</div>', unsafe_allow_html=True)
    st.markdown("# Metodologia y notas tecnicas")

    st.markdown("## Datos")
    st.markdown(
        """
        | Campo | Contenido |
        |---|---|
        | Archivo | `data/processed/dataset_nacional.csv` |
        | Unidad de analisis | Pais (Argentina) |
        | Frecuencia | Anual |
        | Periodo | 1961–2024 (64 observaciones) |
        | Variables usadas | Temperatura, PBI, GEI (CO2eq), Lluvia |

        Se descarto 2025 porque el registro de GEI y de PBI per capita esta incompleto; incluirlo
        habria recortado la muestra de forma desigual entre variables.
        """
    )

    st.markdown("## Procedimientos")
    st.markdown(
        """
        **Correlacion de Pearson.** Mide la fuerza y el sentido de una relacion lineal entre dos
        variables. Va de −1 (movimiento opuesto perfecto) a +1 (movimiento conjunto perfecto).

        **p-valor.** Probabilidad de observar una correlacion tan extrema como la encontrada si en
        realidad no existiera relacion. Con umbral 0,05 se rechaza la hipotesis nula de independencia.

        **VIF (Variance Inflation Factor).** Cuantifica elmulticolinealidad mediante el coeficiente de
        determinacion de cada variable regresada sobre las demas: VIF = 1 / (1 − R²). El minimo teorico
        es 1 (variables ortogonales) y por encima de 5 se considera problemático.

        **Test de Fisher.** Compara dos correlaciones independientes mediante la transformacion
        z = arctanh(r). Devuelve un estadistico z y su p-valor, y es el metodo estandar para contrastar
        si una correlacion cambio entre dos periodos.

        **Regresión simple y modelo con interaccion.** Ajuste por minimos cuadrados. El modelo
        `temp ~ pbi + post + pbi:post` estima si la pendiente del PBI difiere despues del corte temporal.
        """
    )

    st.markdown("## Estructura del proyecto")
    st.markdown(
        """
        ```
        data/
          raw/          datos originales de cada fuente
          processed/    dataset_nacional.csv  <- archivo que usa esta app
          sources.csv   referencia de las fuentes
        app.py         esta interfaz
        ```
        """
    )

    st.markdown("## Limitaciones")
    st.markdown(
        """
        - La correlacion no implica causalidad: una correlacion debil no descarta relaciones no lineales
          ni efectos con rezago (por ejemplo, de los GEI sobre la temperatura con anos de atraso).
        - La temperatura y la lluvia son promedios nacionales, que ocultan contrastes regionales grandes.
        - 64 observaciones anuales es una muestra corta para inferencia; los intervalos de confianza son
          amplios y los p-valores hay que leerlos con cautela.
        - La relacion PBI–temperatura se estima con el PBI de crecimiento anual, una serie muy volatil
          cuyo error de medicion puede diluir correlaciones reales.
        """
    )

    st.markdown("## Reproducir los resultados")
    st.code(
        """pip install -r requirements.txt
streamlit run app.py""",
        language="bash",
    )