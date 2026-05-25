import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# =========================
# CONFIGURACIÓN GENERAL
# =========================
st.set_page_config(
    page_title="Dashboard Control de Calidad Textil",
    page_icon="📊",
    layout="wide"
)
st.config.set_option("theme.base", "light")

# =========================
# ESTILOS CSS GLOBALES
# =========================
 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');
 
/* ── Base ── */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color:#005192;
    color: #1A1D23;
}
 
/* ── Ocultar decoración por defecto ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Background principal ── */
.stApp {
    background-color: #fff !important;
}
 
/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #97b6d3;
    border-right: 1px solid black;
}

/* ── Sidebar siempre visible, sin botón de colapso ── */
button[data-testid="baseButton-headerNoPadding"] {
    display: none !important;
    background-color:#97b6d3;
}

section[data-testid="stSidebar"] {
    min-width: 15% !important;
    max-width: 15% !important;
    transform: none !important;
    visibility: visible !important;
}

div[data-testid="stPlotlyChart"],
div[data-testid="stDataFrame"] {
    background-color: #FFFFFF !important;
}

h2, h3, .stSubheader {
    color: #1A1D23 !important;
}

/* ── Header principal ── */
.dashboard-header {
    margin: -80px 0 0 0;
    padding: -20px 0 1.5rem 0;
    border-bottom: 1px solid #E2E5EC;
    margin-bottom: 2rem;
}
.dashboard-header h1 {
    font-size: 1.6rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #1A1D23;
    margin: 0 0 0.2rem 0;
}
.dashboard-header p {
    font-size: 0.875rem;
    color: #6B7280;
    margin: 0;
    font-weight: 400;
}
 
/* ── KPI Cards ── */
.kpi-grid {
    display: flex;
    gap: 0.5rem;
    padding:0;
    margin: 0rem;
}
.kpi-card {
    flex: 1;
    background: #FFFFFF;
    border: 1px solid #E2E5EC;
    border-radius: 12px;
    padding: 0.2rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    cursor: default;
    min-width: 0;
}
.kpi-card:hover {
    transform: translateY(-4px) scale(1.03);
    box-shadow: 0 8px 24px rgba(0,0,0,0.10);
    border-color: #C7D2FE;
}
.kpi-icon {
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
    display: block;
}
.kpi-label {
    font-size: 0.5rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #9098A9;
    margin-bottom: 0.4rem;
    white-space: nowrap;
    overflow: visible;
    text-overflow: clip;
}
.kpi-value {
    font-size: 1rem;
    font-weight: 700;
    color: #1A1D23;
    font-family: 'DM Mono', monospace;
    letter-spacing: -0.01em;
    line-height: 1.1;
    white-space: nowrap;
}
 
/* ── Subtítulos de sección ── */
h2[data-testid="stHeadingWithActionElements"],
.stSubheader {
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #6B7280 !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
}
 
/* ── Separador ── */
hr {
    border: none;
    border-top: 1px solid #E2E5EC;
    margin: 2rem 0;
}
 
