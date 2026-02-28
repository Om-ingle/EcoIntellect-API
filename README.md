# 🌱 EcoIntellect API

**Tagline:** Sustainability Intelligence Layer for Digital Platforms

[![Hack for Humanity 2026](https://img.shields.io/badge/Hack%20for%20Humanity-2026-brightgreen)](https://hack-for-humanity-26.devpost.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-61dafb?logo=react)](https://reactjs.org)
[![GreenPT](https://img.shields.io/badge/GreenPT-Integrated-22c55e)](https://greenpt.io)
[![Wolfram](https://img.shields.io/badge/Wolfram%7COne-Integrated-DD1100)](https://wolfram.com)

---

## 🎯 Problem Statement

Digital platforms (food delivery, ride booking, e-commerce) contribute significantly to carbon emissions through transportation choices, packaging waste, and inefficient routing. **Users make high-carbon decisions daily without knowing the environmental cost.**

**The Gap:** Platforms lack a plug-and-play sustainability intelligence layer for their checkout flows.

---

## 💡 Solution

EcoIntellect is a **Sustainability Decision Intelligence API** that platforms integrate at checkout to:

| Capability | Description |
|---|---|
| 🔬 **Emission Calculation** | Powered by **GreenPT** emission factors (EPA-sourced baseline) |
| 🔄 **Alternative Comparison** | Rank all 16 transport × packaging combos by Eco Score |
| 📡 **Scale Modelling** | **Wolfram\|One** projects impact from 1,000→1,000,000 users |
| 🎮 **Gamification** | Eco Scores (0–100), achievements, and ranking |
| 🛒 **Checkout Interception** | Live demo showing Swiggy/Zomato-style popup at payment |

---

## 🏗️ Architecture

```
┌──────────────────────────┐
│  Food Delivery Platform  │  (Swiggy, Zomato, etc.)
│  "User presses Pay ₹390" │
└────────────┬─────────────┘
             │ POST /api/v1/analyze-order
             ▼
┌────────────────────────────────────────────────────┐
│               EcoIntellect API                     │
│  (FastAPI · Python · Pydantic)                     │
│                                                    │
│  ┌──────────────────┐  ┌─────────────────────────┐ │
│  │  GreenPTClient   │  │     WolframClient       │ │
│  │  - Emission      │  │  - Yearly projections   │ │
│  │    factors       │  │  - 1k→1M user scenarios │ │
│  │  - Eco estimates │  │  - Tree equivalents     │ │
│  └──────────────────┘  └─────────────────────────┘ │
└────────────────────────────────────────────────────┘
             │
             ▼
┌──────────────────────────┐
│   EcoIntellect Dashboard │  (React + Vite + Recharts)
│   - Analysis charts      │
│   - Alternative rankings │
│   - Wolfram scale chart  │
│   - Mock checkout demo   │
└──────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt

# Add your sponsor API keys
cp .env.example .env

uvicorn app.main:app --reload
# → http://localhost:8000
# → http://localhost:8000/docs  (Swagger UI)
```

### Frontend

```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## 🔑 Environment Variables

```env
# backend/.env
GREENPT_API_KEY=your_greenpt_api_key_here
WOLFRAM_APP_ID=your_wolfram_app_id_here
```

The API root (`GET /`) shows live integration status:
```json
{
  "sponsor_integrations": {
    "greenpt": true,
    "wolfram": true
  }
}
```

---

## 📊 API Reference

### `POST /api/v1/analyze-order`

Calculate the full environmental footprint of a food delivery order.

**Request:**
```json
{
  "distance_km": 5,
  "transport_mode": "car",
  "packaging_type": "plastic",
  "estimated_time_minutes": 30,
  "order_value": 350,
  "frequency_per_week": 3
}
```

**Response:**
```json
{
  "carbon_emission_grams": 650.0,
  "eco_score": 20,
  "rating": "Poor",
  "better_alternatives": [
    {
      "transport_mode": "Bike",
      "packaging_type": "Reusable",
      "carbon_emission_grams": 5.0,
      "carbon_saved_grams": 645.0,
      "time_difference_minutes": 8,
      "eco_score": 95
    }
  ],
  "yearly_projection": {
    "total_orders_per_year": 156,
    "total_carbon_kg": 101.4,
    "trees_needed_to_offset": 5,
    "equivalent_car_km": 845.0,
    "money_spent": 54600.0,
    "scale_scenarios": [
      { "users": 1000,    "total_co2_saved_tonnes": 101.4,   "label": "1,000 users" },
      { "users": 10000,   "total_co2_saved_tonnes": 1014.0,  "label": "10,000 users" },
      { "users": 100000,  "total_co2_saved_tonnes": 10140.0, "label": "100,000 users" },
      { "users": 1000000, "total_co2_saved_tonnes": 101400.0,"label": "1,000,000 users" }
    ]
  },
  "environmental_context": "That's equivalent to driving 811 km by car."
}
```

### `GET /api/v1/compare-alternatives?distance_km=5`

Returns all 16 transport × packaging combinations ranked by Eco Score.

### `GET /api/v1/user-impact/{user_id}`

Returns gamified impact summary: Eco Score, carbon saved, achievements, Wolfram projections.

---

## 🔌 Production Integration Guide

> This section explains how EcoIntellect moves from hackathon demo to production SaaS.

### Decision Matrix: Mock vs Production

| Component | Hackathon Demo | Production |
|---|---|---|
| Emission factors | EPA-sourced constants (in `GreenPTClient`) | Live GreenPT API calls |
| Yearly projections | Wolfram API (active) + math fallback | Full Wolfram\|One computational queries |
| User database | Statistically representative mock data | PostgreSQL / Supabase |
| Authentication | Open (demo) | JWT / API key middleware |

### Upgrading GreenPT to Production

In `backend/app/services/greenpt_integration.py`:

```python
def get_emission_factor(self, category: str, item: str) -> float:
    if self.api_key:
        # ✅ Production: uncomment this block
        # response = requests.post(
        #     f"{self.base_url}/emissions/factor",
        #     headers={"Authorization": f"Bearer {self.api_key}"},
        #     json={"category": category, "item": item}
        # )
        # return response.json().get('co2_grams', 0)
        pass

    # Demo fallback: EPA-sourced baseline data
    return self.demo_transport_factors.get(item, 100)
```

### Example: Zomato Integration

```javascript
// At checkout — call EcoIntellect before showing "Place Order"
const ecoResponse = await fetch('https://api.ecointellect.io/v1/analyze-order', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer YOUR_API_KEY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    distance_km: calculateDistance(restaurant, userAddress),
    transport_mode: selectedDeliveryType,   // "car" | "bike" | "electric_vehicle"
    packaging_type: restaurantPackaging,    // "plastic" | "paper" | "biodegradable"
    order_value: cartTotal,
    frequency_per_week: getUserOrderFrequency(userId)
  })
});

const eco = await ecoResponse.json();

// Show EcoIntellect intercept popup when eco_score < 60
if (eco.eco_score < 60 && eco.better_alternatives.length > 0) {
  const best = eco.better_alternatives[0];
  showEcoInterceptModal({
    carbonSaved: best.carbon_saved_grams,
    ecoOption: `${best.transport_mode} + ${best.packaging_type}`,
    discount: 10   // ₹10 eco-discount
  });
}
```

---

## 🌍 Environmental Impact at Scale

Using **Wolfram|One** modelling (computed live by the API):

| User Adoption | CO₂ Saved / Year |
|---|---|
| 1,000 users switch | ~101 tonnes |
| 10,000 users switch | ~1,014 tonnes |
| 100,000 users switch | ~10,140 tonnes |
| 1,000,000 users switch | ~101,400 tonnes 🌳 |

> Equivalent to planting **4.6 million trees** if 1M delivery users switched to eco-options.

---

## 🎮 Demo Scenarios

| Scenario | Transport | Packaging | Distance | Eco Score |
|---|---|---|---|---|
| High Impact | Car | Plastic | 10 km | 20 (Poor) |
| Mid Range | Motorcycle | Paper | 5 km | — |
| Eco-Friendly | Bike | Reusable | 3 km | 95 (Excellent) |
| EV Transition | Electric Vehicle | Biodegradable | 8 km | — |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| API | FastAPI (Python 3.9+) |
| Validation | Pydantic v2 |
| Sponsor: Emissions | GreenPT API |
| Sponsor: Projections | Wolfram\|One |
| Frontend | React 19 + Vite |
| Styling | Tailwind CSS v4 |
| Charts | Recharts |
| Icons | Lucide React |

---

## 📈 Future Roadmap

- [ ] Production GreenPT API live data feeds
- [ ] Wolfram Alpha complex route optimization queries
- [ ] PostgreSQL user history and carbon ledger
- [ ] Mobile SDK (iOS / Android)
- [ ] Carbon offset marketplace integration
- [ ] Multi-city emission factor calibration
- [ ] AI-powered delivery clustering (reduce total trips)

---

## 📝 License

MIT — see [LICENSE](LICENSE)

---

## 🏆 Built For

**Hack for Humanity 2026** · [hack-for-humanity-26.devpost.com](https://hack-for-humanity-26.devpost.com/)

*Environmental focus: Carbon emissions, waste reduction, sustainable transport*

---

**Built with 💚 for a sustainable future · Powered by GreenPT & Wolfram|One**