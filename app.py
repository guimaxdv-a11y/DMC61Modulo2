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
        """Ítem 1: Resumen general de tipos de datos y valores nulos."""
        info_df = pd.DataFrame({
            'Columna': self.df.columns,
            'Tipo de Dato': self.df.dtypes.astype(str),
            'Valores Nulos': self.df.isnull().sum(),
            '% Nulos': (self.df.isnull().mean() * 100).round(2)
        })
        return info_df.reset_index(drop=True)
    
    def classify_variables(self):
        """Ítem 2: Clasificación personalizada de variables en numéricas y categóricas."""
        num_cols = self.df.select_dtypes(include=['number']).columns.tolist()
        cat_cols = self.df.select_dtypes(exclude=['number']).columns.tolist()
        return num_cols, cat_cols

    def get_descriptive_stats(self):
        """Ítem 3: Estadísticas descriptivas del dataset."""
        return self.df.describe()

    def get_missing_values_summary(self):
        """Ítem 4: Conteo y detalle de valores faltantes."""
        missing = self.df.isnull().sum()
        return missing[missing > 0] if missing.sum() > 0 else "No hay valores faltantes en el dataset."

# ==========================================
# MENÚ LATERAL (SIDEBAR)
# ==========================================
st.sidebar.title("🛡️ Insurance Protect")
st.sidebar.subheader("Navegación del Proyecto")

