import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("📈 Gráficas de series de tiempo")

entrada = st.text_input(
    "Ingrese la serie, separada por comas:",
    value="10,12,33,36,50,65,75,85"
)

# -----------------------------------
# CONVERTIR DATOS
# -----------------------------------

entrada2 = entrada.split(",")

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
# TENDENCIA LINEAL
# -----------------------------------

pendiente, intercepto = np.polyfit(x, y, 1)

# -----------------------------------
# HORIZONTE
# -----------------------------------

horizonte = 6

# Periodos futuros
periodos_futuros = np.arange(
    len(serie) + 1,
    len(serie) + horizonte + 1
)

# Pronóstico futuro
valores_futuros = (
    pendiente * periodos_futuros
    + intercepto
)

# -----------------------------------
# PRONÓSTICO EMPALMADO
# -----------------------------------

# Incluimos el último periodo real para
# que la línea punteada empiece desde allí

x_pronostico = np.concatenate([
    [len(serie)],
    periodos_futuros
])

y_pronostico = np.concatenate([
    [serie[-1]],
    valores_futuros
])

# -----------------------------------
# CREAR GRÁFICO
# -----------------------------------

fig = go.Figure()

# SERIE HISTÓRICA
fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode="lines+markers",
        name="Serie real",
        line=dict(
            width=3
        ),
        marker=dict(
            size=7
        )
    )
)

# PRONÓSTICO PUNTEADO
fig.add_trace(
    go.Scatter(
        x=x_pronostico,
        y=y_pronostico,
        mode="lines+markers",
        name="Pronóstico",
        line=dict(
            dash="dot",
            width=3
        ),
        marker=dict(
            size=7
        )
    )
)

# -----------------------------------
# DISEÑO
# -----------------------------------

fig.update_layout(
    title="Serie histórica + pronóstico",
    xaxis_title="Periodo",
    yaxis_title="Valor",

    hovermode="x unified",

    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),

    height=500
)

fig.update_xaxes(
    dtick=1
)

# -----------------------------------
# MOSTRAR GRÁFICO
# -----------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# ECUACIÓN
# -----------------------------------

st.write(
    f"📊 Tendencia calculada: "
    f"y = {pendiente:.2f}x + {intercepto:.2f}"
)

# -----------------------------------
# TABLA PRONÓSTICO
# -----------------------------------

st.subheader("🔮 Pronóstico próximos 6 periodos")

df_pronostico = pd.DataFrame({
    "Periodo": periodos_futuros,
    "Pronóstico": valores_futuros
})

st.dataframe(
    df_pronostico,
    use_container_width=True,
    hide_index=True
)
