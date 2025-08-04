import streamlit as st
import pandas as pd
from fractions import Fraction
import math

st.title("Análisis de Dispersión de Datos (en Fracciones)")

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
            # Crear DataFrame
            df = pd.DataFrame(datos, columns=['xi', 'fi'])
            df['fi*xi'] = df['xi'] * df['fi']
            suma_fi = sum(df['fi'])
            suma_fixi = sum(df['fi*xi'])
            media = suma_fixi / suma_fi  # Media como fracción

            # Calcular columnas derivadas
            df['xi - Media'] = df['xi'] - media
            df['(xi - Media)^2'] = df['xi - Media'].apply(lambda x: x * x)
            df['(xi - Media)^2 * fi'] = df['(xi - Media)^2'] * df['fi']
            suma_varianza = sum(df['(xi - Media)^2 * fi'])
            varianza = suma_varianza / suma_fi

            # Desviación estándar solo en decimal
            desviacion = math.sqrt(float(varianza))
            rango = max(df['xi']) - min(df['xi'])

            # Mostrar tabla con fracciones
            st.subheader("Tabla de análisis:")
            st.dataframe(df.astype(str))

            # Mostrar resultados
            st.markdown(f"**Media:** {media}")
            st.markdown(f"**Rango:** {rango}")
            st.markdown(f"**Varianza poblacional:** {varianza}")
            st.markdown(f"**Desviación estándar poblacional:** {desviacion:.8f}")

    except Exception as e:
        st.error(f"Error: {e}")

