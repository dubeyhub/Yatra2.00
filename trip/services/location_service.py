from db import get_db
from services.supabase_service import SupabaseService, is_supabase_enabled

class LocationService:
    @staticmethod
    def get_all_destinations(filters=None):
        if is_supabase_enabled():
            sb_dests = SupabaseService.get_all_destinations(filters)
            if sb_dests:
                return sb_dests

        db = get_db()
        query = """
            SELECT d.*, 
                   rsd.opening_hours, rsd.darshan_timings, rsd.morning_aarti_time, rsd.evening_aarti_time,
                   rsd.wheelchair_accessible, rsd.senior_priority_darshan, rsd.battery_car_available,
                   rsd.dress_code, rsd.walking_distance_meters
            FROM destinations d
            LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
            WHERE 1=1
        """
        params = []

        if filters:
            if filters.get("country"):
                query += " AND d.country = ?"
                params.append(filters["country"])
            if filters.get("state"):
                query += " AND d.state = ?"
                params.append(filters["state"])
            if filters.get("category"):
                query += " AND d.category = ?"
                params.append(filters["category"])
            if filters.get("religion"):
                query += " AND d.religion_tradition = ?"
                params.append(filters["religion"])
            if filters.get("search"):
                search_term = f"%{filters['search'].strip()}%"
                query += " AND (d.name LIKE ? OR d.city LIKE ? OR d.state LIKE ? OR d.country LIKE ? OR d.description LIKE ?)"
                params.extend([search_term, search_term, search_term, search_term, search_term])
            if filters.get("wheelchair") in [True, "1", 1]:
                query += " AND rsd.wheelchair_accessible = 1"
            if filters.get("senior_friendly") in [True, "1", 1]:
                query += " AND (rsd.senior_priority_darshan = 1 OR rsd.battery_car_available = 1)"

        query += " ORDER BY d.country ASC, d.state ASC, d.name ASC"
        cur = db.execute(query, params)
        return [dict(row) for row in cur.fetchall()]

    @staticmethod
    def get_destination_by_id(dest_id):
        if is_supabase_enabled():
            dest = SupabaseService.get_destination_by_id(dest_id)
            if dest:
                return dest

        db = get_db()
        query = """
            SELECT d.*, rsd.*
            FROM destinations d
            LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
            WHERE d.id = ?
        """
        row = db.execute(query, (dest_id,)).fetchone()
        return dict(row) if row else None

    @staticmethod
    def get_destinations_by_ids(dest_ids):
        if not dest_ids:
            return []
        if is_supabase_enabled():
            dests = SupabaseService.get_destinations_by_ids(dest_ids)
            if dests:
                return dests

        db = get_db()
        placeholders = ",".join("?" for _ in dest_ids)
        query = f"""
            SELECT d.*, rsd.*
            FROM destinations d
            LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
            WHERE d.id IN ({placeholders})
        """
        rows = db.execute(query, dest_ids).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_all_circuits():
        if is_supabase_enabled():
            circuits = SupabaseService.get_all_circuits()
            if circuits is not None and len(circuits) > 0:
                return circuits

        db = get_db()
        rows = db.execute("SELECT * FROM circuits ORDER BY id ASC").fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_circuit_by_slug_or_id(identifier):
        if is_supabase_enabled() and not str(identifier).isdigit():
            circ = SupabaseService.get_circuit_by_slug(str(identifier))
            if circ:
                return circ

        db = get_db()
        if str(identifier).isdigit():
            circuit = db.execute("SELECT * FROM circuits WHERE id = ?", (int(identifier),)).fetchone()
        else:
            circuit = db.execute("SELECT * FROM circuits WHERE slug = ?", (str(identifier),)).fetchone()
        
        if not circuit:
            return None
        
        circuit_dict = dict(circuit)
        stops_query = """
            SELECT cd.*, d.name as destination_name, d.city, d.state, d.category, d.image_url,
                   rsd.wheelchair_accessible, rsd.senior_priority_darshan, rsd.battery_car_available
            FROM circuit_destinations cd
            JOIN destinations d ON cd.destination_id = d.id
            LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
            WHERE cd.circuit_id = ?
            ORDER BY cd.day_number ASC, cd.sequence_order ASC
        """
        stops = db.execute(stops_query, (circuit_dict["id"],)).fetchall()
        circuit_dict["stops"] = [dict(s) for s in stops]
        return circuit_dict

    @staticmethod
    def get_festivals(destination_id=None, month=None):
        if is_supabase_enabled():
            fests = SupabaseService.get_festivals(month)
            if fests is not None and len(fests) > 0:
                if destination_id:
                    fests = [f for f in fests if f.get("destination_id") == destination_id]
                return fests

        db = get_db()
        query = """
            SELECT f.*, d.name as destination_name, d.city, d.state
            FROM festivals f
            JOIN destinations d ON f.destination_id = d.id
            WHERE 1=1
        """
        params = []
        if destination_id:
            query += " AND f.destination_id = ?"
            params.append(destination_id)
        if month:
            query += " AND f.dated_info_month LIKE ?"
            params.append(f"%{month}%")
        query += " ORDER BY f.id ASC"
        rows = db.execute(query, params).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_featured_destinations(limit=6):
        if is_supabase_enabled():
            featured = SupabaseService.get_featured_destinations(limit)
            if featured:
                return featured

        db = get_db()
        query = """
            SELECT d.*, rsd.opening_hours, rsd.senior_priority_darshan, rsd.wheelchair_accessible
            FROM destinations d
            LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
            WHERE d.verified = 1
            LIMIT ?
        """
        rows = db.execute(query, (limit,)).fetchall()
        return [dict(r) for r in rows]

    @staticmethod
    def get_stats():
        db = get_db()
        try:
            total_destinations = db.execute("SELECT COUNT(*) FROM destinations").fetchone()[0]
        except Exception:
            total_destinations = 24
        try:
            total_circuits = db.execute("SELECT COUNT(*) FROM circuits").fetchone()[0]
        except Exception:
            total_circuits = 8
        try:
            total_festivals = db.execute("SELECT COUNT(*) FROM festivals").fetchone()[0]
        except Exception:
            total_festivals = 19
        try:
            total_hotels = db.execute("SELECT COUNT(*) FROM hotels").fetchone()[0]
        except Exception:
            total_hotels = 28
        try:
            total_restaurants = db.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
        except Exception:
            total_restaurants = 22
        return {
            "destinations": total_destinations,
            "circuits": total_circuits,
            "festivals": total_festivals,
            "hotels": total_hotels,
            "restaurants": total_restaurants
        }
