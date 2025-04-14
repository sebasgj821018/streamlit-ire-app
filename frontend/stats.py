# frontend/stats.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi
from fpdf import FPDF
import os

# ------------------ CARGA DE MODELOS ------------------
@st.cache_resource
def cargar_modelos():
    modelo_rendimiento, cols_rend = joblib.load('modelos/modelo_rendimiento.pkl')
    modelo_disponibilidad, cols_disp = joblib.load('modelos/modelo_disponibilidad.pkl')
    modelo_coste, cols_coste = joblib.load('modelos/modelo_coste.pkl')
    return (modelo_rendimiento, cols_rend), (modelo_disponibilidad, cols_disp), (modelo_coste, cols_coste)

(modelo_rendimiento, cols_rendimiento), (modelo_disponibilidad, cols_disponibilidad), (modelo_coste, cols_coste) = cargar_modelos()

# ------------------ COMENTARIO AUTOMÁTICO ------------------
def generar_comentario(r, d, c):
    if r > 1.5 and c < 50:
        return "Jugador de alto rendimiento con coste competitivo."
    elif r > 1.5 and d > 0.8:
        return "Jugador confiable con alto rendimiento sostenido."
    elif d < 0.6 and r > 1.2:
        return "Jugador con buen rendimiento, pero baja disponibilidad."
    elif c > 90:
        return "Jugador de coste elevado, analizar con más detalle su valor potencial."
    else:
        return "Jugador con métricas estables, apto para análisis en contexto."

# ------------------ PDF ------------------
class ReporteJugadorPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "Reporte Individual del Jugador", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Página {self.page_no()}", align="C")

    def agregar_info_jugador(self, nombre, posicion, r, d, c, ire, comentario):
        self.set_font("Arial", "", 12)
        self.cell(0, 10, f"Nombre del Jugador: {nombre}", ln=True)
        self.cell(0, 10, f"Posición: {posicion}", ln=True)
        self.cell(0, 10, f"Pred. Rendimiento: {r:.2f}", ln=True)
        self.cell(0, 10, f"Pred. Disponibilidad: {d:.2f}", ln=True)
        self.cell(0, 10, f"Pred. Coste (Euros): {c:,.2f}", ln=True)
        self.cell(0, 10, f"IRE: {ire:.2f}", ln=True)
        self.ln(8)
        self.set_font("Arial", "B", 12)
        self.multi_cell(0, 10, f"Comentario del Sistema:\n{comentario}")
        self.ln(10)