/* ── Dataframe ── */
div[data-testid="stDataFrame"] {
    border-radius: 10px;
    border: 1px solid #E2E5EC;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
 
/* ── Info / Alert ── */
div[data-testid="stAlert"] {
    background: #F0F4FF;
    border: 1px solid #C7D2FE;
    border-radius: 10px;
    color: #3730A3;
    font-size: 0.875rem;
}
 
/* ── Charts ── */
div[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #E2E5EC;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
 
 
</style>
""", unsafe_allow_html=True)
 
# =========================
# HEADER PERSONALIZADO
# =========================
 
st.markdown("""
<div class="dashboard-header">
    <h1>Control de Calidad Textil</h1>
    <p>Somos Cuadro · Análisis de rendimiento, defectos y aprovechamiento de tela</p>
</div>
""", unsafe_allow_html=True)

# =========================
# CARGA DE DATOS
# =========================

@st.cache_data

def cargar_datos():
    df = pd.read_csv("data_dashboard_final_2_salida.csv", sep=';')

    # Conversión de fechas
    df['Fecha_ISO'] = pd.to_datetime(df['Fecha_ISO'])
    df['Fecha_Recepción'] = pd.to_datetime(df['Fecha_Recepción'])

    return df


df = cargar_datos()

# =========================
# SIDEBAR - FILTROS
# =========================
 
st.sidebar.header("🔎 Filtros")
 
df_filtrado = df.copy()
 
# FILTRO FECHA
fechas_disponibles = sorted(df_filtrado['Fecha_Recepción'].dt.date.dropna().unique())
opciones_fecha = ['Todas'] + list(fechas_disponibles)
fecha_select = st.sidebar.selectbox("Fecha de recepción", options=opciones_fecha)
if fecha_select != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Fecha_Recepción'].dt.date == fecha_select]
 
# FILTRO TIPO DE TELA
lista_telas = sorted(df_filtrado['Tipo_de_tela'].dropna().unique())
tela_select = st.sidebar.selectbox("Tipo de tela", options=['Todas'] + list(lista_telas))
if tela_select != 'Todas':
    df_filtrado = df_filtrado[df_filtrado['Tipo_de_tela'] == tela_select]
 
# FILTRO COLOR
lista_colores = sorted(df_filtrado['Color'].dropna().unique())
color_select = st.sidebar.selectbox("Color", options=['Todos'] + list(lista_colores))
if color_select != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['Color'] == color_select]
 
# FILTRO ESTATUS
if 'Estatus' in df_filtrado.columns:
    lista_estatus = sorted(df_filtrado['Estatus'].dropna().unique())
    estatus_select = st.sidebar.selectbox("Estatus", options=['Todos'] + list(lista_estatus))
    if estatus_select != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Estatus'] == estatus_select]
 
# FILTRO TIPO DEFECTO
if 'Tipo_Defecto' in df_filtrado.columns:
    lista_defectos = sorted(df_filtrado['Tipo_Defecto'].dropna().unique())
    defecto_select = st.sidebar.selectbox("Tipo de defecto", options=['Todos'] + list(lista_defectos))
    if defecto_select != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['Tipo_Defecto'] == defecto_select]
# =========================
# KPIs PRINCIPALES
# =========================
 
st.subheader("📌 Indicadores Principales")
 
total_rollos = len(df_filtrado)
rollos_defecto = df_filtrado['Tiene_Defecto'].sum()
tasa_defectos = (rollos_defecto / total_rollos * 100 if total_rollos > 0 else 0)
 
if 'Estatus' in df_filtrado.columns:
    rollos_rechazados = df_filtrado['Estatus'].astype(str).str.upper().str.contains('RECHAZ').sum()
    rollos_aprobados = df_filtrado['Estatus'].astype(str).str.upper().str.contains('APROB').sum()
else:
    rollos_rechazados = 0
    rollos_aprobados = 0
 
tasa_rechazo = (rollos_rechazados / total_rollos * 100 if total_rollos > 0 else 0)
tasa_aprobacion = (rollos_aprobados / total_rollos * 100 if total_rollos > 0 else 0)
delta_metros_total = df_filtrado['Delta_Metros'].sum()
delta_kg_total = df_filtrado['Delta_Kg'].sum()
 
kpi_html = f"""
<div  class="kpi-grid">
    <div  class="kpi-card">
        <span class="kpi-icon">🎯</span>
        <div class="kpi-label">Rollos Auditados</div>
        <div class="kpi-value">{total_rollos:,}</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">⚠️</span>
        <div class="kpi-label">Tasa de Defectos</div>
        <div class="kpi-value">{tasa_defectos:.2f}%</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">❌</span>
        <div class="kpi-label">Tasa de Rechazo</div>
        <div class="kpi-value">{tasa_rechazo:.2f}%</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">✅</span>
        <div class="kpi-label">Tasa de Aprobación</div>
        <div class="kpi-value">{tasa_aprobacion:.2f}%</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">📏</span>
        <div class="kpi-label">Δ Histórico Metros</div>
        <div class="kpi-value">{delta_metros_total:,.2f} m</div>
    </div>
    <div class="kpi-card">
        <span class="kpi-icon">⚖️</span>
        <div class="kpi-label">Δ Histórico Kg</div>
        <div class="kpi-value">{delta_kg_total:,.2f} Kg</div>
    </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)
 
st.divider()

# =====================================
# SEMÁFORO HISTÓRICO DE ESTATUS
# =====================================

st.subheader("🚦 Estado Histórico de Calidad")

# -------------------------------------
# Cálculo de estatus
# -------------------------------------

estatus_series = (
    df_filtrado['Estatus']
    .astype(str)
    .str.upper()
)

cantidad_aprobados = estatus_series.str.contains('APROBADO').sum()

cantidad_desviacion = (
    estatus_series
    .str.contains('DESVIACION|DESVIACIÓN')
    .sum()
)

cantidad_rechazados = (
    estatus_series
    .str.contains('RECHAZ')
    .sum()
)

total_estatus = (
    cantidad_aprobados +
    cantidad_desviacion +
    cantidad_rechazados
)

# Evitar división entre cero
if total_estatus == 0:
    total_estatus = 1

# -------------------------------------
# Porcentajes
# -------------------------------------

porc_aprobados = (
    cantidad_aprobados / total_estatus * 100
)

porc_desviacion = (
    cantidad_desviacion / total_estatus * 100
)

porc_rechazados = (
    cantidad_rechazados / total_estatus * 100
)

# -------------------------------------
# DataFrame visual
# -------------------------------------

df_estatus = pd.DataFrame({

    'Estatus': [
        'Aprobado',
        'Aprobado con Desviación',
        'Rechazado'
    ],

    'Cantidad': [
        cantidad_aprobados,
        cantidad_desviacion,
        cantidad_rechazados
    ],

    'Porcentaje': [
        porc_aprobados,
        porc_desviacion,
        porc_rechazados
    ]
})

# -------------------------------------
# Barra horizontal tipo semáforo
# -------------------------------------

fig_estatus = go.Figure()

fig_estatus.add_trace(go.Bar(
    #y=['Estado Histórico'],
    x=[porc_aprobados],
    name='Aprobado',
    orientation='h',
    text=f"{cantidad_aprobados} rollos | {porc_aprobados:.1f}%",
    textposition='inside',
    marker_color='green'
))

fig_estatus.add_trace(go.Bar(
    #y=['Estado Histórico'],
    x=[porc_desviacion],
    name='Con Desviación',
    orientation='h',
    text=f"{cantidad_desviacion} rollos | {porc_desviacion:.1f}%",
    textposition='inside',
    marker_color='gold'
))

fig_estatus.add_trace(go.Bar(
   # y=['Estado Histórico'],
    x=[porc_rechazados],
    name='Rechazado',
    orientation='h',
    text=f"{cantidad_rechazados} rollos | {porc_rechazados:.1f}%",
    textposition='outside',
    marker_color='red'
))

fig_estatus.update_layout(

    paper_bgcolor='#FFFFFF',
    plot_bgcolor='#FFFFFF',
    font=dict(color='#1A1D23'),

    barmode='stack',

    height=220,

    xaxis=dict(
        title='Porcentaje (%)',
        range=[0, 100]
    ),

    yaxis=dict(
        title=''
    ),

    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='center',
        x=0.5
    )
)

