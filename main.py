from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import (
    rutas_roles, 
    rutas_usuarios, 
    rutas_espacios,
    rutas_mediciones, 
    rutas_tipos_dispositivos, 
    rutas_dispositivos,
    rutas_bocina,
    ruta_vvf  # 👈 NUEVO IMPORT
)

app = FastAPI(
    title="Aura API - Control Ambiental", 
    version="2.0",
    description="API para control de sensores y dispositivos ambientales"
)

# ========================================
# CORS
# ========================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================================
# INCLUIR TODAS LAS RUTAS
# ========================================
app.include_router(rutas_roles.router)
app.include_router(rutas_usuarios.router)
app.include_router(rutas_espacios.router)
app.include_router(rutas_mediciones.router)
app.include_router(rutas_tipos_dispositivos.router)
app.include_router(rutas_dispositivos.router)
app.include_router(rutas_bocina.router)  # 👈 NUEVO ROUTER
app.include_router(ruta_vvf.router)
# ========================================
# RUTA PRINCIPAL
# ========================================
@app.get("/")
def home():
    return {
        "message": "API Aura funcionando correctamente!",
        "version": "2.0",
        "endpoints": {
            "bocina": "/api/bocina",
            "mediciones": "/getmediciones",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "aura-api"}