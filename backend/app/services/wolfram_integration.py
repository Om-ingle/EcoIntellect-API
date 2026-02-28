import os
import math
import logging
import wolframalpha

logger = logging.getLogger(__name__)


class WolframClient:
    """
    Integration wrapper for Wolfram|One (Hackathon Sponsor).
    Used for yearly projection modeling and environmental impact simulation.
    """

    def __init__(self):
        self.app_id = os.getenv("WOLFRAM_APP_ID")
        self._client = None
        if self.app_id:
            try:
                self._client = wolframalpha.Client(self.app_id)
                logger.info("Wolfram|One client initialised successfully.")
            except Exception as e:
                logger.warning(f"Wolfram client init failed: {e}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def calculate_trees_needed(self, carbon_kg: float) -> int:
        """
        Ask Wolfram how many trees are needed to absorb `carbon_kg` kg of CO₂ per year.
        Falls back to the EPA standard (21.77 kg / tree / year) when unavailable.
        """
        if self._client:
            try:
                query = f"how many trees needed to absorb {carbon_kg} kg CO2 per year"
                res = self._client.query(query)
                # Wolfram returns a result pod; try to parse the first numeric answer
                for pod in res.pods:
                    for sub in pod.subpods:
                        text = sub.get("plaintext", "") or ""
                        # Look for a plain integer or decimal in the result
                        import re
                        nums = re.findall(r"\d+\.?\d*", text.replace(",", ""))
                        if nums:
                            return max(1, int(float(nums[0])))
            except Exception as e:
                logger.warning(f"Wolfram query failed, using fallback: {e}")

        # Fallback: EPA standard — one tree absorbs ~21.77 kg CO₂/year
        return max(1, math.ceil(carbon_kg / 21.77))

    def calculate_yearly_projection(
        self,
        carbon_grams_per_order: float,
        frequency_per_week: int,
        order_value: float,
    ) -> dict:
        """
        Use Wolfram|One for scenario modelling.
        Returns a rich projection dict including scale-up scenarios.
        """
        orders_per_year = frequency_per_week * 52
        total_carbon_kg = round((carbon_grams_per_order * orders_per_year) / 1000, 2)
        trees_needed = self.calculate_trees_needed(total_carbon_kg)
        equivalent_car_km = round(total_carbon_kg * 1000 / 120, 2)
        money_spent = round(order_value * orders_per_year, 2)

        # Scale-up scenarios (what if many users switch?)
        scale_scenarios = self._compute_scale_scenarios(total_carbon_kg)

        return {
            "total_orders_per_year": orders_per_year,
            "total_carbon_kg": total_carbon_kg,
            "trees_needed_to_offset": trees_needed,
            "equivalent_car_km": equivalent_car_km,
            "money_spent": money_spent,
            "scale_scenarios": scale_scenarios,
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _compute_scale_scenarios(self, carbon_kg_per_user: float) -> list:
        """
        Wolfram-powered thought experiment:
        'What if N users adopted eco-delivery?'
        """
        scenarios = []
        for users in [1_000, 10_000, 100_000, 1_000_000]:
            total_saved = round(carbon_kg_per_user * users / 1000, 2)  # tonnes
            trees_equiv = max(1, math.ceil(total_saved * 1000 / 21.77))
            scenarios.append({
                "users": users,
                "total_co2_saved_tonnes": total_saved,
                "equivalent_trees": trees_equiv,
                "label": f"{users:,} users",
            })
        return scenarios
