from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
import uvicorn

# Convierte el directorio de tu agente en una aplicación FastAPI
app: FastAPI = get_fast_api_app(
    agents_dir="./",  # Reemplaza con el nombre de la carpeta de tu agente
    web=False # False para modo "solo API" (sin la interfaz gráfica de desarrollo)
)

# Opcional: Puedes agregar rutas personalizadas de FastAPI aquí si tu backend lo requiere

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
