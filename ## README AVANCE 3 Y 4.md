## README AVANCE 3 Y 4

📌 ¿Qué armamos en el Avance 3 y 4?
Básicamente dejamos el modelo de Machine Learning listo para funcionar en el mundo real: monitoreado para que no pierda precisión y empaquetado en una API para que cualquiera lo pueda usar.

📊 Avance 3: Monitoreo de Data Drift (Salud del Modelo)
Para que el modelo no quede desactualizado si la economía o los clientes cambian, armamos un sistema que detecta desvíos en los datos:

Script de Monitoreo (model_monitoring.py):

Armamos un script que compara los datos históricos contra los datos nuevos que van entrando.

Le metimos pruebas estadísticas: usamos Kolmogorov-Smirnov para los números (como el capital_prestado o la edad) y Chi-cuadrado para las variables categóricas (como el tipo_laboral).

Guarda todo en un archivo drift_report.json.

Tablero en Streamlit (app.py):

Hicimos un panel visual re simple en Streamlit que lee ese JSON y te tira alertas visuales en rojo si alguna variable cambia bruscamente (por ejemplo, si de golpe la gente empieza a pedir préstamos mucho más altos).

🚀 Avance 4: Despliegue con FastAPI y Docker
Acá el objetivo era sacar el modelo del Jupyter Notebook y ponerlo a correr como un servicio real:

API REST (model_monitoring.py / model_deploy.py):

Creamos una API con FastAPI para que cualquier sistema le pueda mandar datos de un cliente (o una lista entera de clientes en batch) y devuelva las predicciones al toque en /predict.

Usamos Pydantic para validar que los datos entren con el formato correcto sin romper nada.

Docker (Dockerfile y requirements.txt):

Dejamos listo el Dockerfile con una imagen liviana de Python (python:3.10-slim) y el servidor uvicorn. Con esto el proyecto se puede levantar en cualquier computadora o servidor en la nube sin andar renegando con dependencias.

🐙 Git & GitHub
Subimos todo ordenado trabajando sobre la rama developer.

Hicimos los Pull Requests (PR) hacia la rama main para que quede todo el historial prolijo y fusionado como se hace en un equipo de trabajo real.