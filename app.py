import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración inicial de la página de Streamlit
st.set_page_config(
    page_title="EDA - Insurance Company",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CLASE PRINCIPAL DE ANÁLISIS (POO)
# ==========================================
class InsuranceAnalyzer:
    """Clase para encapsular la carga, procesamiento y análisis del dataset de seguros."""
    def __init__(self, uploaded_file):
        self.df = pd.read_csv(uploaded_file)
        
    def get_shape(self):
        """Retorna las dimensiones del dataset (filas, columnas)."""
        return self.df.shape
    
    def get_head(self, n=5):
        """Retorna las primeras n filas del dataset."""
        return self.df.head(n)
    
    def get_info_summary(self):
        """Prepara un resumen de tipos de datos y valores nulos."""
        info_df = pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores Nulos': self.df.isnull().sum(),
            '% Nulos': (self.df.isnull().mean() * 100).round(2)
        })
        return info_df.reset_index(drop=True)

# ==========================================
# MENÚ LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("🛡️ Insurance Protect")
st.sidebar.subheader("Navegación del Proyecto")

# Definimos las opciones exactamente iguales a cómo se renderizan
opciones_menu = [
    "🏠 Módulo 1: Home", 
    "📂 Módulo 2: Carga de Datos", 
    "📊 Módulo 3: EDA"
]
modulo = st.sidebar.radio("Seleccione un Módulo:", opciones_menu)

# ==========================================
# MÓDULO 1: HOME (PRESENTACIÓN)
# ==========================================
if modulo == "🏠 Módulo 1: Home":
    st.title("Proyecto Aplicado: Análisis Exploratorio de Datos (EDA)")
    st.subheader("Especialización en Python for Analytics")
    
    st.markdown("""
    ### 🎯 Objetivo del Análisis
    El propósito de esta aplicación interactiva es analizar el comportamiento histórico de los clientes de una compañía de seguros utilizando el dataset `InsuranceCompany.csv`. El foco principal es explorar y entender **qué factores influyen en la renovación de una póliza de seguro (`renewal`)**, aplicando los conceptos fundamentales aprendidos en el curso de forma integrada y profesional.
    """)
    
    st.markdown("---")
    
    # Columnas para organizar la información del autor y el entorno tecnológico
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨‍💻 Datos del Autor")
        st.markdown("""
        * **Nombre:** Guillermo M. Donayre Vásquez
        * **Curso:** Especialización en Python for Analytics
        * **Institución:** DMC Institute
        * **Año:** 2026
        """)
        
    with col2:
        st.markdown("### ⚙️ Tecnologías Utilizadas")
        st.markdown("""
        * **Python:** Lenguaje principal de programación.
        * **Pandas & NumPy:** Manipulación y cálculo numérico.
        * **Matplotlib & Seaborn:** Visualización avanzada de datos.
        * **Streamlit:** Construcción de la aplicación web interactiva.
         * **Gemini Pro:** Apoyo de IA.
        """)
        
    st.markdown("---")
    st.info("👈 **Instrucción:** Dirígete a **Módulo 2: Carga de Datos** en la barra lateral para cargar tu archivo CSV y comenzar con la exploración.")

# ==========================================
# MÓDULO 2: CARGA DEL DATASET
# ==========================================
elif modulo == "📂 Módulo 2: Carga de Datos":
    st.title("Carga y Validación del Dataset")
    st.markdown("El dataset puede cargarse automáticamente desde el repositorio o mediante la carga manual de un archivo CSV.")
    
    # URL directa al archivo Raw en GitHub (reemplaza esta URL con la tuya real)
    GITHUB_CSV_URL = "https://raw.githubusercontent.com/guimaxdv-a11y/DMC61Modulo2/refs/heads/main/InsuranceCompany.csv"
    
    # Opción para elegir el método de carga
    metodo_carga = st.radio(
        "Seleccione el método de carga de datos:",
        ["Carga automática desde GitHub", "Subir archivo manualmente (.csv)"]
    )
    
    df_cargado = None
    
    if metodo_carga == "Carga automática desde GitHub":
        try:
            # Creamos una instancia usando directamente la URL de GitHub
            analyzer = InsuranceAnalyzer(GITHUB_CSV_URL)
            st.success("¡Dataset cargado exitosamente desde GitHub!")
            df_cargado = analyzer
        except Exception as e:
            st.error(f"No se pudo cargar automáticamente desde GitHub. Verifica la URL. Error: {e}")
            
    else:
        uploaded_file = st.file_uploader("Cargar archivo CSV manualmente", type=["csv"])
        if uploaded_file is not None:
            analyzer = InsuranceAnalyzer(uploaded_file)
            st.success("¡Archivo cargado exitosamente de forma local!")
            df_cargado = analyzer
        else:
            st.warning("⚠️ Por favor, sube tu archivo `InsuranceCompany.csv` para continuar.")
            
    # Si ya tenemos el analyzer listo, mostramos métricas y vista previa
    if df_cargado is not None:
        filas, columnas = df_cargado.get_shape()
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Filas (Clientes/Pólizas)", f"{filas:,}")
        col_m2.metric("Total de Variables (Columnas)", columnas)
        
        st.markdown("### 👁️ Vista Previa del Dataset (Primeros Registros)")
        st.dataframe(df_cargado.get_head(10), use_container_width=True)
        
        # Guardamos en la sesión para el Módulo 3 (EDA)
        st.session_state['analyzer'] = df_cargado