# ------------------ APP PRINCIPAL ------------------
def app():
    st.title("📊 Análisis de Jugadores - Índice de Rentabilidad Esperada (IRE)")

    st.sidebar.header("📂 Carga de datos")
    archivo = st.sidebar.file_uploader("Sube un archivo CSV con datos de jugadores", type=["csv"])

    if archivo is not None:
        df = pd.read_csv(archivo)
        st.success("✅ Datos cargados correctamente.")
        st.dataframe(df.head())

        # Validación de columnas
        for feature_list, nombre_modelo in zip(
            [cols_rendimiento, cols_disponibilidad, cols_coste],
            ['rendimiento', 'disponibilidad', 'coste']
        ):
            faltantes = [col for col in feature_list if col not in df.columns]
            if faltantes:
                st.error(f"❌ El archivo no contiene las columnas necesarias para el modelo de {nombre_modelo}: {faltantes}")
                st.stop()

        # Predicciones
        df['pred_rendimiento'] = modelo_rendimiento.predict(df[cols_rendimiento])
        df['pred_disponibilidad'] = modelo_disponibilidad.predict(df[cols_disponibilidad])
        df['pred_coste'] = np.exp(modelo_coste.predict(df[cols_coste]))

        # Cálculo del IRE
        st.sidebar.subheader("⚖️ Pesos para el cálculo del IRE")
        w1 = st.sidebar.slider("Peso del Rendimiento", 0.0, 1.0, 0.4, step=0.05)
        w2 = st.sidebar.slider("Peso de la Disponibilidad", 0.0, 1.0, 0.4, step=0.05)
        w3 = st.sidebar.slider("Peso del Coste", 0.0, 1.0, 0.2, step=0.05)

        df['IRE'] = (w1 * df['pred_rendimiento']) + (w2 * df['pred_disponibilidad']) - (w3 * df['pred_coste'])

        # Filtros
        st.sidebar.subheader("🎛️ Filtros")
        posiciones = df['posicion'].unique().tolist()
        posiciones_seleccionadas = st.sidebar.multiselect("Filtrar por posición:", posiciones, default=posiciones)
        edad_min, edad_max = st.sidebar.slider("Filtrar por edad:", int(df['Edad'].min()), int(df['Edad'].max()), (18, 35))
        ire_min = st.sidebar.slider("Filtrar por IRE mínimo:", float(df['IRE'].min()), float(df['IRE'].max()), float(df['IRE'].min()))

        df_filtrado = df[(df['posicion'].isin(posiciones_seleccionadas)) &
                         (df['Edad'].between(edad_min, edad_max)) &
                         (df['IRE'] >= ire_min)]

        # Visualización en tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Ranking", "🕸️ Radar", "🔵 Dispersión", "📉 Histogramas", "🔥 Heatmap"])

        with tab1:
            st.subheader("🏅 Ranking por IRE")
            ranking_cols = ['Nombre_jugador', 'posicion', 'pred_rendimiento', 'pred_disponibilidad', 'pred_coste', 'IRE']
            df_ranking = df_filtrado[ranking_cols].sort_values(by='IRE', ascending=False).reset_index(drop=True)
            st.dataframe(df_ranking.style.background_gradient(cmap='Greens'))

            jugador_seleccionado = st.selectbox("Selecciona un jugador para generar PDF:", df_ranking['Nombre_jugador'])
            if st.button("📥 Generar Reporte PDF"):
                jugador = df_ranking[df_ranking['Nombre_jugador'] == jugador_seleccionado].iloc[0]
                comentario = generar_comentario(jugador['pred_rendimiento'], jugador['pred_disponibilidad'], jugador['pred_coste'])
                pdf = ReporteJugadorPDF()
                pdf.add_page()
                pdf.agregar_info_jugador(
                    jugador['Nombre_jugador'], jugador['posicion'],
                    jugador['pred_rendimiento'], jugador['pred_disponibilidad'],
                    jugador['pred_coste'], jugador['IRE'], comentario
                )
                ruta_pdf = f"reporte_{jugador['Nombre_jugador'].replace(' ', '_')}.pdf"
                pdf.output(ruta_pdf)
                with open(ruta_pdf, "rb") as f:
                    st.download_button("⬇️ Descargar Reporte PDF", f, file_name=ruta_pdf, mime="application/pdf")

        with tab2:
            st.subheader("🕸️ Radar Chart - Top 3 jugadores")
            top3 = df_filtrado.sort_values(by='IRE', ascending=False).head(3)

            def radar_plot(player_row):
                categories = ['pred_rendimiento', 'pred_disponibilidad', 'pred_coste']
                values = player_row[categories].values.flatten().tolist()
                values[2] *= -1  # Invertir coste

                max_vals = [df[c].max() if c != 'pred_coste' else -df[c].min() for c in categories]
                values = [v / m if m != 0 else 0 for v, m in zip(values, max_vals)]
                values += values[:1]
                angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
                angles += angles[:1]

                fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
                ax.plot(angles, values, linewidth=2.5, linestyle='solid', color='royalblue')
                ax.fill(angles, values, color='skyblue', alpha=0.5)
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(categories, fontsize=13)
                ax.set_yticklabels([])
                ax.set_title(f"Radar - {player_row['Nombre_jugador']}", size=16, pad=20)
                st.pyplot(fig)

            for _, row in top3.iterrows():
                radar_plot(row)

        with tab3:
            st.subheader("🔵 Dispersión Rendimiento vs Disponibilidad")
            fig, ax = plt.subplots(figsize=(8, 6))
            s = (df_filtrado['IRE'] - df_filtrado['IRE'].min() + 0.01) * 80
            scatter = ax.scatter(df_filtrado['pred_rendimiento'], df_filtrado['pred_disponibilidad'],
                                 s=s, alpha=0.6, c=df_filtrado['pred_coste'], cmap='viridis', edgecolors='black')
            ax.set_xlabel('Rendimiento', fontsize=12)
            ax.set_ylabel('Disponibilidad', fontsize=12)
            plt.colorbar(scatter, label='Coste')
            st.pyplot(fig)

        with tab4:
            st.subheader("📉 Histogramas")
            fig, axs = plt.subplots(1, 3, figsize=(15, 4))
            axs[0].hist(df_filtrado['pred_rendimiento'], bins=10, color='blue', alpha=0.6)
            axs[0].set_title('Distribución de Rendimiento')
            axs[1].hist(df_filtrado['pred_disponibilidad'], bins=10, color='green', alpha=0.6)
            axs[1].set_title('Distribución de Disponibilidad')
            axs[2].hist(df_filtrado['pred_coste'], bins=10, color='red', alpha=0.6)
            axs[2].set_title('Distribución de Coste')
            st.pyplot(fig)

        with tab5:
            st.subheader("🔥 Mapa de Calor")
            corr = df_filtrado[['pred_rendimiento', 'pred_disponibilidad', 'pred_coste', 'IRE']].corr()
            fig, ax = plt.subplots()
            sns.heatmap(corr, annot=True, cmap='coolwarm', center=0, ax=ax)
            st.pyplot(fig)

    else:
        st.warning("🔸 Por favor, carga un archivo CSV con datos de jugadores para comenzar.")
