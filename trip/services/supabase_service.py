import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

_supabase_client = None

def get_supabase():
    global _supabase_client
    if _supabase_client is not None:
        return _supabase_client
    
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        return None
        
    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        return _supabase_client
    except Exception as e:
        print(f"Supabase connection init failed: {e}")
        return None

try:
    from flask import current_app, has_app_context
except ImportError:
    has_app_context = lambda: False
    current_app = None

def is_supabase_enabled():
    if has_app_context() and current_app and current_app.config.get("TESTING"):
        return False
    client = get_supabase()
    return client is not None

class SupabaseService:
    @staticmethod
    def get_supabase():
        return get_supabase()

    # ----------------------------------------------------
    # Users & Auth
    # ----------------------------------------------------
    @staticmethod
    def get_user_by_login(login_id):
        sb = get_supabase()
        if not sb:
            return None
        login_lower = login_id.strip().lower()
        try:
            # Check username
            res = sb.table("users").select("*").ilike("username", login_lower).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
            # Check email
            res = sb.table("users").select("*").ilike("email", login_lower).execute()
            if res.data and len(res.data) > 0:
                return res.data[0]
        except Exception as e:
            print(f"Supabase get_user_by_login error: {e}")
        return None

    @staticmethod
    def get_user_by_id(user_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("users").select("*").eq("id", user_id).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Supabase get_user_by_id error: {e}")
            return None

    @staticmethod
    def create_user(username, email, password_hash, full_name, phone="", role="user"):
        sb = get_supabase()
        if not sb:
            return None
        data = {
            "username": username.strip(),
            "email": email.strip().lower(),
            "password_hash": password_hash,
            "full_name": full_name.strip(),
            "phone": phone.strip() if phone else "",
            "role": role
        }
        try:
            res = sb.table("users").insert(data).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Supabase create_user error: {e}")
            return None

    @staticmethod
    def update_user_profile(user_id, full_name, phone):
        sb = get_supabase()
        if not sb:
            return False
        try:
            sb.table("users").update({"full_name": full_name, "phone": phone}).eq("id", user_id).execute()
            return True
        except Exception as e:
            print(f"Supabase update_user_profile error: {e}")
            return False

    @staticmethod
    def get_user_counts(user_id):
        sb = get_supabase()
        trips_count = 0
        bookings_count = 0
        if not sb:
            return 0, 0
        try:
            trips = sb.table("trips").select("id", count="exact").eq("user_id", user_id).execute()
            trips_count = trips.count or (len(trips.data) if trips.data else 0)
        except Exception:
            pass
        try:
            bookings = sb.table("bookings").select("id", count="exact").eq("user_id", user_id).execute()
            bookings_count = bookings.count or (len(bookings.data) if bookings.data else 0)
        except Exception:
            pass
        return trips_count, bookings_count

    # ----------------------------------------------------
    # Destinations & Religious Details
    # ----------------------------------------------------
    @staticmethod
    def get_all_destinations(filters=None):
        sb = get_supabase()
        if not sb:
            return []
        try:
            query = sb.table("destinations").select("*, religious_site_details(*)")
            if filters:
                if filters.get("country"):
                    query = query.eq("country", filters["country"])
                if filters.get("state"):
                    query = query.eq("state", filters["state"])
                if filters.get("category"):
                    query = query.eq("category", filters["category"])
                if filters.get("religion"):
                    query = query.eq("religion_tradition", filters["religion"])
                if filters.get("search"):
                    search_term = filters["search"].strip()
                    query = query.or_(f"name.ilike.%{search_term}%,city.ilike.%{search_term}%,state.ilike.%{search_term}%,country.ilike.%{search_term}%,description.ilike.%{search_term}%")
            
            res = query.order("country").order("state").order("name").execute()
            rows = []
            for item in (res.data or []):
                # Flatten religious_site_details into dictionary for template compatibility
                details = item.pop("religious_site_details", None)
                if isinstance(details, list) and len(details) > 0:
                    details = details[0]
                elif not isinstance(details, dict):
                    details = {}
                combined = {**item, **details}
                
                # Filter by senior / wheelchair flags if requested
                if filters:
                    if filters.get("wheelchair") in [True, "1", 1] and not combined.get("wheelchair_accessible"):
                        continue
                    if filters.get("senior_friendly") in [True, "1", 1]:
                        if not (combined.get("senior_priority_darshan") or combined.get("battery_car_available")):
                            continue
                rows.append(combined)
            return rows
        except Exception as e:
            print(f"Supabase get_all_destinations error: {e}")
            return []

    @staticmethod
    def get_destination_by_id(dest_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("destinations").select("*, religious_site_details(*)").eq("id", dest_id).execute()
            if not res.data:
                return None
            item = res.data[0]
            details = item.pop("religious_site_details", None)
            if isinstance(details, list) and len(details) > 0:
                details = details[0]
            elif not isinstance(details, dict):
                details = {}
            return {**item, **details}
        except Exception as e:
            print(f"Supabase get_destination_by_id error: {e}")
            return None

    @staticmethod
    def get_destinations_by_ids(dest_ids):
        if not dest_ids:
            return []
        sb = get_supabase()
        if not sb:
            return []
        try:
            res = sb.table("destinations").select("*, religious_site_details(*)").in_("id", dest_ids).execute()
            out = []
            for item in (res.data or []):
                details = item.pop("religious_site_details", None)
                if isinstance(details, list) and len(details) > 0:
                    details = details[0]
                elif not isinstance(details, dict):
                    details = {}
                out.append({**item, **details})
            return out
        except Exception as e:
            print(f"Supabase get_destinations_by_ids error: {e}")
            return []

    @staticmethod
    def get_featured_destinations(limit=6):
        sb = get_supabase()
        if not sb:
            return []
        try:
            res = sb.table("destinations").select("*, religious_site_details(*)").order("id").limit(limit).execute()
            out = []
            for item in (res.data or []):
                details = item.pop("religious_site_details", None)
                if isinstance(details, list) and len(details) > 0:
                    details = details[0]
                elif not isinstance(details, dict):
                    details = {}
                out.append({**item, **details})
            return out
        except Exception as e:
            print(f"Supabase get_featured_destinations error: {e}")
            return []

    # ----------------------------------------------------
    # Circuits & Festivals
    # ----------------------------------------------------
    @staticmethod
    def get_all_circuits():
        sb = get_supabase()
        if not sb:
            return []
        try:
            res = sb.table("circuits").select("*").order("id").execute()
            return res.data or []
        except Exception as e:
            print(f"Supabase get_all_circuits error (fallback to local if table not ready): {e}")
            return None

    @staticmethod
    def get_circuit_by_slug(slug):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("circuits").select("*").eq("slug", slug).execute()
            if not res.data:
                return None
            circuit = res.data[0]
            # Get stops
            stops_res = sb.table("circuit_destinations").select("*, destinations(*)").eq("circuit_id", circuit["id"]).order("day_number").order("sequence_order").execute()
            stops = []
            for st in (stops_res.data or []):
                dest = st.pop("destinations", None) or {}
                stops.append({**dest, **st})
            circuit["destinations"] = stops
            return circuit
        except Exception as e:
            print(f"Supabase get_circuit_by_slug error: {e}")
            return None

    @staticmethod
    def get_festivals(month=None):
        sb = get_supabase()
        if not sb:
            return []
        try:
            query = sb.table("festivals").select("*, destinations(name, city, state)")
            if month:
                query = query.ilike("dated_info_month", f"%{month}%")
            res = query.order("id").execute()
            out = []
            for f in (res.data or []):
                dest = f.pop("destinations", None) or {}
                f["destination_name"] = dest.get("name")
                f["city"] = dest.get("city")
                f["state"] = dest.get("state")
                out.append(f)
            return out
        except Exception as e:
            print(f"Supabase get_festivals error: {e}")
            return None

    # ----------------------------------------------------
    # Hotels
    # ----------------------------------------------------
    @staticmethod
    def get_hotels(filters=None):
        sb = get_supabase()
        if not sb:
            return None
        try:
            query = sb.table("hotels").select("*, destinations(name, city, state)")
            if filters:
                if filters.get("destination_id"):
                    query = query.eq("destination_id", int(filters["destination_id"]))
                if filters.get("type"):
                    query = query.eq("type", filters["type"])
                if filters.get("is_pure_veg") in [True, "1", 1]:
                    query = query.eq("is_pure_veg", 1)
                if filters.get("is_senior_friendly") in [True, "1", 1]:
                    query = query.eq("is_senior_friendly", 1)
                if filters.get("max_price"):
                    try:
                        query = query.lte("price_per_night", float(filters["max_price"]))
                    except ValueError:
                        pass
                
                sort_by = filters.get("sort_by")
                if sort_by == "price_asc":
                    query = query.order("price_per_night", desc=False)
                elif sort_by == "price_desc":
                    query = query.order("price_per_night", desc=True)
                elif sort_by == "rating":
                    query = query.order("rating", desc=True)
                elif sort_by == "distance":
                    query = query.order("proximity_to_temple_km", desc=False)
                else:
                    query = query.order("rating", desc=True)
            else:
                query = query.order("rating", desc=True)
                
            res = query.execute()
            out = []
            for h in (res.data or []):
                dest = h.pop("destinations", None) or {}
                h["destination_name"] = dest.get("name")
                h["city"] = dest.get("city")
                h["state"] = dest.get("state")
                if filters and filters.get("state") and h["state"] != filters["state"]:
                    continue
                out.append(h)
            return out
        except Exception as e:
            print(f"Supabase get_hotels error: {e}")
            return None

    @staticmethod
    def get_hotel_by_id(hotel_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("hotels").select("*, destinations(name, city, state)").eq("id", hotel_id).execute()
            if not res.data:
                return None
            h = res.data[0]
            dest = h.pop("destinations", None) or {}
            h["destination_name"] = dest.get("name")
            h["city"] = dest.get("city")
            h["state"] = dest.get("state")
            return h
        except Exception as e:
            print(f"Supabase get_hotel_by_id error: {e}")
            return None

    # ----------------------------------------------------
    # Restaurants
    # ----------------------------------------------------
    @staticmethod
    def get_restaurants(filters=None):
        sb = get_supabase()
        if not sb:
            return None
        try:
            query = sb.table("restaurants").select("*, destinations(name, city, state)")
            if filters:
                if filters.get("destination_id"):
                    query = query.eq("destination_id", int(filters["destination_id"]))
                if filters.get("cuisine_type"):
                    query = query.eq("cuisine_type", filters["cuisine_type"])
                if filters.get("is_sattvic") in [True, "1", 1]:
                    query = query.eq("is_sattvic", 1)
                if filters.get("max_cost"):
                    try:
                        query = query.lte("avg_cost_for_two", float(filters["max_cost"]))
                    except ValueError:
                        pass
            res = query.order("id").execute()
            out = []
            for r in (res.data or []):
                dest = r.pop("destinations", None) or {}
                r["destination_name"] = dest.get("name")
                r["city"] = dest.get("city")
                r["state"] = dest.get("state")
                if filters and filters.get("state") and r["state"] != filters["state"]:
                    continue
                out.append(r)
            return out
        except Exception as e:
            print(f"Supabase get_restaurants error: {e}")
            return None

    # ----------------------------------------------------
    # Vehicles
    # ----------------------------------------------------
    @staticmethod
    def get_vehicles(filters=None):
        sb = get_supabase()
        if not sb:
            return None
        try:
            query = sb.table("vehicles").select("*")
            if filters:
                if filters.get("capacity"):
                    try:
                        query = query.gte("capacity", int(filters["capacity"]))
                    except ValueError:
                        pass
                if filters.get("ac") in [True, "1", 1]:
                    query = query.eq("ac_available", 1)
                if filters.get("senior_friendly") in [True, "1", 1]:
                    query = query.eq("senior_friendly_comfort", 1)
            res = query.order("capacity").execute()
            return res.data or []
        except Exception as e:
            print(f"Supabase get_vehicles error: {e}")
            return None

    @staticmethod
    def get_vehicle_by_id(vehicle_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("vehicles").select("*").eq("id", vehicle_id).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Supabase get_vehicle_by_id error: {e}")
            return None

    # ----------------------------------------------------
    # Trips & Itineraries
    # ----------------------------------------------------
    @staticmethod
    def save_trip(trip_data, days_data):
        sb = get_supabase()
        if not sb:
            return None
        try:
            # Ensure destination_ids_json is string
            if isinstance(trip_data.get("destination_ids_json"), (list, dict)):
                trip_data["destination_ids_json"] = json.dumps(trip_data["destination_ids_json"])
            res = sb.table("trips").insert(trip_data).execute()
            if not res.data:
                return None
            trip_id = res.data[0]["id"]
            
            # Insert days
            for d in days_data:
                d["trip_id"] = trip_id
            if days_data:
                sb.table("trip_days").insert(days_data).execute()
            return trip_id
        except Exception as e:
            print(f"Supabase save_trip error: {e}")
            return None

    @staticmethod
    def get_user_trips(user_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("trips").select("*, circuits(name)").eq("user_id", user_id).order("id", desc=True).execute()
            out = []
            for t in (res.data or []):
                circ = t.pop("circuits", None) or {}
                t["circuit_name"] = circ.get("name")
                out.append(t)
            return out
        except Exception as e:
            print(f"Supabase get_user_trips error: {e}")
            return None

    @staticmethod
    def get_trip_by_id(trip_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("trips").select("*, circuits(name)").eq("id", trip_id).execute()
            if not res.data:
                return None
            trip = res.data[0]
            circ = trip.pop("circuits", None) or {}
            trip["circuit_name"] = circ.get("name")
            
            # Fetch days
            days_res = sb.table("trip_days").select("*").eq("trip_id", trip_id).order("day_number").execute()
            trip["days"] = days_res.data or []
            return trip
        except Exception as e:
            print(f"Supabase get_trip_by_id error: {e}")
            return None

    # ----------------------------------------------------
    # Bookings
    # ----------------------------------------------------
    @staticmethod
    def create_booking(booking_data):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("bookings").insert(booking_data).execute()
            return res.data[0]["id"] if res.data else None
        except Exception as e:
            print(f"Supabase create_booking error: {e}")
            return None

    @staticmethod
    def get_user_bookings(user_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("bookings").select("*").eq("user_id", user_id).order("id", desc=True).execute()
            bookings = res.data or []
            # Enrich reference titles
            for b in bookings:
                b_type = b.get("booking_type")
                ref_id = b.get("reference_id")
                if b_type == "hotel":
                    h = sb.table("hotels").select("name").eq("id", ref_id).execute()
                    b["reference_title"] = h.data[0]["name"] if h.data else f"Hotel #{ref_id}"
                elif b_type == "vehicle":
                    v = sb.table("vehicles").select("vehicle_type").eq("id", ref_id).execute()
                    b["reference_title"] = v.data[0]["vehicle_type"] if v.data else f"Vehicle #{ref_id}"
                else:
                    b["reference_title"] = "Puja & Darshan VIP Assistance"
            return bookings
        except Exception as e:
            print(f"Supabase get_user_bookings error: {e}")
            return None

    @staticmethod
    def get_booking_by_id(booking_id):
        sb = get_supabase()
        if not sb:
            return None
        try:
            res = sb.table("bookings").select("*, users(username, full_name, email, phone)").eq("id", booking_id).execute()
            if not res.data:
                return None
            b = res.data[0]
            u = b.pop("users", None) or {}
            b = {**b, **u}
            b_type = b.get("booking_type")
            ref_id = b.get("reference_id")
            if b_type == "hotel":
                h = sb.table("hotels").select("name, address").eq("id", ref_id).execute()
                b["reference_title"] = h.data[0]["name"] if h.data else f"Hotel #{ref_id}"
            elif b_type == "vehicle":
                v = sb.table("vehicles").select("vehicle_type, capacity").eq("id", ref_id).execute()
                b["reference_title"] = v.data[0]["vehicle_type"] if v.data else f"Vehicle #{ref_id}"
            else:
                b["reference_title"] = "Puja & Darshan VIP Assistance"
            return b
        except Exception as e:
            print(f"Supabase get_booking_by_id error: {e}")
            return None
