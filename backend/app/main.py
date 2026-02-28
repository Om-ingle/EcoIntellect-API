from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import random

from app.models import (
    OrderAnalysisRequest,
    OrderAnalysisResponse,
    Alternative,
    YearlyProjection,
    UserImpactRequest,
    UserImpactResponse,
)
from app.services.emissions_calculator import EmissionsCalculator
from app.services.greenpt_integration import GreenPTClient
from app.services.wolfram_integration import WolframClient
from app.database import get_db, OrderRecord

# Load environment variables from .env
load_dotenv()

# ── Sponsor clients ──────────────────────────────────────────────────
greenpt = GreenPTClient()    # Uses GREENPT_API_KEY from .env
wolfram = WolframClient()    # Uses WOLFRAM_APP_ID from .env

app = FastAPI(
    title="EcoIntellect API",
    description=(
        "**Sustainability Decision Intelligence Layer for Digital Platforms.**\n\n"
        "Powered by [GreenPT](https://greenpt.io) for emission factors "
        "and [Wolfram|One](https://www.wolframalpha.com) for impact projections."
    ),
    version="1.0.0",
    contact={"name": "EcoIntellect Team"},
    tags_metadata=[
        {"name": "analysis", "description": "Order-level carbon analysis endpoints"},
        {"name": "impact",   "description": "User and platform-level impact projection"},
    ],
)

# ── CORS ─────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Root ─────────────────────────────────────────────────────────────
@app.get("/", tags=["analysis"])
def root():
    return {
        "message": "Welcome to EcoIntellect API",
        "tagline": "Sustainability Intelligence Layer for Digital Platforms",
        "version": "1.0.0",
        "sponsor_integrations": {
            "greenpt":  bool(greenpt.api_key),
            "wolfram":  bool(wolfram.app_id),
        },
        "docs": "/docs",
        "endpoints": {
            "analyze_order":       "POST /api/v1/analyze-order",
            "compare_alternatives":"GET  /api/v1/compare-alternatives",
            "user_impact":         "GET  /api/v1/user-impact/{user_id}",
        },
    }


@app.get("/health", tags=["analysis"])
def health_check():
    return {"status": "healthy", "service": "EcoIntellect API"}


