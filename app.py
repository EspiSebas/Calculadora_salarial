import streamlit as st
import pandas as pd
from datetime import timedelta

st.set_page_config(page_title="Cálculo de Salario Semanal", layout="centered")

st.title("🧮 Cálculo de Salario Semanal de Empleado")

# Subir archivo Excel
archivo = st.file_uploader("📂 Sube el archivo Excel", type=["xlsx"])

if archivo:
    try:
        df = pd.read_excel(archivo)

        # Limpiar datos de entrada
        df["Hora Entrada"] = df["Hora Entrada"].astype(str).str.strip()
        df["Hora Salida"] = df["Hora Salida"].astype(str).str.strip()

        st.success("✅ Archivo cargado correctamente")

        st.subheader("Vista previa del archivo:")
        st.dataframe(df)

        # Ingreso de nombre y valor por hora
        nombre_empleado = st.text_input("👤 Nombre del empleado", value="Carlos")
        precio_hora = st.number_input("💰 Valor por hora", min_value=1000, step=500, value=8000)
        descuento = st.number_input("💰 Valor del descuento", min_value=0, value=0)
        descuentoComida = st.number_input("¿Cuanto dias comio?", min_value=0, value=0)
        
    
        
        if st.button("Calcular salario"):
            df_emp = df[df["Nombre"].str.lower() == nombre_empleado.lower()]

            if df_emp.empty:
                st.warning("⚠️ No se encontraron registros para ese empleado.")
            else:
                
                def calcular_horas(entrada_str, salida_str):
                    try:
                        # Convierte la entrada y salida sin formato fijo, dejando que pandas lo intente inferir
                        entrada = pd.to_datetime(entrada_str, errors='coerce')
                        salida = pd.to_datetime(salida_str, errors='coerce')


                        if pd.isna(entrada) or pd.isna(salida):
                            return 0

                        # Solo interesa la hora y minuto, fijamos la fecha igual para ambos para comparación
                        entrada = entrada.replace(year=1900, month=1, day=1)
                        salida = salida.replace(year=1900, month=1, day=1)

                        if salida <= entrada:
                            salida += timedelta(days=1)

                        duracion = salida - entrada

                        horas = duracion.total_seconds() / 3600

                        return round(horas, 2)
                    except Exception as e:
                        st.error(f"Error al calcular horas: {e}")
                        return 0


                total_horas = 0
                detalles = []
                valorComida = descuentoComida * (precio_hora/4)
                
                
                for _, fila in df_emp.iterrows():
                    horas = calcular_horas(fila["Hora Entrada"], fila["Hora Salida"])
                    total_horas += horas 
                    detalles.append(f"{fila['Día']}: {horas} horas")

                salario_total = (total_horas * precio_hora) - descuento - valorComida

                st.subheader("📋 Detalle de horas trabajadas:")
                for linea in detalles:
                    st.write(linea)

                st.markdown(f"### 🕒 Total horas: `{total_horas}`")
                st.markdown(f"### 💵 Salario total: `$ {salario_total:,.0f}`")
                st.markdown(f"### 💵 Descuento de comida: `$ {valorComida:,.0f}`")
                

    except Exception as e:
        st.error(f"❌ Error al procesar el archivo: {e}")