st.plotly_chart(
    fig_estatus,
    use_container_width=True
)


# =====================================
# PARETO + RENDIMIENTO POR TELA
# =====================================

col_pareto, col_rendimiento = st.columns(2)

# =====================================
# PARETO DE DEFECTOS
# =====================================

with col_pareto:

    st.subheader("📊 Pareto de Defectos")

    # ---------------------------------
    # SOLO rollos con defecto
    # ---------------------------------

    df_defectos = df_filtrado[
        df_filtrado['Tiene_Defecto'] == 1
    ]

    # ---------------------------------
    # Mapeo flags
    # ---------------------------------

    defectos_flags = {

        'Flag_Idos': 'Idos',
        'Flag_Manchas': 'Manchas',
        'Flag_Huecos': 'Huecos',
        'Flag_Marcas_Agua': 'Marcas Agua',
        'Flag_Sucio': 'Sucio',
        'Flag_Empates': 'Empates'

    }

    # ---------------------------------
    # Conteo defectos
    # ---------------------------------

    conteo = []

    for columna, nombre in defectos_flags.items():

        if columna in df_defectos.columns:

            frecuencia = df_defectos[columna].sum()

            conteo.append({

                'Tipo_Defecto': nombre,
                'Frecuencia': frecuencia

            })

    # ---------------------------------
    # DataFrame base
    # ---------------------------------

    pareto_base = pd.DataFrame(conteo)

    # Evitar dataframe vacío
    if pareto_base.empty:

        st.warning("No hay defectos para visualizar.")

    else:

        # ---------------------------------
        # Filtrar > 0
        # ---------------------------------

        pareto_base = pareto_base[
            pareto_base['Frecuencia'] > 0
        ]

        # ---------------------------------
        # Ordenar
        # ---------------------------------

        pareto_base = pareto_base.sort_values(
            by='Frecuencia',
            ascending=False
        )

        # ---------------------------------
        # TOP 10 + OTROS
        # ---------------------------------

        top10 = pareto_base.head(10)

        otros = pareto_base.iloc[10:]['Frecuencia'].sum()

        if otros > 0:

            otros_df = pd.DataFrame({

                'Tipo_Defecto': ['OTROS'],
                'Frecuencia': [otros]

            })

            pareto_df = pd.concat(
                [top10, otros_df],
                ignore_index=True
            )

        else:

            pareto_df = top10.copy()

        # ---------------------------------
        # Porcentaje individual
        # ---------------------------------

        pareto_df['Porcentaje_Individual'] = (

            pareto_df['Frecuencia'] /
            pareto_df['Frecuencia'].sum()

        ) * 100

        # ---------------------------------
        # Porcentaje acumulado
        # ---------------------------------

        pareto_df['Porcentaje_Acumulado'] = (
            pareto_df['Porcentaje_Individual']
            .cumsum()
        )

        # ---------------------------------
        # Etiquetas
        # ---------------------------------

        pareto_df['Etiqueta'] = (

            pareto_df['Frecuencia']
            .astype(int)
            .astype(str)

            + '<br>' +

            pareto_df['Porcentaje_Individual']
            .round(1)
            .astype(str)

            + '%'
        )

        # ---------------------------------
        # Figura
        # ---------------------------------

        fig_pareto = go.Figure()

        # Barras
        fig_pareto.add_trace(

            go.Bar(

                x=pareto_df['Tipo_Defecto'],
                y=pareto_df['Frecuencia'],

                name='Frecuencia',

                marker_color='#4682B4',

                text=pareto_df['Etiqueta'],

                textposition='outside'
            )
        )

        # Línea acumulada
        fig_pareto.add_trace(

            go.Scatter(

                x=pareto_df['Tipo_Defecto'],

                y=pareto_df['Porcentaje_Acumulado'],

                name='% Acumulado',

                yaxis='y2',

                mode='lines+markers',

                line=dict(
                    color='#FF4500',
                    width=3
                )
            )
        )

        # Línea 80%
        fig_pareto.add_hline(

            y=80,

            line_dash='dash',

            line_color='red'
        )

        # ---------------------------------
        # Layout
        # ---------------------------------

        fig_pareto.update_layout(

            paper_bgcolor='#FFFFFF',
            plot_bgcolor='#FFFFFF',
            font=dict(color='#1A1D23'),
            
            height=500,

            xaxis=dict(
                title='Tipo de Defecto'
            ),

            yaxis=dict(
                title='Frecuencia'
            ),

            yaxis2=dict(

                title='% Acumulado',

                overlaying='y',

                side='right',

                range=[0, 100]
            ),

            legend=dict(

                orientation='h',

                yanchor='bottom',

                y=1.02,

                xanchor='center',

                x=0.5
            )
        )

        st.plotly_chart(
            fig_pareto,
            use_container_width=True
        )

