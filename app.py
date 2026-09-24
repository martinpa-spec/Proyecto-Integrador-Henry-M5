import json
import pandas as pd
import streamlit as st

st.title("📊 CrediPulse - Monitoreo de Data Drift")

# Cargar el reporte generado por el script anterior
try:
    with open("drift_report.json") as f:
        datos = json.load(f)
except FileNotFoundError:
    st.error("No se encontró 'drift_report.json'. Corré 'py model_monitoring.py' primero.")
    st.stop()

# Mostrar la tabla con el estado de cada variable
st.write("### Estado de las variables de CrediPulse")
df_resumen = pd.DataFrame(datos).T
st.dataframe(df_resumen)

# Alerta automática
hay_drift = any(v["drift"] for v in datos.values())

if hay_drift:
    st.error("🚨 **ALERTA**: Se detectó Data Drift en una o más variables. Se recomienda revisar la ingesta o reentrenar el modelo.")
else:
    st.success("✅ **OK**: Todas las variables se mantienen estables.")
