from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import obsbakat, obskarakter, charts

app = FastAPI(
    title="Observasi Karakter & Bakat API",
    description="Stateful API for LLM-driven character and talent exploration",
    version="1.0.0"
)

# Enable CORS for frontend clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(obsbakat.router)
app.include_router(obskarakter.router)
app.include_router(charts.router)

@app.get("/")
async def root():
    return {"message": "Welcome to Observasi Karakter & Bakat API"}
