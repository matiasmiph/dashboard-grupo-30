# dashboard_tarea_grupo30.py

# --- Librerías necesarias ---
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime

# --- Configuración de la página ---
st.set_page_config(page_title="Dashboard Ventas - Grupo 30", layout="wide")
sns.set(style="whitegrid")

# --- Cargar datos con caché para rendimiento ---
@st.cache_data
def cargar_datos():
    return pd.read_csv("data.csv")

df = cargar_datos()

# --- Título principal ---
st.title("📊 Dashboard de Ventas - Cadena de Tiendas")
st.markdown("Análisis interactivo sobre ventas, productos, clientes y tendencias de comportamiento.")

# --- Filtros laterales ---
st.sidebar.header("Filtros disponibles")
filtro_ciudad = st.sidebar.multiselect("Selecciona ciudad:", df["City"].unique(), default=df["City"].unique())
filtro_producto = st.sidebar.multiselect("Selecciona línea de producto:", df["Product line"].unique(), default=df["Product line"].unique())

# --- Aplicar filtros al DataFrame ---
df_filtrado = df[(df["City"].isin(filtro_ciudad)) & (df["Product line"].isin(filtro_producto))]

# --- INICIO DEL BLOQUE DE CÓDIGO SOLICITADO (Filtro Slider por Fecha) ---
# Este bloque debe realizar la conversión, crear el slider y filtrar
st.sidebar.subheader("Filtro por Fecha")

# CONVERSIÓN DE FECHA DENTRO DE ESTE BLOQUE (Necesario para .min() y .max() funcionen después)
# Esto puede ser menos eficiente si se repite mucho, pero resuelve el AttributeError
df_filtrado['Date'] = pd.to_datetime(df_filtrado['Date'], errors='coerce')
df_filtrado.dropna(subset=['Date'], inplace=True)
min_date_dt = df_filtrado['Date'].min().to_pydatetime()
max_date_dt = df_filtrado['Date'].max().to_pydatetime()

# Crear el slider de rango de fechas
date_range = st.sidebar.slider(
    "Selecciona un rango de fechas:",
    min_value=min_date_dt,
    max_value=max_date_dt,
    value=(min_date_dt, max_date_dt), # Valor inicial: rango completo del df_filtrado
    format="YYYY-MM-DD")

start_date_dt, end_date_dt = date_range
# Aplicar el filtro de fecha
df_filtrado_por_fecha = df_filtrado[(df_filtrado['Date'] >= start_date_dt) & (df_filtrado['Date'] <= end_date_dt)]

# --- Gráfico 1: Ventas por Fecha ---
st.subheader("1️⃣ Evolución de Ventas Totales en el Tiempo")
ventas_por_fecha = df_filtrado_por_fecha.groupby("Date")["Total"].sum()

fig1, ax1 = plt.subplots()
ventas_por_fecha.plot(kind="line", ax=ax1, marker="o")
ax1.set_title(f"Ventas Totales por Día ({start_date_dt.strftime('%Y-%m-%d')} a {end_date_dt.strftime('%Y-%m-%d')})")
ax1.set_xlabel("Fecha")
ax1.set_ylabel("Monto Total de Ventas")
ax1.grid(True, linestyle='--', alpha=0.6)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

st.pyplot(fig1)

# --- Gráfico 2: Ingresos por Línea de Producto ---
st.subheader("2️⃣ Ingresos por Línea de Producto")
ingresos_por_producto = df_filtrado_por_fecha.groupby("Product line")["Total"].sum().sort_values()

fig2, ax2 = plt.subplots()
ingresos_por_producto.plot(kind="barh", ax=ax2, color="seagreen")
ax2.set_title("Total de Ingresos por Categoría de Producto")
ax2.set_xlabel("Monto Total")
st.pyplot(fig2)

# --- Gráfico 3: Métodos de Pago ---
st.subheader("3️⃣ Distribución de Métodos de Pago")
conteo_pago = df_filtrado_por_fecha["Payment"].value_counts()

fig3, ax3 = plt.subplots()
conteo_pago.plot(kind="pie", autopct="%1.1f%%", startangle=90, ax=ax3, colors=sns.color_palette("pastel"))
ax3.set_ylabel("")
ax3.set_title("Preferencias de Método de Pago")
st.pyplot(fig3)

# --- Gráfico 4: Calificaciones de Clientes ---
st.subheader("4️⃣ Distribución de Calificaciones de Clientes")
fig4, ax4 = plt.subplots()
sns.histplot(df_filtrado_por_fecha["Rating"], bins=20, kde=True, color="mediumpurple", ax=ax4)
ax4.set_title("Distribución del Rating")
ax4.set_xlabel("Rating")
ax4.set_ylabel("Frecuencia")
st.pyplot(fig4)

# --- Gráfico 5: Gasto por Tipo de Cliente ---
st.subheader("5️⃣ Gasto Total por Tipo de Cliente")
fig5, ax5 = plt.subplots()
sns.boxplot(x="Customer type", y="Total", data=df_filtrado_por_fecha, palette="Set2", ax=ax5)
ax5.set_title("Comparación del Gasto Total según Tipo de Cliente")
ax5.set_xlabel("Tipo de Cliente")
ax5.set_ylabel("Total Gastado")
st.pyplot(fig5)

# --- Pie de página ---
st.markdown("---")
st.markdown("🔍 **Grupo 30 | Curso: Visualización de Datos en Python**")
