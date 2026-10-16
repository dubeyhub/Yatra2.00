import json

class ExportService:
    @staticmethod
    def export_trip_to_json(trip):
        """Converts trip details to formatted JSON string."""
        clean_trip = {
            "title": trip.get("title"),
            "total_days": trip.get("total_days"),
            "start_date": trip.get("start_date"),
            "travelers_count": trip.get("travelers_count"),
            "traveler_profile": trip.get("traveler_profile"),
            "pace": trip.get("pace"),
            "budget_tier": trip.get("budget_tier"),
            "estimated_total_cost_inr": trip.get("estimated_total_cost"),
            "destinations": [
                {
                    "name": d.get("name"),
                    "city": d.get("city"),
                    "state": d.get("state"),
                    "category": d.get("category"),
                    "religion_tradition": d.get("religion_tradition")
                }
                for d in trip.get("destinations", [])
            ],
            "itinerary_days": [
                {
                    "day": d.get("day_number"),
                    "title": d.get("title"),
                    "date": d.get("date"),
                    "morning": d.get("morning_plan"),
                    "afternoon": d.get("afternoon_plan"),
                    "evening": d.get("evening_plan"),
                    "estimated_day_cost_inr": d.get("estimated_cost")
                }
                for d in trip.get("days", [])
            ],
            "budget_breakdown": trip.get("budget_info", {}).get("breakdown", {}),
            "disclaimer": "Sample estimated prices in INR (₹) for planning purposes. Actual costs may vary by season and vendor."
        }
        return json.dumps(clean_trip, indent=2, ensure_ascii=False)

    @staticmethod
    def export_trip_to_text(trip):
        """Formats trip details into a clean, printable text document."""
        lines = []
        lines.append("=" * 70)
        lines.append(f"YATRA PILGRIMAGE ITINERARY: {trip.get('title', 'Sacred Journey').upper()}")
        lines.append("=" * 70)
        lines.append(f"Duration: {trip.get('total_days')} Days | Travelers: {trip.get('travelers_count')} ({trip.get('traveler_profile', 'family').capitalize()})")
        lines.append(f"Pace: {trip.get('pace', 'balanced').capitalize()} | Budget Tier: {trip.get('budget_tier', 'standard').capitalize()}")
        lines.append(f"Estimated Total: ₹{trip.get('estimated_total_cost', 0):,.2f} INR")
        if trip.get("start_date"):
            lines.append(f"Start Date: {trip.get('start_date')}")
        lines.append("-" * 70)
        lines.append("DESTINATIONS VISITED:")
        for idx, dest in enumerate(trip.get("destinations", []), 1):
            lines.append(f"  {idx}. {dest.get('name')} ({dest.get('city')}, {dest.get('state')})")
        lines.append("-" * 70)
        lines.append("DAY-WISE PILGRIMAGE SCHEDULE:")
        for day in trip.get("days", []):
            lines.append(f"\n[DAY {day.get('day_number')}: {day.get('title')}]")
            if day.get("date"):
                lines.append(f"Date: {day.get('date')}")
            lines.append(f"  • Morning:   {day.get('morning_plan')}")
            lines.append(f"  • Afternoon: {day.get('afternoon_plan')}")
            lines.append(f"  • Evening:   {day.get('evening_plan')}")
            if day.get("estimated_cost"):
                lines.append(f"  • Day Budget: ₹{day.get('estimated_cost'):,.2f}")

        lines.append("\n" + "=" * 70)
        lines.append("SAMPLE BUDGET BREAKDOWN:")
        budget_info = trip.get("budget_info", {})
        breakdown = budget_info.get("breakdown", {})
        for key, item in breakdown.items():
            lines.append(f"  - {item.get('label')}: ₹{item.get('amount', 0):,.2f} ({item.get('note', '')})")
        lines.append("-" * 70)
        lines.append(f"ESTIMATED TOTAL: ₹{trip.get('estimated_total_cost', 0):,.2f} INR")
        lines.append("\nDISCLAIMER: Prices shown are sample estimates in INR (₹) for budgeting purposes.")
        lines.append("Actual costs, darshan queues, and temple access rules may vary by season and trust authorities.")
        lines.append("May your pilgrimage bring supreme peace, harmony, and divine grace.")
        lines.append("=" * 70)

        return "\n".join(lines)