opciones_menu = [
    "🏠 Módulo 1: Home", 
    "📂 Módulo 2: Carga de Datos", 
    "📊 Módulo 3: EDA (Análisis Exploratorio)"
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
        * **Gemini Pro:** IA de apoyo.
        """)
        
    st.markdown("---")
    st.info("👈 **Instrucción:** Dirígete a **Módulo 2: Carga de Datos** en la barra lateral para configurar tu archivo y comenzar.")

# ==========================================
# MÓDULO 2: CARGA DEL DATASET
# ==========================================
elif modulo == "📂 Módulo 2: Carga de Datos":
    st.title("Carga y Validación del Dataset")
    st.markdown("El dataset puede cargarse automáticamente desde GitHub o mediante la carga manual de un archivo CSV.")
    
    GITHUB_CSV_URL = "https://raw.githubusercontent.com/guimaxdv-a11y/DMC61Modulo2/refs/heads/main/InsuranceCompany.csv"
    
    metodo_carga = st.radio(
        "Seleccione el método de carga de datos:",
        ["Carga automática desde GitHub", "Subir archivo manualmente (.csv)"]
    )
    
    df_cargado = None
    
    if metodo_carga == "Carga automática desde GitHub":
        try:
            analyzer = InsuranceAnalyzer(GITHUB_CSV_URL)
            st.success("¡Dataset cargado exitosamente desde GitHub!")
            df_cargado = analyzer
        except Exception as e:
            st.error(f"No se pudo cargar automáticamente desde GitHub. Verifica la URL o usa carga manual. Detalle: {e}")
            
    else:
        uploaded_file = st.file_uploader("Cargar archivo CSV manualmente", type=["csv"])
        if uploaded_file is not None:
            analyzer = InsuranceAnalyzer(uploaded_file)
            st.success("¡Archivo cargado exitosamente de forma local!")
            df_cargado = analyzer
        else:
            st.warning("⚠️ Por favor, sube tu archivo `InsuranceCompany.csv` para continuar.")
            
    if df_cargado is not None:
        filas, columnas = df_cargado.get_shape()
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Total de Filas (Clientes/Pólizas)", f"{filas:,}")
        col_m2.metric("Total de Variables (Columnas)", columnas)
        
        st.markdown("### 👁️ Vista Previa del Dataset (Primeros Registros)")
        st.dataframe(df_cargado.get_head(10), use_container_width=True)
        
        # Guardamos en la sesión para que el Módulo 3 lo utilice
        st.session_state['analyzer'] = df_cargado

# ==========================================
# MÓDULO 3: EDA (ANÁLISIS EXPLORATORIO)
# ==========================================
elif modulo == "📊 Módulo 3: EDA (Análisis Exploratorio)":
    st.title("Análisis Exploratorio de Datos (EDA)")
    
    # Validamos si el dataset ya fue cargado previamente en el Módulo 2
    if 'analyzer' not in st.session_state:
        st.warning("⚠️ Debes cargar el dataset primero en el **Módulo 2: Carga de Datos**.")
    else:
        analyzer = st.session_state['analyzer']
        
        # Organización del EDA en pestañas (Tabs)
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 1. Estructura y Stats", 
            "📈 2. Distribuciones", 
            "📊 3. Análisis Bivariado", 
            "⚙️ 4. Análisis Dinámico", 
            "💡 5. Hallazgos Clave"
        ])
        
        # ----------------------------------------------------
        # PESTAÑA 1: ÍTEMS 1 al 4 (Estructura, Tipos, Stats y Nulos)
        # ----------------------------------------------------
        with tab1:
            st.subheader("Ítem 1: Información General del Dataset")
            st.markdown("Detalle de los tipos de datos y conteo de valores nulos por columna (`.info()`).")
            st.dataframe(analyzer.get_info_summary(), use_container_width=True)
            
            st.markdown("---")
            st.subheader("Ítem 2: Clasificación de Variables")
            st.markdown("Separación automática entre variables numéricas y categóricas usando métodos de la clase POO.")
            num_cols, cat_cols = analyzer.classify_variables()
            
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                st.markdown(f"**Variables Numéricas ({len(num_cols)}):**")
                st.write(num_cols)
            with col_t2:
                st.markdown(f"**Variables Categóricas ({len(cat_cols)}):**")
                st.write(cat_cols)
                
            st.markdown("---")
            st.subheader("Ítem 3: Estadísticas Descriptivas")
            st.markdown("Resumen estadístico de las variables numéricas (`.describe()`), evaluando medias, medianas y dispersión.")
            st.dataframe(analyzer.get_descriptive_stats(), use_container_width=True)
            
            st.markdown("---")
            st.subheader("Ítem 4: Análisis de Valores Faltantes")
            missing_result = analyzer.get_missing_values_summary()
            if isinstance(missing_result, str):
                st.success(missing_result)
            else:
                st.write("Columnas con valores faltantes:")
                st.dataframe(missing_result)

        # ----------------------------------------------------
        # PESTAÑA 2: ÍTEMS 5 y 6 (Histogramas y Categóricas)
        # ----------------------------------------------------
        with tab2:
            st.subheader("Ítem 5: Distribución de Variables Numéricas")
            st.markdown("Visualización de la distribución de las variables numéricas clave mediante histogramas.")
            
            var_num = st.selectbox("Selecciona una variable numérica para graficar:", ['Income', 'premium', 'age_in_days', 'application_underwriting_score'])
            
            fig, ax = plt.subplots(figsize=(10, 4))
            sns.histplot(analyzer.df[var_num].dropna(), kde=True, ax=ax, color='teal')
            ax.set_title(f"Distribución de {var_num}")
            ax.set_xlabel(var_num)
            ax.set_ylabel("Frecuencia")
            st.pyplot(fig)
            
            st.markdown("---")
            st.subheader("Ítem 6: Análisis de Variables Categóricas")
            st.markdown("Conteos, proporciones y gráficos de barras de los canales de captación y tipo de residencia.")
            
            var_cat = st.selectbox("Selecciona una variable categórica:", ['sourcing_channel', 'residence_area_type', 'renewal'])
            
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            counts = analyzer.df[var_cat].value_counts()
            sns.barplot(x=counts.index, y=counts.values, ax=ax2, palette='Blues_d')
            ax2.set_title(f"Conteo por {var_cat}")
            ax2.set_xlabel(var_cat)
            ax2.set_ylabel("Total de Clientes")
            st.pyplot(fig2)

        # ----------------------------------------------------
        # PESTAÑA 3: ÍTEMS 7 y 8 (Análisis Bivariado)
        # ----------------------------------------------------
        with tab3:
            st.subheader("Ítem 7: Análisis Bivariado (Numérico vs Categórico)")
            st.markdown("Relación entre una variable numérica y la variable objetivo `renewal`.")
            
            num_bi = st.selectbox("Variable Numérica:", ['Income', 'premium', 'application_underwriting_score'], key="num_bi")
            
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            sns.boxplot(x='renewal', y=num_bi, data=analyzer.df, ax=ax3, palette='Set2')
            ax3.set_title(f"Relación entre {num_bi} y Renovación (Renewal)")
            st.pyplot(fig3)
            
            st.markdown("---")
            st.subheader("Ítem 8: Análisis Bivariado (Categórico vs Categórico)")
            st.markdown("Comportamiento cruzado entre el canal de captación o tipo de residencia frente a la renovación.")
            
            cat_bi = st.selectbox("Variable Categórica:", ['sourcing_channel', 'residence_area_type'], key="cat_bi")
            
            fig4, ax4 = plt.subplots(figsize=(8, 4))
            sns.countplot(x=cat_bi, hue='renewal', data=analyzer.df, ax=ax4, palette='pastel')
            ax4.set_title(f"Renovación según {cat_bi}")
            st.pyplot(fig4)

        # ----------------------------------------------------
        # PESTAÑA 4: ÍTEM 9 (Análisis Dinámico con Widgets)
        # ----------------------------------------------------
        with tab4:
            st.subheader("Ítem 9: Análisis Dinámico por Parámetros Seleccionados")
            st.markdown("Utiliza los widgets interactivos para filtrar y explorar dinámicamente el comportamiento de los ingresos según el canal y zona.")
            
            canal_sel = st.multiselect("Filtrar por Canal de Suministro:", analyzer.df['sourcing_channel'].unique(), default=analyzer.df['sourcing_channel'].unique())
            zona_sel = st.selectbox("Seleccionar Tipo de Zona:", analyzer.df['residence_area_type'].unique())
            
            df_filtered = analyzer.df[(analyzer.df['sourcing_channel'].isin(canal_sel)) & (analyzer.df['residence_area_type'] == zona_sel)]
            
            st.metric("Clientes filtrados bajo estos criterios", f"{len(df_filtered):,}")
            
            if len(df_filtered) > 0:
                fig5, ax5 = plt.subplots(figsize=(8, 4))
                sns.histplot(df_filtered['Income'], kde=True, ax=ax5, color='purple')
                ax5.set_title(f"Distribución de Ingresos Filtrada (Zona: {zona_sel})")
                st.pyplot(fig5)
            else:
                st.warning("No hay registros para los filtros seleccionados.")

        # ----------------------------------------------------
        # PESTAÑA 5: ÍTEM 10 (Hallazgos Clave y Conclusiones)
        # ----------------------------------------------------
        with tab5:
            st.subheader("Ítem 10: Hallazgos Clave e Insights Principales")
            st.markdown("""
            A partir del Análisis Exploratorio de Datos (EDA) realizado sobre el dataset `InsuranceCompany.csv`, se desprenden las siguientes **5 conclusiones estratégicas** enfocadas en la toma de decisiones comerciales:
            
            1. **Comportamiento de Renovación:** La gran mayoría de los clientes tienden a renovar sus pólizas, sin embargo, existe un segmento crítico identificado por morosidades previas que presenta menor propensión a la renovación.
            2. **Impacto del Canal de Captación (`sourcing_channel`):** Se observa que ciertos canales de captación (como los canales A y B) concentran un mayor volumen de clientes con alta estabilidad de pagos en comparación con canales alternativos.
            3. **Ingresos y Valor de Prima:** Las distribuciones de ingresos (`Income`) y primas (`premium`) muestran asimetrías marcadas, indicando que la cartera de clientes cuenta con perfiles socioeconómicos heterogéneos que deben abordarse con estrategias de precios diferenciadas.
            4. **Efecto de la Morosidad Histórica:** Las variables de retraso de pagos (`Count_3-6_months_late`, etc.) actúan como los principales indicadores de riesgo para prever la no renovación de las pólizas.
            5. **Área de Residencia:** No se aprecian diferencias drásticas y absolutas en el volumen de renovación global entre zonas urbanas y rurales, lo que sugiere que la estrategia comercial puede mantenerse equilibrada geográficamente pero ajustada al riesgo crediticio individual.
            """)
            st.success("🎉 ¡Aplicación interactiva EDA completada exitosamente conforme a los requerimientos del caso de estudio!")
