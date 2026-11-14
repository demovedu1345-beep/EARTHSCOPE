#!/usr/bin/env python3
"""
EARTHSCOPE — NASA Earth System Trend Detective Server
NASA Space Apps Challenge 2026 (Challenge 02: Trend Detective)

Provides:
- 8 Core NASA Challenge Dataset Integrations (MOD13Q1, MOD11A2, NASA POWER, GPM IMERG, MERRA-2)
- Scientific Trend Detection Engine (Mann-Kendall, Sen's Slope, Yue-Pilon, Benjamini-Hochberg FDR)
- Full REST API with OpenAPI interactive documentation at /docs and /redoc
- Interactive 3D WebGL Earth & Research Station at /
- High-Resolution Multi-Layer Dashboard at /dashboard
"""

import os
import sys
import mimetypes
from pathlib import Path
from fastapi import FastAPI, Query, Request
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Ensure local directory is on path
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "web"
sys.path.insert(0, str(BASE_DIR))

# Import EarthScope Scientific Backend Engine
from earthscope_backend import (
    NASA_VARIABLE_CATALOGUE,
    NASA_DATASETS_REGISTRY,
    APPEEARS_LPDAAC_PRODUCTS,
    build_appeears_task_payload,
    query_nasa_cmr,
    run_earthscope_investigation,
    generate_earthscope_report_html,
    USER_AGENT
)

# Custom MIME types for 3D WebGL assets
mimetypes.add_type('model/gltf-binary', '.glb')
mimetypes.add_type('model/gltf+json', '.gltf')
mimetypes.add_type('image/vnd.radiance', '.hdr')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('application/json', '.json')
mimetypes.add_type('application/wasm', '.wasm')
mimetypes.add_type('audio/mpeg', '.mp3')
mimetypes.add_type('video/mp4', '.mp4')
mimetypes.add_type('video/webm', '.webm')
mimetypes.add_type('font/woff2', '.woff2')
mimetypes.add_type('font/woff', '.woff')

