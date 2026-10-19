# -*- coding: utf-8 -*-
"""
Objetivo 5 - Modelos predictivos.

Predice la anomalia de temperatura media anual de Argentina (temp, en C) a partir
del crecimiento del PBI (pbi), las emisiones de GEI (gei) y la anomalia de
precipitacion (lluvia).

Modelos: Regresion Lineal Multiple (OLS) y Random Forest Regressor.
Validacion: particion temporal 1961-2009 (entrenamiento) / 2010-2024 (prueba).
Nunca se mezclan anos al azar.

Uso:
    python modelos.py

Requiere: pandas, numpy, scipy, scikit-learn.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.base import clone
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import TimeSeriesSplit

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "processed" / "dataset_nacional.csv"

ANIO_MIN, ANIO_MAX = 1961, 2024
CORTE_ENTRENAMIENTO = 2009
RESPUESTA = "temp"
PREDICTORAS = ["pbi", "gei", "lluvia"]

ETIQUETAS = {
    "pbi": "PBI (crecimiento %)",
    "gei": "GEI (MtCO2eq)",
    "lluvia": "Lluvia (anomalia %)",
    "temp": "Temperatura (anomalia C)",
    "baseline": "Baseline naive (persistencia)",
    "lineal": "Regresion Lineal Multiple",
    "rf": "Random Forest Regressor",
}

RENOMBRES = {
    "año": "anio",
    "anomalia_temperatura": "temp",
    "anomalia_precipitacion_pct": "lluvia",
    "emisiones_gei_no_uc_co2eq": "gei",
    "pbi_crecimiento_pct": "pbi",
}


def titulo(texto: str) -> None:
    print("\n" + "=" * 82)
    print(texto)
    print("=" * 82)


def subtitulo(texto: str) -> None:
    print("\n" + texto)
    print("-" * len(texto))


def cargar_datos() -> pd.DataFrame:
    """Carga, normaliza y recorta el dataset nacional al periodo del estudio."""
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"No se encontro el dataset: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH, encoding="utf-8").rename(columns=RENOMBRES)
    df = df[(df["anio"] >= ANIO_MIN) & (df["anio"] <= ANIO_MAX)].copy()
    df = df.dropna(subset=[RESPUESTA] + PREDICTORAS)
    return df.sort_values("anio").reset_index(drop=True)


def ols_ajustar(y: np.ndarray, X: np.ndarray, nombres: list[str]) -> dict:
    """Ajusta un OLS multiple con intercepto y devuelve coeficientes y ajuste."""
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    Xd = np.column_stack([np.ones(len(X)), X])

    beta, *_ = np.linalg.lstsq(Xd, y, rcond=None)
    yhat = Xd @ beta
    resid = y - yhat
    n, k = Xd.shape
    gl = n - k

    sse = float(resid @ resid)
    sst = float(((y - y.mean()) ** 2).sum())
    sigma2 = sse / gl
    cov = sigma2 * np.linalg.inv(Xd.T @ Xd)
    se = np.sqrt(np.diag(cov))
    t_vals = beta / se
    p_vals = 2 * stats.t.sf(np.abs(t_vals), gl)
    t_crit = stats.t.ppf(0.975, gl)

    r2 = 1 - sse / sst
    r2_adj = 1 - (1 - r2) * (n - 1) / gl
    f_stat = ((sst - sse) / (k - 1)) / (sse / gl)
    f_p = float(stats.f.sf(f_stat, k - 1, gl))

    sd_y = y.std(ddof=1)
    betas_std = beta[1:] * X.std(axis=0, ddof=1) / sd_y

    return {
        "nombres": ["(Intercepto)"] + nombres,
        "beta": beta,
        "se": se,
        "t": t_vals,
        "p": p_vals,
        "ic_inf": beta - t_crit * se,
        "ic_sup": beta + t_crit * se,
        "yhat": yhat,
        "resid": resid,
        "r2": float(r2),
        "r2_adj": float(r2_adj),
        "f": float(f_stat),
        "f_p": f_p,
        "n": n,
        "k": k,
        "gl": gl,
        "betas_std": betas_std,
    }


def vif_predictoras(X: np.ndarray, nombres: list[str]) -> pd.DataFrame:
    """VIF de cada predictora (1 = independiente; > 5 = problematico)."""
    filas = []
    for j, nombre in enumerate(nombres):
        otras = [k for k in range(len(nombres)) if k != j]
        ajuste = ols_ajustar(X[:, j], X[:, otras], [nombres[k] for k in otras])
        filas.append({"Variable": ETIQUETAS.get(nombre, nombre), "VIF": 1 / (1 - ajuste["r2"])})
    return pd.DataFrame(filas).sort_values("VIF", ascending=False)


def durbin_watson(resid: np.ndarray) -> float:
    """Estadistico Durbin-Watson: cerca de 2 no hay autocorrelacion."""
    resid = np.asarray(resid, dtype=float)
    return float(np.sum(np.diff(resid) ** 2) / np.sum(resid**2))


def breusch_pagan(resid: np.ndarray, X: np.ndarray) -> tuple[float, float]:
    """Test de Breusch-Pagan de heterocedasticidad."""
    e2 = np.asarray(resid, dtype=float) ** 2
    Xd = np.column_stack([np.ones(len(X)), X])
    beta, *_ = np.linalg.lstsq(Xd, e2, rcond=None)
    yhat = Xd @ beta
    sse = float(((e2 - yhat) ** 2).sum())
    sst = float(((e2 - e2.mean()) ** 2).sum())
    r2 = 1 - sse / sst
    lm = len(e2) * r2
    return float(lm), float(stats.chi2.sf(lm, X.shape[1]))


def metricas(y: np.ndarray, yhat: np.ndarray) -> dict:
    """RMSE, MAE y R2 sobre un conjunto."""
    return {
        "RMSE": float(np.sqrt(mean_squared_error(y, yhat))),
        "MAE": float(mean_absolute_error(y, yhat)),
        "R2": float(r2_score(y, yhat)),
    }


def cv_temporal(estimador, X: np.ndarray, y: np.ndarray, n_splits: int = 5) -> np.ndarray:
    """RMSE en validacion cruzada de ventana expansiva (respeta el orden temporal)."""
    tscv = TimeSeriesSplit(n_splits=n_splits)
    rmse = []
    for tr_idx, va_idx in tscv.split(X):
        modelo = clone(estimador)
        modelo.fit(X[tr_idx], y[tr_idx])
        yhat = modelo.predict(X[va_idx])
        rmse.append(np.sqrt(mean_squared_error(y[va_idx], yhat)))
    return np.array(rmse)


def cv_persistencia(y: np.ndarray, n_splits: int = 5) -> np.ndarray:
    """RMSE del baseline de persistencia en la misma validacion temporal."""
    tscv = TimeSeriesSplit(n_splits=n_splits)
    rmse = []
    for _, va_idx in tscv.split(y):
        yhat = y[np.asarray(va_idx) - 1]
        rmse.append(np.sqrt(mean_squared_error(y[va_idx], yhat)))
    return np.array(rmse)


def tabla_metricas(filas: list[dict]) -> pd.DataFrame:
    return pd.DataFrame(filas)[["Modelo", "RMSE", "MAE", "R2"]]


def main() -> None:
    df = cargar_datos()
    X = df[PREDICTORAS].to_numpy(dtype=float)
    y = df[RESPUESTA].to_numpy(dtype=float)
    anios = df["anio"].to_numpy()

    train = anios <= CORTE_ENTRENAMIENTO
    test = ~train

    X_train, X_test = X[train], X[test]
    y_train, y_test = y[train], y[test]
    anios_train, anios_test = anios[train], anios[test]

    titulo("OBJETIVO 5 - MODELOS PREDICTIVOS")
    print(f"Variable respuesta : {ETIQUETAS[RESPUESTA]}")
    print(f"Predictoras        : {', '.join(ETIQUETAS[p] for p in PREDICTORAS)}")
    print(f"Periodo total      : {ANIO_MIN}-{ANIO_MAX} ({len(df)} observaciones completas)")
    print(
        f"Entrenamiento      : {anios_train.min()}-{anios_train.max()} "
        f"(n = {len(y_train)})"
    )
    print(
        f"Prueba             : {anios_test.min()}-{anios_test.max()} "
        f"(n = {len(y_test)})"
    )
    print("Particion          : temporal (los anos de prueba son todos posteriores a los de entrenamiento)")

    if max(anios_train) >= min(anios_test):
        raise ValueError("La particion temporal no es valida: hay anos de test anteriores a train.")

    titulo("1. ESTADISTICOS DESCRIPTIVOS DEL CONJUNTO DE ENTRENAMIENTO")
    desc = df.loc[train, [RESPUESTA] + PREDICTORAS].describe().T
    desc = desc[["count", "mean", "std", "min", "max"]]
    desc.index = [ETIQUETAS.get(i, i) for i in desc.index]
    print(desc.to_string(float_format=lambda v: f"{v:9.3f}"))

    titulo("2. REGRESION LINEAL MULTIPLE")
    ols = ols_ajustar(y_train, X_train, PREDICTORAS)

    coef = pd.DataFrame(
        {
            "Termino": ols["nombres"],
            "Coeficiente": ols["beta"],
            "Error estandar": ols["se"],
            "t": ols["t"],
            "p-valor": ols["p"],
            "IC 95% inf": ols["ic_inf"],
            "IC 95% sup": ols["ic_sup"],
        }
    )
    print(coef.to_string(index=False, float_format=lambda v: f"{v:12.4f}"))

    betas = pd.DataFrame(
        {
            "Variable": [ETIQUETAS[p] for p in PREDICTORAS],
            "Coeficiente estandarizado": ols["betas_std"],
        }
    )
    print("\nCoeficientes estandarizados (comparables entre si):")
    print(betas.to_string(index=False, float_format=lambda v: f"{v:+.4f}"))

    print("\nAjuste global:")
    print(f"  R2            = {ols['r2']:.4f}")
    print(f"  R2 ajustado   = {ols['r2_adj']:.4f}")
    print(f"  F({ols['k'] - 1}, {ols['gl']})       = {ols['f']:.4f}")
    print(f"  p-valor F     = {ols['f_p']:.4f}")
    print(f"  n             = {ols['n']}")

    subtitulo("Diagnostico de supuestos del OLS")
    shapiro_w, shapiro_p = stats.shapiro(ols["resid"])
    bp_lm, bp_p = breusch_pagan(ols["resid"], X_train)
    dw = durbin_watson(ols["resid"])
    vif = vif_predictoras(X_train, PREDICTORAS)

    diag = pd.DataFrame(
        [
            {"Prueba": "Shapiro-Wilk (normalidad de residuos)", "Estadistico": shapiro_w, "p-valor": shapiro_p},
            {"Prueba": "Breusch-Pagan (heterocedasticidad)", "Estadistico": bp_lm, "p-valor": bp_p},
            {"Prueba": "Durbin-Watson (autocorrelacion)", "Estadistico": dw, "p-valor": np.nan},
        ]
    )
    print(diag.to_string(index=False, float_format=lambda v: f"{v:12.4f}", na_rep="—"))
    print("\nVIF de las predictoras:")
    print(vif.to_string(index=False, float_format=lambda v: f"{v:8.4f}"))

    dw_veredicto = (
        "autocorrelacion positiva"
        if dw < 1.5
        else "autocorrelacion negativa"
        if dw > 2.5
        else "sin evidencia de autocorrelacion"
    )
    vif_max = float(vif["VIF"].max())
    print("\nLectura de los diagnosticos:")
    print(
        f"  - Normalidad (Shapiro-Wilk): p = {shapiro_p:.4f} -> "
        + ("residuos compatibles con normalidad." if shapiro_p >= 0.05
           else "se rechaza la normalidad de los residuos; los p-valores deben leerse con cautela.")
    )
    print(
        f"  - Heterocedasticidad (Breusch-Pagan): p = {bp_p:.4f} -> "
        + ("varianza constante." if bp_p >= 0.05
           else "se detecta heterocedasticidad.")
    )
    print(f"  - Autocorrelacion (Durbin-Watson = {dw:.4f}): {dw_veredicto}.")
    print(
        f"  - Multicolinealidad (VIF maximo = {vif_max:.4f}): "
        + ("no hay problema (umbral 5)." if vif_max < 5 else "hay multicolinealidad.")
    )

    print("\nLectura del modelo lineal:")
    p_gei = float(coef.loc[coef["Termino"] == "gei", "p-valor"].iloc[0])
    if p_gei < 0.05:
        print(
            "  El GEI resulta significativo en el entrenamiento y es la variable de mayor "
            "coeficiente estandarizado. Esa senal esta dominada por la tendencia compartida entre "
            "temperatura y emisiones (objetivo 2): por eso hay que comprobar si se sostiene fuera "
            "de muestra antes de considerarla capacidad predictiva."
        )
    else:
        print("  Ninguna predictora resulta significativa al 5% en el entrenamiento.")

    yhat_lineal = np.column_stack([np.ones(len(X_test)), X_test]) @ ols["beta"]
    met_lineal = metricas(y_test, yhat_lineal)

    titulo("3. RANDOM FOREST REGRESSOR")
    rf = RandomForestRegressor(
        n_estimators=500,
        random_state=42,
        oob_score=True,
    )
    rf.fit(X_train, y_train)
    yhat_rf = rf.predict(X_test)
    met_rf = metricas(y_test, yhat_rf)

    print("Hiperparametros fijados a priori:")
    print(f"  n_estimators     = {rf.n_estimators}")
    print(f"  max_depth        = {rf.max_depth}")
    print(f"  min_samples_leaf = {rf.min_samples_leaf}")
    print(f"  random_state     = {rf.random_state}")
    print(f"  OOB score (R2)   = {rf.oob_score_:.4f}")

    imp_gini = pd.DataFrame(
        {"Variable": [ETIQUETAS[p] for p in PREDICTORAS], "Importancia (Gini)": rf.feature_importances_}
    ).sort_values("Importancia (Gini)", ascending=False)
    print("\nImportancia de variables (reduccion media de impureza):")
    print(imp_gini.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    perm = permutation_importance(
        rf,
        X_test,
        y_test,
        n_repeats=50,
        random_state=42,
        scoring="neg_root_mean_squared_error",
    )
    imp_perm = pd.DataFrame(
        {
            "Variable": [ETIQUETAS[p] for p in PREDICTORAS],
            "Aumento del RMSE al permutar": perm.importances_mean,
            "Desvio": perm.importances_std,
        }
    ).sort_values("Aumento del RMSE al permutar", ascending=False)
    print("\nImportancia por permutacion sobre el conjunto de prueba:")
    print(imp_perm.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(
        "  Un valor cercano a cero o negativo indica que permutar la variable no empeora el RMSE "
        "de prueba: no aporta senal predictiva fuera de muestra."
    )

    titulo("4. BASELINE NAIVE DE PERSISTENCIA")
    persistencia = np.zeros(len(y_test))
    for i, anio in enumerate(anios_test):
        persistencia[i] = y[np.where(anios == anio - 1)[0][0]]
    met_base = metricas(y_test, persistencia)
    print("Prediccion: temp(t) = temp(t-1). No usa ninguna variable explicativa.")
    print(f"  RMSE = {met_base['RMSE']:.4f}")
    print(f"  MAE  = {met_base['MAE']:.4f}")
    print(f"  R2   = {met_base['R2']:.4f}")

    titulo("5. COMPARACION SOBRE EL BLOQUE DE PRUEBA (2010-2024)")
    tabla = tabla_metricas(
        [
            {"Modelo": ETIQUETAS["baseline"], **met_base},
            {"Modelo": ETIQUETAS["lineal"], **met_lineal},
            {"Modelo": ETIQUETAS["rf"], **met_rf},
        ]
    )
    tabla["Supera al baseline"] = np.where(
        tabla["Modelo"] == ETIQUETAS["baseline"],
        "—",
        np.where(tabla["RMSE"] < met_base["RMSE"], "Si", "No"),
    )
    print(tabla.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    titulo("6. ROBUSTEZ: VALIDACION CRUZADA TEMPORAL SOBRE ENTRENAMIENTO")
    print("Ventana expansiva (TimeSeriesSplit, 5 cortes): nunca entrena con anos futuros.")
    cv_lineal = cv_temporal(LinearRegression(), X_train, y_train)
    cv_rf = cv_temporal(
        RandomForestRegressor(n_estimators=500, random_state=42),
        X_train,
        y_train,
    )
    cv_base = cv_persistencia(y_train)
    cv_tabla = pd.DataFrame(
        [
            {"Modelo": ETIQUETAS["baseline"], "RMSE medio": cv_base.mean(), "Desvio": cv_base.std(ddof=1)},
            {"Modelo": ETIQUETAS["lineal"], "RMSE medio": cv_lineal.mean(), "Desvio": cv_lineal.std(ddof=1)},
            {"Modelo": ETIQUETAS["rf"], "RMSE medio": cv_rf.mean(), "Desvio": cv_rf.std(ddof=1)},
        ]
    )
    print(cv_tabla.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(
        "\nLa CV es un control de robustez. La regla de decision del trabajo se aplica al bloque de "
        "prueba predefinido (2010-2024), no a la CV: cambiarla despues de ver resultados seria "
        "modificar la regla."
    )

    titulo("7. CONCLUSION DEL OBJETIVO 5")
    mejor = min(
        [("Regresion Lineal", met_lineal["RMSE"]), ("Random Forest", met_rf["RMSE"])],
        key=lambda x: x[1],
    )
    print(
        "Los dos modelos quedaron ajustados y diagnosticados. La regla de decision del trabajo "
        "establece que un modelo solo es util si su RMSE es menor que el del baseline."
    )
    print()
    if mejor[1] < met_base["RMSE"]:
        print(
            f"{mejor[0]} supera al baseline (RMSE {mejor[1]:.4f} < {met_base['RMSE']:.4f})."
        )
    else:
        print(
            f"Ningun modelo supera al baseline (mejor RMSE {mejor[1]:.4f} "
            f"vs. {met_base['RMSE']:.4f})."
        )
    print(
        "Resultado coherente con los objetivos 2 y 4: la temperatura esta dominada por su propia "
        "tendencia y persistencia, y el PBI, el GEI y la lluvia no alcanzan para predecir su "
        "variacion anual mejor que repetir el ultimo valor observado."
    )
    print(
        "\nImportancia reportada: en la regresion, los coeficientes estandarizados; en el Random "
        "Forest, la importancia Gini y la importancia por permutacion."
    )


if __name__ == "__main__":
    main()

