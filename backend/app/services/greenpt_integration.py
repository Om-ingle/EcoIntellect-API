import os
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class GreenPTClient:
    """
    Integration wrapper for GreenPT API (Hackathon Sponsor)
    Provides sustainability metrics and carbon emission factors.
    """
    def __init__(self):
        self.api_key = os.getenv("GREENPT_API_KEY")
        self.base_url = "https://api.greenpt.io/v1"
        
        # DEMO Mode: Using EPA-sourced baseline data for consistent hackathon demo
        self.demo_transport_factors = {
            "car": 120,
            "motorcycle": 80,
            "electric_vehicle": 40,
            "bike": 0,
            "walk": 0
        }
        self.demo_packaging_factors = {
            "plastic": 50,
            "paper": 30,
            "biodegradable": 15,
            "reusable": 5
        }

    def get_emission_factor(self, category: str, item: str) -> float:
        """
        Fetch emission factor from GreenPT API.
        Returns CO2 equivalent in grams.
        """
        if self.api_key:
            # TODO: Production Implementation
            # Example: 
            # response = requests.post(f"{self.base_url}/emissions/factor", 
            #                          headers={"Authorization": f"Bearer {self.api_key}"},
            #                          json={"category": category, "item": item})
            # return response.json().get('co2_grams', 0)
            logger.info(f"GreenPT API Key found. Would call API for {category}:{item}")
            pass
            
        # Demo Mode Fallback
        if category == "transport":
            return self.demo_transport_factors.get(item, 100)
        elif category == "packaging":
            return self.demo_packaging_factors.get(item, 50)
            
        return 0.0

    def get_eco_recommendation(self, current_choice: Dict[str, Any]) -> str:
        """
        Get AI-powered sustainability recommendation from GreenPT
        """
        # TODO: Production Implementation
        return "Switch to bike delivery to save significant carbon emissions."