app = FastAPI(
    title="EARTHSCOPE — NASA Earth System Trend Detective API",
    description="Scientific API engine for multi-decadal Earth observation trend analysis, autocorrelation diagnostics, and NASA Earthdata data services.",
    version="2026.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class TrendAnalysisRequest(BaseModel):
    lat: float = 12.3375
    lon: float = 75.8069
    region_name: str = "Kodagu Forest Region"
    variables: list[str] = ["ndvi", "t2m", "precipitation", "lst_day"]
    start_year: int = 2015
    end_year: int = 2024
    alpha: float = 0.05

class TrendCompareRequest(BaseModel):
    regions: list[dict]
    variables: list[str] = ["ndvi", "t2m", "precipitation"]
    start_year: int = 2015
    end_year: int = 2024

class AppEEARSTaskRequest(BaseModel):
    task_name: str = "earthscope_sample"
    lat: float = 12.3375
    lon: float = 75.8069
    product_id: str = "MOD13Q1.061"
    layer_name: str = "_250m_16_days_NDVI"
    start_date: str = "2020-01-01"
    end_date: str = "2024-12-31"

# --- API Endpoints ---

@app.get('/api/earth/health', tags=["System"])
async def health_check():
    return {
        "status": "OPERATIONAL",
        "service": "EARTHSCOPE Trend Detective Engine",
        "challenge": "NASA Space Apps Challenge 2026",
        "datasets_available": len(NASA_VARIABLE_CATALOGUE)
    }

@app.get('/api/earth/variables', tags=["Catalogue"])
async def get_earth_variables():
    """Returns the official catalogue of 8 core NASA challenge variables."""
    return {"ok": True, "count": len(NASA_VARIABLE_CATALOGUE), "variables": NASA_VARIABLE_CATALOGUE}

@app.get('/api/earth/datasets', tags=["Catalogue"])
async def get_earth_datasets():
    """Returns the official datasets registry across P0, P1, and P2 priority tiers."""
    return {"ok": True, "count": len(NASA_DATASETS_REGISTRY), "datasets": NASA_DATASETS_REGISTRY}

@app.get('/api/earth/appeears/products', tags=["AppEEARS"])
async def get_appeears_products():
    """Returns AppEEARS supported LP DAAC product definitions."""
    return {"ok": True, "count": len(APPEEARS_LPDAAC_PRODUCTS), "products": APPEEARS_LPDAAC_PRODUCTS}

@app.post('/api/earth/appeears/task', tags=["AppEEARS"])
async def create_appeears_task(req: AppEEARSTaskRequest):
    """Builds and validates an official AppEEARS point task request payload."""
    payload = build_appeears_task_payload(
        task_name=req.task_name,
        lat=req.lat,
        lon=req.lon,
        product_id=req.product_id,
        layer_name=req.layer_name,
        start_date=req.start_date,
        end_date=req.end_date
    )
    return {
        "ok": True,
        "task_payload": payload,
        "appeears_api_url": "https://appeears.earthdatacloud.nasa.gov/api/v1/task",
        "documentation": "https://appeears.earthdatacloud.nasa.gov/api/"
    }

@app.get('/api/earth/cmr/search', tags=["NASA CMR"])
async def search_nasa_cmr(keyword: str = Query("MODIS"), limit: int = Query(5)):
    """Queries NASA Common Metadata Repository (CMR) with Earthdata authentication."""
    return query_nasa_cmr(keyword=keyword, limit=limit)

@app.get('/api/earth/coverage', tags=["Catalogue"])
async def get_earth_coverage(lat: float = Query(12.3375), lon: float = Query(75.8069)):
    """Returns spatial and temporal availability metrics for key NASA satellite products."""
    return {
        "ok": True,
        "location": {"lat": lat, "lon": lon},
        "coverage": {
            "MOD13Q1": {"status": "AVAILABLE", "temporal_range": "2000-02-18 to Present", "resolution": "250m"},
            "MOD11A2": {"status": "AVAILABLE", "temporal_range": "2000-03-05 to Present", "resolution": "1km"},
            "NASA_POWER": {"status": "AVAILABLE", "temporal_range": "1981-01-01 to Present", "resolution": "0.5°"},
            "GPM_IMERG": {"status": "AVAILABLE", "temporal_range": "2000-06-01 to Present", "resolution": "0.1°"},
            "MERRA2": {"status": "AVAILABLE", "temporal_range": "1980-01-01 to Present", "resolution": "0.5°x0.625°"},
            "GLDAS": {"status": "AVAILABLE", "temporal_range": "2000-01-01 to Present", "resolution": "0.25°"}
        }
    }

@app.post('/api/earth/trends/analyze', tags=["Scientific Trend Engine"])
async def analyze_earth_trends(req: TrendAnalysisRequest):
    """
    Executes full scientific trend detection:
    - Non-parametric Mann-Kendall Test
    - Sen's Slope Estimator with 95% Confidence Intervals
    - Seasonal Mann-Kendall & Yue-Pilon Autocorrelation Diagnostics
    - Climatological Deseasonalization & Monthly Anomalies
    - Multi-variable Pearson/Spearman Cross-Correlation Matrix
    """
    return await run_earthscope_investigation(
        lat=req.lat,
        lon=req.lon,
        region_name=req.region_name,
        variables=req.variables,
        start_year=req.start_year,
        end_year=req.end_year,
        alpha=req.alpha
    )

@app.post('/api/earth/trends/compare', tags=["Scientific Trend Engine"])
async def compare_earth_trends(req: TrendCompareRequest):
    """Compares Earth System trends across multiple geographic regions."""
    results = []
    for r in req.regions:
        r_name = r.get("name", "Unknown Region")
        r_lat = float(r.get("lat", 12.3375))
        r_lon = float(r.get("lon", 75.8069))
        inv = await run_earthscope_investigation(
            lat=r_lat, lon=r_lon, region_name=r_name,
            variables=req.variables, start_year=req.start_year, end_year=req.end_year
        )
        results.append(inv)
    return {"ok": True, "count": len(results), "comparisons": results}

@app.get('/api/earth/report', tags=["Scientific Trend Engine"])
async def get_earthscope_report(
    lat: float = Query(12.3375),
    lon: float = Query(75.8069),
    region_name: str = Query("Kodagu Forest Region"),
    start_year: int = Query(2015),
    end_year: int = Query(2024),
    format: str = Query("html")
):
    """Generates a reproducible scientific research report with Mann-Kendall statistics and data provenance."""
    inv = await run_earthscope_investigation(
        lat=lat,
        lon=lon,
        region_name=region_name,
        variables=["ndvi", "t2m", "precipitation", "lst_day"],
        start_year=start_year,
        end_year=end_year
    )
    if format.lower() == "json":
        return inv
    html = generate_earthscope_report_html(inv)
    return HTMLResponse(content=html, media_type="text/html")

# --- Static Frontend Serving ---
@app.get('/', include_in_schema=False)
async def serve_index():
    index_file = STATIC_DIR / "index.html"
    return FileResponse(index_file)

@app.get('/dashboard', include_in_schema=False)
async def serve_dashboard():
    dash_file = STATIC_DIR / "dashboard.html"
    return FileResponse(dash_file)

if STATIC_DIR.exists():
    app.mount('/', StaticFiles(directory=str(STATIC_DIR), html=True), name='static_web')

PORT = int(os.getenv("PORT", "8000"))

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    print(f"🚀 EARTHSCOPE Server running at: http://127.0.0.1:{port}/")
    print(f"📡 API Documentation at: http://127.0.0.1:{port}/docs")
    print(f"🔬 Multi-Layer Dashboard at: http://127.0.0.1:{port}/dashboard")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
