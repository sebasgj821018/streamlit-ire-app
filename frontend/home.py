# frontend/home.py
import streamlit as st

def app():
    st.title("⚽ Bienvenido al MVP - Índice de Rentabilidad Esperada (IRE)")

    st.markdown("""
    ---
    ## 🎯 Objetivo de la aplicación

    Esta aplicación te permite analizar la **rentabilidad esperada de posibles fichajes**, basada en tres dimensiones clave:

    - 📈 **Rendimiento proyectado** (predicción del impacto deportivo)
    - ❤️ **Disponibilidad esperada** (probabilidad de que el jugador esté disponible)
    - 💰 **Coste estimado por minuto de juego**

    Estos tres factores se combinan en un índice personalizado llamado **IRE (Índice de Rentabilidad Esperada)**.

    ---

    ## 🛠️ ¿Qué puedes hacer aquí?

    - Subir datos de jugadores reales o sintéticos (formato CSV)
    - Calcular predicciones automáticas con modelos IA entrenados previamente
    - Ajustar los pesos de las dimensiones del IRE
    - Visualizar gráficas interactivas: radar, dispersión, histogramas, heatmap
    - Generar reportes PDF individuales por jugador

    ---

    ## 📁 Recomendación de estructura del archivo CSV

    Asegúrate de que tu archivo contenga las siguientes columnas mínimas:

    - `Nombre_jugador`, `Edad`, `posicion`
    - + Variables requeridas por los modelos de rendimiento, disponibilidad y coste

    ---

    ## 🚀 Empecemos

    Dirígete a la sección **"📈 Stats"** desde el menú lateral para subir tu archivo y visualizar resultados.
    """)
