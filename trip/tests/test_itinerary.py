from services.itinerary_service import ItineraryService
from services.location_service import LocationService
from services.export_service import ExportService

def test_generate_itinerary(app):
    with app.app_context():
        dests = LocationService.get_destinations_by_ids([1, 2])
        itinerary = ItineraryService.generate_itinerary(
            destinations=dests,
            total_days=3,
            travelers_count=2,
            traveler_profile="seniors",
            pace="relaxed",
            budget_tier="standard",
            start_date="2026-11-01"
        )

        assert itinerary is not None
        assert len(itinerary["days"]) == 3
        assert itinerary["total_days"] == 3
        assert itinerary["traveler_profile"] == "seniors"
        assert itinerary["pace"] == "relaxed"
        assert "budget_info" in itinerary

        day1 = itinerary["days"][0]
        assert "morning_plan" in day1
        assert "afternoon_plan" in day1
        assert "evening_plan" in day1
        assert "Sunday, 01 Nov 2026" in day1["date"]

def test_save_and_retrieve_trip(app):
    with app.app_context():
        dests = LocationService.get_destinations_by_ids([1, 2])
        gen = ItineraryService.generate_itinerary(dests, total_days=2, travelers_count=2)

        trip_id = ItineraryService.save_trip(
            user_id=2, # Demo pilgrim user
            title="Vrindavan & Mathura Bhakti Yatra",
            destination_ids=[1, 2],
            total_days=2,
            travelers_count=2,
            traveler_profile="family",
            pace="balanced",
            budget_tier="standard",
            estimated_total_cost=15000.0,
            days_plan=gen["days"],
            start_date="2026-12-05",
            notes="Include evening Prem Mandir darshan."
        )

        assert trip_id > 0

        # Retrieve
        trip = ItineraryService.get_trip_details(trip_id, user_id=2)
        assert trip is not None
        assert trip["title"] == "Vrindavan & Mathura Bhakti Yatra"
        assert len(trip["destinations"]) == 2
        assert len(trip["days"]) == 2

        # Export tests
        json_export = ExportService.export_trip_to_json(trip)
        assert "Vrindavan & Mathura Bhakti Yatra" in json_export
        assert "itinerary_days" in json_export

        text_export = ExportService.export_trip_to_text(trip)
        assert "YATRA PILGRIMAGE ITINERARY" in text_export
        assert "DAY 1" in text_export

        # Delete
        success = ItineraryService.delete_trip(trip_id, user_id=2)
        assert success is True
        assert ItineraryService.get_trip_details(trip_id) is None
