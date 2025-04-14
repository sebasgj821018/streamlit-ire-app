import streamlit as st
import os
st.set_page_config(page_title="MVP IRE", layout="wide")


# Asegurar que la carpeta 'modelos' exista
if not os.path.exists("modelos"):
    os.makedirs("modelos")

# Paso 1: Ejecutar el script para descargar los modelos si no existen
def descargar_modelos_si_es_necesario():
    import requests

    os.makedirs("modelos", exist_ok=True)

    modelos = {
        "modelo_coste.pkl": "https://drive.google.com/uc?export=download&id=1HH_tj48XOq11uUoeUf9YHiEKN879K36D",
        "modelo_disponibilidad.pkl": "https://drive.google.com/uc?export=download&id=1HIjw1Gy9emTrmcIV7cBfMNbNHLO2gT6k",
        "modelo_rendimiento.pkl": "https://drive.google.com/uc?export=download&id=1HL3sNtUcqVYTdOC4uKhpx9OJj2-SGHEI"
    }

    for nombre, url in modelos.items():
        ruta = os.path.join("modelos", nombre)
        if os.path.exists(ruta):
            continue
        st.write(f"⬇️ Descargando `{nombre}` ...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(ruta, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            st.success(f"✅ `{nombre}` descargado correctamente.")
        else:
            st.error(f"❌ Error al descargar `{nombre}`: código {response.status_code}")

# Ejecutar descarga antes de todo
descargar_modelos_si_es_necesario()

# Paso 2: Configuración y autenticación

from auth.login import autenticar_usuario
from frontend import home, stats

authenticator = autenticar_usuario()
name, authentication_status, username = authenticator.login("Iniciar sesión", "main")

# Paso 3: Navegación protegida
if authentication_status:
    authenticator.logout("Cerrar sesión", "sidebar")
    st.sidebar.success(f"Bienvenido {name} 👋")

    menu = st.sidebar.radio("Navegación", ["🏠 Home", "📊 Stats"])
    if menu == "🏠 Home":
        home.app()
    elif menu == "📊 Stats":
        stats.app()

elif authentication_status is False:
    st.error("Usuario o contraseña incorrectos.")
elif authentication_status is None:
    st.warning("Por favor inicia sesión.")