# =====================================
# RENDIMIENTO TALLER vs PROVEEDOR
# =====================================

with col_rendimiento:

    st.subheader("📈 Rendimiento por Tipo de Tela")

    # ---------------------------------
    # Agregación: media de ambos rendimientos
    # ---------------------------------

    rendimiento_tela = (
        df_filtrado
        .groupby('Tipo_de_tela')
        .agg(
            Rendimiento_Taller=('Rendimiento_Taller', 'mean'),
            Rendimiento_Proveedor=('Rendimiento_teorico_proveedor', 'mean')
        )
        .reset_index()
        .sort_values(by='Rendimiento_Taller', ascending=True)
    )

    # ---------------------------------
    # Gap: positivo = taller supera proveedor
    # ---------------------------------

    rendimiento_tela['Gap'] = (
        rendimiento_tela['Rendimiento_Taller'] -
        rendimiento_tela['Rendimiento_Proveedor']
    )

    # Color de la barra taller según gap
    rendimiento_tela['Color_barra'] = rendimiento_tela['Gap'].apply(
        lambda g: '#2ca02c' if g >= 0 else '#d62728'
    )

    # ---------------------------------
    # Figura
    # ---------------------------------

    fig_rend = go.Figure()

    # Barras horizontales - Rendimiento Taller
    fig_rend.add_trace(go.Bar(
        y=rendimiento_tela['Tipo_de_tela'],
        x=rendimiento_tela['Rendimiento_Taller'],
        name='Taller',
        orientation='h',
        marker_color=rendimiento_tela['Color_barra'].tolist(),
        text=rendimiento_tela['Rendimiento_Taller'].round(2).astype(str),
        textposition='outside',
    ))

    # Puntos - Rendimiento Proveedor
    fig_rend.add_trace(go.Scatter(
        y=rendimiento_tela['Tipo_de_tela'],
        x=rendimiento_tela['Rendimiento_Proveedor'],
        name='Proveedor',
        mode='markers',
        marker=dict(
            color='#FF7F0E',
            size=10,
            symbol='diamond',
            line=dict(color='white', width=1)
        ),
    ))

    # ---------------------------------
    # Layout
    # ---------------------------------

    x_min = rendimiento_tela[['Rendimiento_Taller', 'Rendimiento_Proveedor']].min().min()
    x_max = rendimiento_tela[['Rendimiento_Taller', 'Rendimiento_Proveedor']].max().max()

    fig_rend.update_layout(
        paper_bgcolor='#FFFFFF',
        plot_bgcolor='#FFFFFF',
        font=dict(color='#1A1D23'),
        
        height=500,
        xaxis=dict(
            title='Rendimiento (m/kg)',
            range=[max(0, x_min - 0.5), x_max + 0.8]
        ),
        yaxis=dict(title=''),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        ),
        bargap=0.25,
    )

    st.plotly_chart(fig_rend, use_container_width=True)

