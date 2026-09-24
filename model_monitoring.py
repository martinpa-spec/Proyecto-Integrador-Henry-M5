import json
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ks_2samp

# =========================================================
# PASO 1: Cargar tu dataset real (Baseline / Entrenamiento)
# =========================================================
# Leemos el archivo de Excel
df_real = pd.read_excel(r"C:\Users\pjpav\Downloads\Base_de_datos (1).xlsx")

# Eliminamos columnas que no entran al modelo
df_limpio = df_real.drop(
    columns=["Pago_atiempo", "fecha_prestamo", "puntaje"], errors="ignore"
)

# Nuestro baseline es una muestra del dataset limpio
baseline = df_limpio.sample(n=3000, random_state=42).copy()

# =========================================================
# PASO 2: Simular datos de producción (Current)
# =========================================================
# Para probar que el script detecta Drift, tomamos otra muestra
# y le aumentamos artificialmente un 20% al 'capital_prestado'
current = df_limpio.sample(n=3000, random_state=99).copy()
current["capital_prestado"] = current["capital_prestado"] * 1.20

# =========================================================
# PASO 3: Evaluar las variables del modelo
# =========================================================
reporte = {}

# Variables numéricas clave de tu dataset
num_cols = ["capital_prestado", "salario_cliente", "cuota_pactada", "edad_cliente"]

for col in num_cols:
    # KS-Test: compara distribuciones continuas
    stat, p_val = ks_2samp(baseline[col].dropna(), current[col].dropna())
    reporte[col] = {
        "tipo": "numerica",
        "p_value": float(p_val),
        "drift": bool(p_val < 0.05),  # True si p-valor es menor a 5%
    }

# Variables categóricas clave de tu dataset
cat_cols = ["tipo_laboral", "tendencia_ingresos"]

# Variables categóricas clave de tu dataset
cat_cols = ["tipo_laboral", "tendencia_ingresos"]

for col in cat_cols:
    # 1. Aseguramos que ambas muestras tengan exactamente las mismas categorías asociadas
    categorias_unicas = list(
        set(baseline[col].dropna().unique()).union(
            set(current[col].dropna().unique())
        )
    )

    # 2. Contamos la frecuencia de cada categoría en Baseline y en Current
    freq_baseline = (
        baseline[col].value_counts().reindex(categorias_unicas, fill_value=0)
    )
    freq_current = (
        current[col].value_counts().reindex(categorias_unicas, fill_value=0)
    )

    # 3. Armamos la tabla de contingencia comparando frecuencias globales
    tabla = pd.DataFrame([freq_baseline, freq_current])

    # 4. Evaluamos Chi-cuadrado
    _, p_val, _, _ = chi2_contingency(tabla)

    reporte[col] = {
        "tipo": "categorica",
        "p_value": float(p_val),
        "drift": bool(p_val < 0.05),
    }
# =========================================================
# PASO 4: Guardar los resultados en JSON
# =========================================================
with open("drift_report.json", "w") as f:
    json.dump(reporte, f, indent=4)

print("✅ Monitoreo completado. Archivo 'drift_report.json' generado.")
