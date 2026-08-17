import streamlit as st
import pandas as pd

# --------------------------------------------------
# CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------

st.set_page_config(
    page_title="Analizador de Series",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# TÍTULO
# --------------------------------------------------

st.title("📈 Analizador de Series de Tiempo")

st.write(
    """
    Ingresa una serie de números separados por comas para analizar
    su comportamiento y visualizar diferentes gráficos.
    """
)

st.divider()


# --------------------------------------------------
# BARRA LATERAL
# --------------------------------------------------

st.sidebar.header("⚙️ Configuración")

entrada = st.sidebar.text_input(
    "Ingrese la serie",
    value="10,20,30,40,50",
    help="Ejemplo: 10,20,30,40,50"
)

tipo_grafico = st.sidebar.selectbox(
    "Tipo de gráfico",
    [
        "Línea",
        "Área",
        "Barras"
    ]
)

mostrar_promedio = st.sidebar.checkbox(
    "Mostrar promedio móvil"
)

ventana = st.sidebar.slider(
    "Ventana del promedio móvil",
    min_value=2,
    max_value=10,
    value=3
)


# --------------------------------------------------
# PROCESAR DATOS
# --------------------------------------------------

try:

    entrada2 = entrada.split(",")

    # Eliminamos espacios y valores vacíos
    serie = [
        float(i.strip())
        for i in entrada2
        if i.strip() != ""
    ]

    if len(serie) == 0:
        st.warning("⚠️ Debes ingresar al menos un número.")
        st.stop()

except ValueError:

    st.error(
        "❌ La serie contiene valores que no son números."
    )

    st.info(
        "Ejemplo correcto: 10,20,30,40,50"
    )

    st.stop()


# --------------------------------------------------
# CREAR DATAFRAME
# --------------------------------------------------

df = pd.DataFrame({
    "Periodo": range(1, len(serie) + 1),
    "Valor": serie
})

df = df.set_index("Periodo")


# --------------------------------------------------
# MÉTRICAS
# --------------------------------------------------

st.subheader("📊 Resumen estadístico")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Cantidad de datos",
        len(serie)
    )

with col2:
    st.metric(
        "Promedio",
        f"{df['Valor'].mean():.2f}"
    )

with col3:
    st.metric(
        "Valor máximo",
        f"{df['Valor'].max():.2f}"
    )

with col4:
    st.metric(
        "Valor mínimo",
        f"{df['Valor'].min():.2f}"
    )


st.divider()


# --------------------------------------------------
# GRÁFICO
# --------------------------------------------------

st.subheader("📈 Visualización")

datos_grafico = df.copy()

if mostrar_promedio:

    datos_grafico["Promedio móvil"] = (
        datos_grafico["Valor"]
        .rolling(window=ventana)
        .mean()
    )


if tipo_grafico == "Línea":

    st.line_chart(
        datos_grafico,
        height=450
    )


elif tipo_grafico == "Área":

    st.area_chart(
        datos_grafico,
        height=450
    )


elif tipo_grafico == "Barras":

    st.bar_chart(
        datos_grafico,
        height=450
    )


# --------------------------------------------------
# INFORMACIÓN ADICIONAL
# --------------------------------------------------

st.divider()

col_izquierda, col_derecha = st.columns(2)


# TABLA
with col_izquierda:

    st.subheader("📋 Datos ingresados")

    st.dataframe(
        df,
        use_container_width=True
    )


# ESTADÍSTICAS
with col_derecha:

    st.subheader("📐 Estadísticas")

    estadisticas = df.describe()

    st.dataframe(
        estadisticas,
        use_container_width=True
    )


# --------------------------------------------------
# VARIACIÓN
# --------------------------------------------------

st.divider()

st.subheader("🔄 Variación entre periodos")

df_variacion = df.copy()

df_variacion["Variación"] = (
    df_variacion["Valor"]
    .diff()
)

df_variacion["Variación %"] = (
    df_variacion["Valor"]
    .pct_change() * 100
)

st.dataframe(
    df_variacion,
    use_container_width=True
)


# --------------------------------------------------
# DESCARGAR CSV
# --------------------------------------------------

st.divider()

st.subheader("📥 Descargar información")

csv = df_variacion.to_csv().encode("utf-8")

st.download_button(
    label="📥 Descargar CSV",
    data=csv,
    file_name="serie_tiempo.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "Aplicación desarrollada con Python + Streamlit 🐍"
)
