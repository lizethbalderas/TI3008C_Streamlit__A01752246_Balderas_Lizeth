import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Explorador de operación",
    page_icon="📊",
    layout="wide",
)


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Carga los datos que utilizará la aplicación."""
    datos = pd.read_csv("datos_ejemplo.csv")
    datos["Fecha"] = pd.to_datetime(datos["Fecha"])
    return datos


df = cargar_datos()

st.title("Explorador de operación")
st.caption("Aplicación inicial para explorar resultados por área y región.")

# TODO OBLIGATORIO: escribe tu nombre completo.
st.write("**Desarrollado por: Lizeth Jaqueline Balderas Sánchez :)")

st.sidebar.header("Filtros")

areas_disponibles = sorted(df["Área"].unique())
areas_seleccionadas = st.sidebar.multiselect(
    "Área",
    options=areas_disponibles,
    default=areas_disponibles,
)

df_filtrado = df[df["Área"].isin(areas_seleccionadas)].copy()

st.subheader("Datos disponibles")
st.dataframe(df_filtrado, width="stretch", hide_index=True)

casos_por_fecha = (
    df_filtrado.groupby("Fecha", as_index=False)["Casos"]
    .sum()
    .sort_values("Fecha")
)

fig = px.line(
    casos_por_fecha,
    x="Fecha",
    y="Casos",
    markers=True,
    title="Casos por fecha",
)
st.plotly_chart(fig, width="stretch")

st.info(
    "Esta es la versión inicial. Selecciona una opción de la actividad y agrega "
    "una mejora funcional para el usuario."
)


# ================================================================
# ZONA DE TRABAJO
# Implementa UNA de las opciones indicadas en INSTRUCCIONES_ACTIVIDAD.md.
# Puedes reorganizar el código existente cuando sea necesario.
# ================================================================



# TODO OPCIÓN C: Simulador
# - Solicita al menos dos valores al usuario.
# - Realiza un cálculo con esos valores.
# - Muestra un resultado y un mensaje success, warning o error.

st.divider()
st.subheader("Simulador de Estimación de Horas de Trabajo")

# 1. estas serán las entrdas del usuario:
col_input1, col_input2 = st.columns(2)

with col_input1:
    casos_esperados = st.number_input(
        "Número de casos esperados",
        min_value=1,
        max_value=500,
        value=100,
        step=5
    )

with col_input2:
    minutos_por_caso = st.slider(
        "Tiempo promedio por caso (minutos)",
        min_value=5,
        max_value=120,
        value=30
    )

# 2 calculo que se hace basado en las entradas
horas_totales = (casos_esperados * minutos_por_caso) / 60.0

# 3 mostrar resultado mediante st.metric (visualización)
st.metric(
    label="Horas Totales Estimadas",
    value=f"{horas_totales:.1f} hrs"
)

# 4. Retroalimentación dinamica (st.success / st.warning)
limite_capacidad = 40.0  # Límite de horas semanales

if horas_totales > limite_capacidad:
    st.warning(
        f"La estimación ({horas_totales:.1f} hrs) supera la capacidad semanal disponible ({limite_capacidad} hrs)."
    )
else:
    st.success("La capacidad estimada es suficiente para cubrir la carga de trabajo.")