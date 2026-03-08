import streamlit as st
import pandas as pd
import pydeck as pdk
import time
import re

st.set_page_config(page_title="Radar ATC", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0b0d11; } 
    [data-testid="stSidebar"] { background-color: #131720; border-right: 2px solid #00ffc8; }
    </style>
    """, unsafe_allow_html=True)#==========> Estilo estandar

@st.cache_data
def load_flight_data():#============recoleccion
    vuelos = {
        "AFR-861A (Direct)": "trayectoria_A320_AFR861A.csv",
        "AFR-58XP (Standard)": "trayectoria_A320_AFR58XP.csv"
    }
    dataframes = {}
    for nombre, archivo in vuelos.items():
        rows = []
        with open(archivo, 'r', encoding='utf-16') as f:
            content = f.readlines()
        for line in content:
            nums = re.findall(r"[-+]?\d*\.\d+|\d+", line)#===========corazon
            if len(nums) >= 6:
                rows.append({
                    "time": float(nums[0]), "lat": float(nums[1]), "lon": float(nums[2]),
                    "vel": float(nums[3]), "alt": float(nums[4]), "hdg": float(nums[5])
                })
        if rows:
            dataframes[nombre] = pd.DataFrame(rows)
    return dataframes

aeropuertos_datos = [
    {"name": "Toulouse-Blagnac (LFBO)", "lat": 43.6291, "lon": 1.3641},#origen
    {"name": "Limoges-Bellegarde (LFBL)", "lat": 45.8611, "lon": 1.1794},#alternativo
    {"name": "Châteauroux-Centre (LFLX)", "lat": 46.8608, "lon": 1.7303},#alternativo
    {"name": "Orléans-Bricy (LFOB)", "lat": 47.9878, "lon": 1.7602},#alternativo
    {"name": "Paris-Orly (LFPO)", "lat": 48.7262, "lon": 2.3652},#alternativo
    {"name": "Paris-Charles de Gaulle (LFPG)", "lat": 49.0097, "lon": 2.5479}#destino
]
df_airports = pd.DataFrame(aeropuertos_datos)#===============================> FILTRO aeropuertos

flota_data = load_flight_data()
if 'reloj_global' not in st.session_state:
    tiempos_inicio = [df['time'].min() for df in flota_data.values()]#===========Corazon logistico, tiempo
    st.session_state.reloj_global = min(tiempos_inicio)

st.sidebar.title("||AVIONS DISPONIBLES||")
flota = list(flota_data.keys())
seleccion = st.sidebar.radio("Sélectionner une unité:", flota)
st.sidebar.markdown("___")
st.sidebar.subheader("ETAT ACTUEL")
stats_container = st.sidebar.empty()
#=============> avion simbolo prfecto
ICON_URL = "https://img.icons8.com/ios-filled/100/FFFFFF/airplane-mode-on.png"
ICON_MAPPING = {"avion_pro": {"x": 0, "y": 0, "width": 100, "height": 100, "mask": False}}

map_placeholder = st.empty()
while True:
    layers = []
    info_focada = None#====================>icono aeropuerto (punto rojo)

    layers.append(pdk.Layer(
        "ScatterplotLayer", df_airports,
        get_position="[lon, lat]", get_color="[0, 255, 200, 40]", 
        get_radius=50000, stroked=True, filled=True
    ))
    layers.append(pdk.Layer(
        "ScatterplotLayer", df_airports,
        get_position="[lon, lat]", get_color="[255, 0, 0, 200]", get_radius=3000 #==============MARGEN DE ERROR 50KM
    ))

    for nombre_avion, df_vuelo in flota_data.items():
        trayecto = df_vuelo[df_vuelo['time'] <= st.session_state.reloj_global] #corazon
        if not trayecto.empty:
            actual = trayecto.tail(1).copy()
            actual["icon"] = "avion_pro" #==========icono avion
            es_sel = (nombre_avion == seleccion)
            if es_sel:
                info_focada = actual.iloc[0]
                color_tray = "[0, 255, 200, 200]"
            else:
                color_tray = "[0, 100, 100, 80]"

            layers.append(pdk.Layer(
                "PathLayer", [{"path": trayecto[['lon', 'lat']].values.tolist()}],
                get_path="path", get_width=400, get_color=color_tray
            ))
            layers.append(pdk.Layer(
                "IconLayer", actual, get_icon='icon',
                icon_atlas=ICON_URL, icon_mapping=ICON_MAPPING,
                get_position="[lon, lat]", size_units="pixels",
                get_size=8000, get_angle="-hdg + 90",
                get_color="[255, 255, 255]" if es_sel else "[150, 150, 150]"
            ))

    with stats_container.container(): #====================>Lectura de datos pertinentes 1altitud 2velocidd 3direccion
        if info_focada is not None:
            st.metric("ALTITUDE", f"{int(info_focada['alt'])} m")
            st.metric("VITESSE", f"{int(info_focada['vel'] * 3.6)} km/h")
            st.write(f"Cap: {int(info_focada['hdg'])}°")
        else:
            st.write("En attente...")

    with map_placeholder.container():#======>corazon estetico, mapa inciado
        st.pydeck_chart(pdk.Deck(
            map_style="https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json",
            initial_view_state=pdk.ViewState(latitude=46.5, longitude=2.5, zoom=6, pitch=30),
            layers=layers
        ))
    
    st.session_state.reloj_global += 5 #==============> Velocidad de vuelo :)
    time.sleep(0.1)
