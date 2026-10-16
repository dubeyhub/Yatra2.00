from db import get_db
from services.supabase_service import SupabaseService, is_supabase_enabled

class HotelService:
    @staticmethod
    def get_hotels(filters=None):
        if is_supabase_enabled():
            sb_hotels = SupabaseService.get_hotels(filters)
            if sb_hotels is not None and len(sb_hotels) > 0:
                return sb_hotels

        db = get_db()
        query = """
            SELECT h.*, d.name as destination_name, d.city, d.state
            FROM hotels h
            JOIN destinations d ON h.destination_id = d.id
            WHERE 1=1
        """
        params = []

        if filters:
            if filters.get("destination_id"):
                query += " AND h.destination_id = ?"
                params.append(filters["destination_id"])
            if filters.get("state"):
                query += " AND d.state = ?"
                params.append(filters["state"])
            if filters.get("type"):
                query += " AND h.type = ?"
                params.append(filters["type"])
            if filters.get("is_pure_veg") in [True, "1", 1]:
                query += " AND h.is_pure_veg = 1"
            if filters.get("is_senior_friendly") in [True, "1", 1]:
                query += " AND (h.is_senior_friendly = 1 OR h.has_lift = 1 OR h.has_wheelchair_ramp = 1)"
            if filters.get("max_price"):
                try:
                    query += " AND h.price_per_night <= ?"
                    params.append(float(filters["max_price"]))
                except (ValueError, TypeError):
                    pass

        # Sort
        sort_by = filters.get("sort_by") if filters else None
        if sort_by == "price_asc":
            query += " ORDER BY h.price_per_night ASC"
        elif sort_by == "price_desc":
            query += " ORDER BY h.price_per_night DESC"
        elif sort_by == "rating":
            query += " ORDER BY h.rating DESC"
        elif sort_by == "distance":
            query += " ORDER BY h.proximity_to_temple_km ASC"
        else:
            query += " ORDER BY h.rating DESC, h.price_per_night ASC"

        rows = db.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_hotel_by_id(hotel_id):
        if is_supabase_enabled():
            sb_hotel = SupabaseService.get_hotel_by_id(hotel_id)
            if sb_hotel:
                return sb_hotel

        db = get_db()
        query = """
            SELECT h.*, d.name as destination_name, d.city, d.state
            FROM hotels h
            JOIN destinations d ON h.destination_id = d.id
            WHERE h.id = ?
        """
        row = db.execute(query, (hotel_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_hotels_by_destinations(destination_ids):
        if not destination_ids:
            return []
        db = get_db()
        placeholders = ",".join("?" for _ in destination_ids)
        query = f"""
            SELECT h.*, d.name as destination_name, d.city, d.state
            FROM hotels h
            JOIN destinations d ON h.destination_id = d.id
            WHERE h.destination_id IN ({placeholders})
            ORDER BY h.rating DESC
        """
        rows = db.execute(query, destination_ids).fetchall()
        return [dict(r) for r in rows]
