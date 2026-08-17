import streamlit as st
import pandas as pd
import numpy as np

st.title("📈 Gráficas de series de tiempo")

entrada = st.text_input(
    "Ingrese la serie, separada por comas:",
    value="10,20,30,40,50"
)

entrada2 = entrada.split(",")

# Convertimos los datos a números
serie = [float(i.strip()) for i in entrada2 if i.strip() != ""]

# -----------------------------
# PERIODOS HISTÓRICOS
# -----------------------------

x = np.arange(1, len(serie) + 1)
y = np.array(serie)

# -----------------------------
# TENDENCIA LINEAL
# y = mx + b
# -----------------------------

pendiente, intercepto = np.polyfit(x, y, 1)

# -----------------------------
# PROYECCIÓN DE 6 PERIODOS
# -----------------------------

horizonte = 6

periodos_totales = np.arange(
    1,
    len(serie) + horizonte + 1
)

tendencia = (
    pendiente * periodos_totales
    + intercepto
)

# -----------------------------
# DATAFRAME PARA EL GRÁFICO
# -----------------------------

df = pd.DataFrame({
    "Periodo": periodos_totales,
    "Serie real": serie + [np.nan] * horizonte,
    "Tendencia": tendencia
})

df = df.set_index("Periodo")

# -----------------------------
# GRÁFICO
# -----------------------------

st.subheader("Serie histórica + tendencia")

st.line_chart(df)

# -----------------------------
# INFORMACIÓN DE LA TENDENCIA
# -----------------------------

st.write(
    f"📊 Ecuación de tendencia: "
    f"y = {pendiente:.2f}x + {intercepto:.2f}"
)

# -----------------------------
# PRONÓSTICO
# -----------------------------

st.subheader("🔮 Proyección próximos 6 periodos")

pronostico = df.tail(horizonte)[["Tendencia"]]

pronostico = pronostico.rename(
    columns={"Tendencia": "Pronóstico"}
)

st.dataframe(pronostico)
