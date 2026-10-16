from db import get_db
from services.supabase_service import SupabaseService, is_supabase_enabled

class VehicleService:
    @staticmethod
    def get_all_vehicles():
        if is_supabase_enabled():
            sb_vehicles = SupabaseService.get_vehicles()
            if sb_vehicles is not None and len(sb_vehicles) > 0:
                return sb_vehicles

        db = get_db()
        rows = db.execute("SELECT * FROM vehicles ORDER BY capacity ASC, price_per_day ASC").fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        if is_supabase_enabled():
            sb_vehicle = SupabaseService.get_vehicle_by_id(vehicle_id)
            if sb_vehicle:
                return sb_vehicle

        db = get_db()
        row = db.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def calculate_vehicle_cost(vehicle_id, total_days, estimated_km_per_day=120):
        vehicle = VehicleService.get_vehicle_by_id(vehicle_id)
        if not vehicle:
            return 0.0

        total_days = max(1, int(total_days))
        estimated_km = total_days * estimated_km_per_day

        base_rental = vehicle["price_per_day"] * total_days
        distance_charge = vehicle["price_per_km"] * estimated_km
        driver_allowance = vehicle["driver_allowance_per_day"] * total_days

        total = base_rental + distance_charge + driver_allowance
        return {
            "vehicle": vehicle,
            "days": total_days,
            "estimated_km": estimated_km,
            "base_rental": round(base_rental, 2),
            "distance_charge": round(distance_charge, 2),
            "driver_allowance": round(driver_allowance, 2),
            "total_estimated": round(total, 2)
        }

    @staticmethod
    def recommend_vehicle(travelers_count, has_seniors=False):
        vehicles = VehicleService.get_all_vehicles()
        if not vehicles:
            return None

        # Filter by capacity
        suitable = [v for v in vehicles if v["capacity"] >= travelers_count]
        if not suitable:
            return max(vehicles, key=lambda v: v["capacity"])

        if has_seniors:
            # Prioritize senior friendly comfort
            senior_suited = [v for v in suitable if v.get("senior_friendly_comfort") == 1]
            if senior_suited:
                return min(senior_suited, key=lambda v: v["price_per_day"])

        return min(suitable, key=lambda v: v["price_per_day"])