# =========================
# GRÁFICOS
# =========================

col_g1, col_g2 = st.columns(2)

# =========================================================
# SECCIÓN INFERIOR - ANALÍTICA AVANZADA
# =========================================================

st.divider()

# =========================
# 1. MAPA DE SEVERIDAD (ÚLTIMOS 10 ROLLOS)
# =========================

st.subheader("🧾 Mapa de Severidad - Últimos 10 Rollos")

df_ultimos = df_filtrado.sort_values(
    by='Fecha_ISO',
    ascending=False
).head(10)

# ---------------------------------
# Columnas a mostrar
# ---------------------------------

tabla_sev_df = df_ultimos[[
    'ID_Recepcion',
    'Tipo_de_tela',
    'Color',
    'Tipo_Defecto',
    'Severidad_label',
    'Estatus',
]].copy().reset_index(drop=True)

# ---------------------------------
# Mapa de colores por columna
# ---------------------------------

COLORES_ESTATUS = {
    'Aprobado':                 ('background-color:#C8E6C9', 'color:#1B5E20; font-weight:600'),
    'Aprobado con Desviación':  ('background-color:#FFF9C4', 'color:#F57F17; font-weight:600'),
    'Rechazado':                ('background-color:#FFCDD2', 'color:#B71C1C; font-weight:600'),
}

