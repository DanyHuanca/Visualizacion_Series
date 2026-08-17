import streamlit as st

st.title("Graficas de series de tiempo")

entrada = st.text_input("Ingrese la serie, separada por comas,", value="10,20,30,40,50")
entrada2 = entrada.split(",")

serie = [float(i) for i in entrada2]

st.line_chart(serie)
