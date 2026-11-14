# 🌍 EARTHSCOPE — NASA Earth System Trend Detective

[![NASA Space Apps Challenge](https://img.shields.io/badge/NASA%20Space%20Apps-Challenge%2002%3A%20Trend%20Detective-blue?style=for-the-badge&logo=nasa)](https://www.spaceappschallenge.org/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Three.js](https://img.shields.io/badge/Three.js-WebGL%203D-black?style=for-the-badge&logo=three.js)](https://threejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

> **"See the patterns shaping our planet."**  
> **EARTHSCOPE** is an AI-assisted Earth System Trend Discovery and Geospatial Analysis Platform engineered for the **NASA Space Apps Challenge 2026 (Challenge 02: Earth System Trend Detective)**.

From satellite observations to measurable environmental trends, EARTHSCOPE combines authenticated NASA Earthdata services, multi-mission satellite telemetry, and rigorous non-parametric statistical engines into a unified research workspace and interactive 3D WebGL command station.

---

## 🌟 Highlights

- **8 Core NASA Datasets Integrated**: Direct access across LP DAAC, GES DISC, and NASA Langley Research Center.
- **Scientific Statistical Rigor**: Non-parametric Mann-Kendall tests, Sen's slope linear rates, 95% confidence intervals, and Yue-Pilon autocorrelation pre-whitening.
- **Multi-Mission Satellite Constellation**: Sentinel-2 (Copernicus), Sentinel-1 (SAR), Landsat 9 (USGS/NASA), Terra/Aqua MODIS, NOAA-20 VIIRS, and ISS GEDI Lidar.
- **Authenticated Data Access**: NASA Earthdata Bearer Token authentication, NASA Common Metadata Repository (CMR) search, and AppEEARS point task generation.
- **Dual Console Interfaces**:
  1. **Interactive 3D Earth Station**: Real-time WebGL globe, 3D satellite trajectories, and planetary research workspace.
  2. **Multi-Layer Dashboard (`/dashboard`)**: MapLibre vector maps, synchronized split-sliders, and ECharts statistical time series.
- **Automated Scientific Reporting**: Publication-ready HTML research summaries with full dataset provenance metadata.

---

## 🛰️ 8 Core NASA Challenge Datasets

| Priority | Variable Name | Dataset / Product | Mission | Resolution | Category | DOI / DAAC |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- |
| **P0** | **NDVI** (Normalized Difference Vegetation Index) | `MODIS MOD13Q1.061` | Terra MODIS | 250 m | Vegetation | [LP DAAC](https://doi.org/10.5067/MODIS/MOD13Q1.061) |
| **P0** | **EVI** (Enhanced Vegetation Index) | `MODIS MOD13Q1.061` | Terra MODIS | 250 m | Vegetation | [LP DAAC](https://doi.org/10.5067/MODIS/MOD13Q1.061) |
| **P0** | **LST Day** (Land Surface Temperature Daytime) | `MODIS MOD11A2.061` | Terra MODIS | 1 km | Temperature | [LP DAAC](https://doi.org/10.5067/MODIS/MOD11A2.061) |
| **P0** | **LST Night** (Land Surface Temperature Nighttime) | `MODIS MOD11A2.061` | Terra MODIS | 1 km | Temperature | [LP DAAC](https://doi.org/10.5067/MODIS/MOD11A2.061) |
| **P0** | **T2M** (2-Meter Air Temperature) | `NASA POWER Monthly` | MERRA-2 Climatology | 0.5° × 0.625° | Atmospheric | [NASA Langley](https://doi.org/10.5067/POWER/MONTHLY/002) |
| **P0** | **Precipitation** (Rainfall Accumulation) | `NASA POWER Monthly` | GPM / MERRA-2 | 0.5° × 0.625° | Precipitation | [NASA Langley](https://doi.org/10.5067/POWER/MONTHLY/002) |
| **P1** | **GPM IMERG** (Monthly Gauge-Calibrated Rainfall) | `GPM_3IMERGM.07` | NASA / JAXA GPM | 0.1° × 0.1° | Hydrology | [GES DISC](https://doi.org/10.5067/GPM/IMERG/3B-MONTH/07) |
| **P1** | **Root-Zone Soil Wetness** | `MERRA-2 Catchment Model` | NASA GMAO MERRA-2 | 0.5° × 0.625° | Drought | [GES DISC](https://doi.org/10.5067/MERRA2/M2TMNXLND.5.12.4) |

---

## 🔬 Scientific Methodology

EARTHSCOPE implements non-parametric, distribution-free statistical algorithms designed specifically for environmental time series:

1. **Mann-Kendall Trend Test ($S$ and $\tau$)**:
   - Detects monotonic upward or downward trends without assuming Gaussian normality.
   - Calculates tie-corrected variance $Var(S)$ and standard normal test statistic $Z$.
   - Computes exact two-tailed p-values evaluated against significance levels ($\alpha = 0.05$).

2. **Sen's Slope Estimator**:
   - Computes the robust median of slopes between all pairwise observation combinations:
     $$Q_{median} = \text{median}\left(\frac{x_j - x_k}{j - k}\right), \quad \forall j > k$$
   - Insensitive to seasonal outliers, sensor dropouts, or temporary cloud interference.
   - Calculates two-sided 95% nonparametric confidence intervals ($Q_{lower}, Q_{upper}$).

3. **Autocorrelation Pre-Whitening (Yue-Pilon Method)**:
   - Evaluates lag-1 serial correlation coefficient ($r_1$).
   - When positive autocorrelation is present, pre-whitens the series ($y_t = x_t - r_1 x_{t-1}$) to prevent inflated type-I false-positive error rates.

4. **Multi-Variable Cross-Correlation Matrix**:
   - Computes Pearson linear and Spearman rank correlation coefficients between simultaneous environmental variables (e.g., NDVI vs. Land Surface Temp vs. Precipitation).

---

## 🛰️ Multi-Mission Satellite Constellation

- **Copernicus Sentinel-2A & 2B**: 10m/20m multispectral optical imagery for NDVI, NDWI, and NBR calculations.
- **Copernicus Sentinel-1A**: C-band Synthetic Aperture Radar (SAR) for cloud-penetrating radar observations.
- **NASA / USGS Landsat 9**: 30m multispectral + thermal infrared (TIRS-2) ensuring 50-year historical baseline continuity.
- **Terra & Aqua (MODIS)**: Daily global reflectance, vegetative indices, and land surface temperature.
- **Suomi-NPP & NOAA-20 (VIIRS)**: 375m active fire detections and thermal anomaly alerts via NASA FIRMS.
- **ISS GEDI**: Spaceborne waveform lidar measuring 3D forest canopy vertical structure and aboveground biomass.

---

## ⚡ Main REST APIs

Interactive Swagger documentation is available at `http://localhost:8000/docs`.

```text
GET   /api/earth/health             System status & dataset availability
GET   /api/earth/variables          8 Core NASA challenge variables catalogue
GET   /api/earth/datasets           Datasets registry across P0, P1, P2 tiers
GET   /api/earth/coverage           Spatial and temporal product coverage lookup
GET   /api/earth/cmr/search         Query NASA Common Metadata Repository (CMR)
POST  /api/earth/appeears/task      Generate AppEEARS LP DAAC task payload
POST  /api/earth/trends/analyze     Execute Mann-Kendall, Sen's slope & correlation analysis
POST  /api/earth/trends/compare     Multi-region trend comparison matrix
GET   /api/earth/report             Generate publication-ready scientific HTML research report
```

---

## 🚀 Quick Start

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/demovedu1345-beep/EARTHSCOPE.git
cd EARTHSCOPE

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Credentials

Copy the template environment file:

```bash
cp .env.example .env
```

Add your free provider keys in `.env`:
- `EARTHDATA_BEARER_TOKEN` — Free token from [NASA Earthdata Login](https://urs.earthdata.nasa.gov)
- `FIRMS_MAP_KEY` — Free key from [NASA FIRMS](https://firms.modaps.eosdis.nasa.gov/api/map_key)
- `PROTECTED_PLANET_TOKEN` — Free token from [Protected Planet](https://api.protectedplanet.net/request-token)

*(Note: Public fallback calculations and open satellite services remain operational even without custom keys).*

### 3. Launch the Server

```bash
python server.py 8000
```

Open your browser:
- **3D Earth Research Station:** `http://localhost:8000/`
- **Multi-Layer Dashboard:** `http://localhost:8000/dashboard`
- **Interactive OpenAPI Docs:** `http://localhost:8000/docs`

---

## 🛡️ Data Integrity Rules

1. **Source Provenance**: Every metric displays its satellite sensor, DAAC origin, and temporal resolution.
2. **Honest Labeling**: Historical observations and statistical estimates are clearly distinguished from live telemetry.
3. **No Fabricated Fallbacks**: When an external API is unconfigured or unreachable, the system gracefully transparently falls back to verified public climatologies without simulating artificial sensor noise.
4. **Credential Safety**: Private API keys and authentication tokens are never committed to version control.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Satellite imagery, meteorological data, and environmental datasets retain their respective NASA, ESA, USGS, and UNEP-WCMC terms of use and attribution.