# ── POST /api/v1/analyze-order ────────────────────────────────────────
@app.post(
    "/api/v1/analyze-order",
    response_model=OrderAnalysisResponse,
    tags=["analysis"],
    summary="Analyse the environmental impact of a food delivery order",
)
async def analyze_order(request: OrderAnalysisRequest, db: Session = Depends(get_db)):
    """
    Returns carbon emissions, eco score, better alternatives,
    and a Wolfram|One-powered yearly projection.

    **Emission factors** are sourced via the GreenPT integration layer.  
    **Yearly projections** are computed by Wolfram|One.
    """
    try:
        transport_mode  = request.transport_mode.value
        packaging_type  = request.packaging_type.value

        # ── Emissions (GreenPT-backed factors) ──────────────────────
        transport_factor  = greenpt.get_emission_factor("transport", transport_mode)
        packaging_factor  = greenpt.get_emission_factor("packaging", packaging_type)
        total_emissions   = round(request.distance_km * transport_factor + packaging_factor, 2)

        # ── Eco score & rating ───────────────────────────────────────
        eco_score = EmissionsCalculator.calculate_eco_score(total_emissions, request.distance_km)
        rating    = EmissionsCalculator.get_rating(eco_score)

        # ── Alternatives ─────────────────────────────────────────────
        alternatives = EmissionsCalculator.find_alternatives(
            request.distance_km, transport_mode, packaging_type
        )

        # ── Yearly projection (Wolfram|One) ───────────────────────────
        yearly_proj = wolfram.calculate_yearly_projection(
            total_emissions,
            request.frequency_per_week,
            request.order_value,
        )

        # ── Environmental context ────────────────────────────────────
        env_context = EmissionsCalculator.get_environmental_context(
            yearly_proj["total_carbon_kg"]
        )

        # ── Database Ledger Save ─────────────────────────────────────
        db_order = OrderRecord(
            user_id="user_demo", # In production, this comes from JWT
            distance_km=request.distance_km,
            transport_mode=transport_mode,
            packaging_type=packaging_type,
            carbon_emission_grams=total_emissions,
            eco_score=eco_score
        )
        db.add(db_order)
        db.commit()

        return OrderAnalysisResponse(
            carbon_emission_grams=total_emissions,
            eco_score=eco_score,
            rating=rating,
            better_alternatives=alternatives,
            yearly_projection=YearlyProjection(**yearly_proj),
            environmental_context=env_context,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /api/v1/compare-alternatives ─────────────────────────────────
@app.get(
    "/api/v1/compare-alternatives",
    tags=["analysis"],
    summary="Compare every transport × packaging combination for a given distance",
)
async def compare_alternatives(
    distance_km: float,
    transport_mode: str = "car",
    packaging_type: str = "plastic",
):
    """
    Returns a sorted matrix of all 16 transport × packaging combinations,
    ranked by eco score (best first).
    """
    try:
        results = []
        for transport in ["car", "motorcycle", "electric_vehicle", "bike"]:
            for packaging in ["plastic", "paper", "biodegradable", "reusable"]:
                t_factor = greenpt.get_emission_factor("transport", transport)
                p_factor = greenpt.get_emission_factor("packaging", packaging)
                emissions = round(distance_km * t_factor + p_factor, 2)
                time_min  = EmissionsCalculator.estimate_time(distance_km, transport)
                score     = EmissionsCalculator.calculate_eco_score(emissions, distance_km)

                results.append({
                    "transport_mode":          transport,
                    "packaging_type":          packaging,
                    "carbon_emission_grams":   emissions,
                    "estimated_time_minutes":  time_min,
                    "eco_score":               score,
                    "rating":                  EmissionsCalculator.get_rating(score),
                })

        results.sort(key=lambda x: x["eco_score"], reverse=True)

        return {
            "distance_km":   distance_km,
            "total_options": len(results),
            "options":       results,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── GET /api/v1/user-impact/{user_id} ────────────────────────────────
@app.get(
    "/api/v1/user-impact/{user_id}",
    response_model=UserImpactResponse,
    tags=["impact"],
    summary="Get a user's cumulative environmental impact and Eco Score",
)
async def get_user_impact(user_id: str, days: int = 365, db: Session = Depends(get_db)):
    """
    Returns gamified sustainability metrics for a given user.

    Fetches actual order history from SQLite database and aggregates the 
    carbon ledger dynamically.
    """
    try:
        orders = db.query(OrderRecord).filter(OrderRecord.user_id == user_id).all()
        total_orders = len(orders)
        
        if total_orders == 0:
            avg_carbon_per_order = 0
            eco_score = 0
            total_carbon_kg = 0.0
            carbon_saved_kg = 0.0
        else:
            total_emissions_g = sum(o.carbon_emission_grams for o in orders)
            avg_carbon_per_order = total_emissions_g / total_orders
            total_carbon_kg = round(total_emissions_g / 1000, 2)
            
            # Baseline benchmark: assume 500g is a "standard" unchecked order
            potential_carbon = total_orders * 500   
            carbon_saved_kg  = round((potential_carbon - total_emissions_g) / 1000, 2)
            eco_score        = int(sum(o.eco_score for o in orders) / total_orders)

        # Wolfram-powered projection
        proj = wolfram.calculate_yearly_projection(
            avg_carbon_per_order, 3, 350
        )
        ratio = 365 / max(days, 1)
        yearly = YearlyProjection(
            total_orders_per_year  = int(proj["total_orders_per_year"] * ratio),
            total_carbon_kg        = round(proj["total_carbon_kg"] * ratio, 2),
            trees_needed_to_offset = max(1, int(proj["trees_needed_to_offset"] * ratio)),
            equivalent_car_km      = round(proj["equivalent_car_km"] * ratio, 2),
            money_spent            = round(proj["money_spent"] * ratio, 2),
            scale_scenarios        = proj.get("scale_scenarios"),
        )

        # Achievements
        achievements = []
        if eco_score > 80:
            achievements.append("🌟 Eco Champion")
        if total_orders > 50:
            achievements.append("🌱 Sustainability Advocate")
        if carbon_saved_kg > 10:
            achievements.append("🌍 Carbon Saver")

        return UserImpactResponse(
            total_orders           = total_orders,
            eco_score              = eco_score,
            total_carbon_saved_kg  = carbon_saved_kg,
            rank_percentile        = random.randint(75, 95),
            achievements           = achievements,
            yearly_projection      = yearly,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)