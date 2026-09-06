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
    "📊 Módulo 3: EDA (Próximamente)"
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
    El propósito de esta aplicación interactiva es analizar el comportamiento histórico de los clientes de una compañía de seguros utilizando el dataset `InsuranceCompany.csv`. El foco principal es explorar y entender **qué factores influyen en la renovación de una póliza de seguro (`renewal`)**, aplicando los conceptos fundamentales aprendidos en el curso de forma integrada y profesional[cite: 1].
    """)
    
    st.markdown("---")
    
    # Columnas para organizar la información del autor y el entorno tecnológico
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👨‍💻 Datos del Autor / Estudiante")
        st.markdown("""
        * **Nombre:** [Tu Nombre Completo]
        * **Curso:** Especialización en Python for Analytics[cite: 1]
        * **Institución:** Dilic Institute[cite: 1]
        * **Año:** 2026
        """)
        
    with col2:
        st.markdown("### ⚙️ Tecnologías Utilizadas")
        st.markdown("""
        * **Python:** Lenguaje principal de programación[cite: 1].
        * **Pandas & NumPy:** Manipulación y cálculo numérico[cite: 1].
        * **Matplotlib & Seaborn:** Visualización avanzada de datos[cite: 1].
        * **Streamlit:** Construcción de la aplicación web interactiva[cite: 1].
        """)
        
    st.markdown("---")
    st.info("👈 **Instrucción:** Dirígete a **Módulo 2: Carga de Datos** en la barra lateral para cargar tu archivo CSV y comenzar con la exploración.")

# ==========================================
# MÓDULO 2: CARGA DEL DATASET
# ==========================================
elif modulo == "📂 Módulo 2: Carga de Datos":
    st.title("Carga y Validación del Dataset")
    st.markdown("Sube tu archivo `InsuranceCompany.csv` para habilitar el motor de análisis exploratorio.")
    
    uploaded_file = st.file_uploader("Cargar archivo CSV", type=["csv"])
    
    if uploaded_file is not None:
        # Instanciamos nuestra clase POO
        analyzer = InsuranceAnalyzer(uploaded_file)
        
        st.success("¡Archivo cargado exitosamente!")
        
        # Mostrar dimensiones
        filas, columnas = analyzer.get_shape()
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Filas (Clientes/Pólizas)", f"{filas:,}")
        col_m2.metric("Total de Variables (Columnas)", columnas)
        
        st.markdown("### 👁️ Vista Previa del Dataset (Primeros Registros)")
        st.dataframe(analyzer.get_head(10), use_container_width=True)
        
        # Guardamos el archivo en la sesión para usarlo en los siguientes módulos
        st.session_state['analyzer'] = analyzer
    else:
        st.warning("⚠️ Por favor, carga el archivo `InsuranceCompany.csv` para continuar.")
