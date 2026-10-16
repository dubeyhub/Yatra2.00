import json
from datetime import datetime, timedelta
from db import get_db
from services.location_service import LocationService
from services.budget_service import BudgetService
from services.supabase_service import SupabaseService, is_supabase_enabled

class ItineraryService:
    @staticmethod
    def generate_itinerary(destinations, total_days=3, travelers_count=2, traveler_profile="family", pace="balanced", budget_tier="standard", start_date=None):
        """
        Generates a culturally respectful, realistic, day-by-day pilgrimage itinerary.
        """
        total_days = max(1, int(total_days))
        travelers_count = max(1, int(travelers_count))

        if not destinations:
            return {"days": [], "summary": "No destinations selected."}

        # Parse start date if provided
        base_date = None
        if start_date:
            try:
                base_date = datetime.strptime(start_date, "%Y-%m-%d")
            except ValueError:
                base_date = None

        dest_count = len(destinations)
        days_list = []

        # Calculate budget for entire trip
        dest_ids = [d["id"] for d in destinations]
        budget_info = BudgetService.calculate_budget(
            destination_ids=dest_ids,
            total_days=total_days,
            travelers_count=travelers_count,
            budget_tier=budget_tier,
            traveler_profile=traveler_profile
        )
        avg_cost_per_day = round(budget_info["grand_total"] / total_days, 2)

        is_senior = (traveler_profile == "seniors")

        for day_num in range(1, total_days + 1):
            # Pick primary destination for this day
            dest_index = (day_num - 1) % dest_count
            primary_dest = destinations[dest_index]
            dest_name = primary_dest.get("name", "Sacred Pilgrimage Site")
            city = primary_dest.get("city", "")
            state = primary_dest.get("state", "")

            # Formulate day date
            current_date_str = ""
            if base_date:
                curr_dt = base_date + timedelta(days=day_num - 1)
                current_date_str = curr_dt.strftime("%A, %d %b %Y")

            # Extract timings
            morning_aarti = primary_dest.get("morning_aarti_time") or "06:00 AM"
            evening_aarti = primary_dest.get("evening_aarti_time") or "07:00 PM"
            darshan_timings = primary_dest.get("darshan_timings") or "07:00 AM - 12:00 PM"
            dress_code = primary_dest.get("dress_code") or "Modest traditional attire"
            wheelchair = primary_dest.get("wheelchair_accessible", 0)
            battery_car = primary_dest.get("battery_car_available", 0)
            senior_priority = primary_dest.get("senior_priority_darshan", 0)

            # Build Morning Plan
            if day_num == 1:
                morning_plan = (
                    f"Arrival in {city}, {state}. Check into your pre-arranged hotel/dharamshala. "
                    f"Freshen up and acclimatize. "
                )
                if is_senior:
                    morning_plan += "Take leisurely tea/breakfast and review the day's temple entry logistics without rush."
                else:
                    morning_plan += f"Head towards {dest_name} for preliminary orientation and morning parikrama."
            else:
                morning_plan = f"Rise early for auspicious morning prayers. "
                if is_senior and senior_priority:
                    morning_plan += (
                        f"Proceed to {dest_name} via Senior Citizen Priority Queue at {morning_aarti}. "
                        f"Avail electric battery cart from the entrance gate. "
                        f"Experience blissful morning darshan followed by sacred Prasad."
                    )
                else:
                    morning_plan += (
                        f"Attend {morning_aarti} at {dest_name}. "
                        f"Participate in general/Sugam darshan ({darshan_timings}). "
                        f"Receive sanctified Mahaprasad."
                    )

            # Build Afternoon Plan
            if pace == "relaxed" or is_senior:
                afternoon_plan = (
                    f"Sattvic pure-vegetarian lunch at nearby temple bhojanalaya or verified restaurant. "
                    f"Afternoon rest period (1:00 PM - 4:00 PM) to avoid afternoon heat and allow elders comfortable relaxation. "
                    f"Listen to devotional chants or sacred readings."
                )
            else:
                afternoon_plan = (
                    f"Relish traditional regional vegetarian thali. "
                    f"Explore local heritage corridors, historic ashrams, and sacred theertham ponds around {city}. "
                    f"Quiet contemplation or satsang."
                )

            # Build Evening Plan
            if day_num == total_days:
                evening_plan = (
                    f"Attend concluding evening prayers and magnificent {evening_aarti} at {dest_name}. "
                    f"Offer heartfelt gratitude and prayer. Light earthen lamps (diyas). "
                    f"Light dinner and pack sacred prasad souvenirs for departure."
                )
            else:
                evening_plan = (
                    f"Assemble for {evening_aarti} at {dest_name}. "
                    f"The reverberations of temple bells, conches, and sacred lamps create a deeply transformative atmosphere. "
                )
                if primary_dest.get("category") == "sacred_river":
                    evening_plan += "Float illuminated flower deepas upon the river waters with prayers for family welfare."
                else:
                    evening_plan += "Leisurely walk through the spiritual bazaars for tulsi malas, brass puja items, and sweets."
                evening_plan += " Wholesome light dinner and restful night."

            # Accessibility & Etiquette Advisory
            advisory = []
            if dress_code:
                advisory.append(f"Dress Code: {dress_code}")
            if is_senior:
                if battery_car:
                    advisory.append("Senior Note: Battery car / golf cart service is available from main gate.")
                if senior_priority:
                    advisory.append("Senior Note: Carry original government Photo ID (Aadhaar/Passport) for senior priority darshan counter.")
                if wheelchair:
                    advisory.append("Wheelchair ramps and assistance available.")
            
            day_title = f"Day {day_num}: {dest_name} & Spiritual Darshan"
            if day_num == 1:
                day_title = f"Day 1: Arrival & Sacred Welcome in {city}"
            elif day_num == total_days:
                day_title = f"Day {total_days}: Final Blessings & Auspicious Farewell"

            days_list.append({
                "day_number": day_num,
                "date": current_date_str,
                "title": day_title,
                "destination_name": dest_name,
                "city": city,
                "state": state,
                "morning_plan": morning_plan,
                "afternoon_plan": afternoon_plan,
                "evening_plan": evening_plan,
                "advisories": advisory,
                "estimated_cost": avg_cost_per_day
            })

        return {
            "title": f"{total_days}-Day Sacred Pilgrimage: {', '.join(d['city'] for d in destinations[:3])}",
            "destinations": destinations,
            "total_days": total_days,
            "travelers_count": travelers_count,
            "traveler_profile": traveler_profile,
            "pace": pace,
            "budget_tier": budget_tier,
            "start_date": start_date,
            "budget_info": budget_info,
            "days": days_list
        }

    @staticmethod
    def save_trip(user_id, title, destination_ids, total_days, travelers_count, traveler_profile, pace, budget_tier, estimated_total_cost, days_plan, circuit_id=None, start_date=None, notes=""):
        dest_ids_json = json.dumps(destination_ids)
        sb_trip_id = None

        # 1. Save to Supabase
        if is_supabase_enabled():
            trip_data = {
                "user_id": user_id,
                "title": title,
                "circuit_id": circuit_id,
                "destination_ids_json": dest_ids_json,
                "start_date": start_date or "",
                "total_days": total_days,
                "travelers_count": travelers_count,
                "traveler_profile": traveler_profile,
                "pace": pace,
                "budget_tier": budget_tier,
                "estimated_total_cost": estimated_total_cost,
                "notes": notes or ""
            }
            days_data = [
                {
                    "day_number": day["day_number"],
                    "date": day.get("date", ""),
                    "title": day["title"],
                    "morning_plan": day["morning_plan"],
                    "afternoon_plan": day["afternoon_plan"],
                    "evening_plan": day["evening_plan"],
                    "estimated_cost": day.get("estimated_cost", 0.0)
                }
                for day in days_plan
            ]
            sb_trip_id = SupabaseService.save_trip(trip_data, days_data)

        # 2. Local SQLite Sync / Fallback
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO trips (
                    user_id, title, circuit_id, destination_ids_json, start_date,
                    total_days, travelers_count, traveler_profile, pace, budget_tier,
                    estimated_total_cost, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, title, circuit_id, dest_ids_json, start_date,
                 total_days, travelers_count, traveler_profile, pace, budget_tier,
                 estimated_total_cost, notes)
            )
            trip_id = cursor.lastrowid
            for day in days_plan:
                cursor.execute(
                    """
                    INSERT INTO trip_days (
                        trip_id, day_number, date, title, morning_plan, afternoon_plan, evening_plan, estimated_cost
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (trip_id, day["day_number"], day.get("date", ""), day["title"],
                     day["morning_plan"], day["afternoon_plan"], day["evening_plan"],
                     day.get("estimated_cost", 0.0))
                )
            db.commit()
            return sb_trip_id or trip_id
        except Exception as e:
            print(f"Local db trip sync note: {e}")
            return sb_trip_id or 1

    @staticmethod
    def get_user_trips(user_id):
        if is_supabase_enabled():
            sb_trips = SupabaseService.get_user_trips(user_id)
            if sb_trips is not None and len(sb_trips) > 0:
                for trip_dict in sb_trips:
                    try:
                        raw = trip_dict.get("destination_ids_json")
                        dest_ids = json.loads(raw) if isinstance(raw, str) else (raw or [])
                    except Exception:
                        dest_ids = []
                    trip_dict["destinations"] = LocationService.get_destinations_by_ids(dest_ids)
                return sb_trips

        db = get_db()
        query = """
            SELECT t.*, c.name as circuit_name
            FROM trips t
            LEFT JOIN circuits c ON t.circuit_id = c.id
            WHERE t.user_id = ?
            ORDER BY t.created_at DESC
        """
        rows = db.execute(query, (user_id,)).fetchall()
        trips = []
        for r in rows:
            trip_dict = dict(r)
            try:
                dest_ids = json.loads(trip_dict["destination_ids_json"])
            except Exception:
                dest_ids = []
            trip_dict["destinations"] = LocationService.get_destinations_by_ids(dest_ids)
            trips.append(trip_dict)
        return trips

    @staticmethod
    def get_trip_details(trip_id, user_id=None):
        if is_supabase_enabled():
            trip = SupabaseService.get_trip_by_id(trip_id)
            if trip:
                try:
                    raw = trip.get("destination_ids_json")
                    dest_ids = json.loads(raw) if isinstance(raw, str) else (raw or [])
                except Exception:
                    dest_ids = []
                trip["destinations"] = LocationService.get_destinations_by_ids(dest_ids)
                trip["budget_info"] = BudgetService.calculate_budget(
                    destination_ids=dest_ids,
                    total_days=trip["total_days"],
                    travelers_count=trip["travelers_count"],
                    budget_tier=trip["budget_tier"],
                    traveler_profile=trip["traveler_profile"]
                )
                return trip

        db = get_db()
        query = """
            SELECT t.*, c.name as circuit_name
            FROM trips t
            LEFT JOIN circuits c ON t.circuit_id = c.id
            WHERE t.id = ?
        """
        params = [trip_id]
        if user_id:
            query += " AND t.user_id = ?"
            params.append(user_id)

        trip_row = db.execute(query, params).fetchone()
        if not trip_row:
            return None

        trip = dict(trip_row)
        try:
            dest_ids = json.loads(trip["destination_ids_json"])
        except Exception:
            dest_ids = []

        trip["destinations"] = LocationService.get_destinations_by_ids(dest_ids)

        days_rows = db.execute(
            "SELECT * FROM trip_days WHERE trip_id = ? ORDER BY day_number ASC",
            (trip_id,)
        ).fetchall()
        trip["days"] = [dict(d) for d in days_rows]

        trip["budget_info"] = BudgetService.calculate_budget(
            destination_ids=dest_ids,
            total_days=trip["total_days"],
            travelers_count=trip["travelers_count"],
            budget_tier=trip["budget_tier"],
            traveler_profile=trip["traveler_profile"]
        )

        return trip

    @staticmethod
    def delete_trip(trip_id, user_id):
        if is_supabase_enabled():
            sb = SupabaseService.get_supabase()
            if sb:
                try:
                    sb.table("trips").delete().eq("id", trip_id).eq("user_id", user_id).execute()
                except Exception:
                    pass

        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM trips WHERE id = ? AND user_id = ?", (trip_id, user_id))
        db.commit()
        return cursor.rowcount > 0
