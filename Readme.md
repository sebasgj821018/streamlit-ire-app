# ? MVP - Índice de Rentabilidad Esperada (IRE)

Esta aplicación web predice el **rendimiento**, la **disponibilidad** y el **coste estimado** de jugadores de fútbol,
generando un índice personalizado llamado **IRE (Índice de Rentabilidad Esperada)**, ideal para tomar decisiones de scouting o fichajes.

- Rendimiento proyectado
- Disponibilidad
- Coste económico

## ?? ¿Cómo usarla?

1. Clona este repositorio
2. Instala dependencias con `pip install -r requirements.txt`
3. Ejecuta la app con `streamlit run app.py`
4. Carga un archivo CSV con los datos de jugadores

## ?? Funcionalidades


- ?? Sistema de login seguro (`streamlit-authenticator`)
- ?? Carga de datos CSV con validación automática
- ?? Predicciones usando modelos de ML previamente entrenados (.pkl)
- ?? Ajuste personalizado del IRE vía sliders
- ?? Visualización avanzada: radar, dispersión, histogramas, heatmap
- ?? Exportación de análisis individual en PDF
- ?? Descarga de resultados globales en CSV


## ?? Tecnologías utilizadas

- Python (pandas, scikit-learn, matplotlib, seaborn)
- Streamlit
- Modelos `.pkl` previamente entrenados


## ?? Descarga automática de modelos `.pkl`

Para mantener el repositorio liviano y evitar límites de tamaño de GitHub, los modelos predictivos no se incluyen directamente en el repositorio.  
En su lugar, al ejecutar la aplicación se descargan automáticamente desde Google Drive.

### ? ¿Cómo funciona?

El archivo `main.py` incluye un bloque que:

1. Crea la carpeta `modelos/` si no existe.
2. Verifica si ya existen los archivos:
   - `modelo_rendimiento.pkl`
   - `modelo_disponibilidad.pkl`
   - `modelo_coste.pkl`
3. Si alguno falta, lo descarga automáticamente desde enlaces públicos de Google Drive.

### ?? Requisitos

Asegúrate de que los modelos estén subidos a Google Drive con enlace compartido (modo: **"Cualquiera con el enlace"**), y reemplaza los IDs de los archivos en `main.py` aquí:

```python
modelos = {
		"modelo_coste.pkl": "https://drive.google.com/uc?export=download&id=1HH_tj48XOq11uUoeUf9YHiEKN879K36D",
        "modelo_disponibilidad.pkl": "https://drive.google.com/uc?export=download&id=1HIjw1Gy9emTrmcIV7cBfMNbNHLO2gT6k",
        "modelo_rendimiento.pkl": "https://drive.google.com/uc?export=download&id=1HL3sNtUcqVYTdOC4uKhpx9OJj2-SGHEI"
}


## ?? Autor

Sebastián Gaviria Jaramillo – Proyecto TFM | Máster en python Avanzado Aplicado al Deporte

