import os
import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Dict, List
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from models import HouseholdProfile, RecommendationResponse, HouseholdMission
from engine import HouseholdRecommendationEngine
from catalog_data import PRODUCTS_CATALOG, MISSIONS_TEMPLATE

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("heyblinkit.main")

# Background keep-alive task for Render free tier
async def keep_alive_ping_loop():
    """
    Prevents Render free tier from sleeping by self-pinging every 10 minutes.
    Uses RENDER_EXTERNAL_URL (set automatically by Render) or SELF_PING_URL environment variable.
    """
    self_url = os.getenv("RENDER_EXTERNAL_URL") or os.getenv("SELF_PING_URL")
    if not self_url:
        logger.info("No RENDER_EXTERNAL_URL or SELF_PING_URL set. Self-ping loop disabled.")
        return

    health_url = f"{self_url.rstrip('/')}/api/health"
    logger.info(f"Starting Render keep-alive ping loop targeting {health_url}")

    async with httpx.AsyncClient(timeout=10.0) as client:
        while True:
            await asyncio.sleep(600)  # Ping every 10 minutes (600s)
            try:
                resp = await client.get(health_url)
                logger.info(f"Keep-alive self-ping status: {resp.status_code}")
            except Exception as e:
                logger.warning(f"Keep-alive ping failed: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: trigger keep-alive loop task
    task = asyncio.create_task(keep_alive_ping_loop())
    yield
    # Shutdown: cancel task
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="HeyBlinkit Household Recommendation Engine",
    description="Stanford AI PM Household Mental Model Recommendation Backend for Blinkit 8-Min Hyperlocal Delivery",
    version="1.0.0",
    lifespan=lifespan
)

# Universal CORS setup supporting all origins (Vercel, local, custom domains) & credentials
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = HouseholdRecommendationEngine()
user_profiles_db: Dict[str, HouseholdProfile] = {}

@app.get("/")
def read_root():
    return {
        "service": "HeyBlinkit Household AI Engine",
        "status": "online",
        "mental_model": "Household Missions -> Tasks -> Buy Products",
        "architecture": "FastAPI + Pydantic + Mission Alignment Scoring Engine",
        "groq_ai_enabled": bool(os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY"))
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "ok",
        "products_loaded": len(PRODUCTS_CATALOG),
        "missions_available": len(MISSIONS_TEMPLATE),
        "groq_ai_enabled": bool(os.getenv("GROQ_API_KEY") or os.getenv("GROK_API_KEY") or os.getenv("XAI_API_KEY")),
        "render_url": os.getenv("RENDER_EXTERNAL_URL")
    }

@app.post("/api/onboarding/profile", response_model=Dict)
def save_household_profile(profile: HouseholdProfile):
    user_id = profile.user_id or "user_default"
    user_profiles_db[user_id] = profile
    return {
        "message": "Household profile saved successfully",
        "user_id": user_id,
        "rooms_registered": len(profile.rooms),
        "goals_registered": len(profile.monthly_goals)
    }

@app.post("/api/recommendations", response_model=RecommendationResponse)
def get_recommendations(profile: HouseholdProfile):
    """
    Computes score-ranked household missions, collection feed, and product priorities
    based on the Household Mental Model algorithm. Uses Grok AI if XAI_API_KEY is configured.
    """
    return engine.compute_recommendations(profile)

@app.get("/api/missions", response_model=List[HouseholdMission])
def get_all_missions():
    """
    Returns available pre-packaged household mission bundles.
    """
    default_profile = HouseholdProfile(rooms=["Kitchen", "Living Area", "Bedrooms", "Gym"])
    res = engine.compute_recommendations(default_profile)
    return res.missions

@app.options("/{full_path:path}")
def handle_options_preflight(full_path: str):
    """
    Catch-all OPTIONS handler to guarantee 200 OK preflight responses for all endpoints.
    """
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)

