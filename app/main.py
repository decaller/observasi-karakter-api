from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
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

templates = Jinja2Templates(directory="app/templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