COLORES_SEV = {
    'Sin defecto':       ('background-color:#E8F5E9', 'color:#388E3C'),
    'Puntual simple':    ('background-color:#FFF8E1', 'color:#F9A825'),
    'Puntual combinado': ('background-color:#FFF3E0', 'color:#E65100'),
    'Frecuente':         ('background-color:#FCE4EC', 'color:#880E4F'),
    'Crítico':           ('background-color:#EDE7F6', 'color:#4527A0; font-weight:700'),
}

def estilo_fila(row):
    styles = [''] * len(row)
    idx = list(row.index)

    # Columna Estatus
    if 'Estatus' in idx:
        bg, fg = COLORES_ESTATUS.get(row['Estatus'], ('', ''))
        styles[idx.index('Estatus')] = f'{bg}; {fg}'

    # Columna Severidad_label
    if 'Severidad_label' in idx:
        bg, fg = COLORES_SEV.get(row['Severidad_label'], ('', ''))
        styles[idx.index('Severidad_label')] = f'{bg}; {fg}'

    return styles

tabla_styled = (
    tabla_sev_df
    .style
    .apply(estilo_fila, axis=1)
    .set_properties(**{
        'font-size': '13px',
        'border': '1px solid #e0e0e0',
        'padding': '6px 10px',
    })
    .set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#1e3a5f'),
            ('color', 'white'),
            ('font-weight', '700'),
            ('font-size', '13px'),
            ('padding', '8px 10px'),
            ('text-align', 'left'),
        ]},
        {'selector': 'tr:hover td', 'props': [
            ('background-color', '#f0f4ff'),
        ]},
    ])
    .hide(axis='index')
)

st.dataframe(tabla_styled, use_container_width=True, height=380)

# =========================
# RANKING DE CALIDAD
# =========================

st.subheader("🏆 Ranking de Calidad por Tipo de Tela")

# ---------------------------------
# Agregación base
# ---------------------------------

ranking = df_filtrado.groupby('Tipo_de_tela').agg(
    Con_Defectos=('Tiene_Defecto', 'sum'),
    Rendimiento_Taller=('Rendimiento_Taller', 'mean'),
    Total_Rollos=('ID_Rollo', 'count'),
).reset_index()

ranking['Sin_Defecto'] = ranking['Total_Rollos'] - ranking['Con_Defectos']

ranking['Tasa_Defectos_%'] = (
    ranking['Con_Defectos'] / ranking['Total_Rollos'] * 100
).round(1)

ranking['Tasa_Sin_Defecto_%'] = (
    ranking['Sin_Defecto'] / ranking['Total_Rollos'] * 100
).round(1)

ranking['Rendimiento_Taller'] = ranking['Rendimiento_Taller'].round(2)

