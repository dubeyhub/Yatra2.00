from services.budget_service import BudgetService

def test_budget_calculation_standard_tier(app):
    with app.app_context():
        res = BudgetService.calculate_budget(
            destination_ids=[1, 2],
            total_days=3,
            travelers_count=2,
            budget_tier="standard",
            traveler_profile="family"
        )
        assert res is not None
        assert res["total_days"] == 3
        assert res["travelers_count"] == 2
        assert res["grand_total"] > 0
        assert res["per_person_cost"] == round(res["grand_total"] / 2, 2)
        assert "accommodation" in res["breakdown"]
        assert "food" in res["breakdown"]
        assert "transport" in res["breakdown"]
        assert "darshan_pooja" in res["breakdown"]
        assert "emergency_buffer" in res["breakdown"]
        assert "disclaimer" in res

def test_budget_senior_profile_extras(app):
    with app.app_context():
        res_family = BudgetService.calculate_budget(
            destination_ids=[1],
            total_days=2,
            travelers_count=2,
            budget_tier="standard",
            traveler_profile="family"
        )
        res_seniors = BudgetService.calculate_budget(
            destination_ids=[1],
            total_days=2,
            travelers_count=2,
            budget_tier="standard",
            traveler_profile="seniors"
        )
        # Senior profile includes battery car & accessibility extras
        assert res_seniors["breakdown"]["accessibility_misc"]["amount"] > res_family["breakdown"]["accessibility_misc"]["amount"]

def test_budget_tiers_scaling(app):
    with app.app_context():
        econ = BudgetService.calculate_budget([1], 3, 2, "economy", "family")
        stand = BudgetService.calculate_budget([1], 3, 2, "standard", "family")
        comf = BudgetService.calculate_budget([1], 3, 2, "comfort", "family")

        assert econ["grand_total"] < stand["grand_total"] < comf["grand_total"]

def test_budget_with_vehicle(app):
    with app.app_context():
        res = BudgetService.calculate_budget(
            destination_ids=[1, 2],
            total_days=3,
            travelers_count=4,
            budget_tier="standard",
            vehicle_id=2 # Innova Crysta
        )
        assert res["breakdown"]["transport"]["amount"] > 0
        assert "Innova" in res["breakdown"]["transport"]["note"]
