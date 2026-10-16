import math
from services.vehicle_service import VehicleService
from config import Config

class BudgetService:
    @staticmethod
    def calculate_budget(destination_ids, total_days, travelers_count=2, budget_tier="standard", traveler_profile="family", vehicle_id=None):
        """
        Calculates itemized pilgrimage travel budget.
        All prices are clearly documented sample estimates in INR (₹).
        """
        total_days = max(1, int(total_days))
        travelers_count = max(1, int(travelers_count))
        rooms_needed = math.ceil(travelers_count / 2)

        # 1. Accommodation estimation per room per night
        if budget_tier == "economy":
            room_rate_per_night = 800.0   # Dharamshala / Ashram / Pilgrim Niwas
            tier_label = "Economy (Ashrams & Dharamshalas)"
        elif budget_tier == "comfort":
            room_rate_per_night = 4000.0  # Heritage Haveli / 3-4 Star Premium Stay
            tier_label = "Comfort (Heritage Havelis & Premium Hotels)"
        else: # standard
            room_rate_per_night = 2200.0  # Quality Pure-Veg Standard Hotel
            tier_label = "Standard (Verified Pure-Veg Hotels)"

        total_accommodation = room_rate_per_night * rooms_needed * total_days

        # 2. Food estimation per person per day
        if budget_tier == "economy":
            food_rate_per_person_day = 200.0  # Langar, Mahaprasad & Simple Thali
        elif budget_tier == "comfort":
            food_rate_per_person_day = 850.0  # Multi-course Sattvic Bhojan & Sweets
        else: # standard
            food_rate_per_person_day = 450.0  # Authentic regional Pure Veg Thalis

        total_food = food_rate_per_person_day * travelers_count * total_days

        # 3. Transport estimation
        if vehicle_id:
            vehicle_cost_data = VehicleService.calculate_vehicle_cost(vehicle_id, total_days)
            total_transport = vehicle_cost_data["total_estimated"]
            transport_details = f"Dedicated {vehicle_cost_data['vehicle']['vehicle_type']} for {total_days} days"
        else:
            # Local transit estimation (E-rickshaws, autos, shared transit)
            if budget_tier == "economy":
                total_transport = 150.0 * travelers_count * total_days
                transport_details = "Local E-Rickshaws & Shared Taxis"
            elif budget_tier == "comfort":
                # Auto-recommend comfortable SUV
                rec_vehicle = VehicleService.recommend_vehicle(travelers_count, traveler_profile == "seniors")
                if rec_vehicle:
                    vehicle_cost_data = VehicleService.calculate_vehicle_cost(rec_vehicle["id"], total_days)
                    total_transport = vehicle_cost_data["total_estimated"]
                    transport_details = f"Chauffeur-driven {rec_vehicle['vehicle_type']}"
                else:
                    total_transport = 1200.0 * total_days
                    transport_details = "Private Chauffeur Cab"
            else: # standard
                rec_vehicle = VehicleService.recommend_vehicle(travelers_count, traveler_profile == "seniors")
                if rec_vehicle:
                    vehicle_cost_data = VehicleService.calculate_vehicle_cost(rec_vehicle["id"], total_days)
                    total_transport = vehicle_cost_data["total_estimated"]
                    transport_details = f"Chauffeur-driven {rec_vehicle['vehicle_type']}"
                else:
                    total_transport = 800.0 * total_days
                    transport_details = "Dedicated Pilgrimage Cab"

        # 4. Temple Darshan, Special Passes & Offerings per person
        if budget_tier == "economy":
            # Free Sarva Darshan queues, standard prasad tokens
            darshan_per_person_day = 100.0
        elif budget_tier == "comfort":
            # VIP Sugam Darshan passes (e.g. ₹300 per shrine), Special Pooja/Archana, Prasad baskets
            darshan_per_person_day = 450.0
        else: # standard
            # Occasional special darshan pass and archana offering
            darshan_per_person_day = 250.0

        total_darshan_pooja = darshan_per_person_day * travelers_count * total_days

        # 5. Senior / Family Accessibility & Miscellany buffer
        accessibility_extras = 0.0
        if traveler_profile == "seniors":
            # Battery cart rides, wheelchair assistance, porter/seva tokens
            accessibility_extras = 200.0 * travelers_count * total_days
        elif traveler_profile == "family":
            accessibility_extras = 100.0 * travelers_count * total_days

        # 6. Contingency Buffer (approx 8%)
        subtotal = total_accommodation + total_food + total_transport + total_darshan_pooja + accessibility_extras
        emergency_buffer = round(subtotal * 0.08, 2)
        grand_total = round(subtotal + emergency_buffer, 2)
        per_person = round(grand_total / travelers_count, 2)

        return {
            "currency": Config.CURRENCY_SYMBOL,
            "tier": budget_tier,
            "tier_label": tier_label,
            "travelers_count": travelers_count,
            "rooms_needed": rooms_needed,
            "total_days": total_days,
            "traveler_profile": traveler_profile,
            "breakdown": {
                "accommodation": {
                    "label": "Accommodation & Dharamshalas",
                    "amount": round(total_accommodation, 2),
                    "note": f"{rooms_needed} room(s) × ₹{room_rate_per_night:,.0f}/night × {total_days} days"
                },
                "food": {
                    "label": "Sattvic Food, Prasad & Dining",
                    "amount": round(total_food, 2),
                    "note": f"₹{food_rate_per_person_day:,.0f}/person/day × {travelers_count} pilgrims"
                },
                "transport": {
                    "label": "Travel & Local Transport",
                    "amount": round(total_transport, 2),
                    "note": transport_details
                },
                "darshan_pooja": {
                    "label": "Darshan Passes, Aarti Seva & Prasad",
                    "amount": round(total_darshan_pooja, 2),
                    "note": f"Sample darshan & archana estimated at ₹{darshan_per_person_day:,.0f}/person/day"
                },
                "accessibility_misc": {
                    "label": "Senior/Family Accessibility & Extras",
                    "amount": round(accessibility_extras, 2),
                    "note": "Battery carts, shoe counter tokens, wheelchair attendants" if traveler_profile == "seniors" else "Local guides, ghat diya offerings, token fees"
                },
                "emergency_buffer": {
                    "label": "Contingency & Seasonal Buffer (8%)",
                    "amount": emergency_buffer,
                    "note": "Safety reserve for unforeseen pilgrimage expenses"
                }
            },
            "subtotal": round(subtotal, 2),
            "grand_total": grand_total,
            "per_person_cost": per_person,
            "disclaimer": Config.SAMPLE_PRICE_DISCLAIMER
        }