if 'Rendimiento_teorico_proveedor' in df_filtrado.columns:
    prov = (
        df_filtrado
        .groupby('Tipo_de_tela')['Rendimiento_teorico_proveedor']
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={'Rendimiento_teorico_proveedor': 'Rend_Proveedor'})
    )
    ranking = ranking.merge(prov, on='Tipo_de_tela', how='left')
    ranking['Factor_%'] = (
        (ranking['Rendimiento_Taller'] - ranking['Rend_Proveedor'])
        / ranking['Rend_Proveedor'] * 100
    ).round(1)
else:
    ranking['Rend_Proveedor'] = None
    ranking['Factor_%'] = 0

# ---------------------------------
# Tasa de Rechazo real por tela
# Fuente: Estatus == 'Rechazado' (no confundir con tasa de defectos)
# ---------------------------------

df_filtrado['_Es_Rechazado'] = (
    df_filtrado['Estatus']
    .astype(str)
    .str.upper()
    .str.contains('RECHAZ')
)

rechazo_real = (
    df_filtrado
    .groupby('Tipo_de_tela')['_Es_Rechazado']
    .sum()
    .reset_index()
    .rename(columns={'_Es_Rechazado': 'Rollos_Rechazados'})
)

ranking = ranking.merge(rechazo_real, on='Tipo_de_tela', how='left')

ranking['Tasa_Rechazo_%'] = (
    ranking['Rollos_Rechazados'] / ranking['Total_Rollos'] * 100
).round(2)

# ---------------------------------
# CTA y Factor de Amortiguación
# CTA = DP / (1 - TR_decimal)   donde DP = 100 rollos base
# Factor_Amort_% = TR / (1 - TR) * 100
# Fuente correcta: Tasa_Rechazo_% (Estatus Rechazado), NO tasa de defectos
# ---------------------------------

DP = 100  # Pronóstico de demanda base para comparar todas las telas

ranking['TR_decimal'] = ranking['Tasa_Rechazo_%'] / 100

# Caso borde: TR = 100% → división por cero
ranking['CTA'] = ranking['TR_decimal'].apply(
    lambda tr: round(DP / (1 - tr), 1) if tr < 1 else float('inf')
)

ranking['Factor_Amort_%'] = ranking['TR_decimal'].apply(
    lambda tr: round((tr / (1 - tr)) * 100, 1) if tr < 1 else float('inf')
)

ranking = ranking.drop(columns=['TR_decimal', 'Rollos_Rechazados'])
ranking = ranking.sort_values(by='Tasa_Defectos_%', ascending=False).reset_index(drop=True)

# Medalla para top 3 con menor tasa de defectos
ranking_sorted_asc = ranking.sort_values('Tasa_Defectos_%', ascending=True)
medallas = {
    ranking_sorted_asc.iloc[0]['Tipo_de_tela']: '🥇',
    ranking_sorted_asc.iloc[1]['Tipo_de_tela']: '🥈',
    ranking_sorted_asc.iloc[2]['Tipo_de_tela']: '🥉',
} if len(ranking) >= 3 else {}

ranking.insert(0, '🏅', ranking['Tipo_de_tela'].map(medallas).fillna(''))

# Columnas finales a mostrar
cols_ranking = [
    '🏅', 'Tipo_de_tela', 'Total_Rollos', 'Con_Defectos', 'Sin_Defecto',
    'Tasa_Defectos_%', 'Tasa_Aprobación_%',
    'Rendimiento_Taller', 'Rend_Proveedor', 'Factor_%',
    'Tasa_Rechazo_%', 'CTA', 'Factor_Amort_%'
]
cols_ranking = [c for c in cols_ranking if c in ranking.columns]

# ---------------------------------
# Estilos por columna
# ---------------------------------

def color_tasa_defecto(val):
    if isinstance(val, (int, float)):
        if val >= 40:
            return 'background-color:#FFCDD2; color:#B71C1C; font-weight:700'
        elif val >= 20:
            return 'background-color:#FFF9C4; color:#F57F17; font-weight:600'
        else:
            return 'background-color:#C8E6C9; color:#1B5E20'
    return ''

