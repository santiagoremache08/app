
import streamlit as st
import pandas as pd
import math
from fractions import Fraction

st.title("Análisis de Dispersión de Datos")

st.write("Ingresa hasta 5 pares de datos `xi` y `fi`")

N_FILAS = 5
xi_vals = []
fi_vals = []

for i in range(N_FILAS):
    col1, col2 = st.columns(2)
    with col1:
        xi_input = st.text_input(f"xi {i+1}", key=f"xi_{i}")
    with col2:
        fi_input = st.text_input(f"fi {i+1}", key=f"fi_{i}")
    xi_vals.append(xi_input)
    fi_vals.append(fi_input)

if st.button("Calcular"):
    try:
        datos = []
        for xi_str, fi_str in zip(xi_vals, fi_vals):
            if xi_str.strip() and fi_str.strip():
                xi = Fraction(xi_str)
                fi = Fraction(fi_str)
                datos.append((xi, fi))

        if not datos:
            st.warning("Por favor ingresa al menos un par de valores xi y fi.")
        else:
            df = pd.DataFrame(datos, columns=['xi', 'fi'])
            df['fi*xi'] = df['xi'] * df['fi']
            suma_fi = sum(df['fi'])
            suma_fixi = sum(df['fi*xi'])
            media = suma_fixi / suma_fi
            df['xi - Media'] = df['xi'] - media
            df['(xi - Media)^2'] = df['xi - Media'] ** 2
            df['(xi - Media)^2 * fi'] = df['(xi - Media)^2'] * df['fi']
            suma_varianza = sum(df['(xi - Media)^2 * fi'])
            varianza = suma_varianza / suma_fi
            desviacion = math.sqrt(float(varianza))
            rango = max(df['xi']) - min(df['xi'])

            st.subheader("Tabla de análisis:")
            st.dataframe(df)

            st.markdown(f"**Media:** {float(media):.4f}")
            st.markdown(f"**Rango:** {float(rango):.4f}")
            st.markdown(f"**Varianza poblacional:** {float(varianza):.4f}")
            st.markdown(f"**Desviación estándar poblacional:** {desviacion:.8f}")

    except Exception as e:
        st.error(f"Error: {e}")
