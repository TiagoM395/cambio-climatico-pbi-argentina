@echo off
setlocal enabledelayedexpansion
title Cambio climatico y PBI - Streamlit

REM ==========================================================================
REM  Lanzador del proyecto - Cambio climatico y PBI en Argentina (1961-2024)
REM  Objetivos 1 a 6
REM
REM  Uso:  doble clic sobre este archivo, o desde la terminal:
REM        Levantar.bat
REM ==========================================================================

cd /d "%~dp0"

echo.
echo  ==============================================================
echo    Cambio climatico y PBI en Argentina
echo    Objetivos 1 a 6  ^|  Streamlit
echo  ==============================================================
echo.

REM --------------------------------------------------------------------------
REM  1. Determinar que interprete de Python usar
REM --------------------------------------------------------------------------
set "PY="
if exist ".venv\Scripts\python.exe" (
    set "PY=.venv\Scripts\python.exe"
    echo  [OK]   Entorno virtual .venv detectado
) else (
    set "PY=python"
    echo  [INFO] Se usara Python del sistema
)
echo.

REM --------------------------------------------------------------------------
REM  2. Verificar que Python exista
REM --------------------------------------------------------------------------
%PY% --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] No se encontro Python en este equipo.
    echo.
    echo  Instalalo desde:  https://www.python.org/downloads/
    echo  During the setup, mark the option "Add Python to PATH".
    echo.
    pause
    exit /b 1
)

%PY% --version 2>&1 | findstr /i "python" >nul
if not errorlevel 1 (
    for /f "tokens=*" %%v in ('%PY% --version 2^>^&1') do set "PYVER=%%v"
    echo  [OK]   !PYVER!
)
echo.

REM --------------------------------------------------------------------------
REM  3. Verificar e instalar dependencias
REM --------------------------------------------------------------------------
%PY% -c "import streamlit, pandas, numpy, scipy, statsmodels, plotly, sklearn" >nul 2>&1
if errorlevel 1 (
    echo  [AVISO] Faltan dependencias. Instalando, puede tardar unos minutos...
    echo.
    %PY% -m pip install --upgrade pip --quiet
    %PY% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo  [ERROR] No se pudieron instalar las dependencias.
        echo  Revisa tu conexion a internet o el archivo requirements.txt.
        echo.
        pause
        exit /b 1
    )
    echo.
    echo  [OK]   Dependencias instaladas correctamente
) else (
    echo  [OK]   Todas las dependencias estan instaladas
)
echo.

REM --------------------------------------------------------------------------
REM  4. Verificar que existan los datos
REM --------------------------------------------------------------------------
if not exist "data\processed\dataset_nacional.csv" (
    echo  [ERROR] No se encontro el archivo de datos:
    echo          data\processed\dataset_nacional.csv
    echo.
    echo  La aplicacion no puede funcionar sin el dataset.
    echo  Verifica que la carpeta "data" este junto a este archivo .bat
    echo.
    pause
    exit /b 1
)
echo  [OK]   Dataset encontrado - data\processed\dataset_nacional.csv
echo.

REM --------------------------------------------------------------------------
REM  5. Elegir puerto disponible
REM --------------------------------------------------------------------------
set "PUERTO=8501"
%PY% -c "import socket,sys; s=socket.socket(); r=s.connect_ex(('127.0.0.1',8501)); s.close(); sys.exit(0 if r==0 else 1)" >nul 2>&1
if not errorlevel 1 (
    set "PUERTO=8502"
    echo  [AVISO] El puerto 8501 esta ocupado, se usara el 8502
    echo.
)

REM --------------------------------------------------------------------------
REM  6. Abrir el navegador y lanzar la app
REM --------------------------------------------------------------------------
echo  --------------------------------------------------------------
echo   Iniciando Streamlit en  http://localhost:!PUERTO!
echo   Presiona Ctrl+C en esta ventana para detener la aplicacion.
echo  --------------------------------------------------------------
echo.

start "" /min cmd /c "timeout /t 5 /nobreak >nul & start "" http://localhost:!PUERTO!"

%PY% -m streamlit run app.py --server.port !PUERTO!

echo.
echo  La aplicacion se detuvo.
pause