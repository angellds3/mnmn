# -*- coding: utf-8 -*-
"""Aplicaciona.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1N45EB0qM2ngHSjvI-vtaiFDv3wyVKvYo
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

#funcion que si gana, vuelve a tradear el mismo dia.
#si pierde deja de tradear, y vuelve el proximo dia.
def simulacion_trading_nasdaq(n, exito, fecha_inicio, capital_inicial, pip_win, pip_lose, valor_pip):
    # Crear un DataFrame vacío
  data = pd.DataFrame({
        'fecha': [None] * n,
        'win': [None] * n,
        'capital': [None] * n,
        'lote': [None] * n,
        'ganancia/perdida': [None] * n
    })

    # Inicializar la primera fila con la fecha de inicio y el capital inicial
  data['fecha'][0] = fecha_inicio
  data['capital'][0] = capital_inicial

    # Generar valores aleatorios para la columna 'win'
  data['win'] = np.random.binomial(n=1, p=exito, size=n)
  data['win'] = np.where(data['win'] == 1, 'si', 'no')

    # Rellenar las columnas según las condiciones dadas
  for i in range(1, n):
        # Fecha
      if data['win'][i-1] == 'si':
          data['fecha'][i] = data['fecha'][i-1]
      else:
          data['fecha'][i] = data['fecha'][i-1] + timedelta(days=1)

        # Calcular el lote según el capital
      if data['capital'][i-1] >= 370000:
          data['lote'][i] = 0.07
      elif data['capital'][i-1] >= 300000:
          data['lote'][i] = 0.06
      elif data['capital'][i-1] >= 230000:
          data['lote'][i] = 0.05
      elif data['capital'][i-1] >= 190000:
          data['lote'][i] = 0.04
      elif data['capital'][i-1] >= 140000:
          data['lote'][i] = 0.03
      elif data['capital'][i-1] >= 90000:
          data['lote'][i] = 0.02
      elif data['capital'][i-1] >= 20000:
          data['lote'][i] = 0.01
      else:
          data['lote'][i] = 0.0

        # Ganancia/Pérdida
      if data['win'][i-1] == 'si':
            data['ganancia/perdida'][i] = valor_pip * data['lote'][i] * 100 * pip_win
      else:
          data['ganancia/perdida'][i] = valor_pip*-data['lote'][i] * 100 * pip_lose

        # Capital
      data['capital'][i] = data['capital'][i-1] + data['ganancia/perdida'][i]

  return data

import streamlit as st
import pandas as pd

def graficar_convergencia_streamlit(estimaciones, titulo="Gráfica de Convergencia de Rentabilidad",
                                    nombre_x="Repeticiones", nombre_y="Rentabilidad Media"):
    """
    Genera una gráfica de convergencia básica usando st.line_chart de Streamlit.

    Parámetros:
        estimaciones (list): Lista con los valores a graficar.
        titulo (str): Título principal del gráfico.
        nombre_x (str): Nombre del eje X.
        nombre_y (str): Nombre del eje Y.
    """
    # Crear DataFrame
    data = pd.DataFrame({
        nombre_x: range(1, len(estimaciones) + 1),
        nombre_y: estimaciones
    })

    # Calcular media y mediana
    media = sum(estimaciones) / len(estimaciones)
    mediana = sorted(estimaciones)[len(estimaciones) // 2]

    # Mostrar gráfico
    st.subheader(titulo)
    st.line_chart(data, x=nombre_x, y=nombre_y)

    # Mostrar media y mediana como texto
    st.text(f"Media: {media:.2f}")
    st.text(f"Mediana: {mediana:.2f}")

import streamlit as st
import pandas as pd
import numpy as np

# Título de la aplicación
st.title("Simulación de Estrategias de Trading")

# Entradas de usuario
st.header("Parámetros de Simulación")

nsimulaciones = st.number_input("Número de simulaciones", min_value=1, value=100, max_value=500, step=1)
nreplicas = st.number_input("Número de réplicas", min_value=1, value=5, max_value=10, step=1)

ndias = st.number_input("Número de días", min_value=1, value=60, step=1)

exito = st.slider("Probabilidad de éxito (%)", min_value=0, max_value=100, value=50) / 100

fecha_inicio = st.date_input("Fecha de inicio")
capital_inicial = st.number_input("Capital inicial ($)", min_value=0, value=100000, step=1)

pip_win = st.number_input("Pips por operación ganadora", value=20, step=1)
pip_lose = st.number_input("Pips por operación perdedora", value=-20, step=1)

valor_pip = st.number_input("Valor de un pip ($)", min_value=1.00, value=18.00, step=0.01)

criterio_exito = st.number_input("Criterio de éxito (capital máximo $)", min_value=0, value=1500, step=1)
criterio_fracaso = st.number_input("Criterio de fracaso (capital mínimo $)", min_value=0, value=500, step=1)

# Botón para iniciar la simulación
if st.button("Iniciar Simulación"):
  estimaciones_r1 =[]
  simulacion_fracaso = 0
  simulacion_exito = 0

  for i in range(nsimulaciones):
    for j in range(nreplicas):
      resultado = simulacion_trading_nasdaq(ndias, exito,fecha_inicio, capital_inicial, pip_win, pip_lose, valor_pip)
      estimaciones_r1.append(resultado['capital'][ndias-1])
      if estimaciones_r1[i] < criterio_fracaso:
        simulacion_fracaso = simulacion_fracaso + 1
      else:
        if estimaciones_r1[i] > criterio_exito:
          simulacion_exito = simulacion_exito + 1

  st.write(f"**Total de simulaciones:** {nsimulaciones*nreplicas}")
  st.write(f"**Resultados**")
  st.write(f"**Simulaciones con éxito** (capital final > {criterio_exito}): {simulacion_exito}")
  st.write(f"**Simulaciones con fracaso** (capital final < {criterio_fracaso}):  {simulacion_fracaso}")
  st.write(f"")

  st.write(f"**Proporción de éxito con la estrategia:** {simulacion_exito/(simulacion_fracaso+simulacion_exito)}")
  st.write(f"")

  graficar_convergencia_streamlit(estimaciones_r1)