def color_factor(val):
    if isinstance(val, (int, float)):
        if val > 0:
            return 'color:#1B5E20; font-weight:600'
        elif val < 0:
            return 'color:#B71C1C; font-weight:600'
    return ''

def color_amort(val):
    """Gradiente de riesgo según cuánto hay que sobredimensionar el pedido."""
    if isinstance(val, (int, float)) and val != float('inf'):
        if val >= 60:
            return 'background-color:#FFCDD2; color:#B71C1C; font-weight:700'
        elif val >= 25:
            return 'background-color:#FFF9C4; color:#F57F17; font-weight:600'
        else:
            return 'background-color:#C8E6C9; color:#1B5E20'
    return ''

ranking_styled = (
    ranking[cols_ranking]
    .style
    .map(color_tasa_defecto, subset=['Tasa_Defectos_%'])
    .map(color_factor, subset=['Factor_%'])
    .map(color_amort, subset=['Factor_Amort_%'])
    .format({
        'Tasa_Defectos_%':   '{:.1f}%',
        'Tasa_Aprobación_%': '{:.1f}%',
        'Rendimiento_Taller': '{:.2f}',
        'Rend_Proveedor':    '{:.2f}',
        'Factor_%':          '{:+.1f}%',
        'Tasa_Rechazo_%':    '{:.2f}%',
        'CTA':               '{:.1f} rollos',
        'Factor_Amort_%':    '{:.1f}%',
    }, na_rep='-')
    .set_properties(**{
        'font-size': '13px',
        'border': '1px solid #e0e0e0',
        'padding': '6px 10px',
    })
    .set_table_styles([
        {'selector': 'th', 'props': [
            ('background-color', '#1e3a5f'),
            ('color', 'white'),
            ('font-weight', '700'),
            ('font-size', '13px'),
            ('padding', '8px 10px'),
            ('text-align', 'center'),
        ]},
        {'selector': 'tr:hover td', 'props': [
            ('background-color', '#f0f4ff'),
        ]},
    ])
    .hide(axis='index')
)

st.dataframe(ranking_styled, use_container_width=True, height=480)

# =========================
# INSIGHTS AUTOMÁTICOS
# =========================

st.subheader("📌 Insights Automáticos")

top_riesgo = ranking.iloc[0]

# Mejor tela (última fila del ranking ya está ordenado desc por tasa defecto)
mejor_tela = ranking.iloc[-1]

col_ins1, col_ins2 = st.columns(2)

with col_ins1:
    st.error(
        f"🔴 **Tela con mayor riesgo:** {top_riesgo['Tipo_de_tela']}  \n"
        f"Tasa de defectos: **{top_riesgo['Tasa_Defectos_%']:.1f}%** · "
        f"Rendimiento taller: **{top_riesgo['Rendimiento_Taller']:.2f} m/kg** · "
        f"Factor amortiguación: **{top_riesgo['Factor_Amort_%']:.1f}%** (pedir **{top_riesgo['CTA']:.0f}** rollos por cada 100 necesarios)"
    )

with col_ins2:
    st.success(
        f"🟢 **Tela con mejor calidad:** {mejor_tela['Tipo_de_tela']}  \n"
        f"Tasa de defectos: **{mejor_tela['Tasa_Defectos_%']:.1f}%** · "
        f"Rendimiento taller: **{mejor_tela['Rendimiento_Taller']:.2f} m/kg** · "
        f"Factor amortiguación: **{mejor_tela['Factor_Amort_%']:.1f}%** (pedir **{mejor_tela['CTA']:.0f}** rollos por cada 100 necesarios)"
    )

# =========================
# FOOTER
# =========================

st.markdown("---")
st.caption("Dashboard desarrollado en Streamlit + Plotly")