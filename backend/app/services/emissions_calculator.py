"""
Emissions Calculator Service
Based on industry-standard emission factors
"""

class EmissionsCalculator:
    # CO2 emissions in grams per km
    TRANSPORT_EMISSIONS = {
        "car": 120,  # Average petrol car
        "motorcycle": 80,
        "electric_vehicle": 40,
        "bike": 0,
        "walk": 0
    }
    
    # CO2 emissions in grams per package
    PACKAGING_EMISSIONS = {
        "plastic": 50,
        "paper": 30,
        "biodegradable": 15,
        "reusable": 5
    }
    
    # Average time per km (minutes)
    TRANSPORT_TIME = {
        "car": 2.5,
        "motorcycle": 2.0,
        "electric_vehicle": 2.5,
        "bike": 4.0,
        "walk": 12.0
    }
    
    @staticmethod
    def calculate_transport_emissions(distance_km: float, mode: str) -> float:
        """Calculate CO2 emissions from transport"""
        return distance_km * EmissionsCalculator.TRANSPORT_EMISSIONS.get(mode, 100)
    
    @staticmethod
    def calculate_packaging_emissions(packaging_type: str) -> float:
        """Calculate CO2 emissions from packaging"""
        return EmissionsCalculator.PACKAGING_EMISSIONS.get(packaging_type, 50)
    
    @staticmethod
    def calculate_total_emissions(distance_km: float, transport_mode: str, packaging_type: str) -> float:
        """Calculate total CO2 emissions"""
        transport = EmissionsCalculator.calculate_transport_emissions(distance_km, transport_mode)
        packaging = EmissionsCalculator.calculate_packaging_emissions(packaging_type)
        return transport + packaging
    
    @staticmethod
    def estimate_time(distance_km: float, transport_mode: str) -> int:
        """Estimate delivery time in minutes"""
        base_time = distance_km * EmissionsCalculator.TRANSPORT_TIME.get(transport_mode, 3.0)
        prep_time = 15  # Food preparation time
        return int(base_time + prep_time)
    
    @staticmethod
    def calculate_eco_score(carbon_grams: float, distance_km: float) -> int:
        """
        Calculate eco score (0-100)
        Lower emissions = higher score
        """
        # Best possible: bike + biodegradable = 15g for 5km = 115g total
        # Worst case: car + plastic = 50g + 600g = 650g for 5km
        baseline = distance_km * 20  # Reasonable baseline
        
        if carbon_grams <= baseline * 0.3:
            return 95
        elif carbon_grams <= baseline * 0.5:
            return 85
        elif carbon_grams <= baseline * 0.7:
            return 70
        elif carbon_grams <= baseline:
            return 55
        elif carbon_grams <= baseline * 1.5:
            return 35
        else:
            return 20
    
    @staticmethod
    def get_rating(eco_score: int) -> str:
        """Get text rating based on eco score"""
        if eco_score >= 85:
            return "Excellent"
        elif eco_score >= 70:
            return "Good"
        elif eco_score >= 50:
            return "Moderate"
        else:
            return "Poor"
    
    @staticmethod
    def calculate_yearly_projection(carbon_grams: float, frequency_per_week: int, order_value: float):
        """Calculate yearly environmental impact"""
        orders_per_year = frequency_per_week * 52
        total_carbon_kg = (carbon_grams * orders_per_year) / 1000
        
        # One tree absorbs ~21.77 kg CO2 per year
        trees_needed = int(total_carbon_kg / 21.77) + 1
        
        # Average car emits ~120g CO2 per km
        equivalent_car_km = total_carbon_kg * 1000 / 120
        
        money_spent = order_value * orders_per_year
        
        return {
            "total_orders_per_year": orders_per_year,
            "total_carbon_kg": round(total_carbon_kg, 2),
            "trees_needed_to_offset": trees_needed,
            "equivalent_car_km": round(equivalent_car_km, 2),
            "money_spent": round(money_spent, 2)
        }
    
    @staticmethod
    def find_alternatives(distance_km: float, current_transport: str, current_packaging: str):
        """Find better alternatives"""
        current_emissions = EmissionsCalculator.calculate_total_emissions(
            distance_km, current_transport, current_packaging
        )
        current_time = EmissionsCalculator.estimate_time(distance_km, current_transport)
        
        alternatives = []
        
        # Try different combinations
        transport_options = ["bike", "electric_vehicle", "motorcycle"]
        packaging_options = ["biodegradable", "reusable"]
        
        for transport in transport_options:
            for packaging in packaging_options:
                if transport == current_transport and packaging == current_packaging:
                    continue
                    
                alt_emissions = EmissionsCalculator.calculate_total_emissions(
                    distance_km, transport, packaging
                )
                alt_time = EmissionsCalculator.estimate_time(distance_km, transport)
                carbon_saved = current_emissions - alt_emissions
                
                if carbon_saved > 0:  # Only show if it saves carbon
                    eco_score = EmissionsCalculator.calculate_eco_score(alt_emissions, distance_km)
                    alternatives.append({
                        "transport_mode": transport.replace("_", " ").title(),
                        "packaging_type": packaging.title(),
                        "carbon_emission_grams": round(alt_emissions, 2),
                        "estimated_time_minutes": alt_time,
                        "carbon_saved_grams": round(carbon_saved, 2),
                        "time_difference_minutes": alt_time - current_time,
                        "eco_score": eco_score
                    })
        
        # Sort by carbon saved (descending)
        alternatives.sort(key=lambda x: x["carbon_saved_grams"], reverse=True)
        
        return alternatives[:3]  # Return top 3
    
    @staticmethod
    def get_environmental_context(carbon_kg: float) -> str:
        """Provide context for carbon emissions"""
        if carbon_kg < 0.5:
            return "That's less than charging a smartphone for a year!"
        elif carbon_kg < 2:
            return "That's equivalent to boiling water for 10 cups of tea."
        elif carbon_kg < 5:
            return "That's like driving a car for 40 km."
        elif carbon_kg < 10:
            return "That's equivalent to a short car trip of 80 km."
        else:
            return f"That's equivalent to driving {int(carbon_kg * 8)} km by car."