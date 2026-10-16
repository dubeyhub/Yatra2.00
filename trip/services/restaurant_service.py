from db import get_db
from services.supabase_service import SupabaseService, is_supabase_enabled

class RestaurantService:
    @staticmethod
    def get_restaurants(filters=None):
        if is_supabase_enabled():
            sb_restaurants = SupabaseService.get_restaurants(filters)
            if sb_restaurants is not None and len(sb_restaurants) > 0:
                return sb_restaurants

        db = get_db()
        query = """
            SELECT r.*, d.name as destination_name, d.city, d.state
            FROM restaurants r
            JOIN destinations d ON r.destination_id = d.id
            WHERE 1=1
        """
        params = []

        if filters:
            if filters.get("destination_id"):
                query += " AND r.destination_id = ?"
                params.append(filters["destination_id"])
            if filters.get("state"):
                query += " AND d.state = ?"
                params.append(filters["state"])
            if filters.get("cuisine_type"):
                query += " AND r.cuisine_type = ?"
                params.append(filters["cuisine_type"])
            if filters.get("is_sattvic") in [True, "1", 1]:
                query += " AND r.is_sattvic = 1"
            if filters.get("search"):
                search_term = f"%{filters['search'].strip()}%"
                query += " AND (r.name LIKE ? OR r.special_dishes LIKE ? OR d.city LIKE ?)"
                params.extend([search_term, search_term, search_term])

        query += " ORDER BY r.avg_cost_for_two ASC"
        rows = db.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_restaurant_by_id(restaurant_id):
        db = get_db()
        query = """
            SELECT r.*, d.name as destination_name, d.city, d.state
            FROM restaurants r
            JOIN destinations d ON r.destination_id = d.id
            WHERE r.id = ?
        """
        row = db.execute(query, (restaurant_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_restaurants_by_destinations(destination_ids):
        if not destination_ids:
            return []
        db = get_db()
        placeholders = ",".join("?" for _ in destination_ids)
        query = f"""
            SELECT r.*, d.name as destination_name, d.city, d.state
            FROM restaurants r
            JOIN destinations d ON r.destination_id = d.id
            WHERE r.destination_id IN ({placeholders})
            ORDER BY r.avg_cost_for_two ASC
        """
        rows = db.execute(query, destination_ids).fetchall()
        return [dict(r) for r in rows]
