
import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Gráficas de series de tiempo")

entrada = st.text_input(
    "Ingrese la serie, separada por comas:",
    value="10,20,30,40,50"
)

entrada2 = entrada.split(",")

# Convertir datos ingresados a números
serie = [
    float(i.strip())
    for i in entrada2
    if i.strip() != ""
]

# -----------------------------------
# PERIODOS HISTÓRICOS
# -----------------------------------

x = np.arange(1, len(serie) + 1)
y = np.array(serie)

# -----------------------------------
# CALCULAR TENDENCIA LINEAL
# -----------------------------------

pendiente, intercepto = np.polyfit(x, y, 1)

# -----------------------------------
# HORIZONTE FUTURO
# -----------------------------------

horizonte = 6

periodos_totales = np.arange(
    1,
    len(serie) + horizonte + 1
)

# -----------------------------------
# SERIE HISTÓRICA
# -----------------------------------

serie_historica = serie + [np.nan] * horizonte

# -----------------------------------
# TENDENCIA SOLO PARA EL FUTURO
# -----------------------------------

tendencia_futura = [np.nan] * len(serie)

for periodo in range(
    len(serie) + 1,
    len(serie) + horizonte + 1
):
    valor_tendencia = pendiente * periodo + intercepto
    tendencia_futura.append(valor_tendencia)

# -----------------------------------
# DATAFRAME
# -----------------------------------

df = pd.DataFrame({
    "Periodo": periodos_totales,
    "Serie real": serie_historica,
    "Pronóstico": tendencia_futura
})

df = df.set_index("Periodo")

# -----------------------------------
# GRÁFICO
# -----------------------------------

st.subheader("Serie histórica + pronóstico")

st.line_chart(df)

# -----------------------------------
# ECUACIÓN DE TENDENCIA
# -----------------------------------

st.write(
    f"📊 Tendencia calculada: "
    f"y = {pendiente:.2f}x + {intercepto:.2f}"
)

# -----------------------------------
# TABLA DE PRONÓSTICO
# -----------------------------------

st.subheader("🔮 Pronóstico de los próximos 6 periodos")

pronostico = df.tail(horizonte)[["Pronóstico"]]

st.dataframe(
    pronostico,
    use_container_width=True
)
