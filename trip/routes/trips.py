import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, Response, abort
from services.location_service import LocationService
from services.itinerary_service import ItineraryService
from services.budget_service import BudgetService
from services.export_service import ExportService
from services.vehicle_service import VehicleService
from routes.auth import login_required
from config import Config

trips_bp = Blueprint('trips', __name__)

@trips_bp.route('/planner', methods=['GET', 'POST'])
def planner():
    destinations = LocationService.get_all_destinations()
    circuits = LocationService.get_all_circuits()
    vehicles = VehicleService.get_all_vehicles()

    circuit_id = request.args.get('circuit_id', type=int)
    preset_circuit = None
    if circuit_id:
        preset_circuit = LocationService.get_circuit_by_slug_or_id(circuit_id)

    generated_itinerary = None

    if request.method == 'POST':
        selected_dest_ids = request.form.getlist('destination_ids', type=int)
        circuit_selected = request.form.get('circuit_id', type=int)
        total_days = request.form.get('total_days', 3, type=int)
        travelers_count = request.form.get('travelers_count', 2, type=int)
        traveler_profile = request.form.get('traveler_profile', 'family')
        pace = request.form.get('pace', 'balanced')
        budget_tier = request.form.get('budget_tier', 'standard')
        start_date = request.form.get('start_date')

        # If a circuit was chosen and no destinations manually checked, pull circuit destinations
        if circuit_selected and not selected_dest_ids:
            circ = LocationService.get_circuit_by_slug_or_id(circuit_selected)
            if circ and 'stops' in circ:
                selected_dest_ids = [s['destination_id'] for s in circ['stops']]

        if not selected_dest_ids:
            flash("Please select at least one sacred destination or circuit for your pilgrimage.", "warning")
            return redirect(url_for('trips.planner'))

        selected_dests = LocationService.get_destinations_by_ids(selected_dest_ids)
        generated_itinerary = ItineraryService.generate_itinerary(
            destinations=selected_dests,
            total_days=total_days,
            travelers_count=travelers_count,
            traveler_profile=traveler_profile,
            pace=pace,
            budget_tier=budget_tier,
            start_date=start_date
        )
        generated_itinerary['circuit_id'] = circuit_selected

    return render_template(
        'planner.html',
        destinations=destinations,
        circuits=circuits,
        vehicles=vehicles,
        preset_circuit=preset_circuit,
        generated_itinerary=generated_itinerary,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@trips_bp.route('/trips/save', methods=['POST'])
@login_required
def save_trip():
    user_id = session['user_id']
    title = request.form.get('title', 'My Sacred Pilgrimage')
    circuit_id = request.form.get('circuit_id', type=int) or None
    destination_ids = request.form.getlist('destination_ids', type=int)
    total_days = request.form.get('total_days', 3, type=int)
    travelers_count = request.form.get('travelers_count', 2, type=int)
    traveler_profile = request.form.get('traveler_profile', 'family')
    pace = request.form.get('pace', 'balanced')
    budget_tier = request.form.get('budget_tier', 'standard')
    start_date = request.form.get('start_date')
    notes = request.form.get('notes', '')

    days_plan_json = request.form.get('days_plan_json')
    if days_plan_json:
        try:
            days_plan = json.loads(days_plan_json)
        except Exception:
            days_plan = []
    else:
        # Re-generate if not passed as json
        selected_dests = LocationService.get_destinations_by_ids(destination_ids)
        gen = ItineraryService.generate_itinerary(
            destinations=selected_dests,
            total_days=total_days,
            travelers_count=travelers_count,
            traveler_profile=traveler_profile,
            pace=pace,
            budget_tier=budget_tier,
            start_date=start_date
        )
        days_plan = gen.get('days', [])

    estimated_total_cost = request.form.get('estimated_total_cost', 0.0, type=float)
    if not estimated_total_cost and days_plan:
        budget = BudgetService.calculate_budget(
            destination_ids=destination_ids,
            total_days=total_days,
            travelers_count=travelers_count,
            budget_tier=budget_tier,
            traveler_profile=traveler_profile
        )
        estimated_total_cost = budget['grand_total']

    trip_id = ItineraryService.save_trip(
        user_id=user_id,
        title=title,
        destination_ids=destination_ids,
        total_days=total_days,
        travelers_count=travelers_count,
        traveler_profile=traveler_profile,
        pace=pace,
        budget_tier=budget_tier,
        estimated_total_cost=estimated_total_cost,
        days_plan=days_plan,
        circuit_id=circuit_id,
        start_date=start_date,
        notes=notes
    )

    flash("Your sacred pilgrimage itinerary has been saved successfully!", "success")
    return redirect(url_for('trips.trip_summary', trip_id=trip_id))

@trips_bp.route('/my-trips')
@login_required
def my_trips():
    user_id = session['user_id']
    trips = ItineraryService.get_user_trips(user_id)
    return render_template('my_trips.html', trips=trips, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

@trips_bp.route('/trips/<int:trip_id>')
def trip_summary(trip_id):
    user_id = session.get('user_id')
    trip = ItineraryService.get_trip_details(trip_id)
    if not trip:
        abort(404)
    return render_template('trip_summary.html', trip=trip, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

@trips_bp.route('/trips/<int:trip_id>/export/json')
def export_json(trip_id):
    trip = ItineraryService.get_trip_details(trip_id)
    if not trip:
        abort(404)
    json_data = ExportService.export_trip_to_json(trip)
    return Response(
        json_data,
        mimetype="application/json",
        headers={"Content-disposition": f"attachment; filename=Yatra_Trip_{trip_id}.json"}
    )

@trips_bp.route('/trips/<int:trip_id>/export/text')
def export_text(trip_id):
    trip = ItineraryService.get_trip_details(trip_id)
    if not trip:
        abort(404)
    text_data = ExportService.export_trip_to_text(trip)
    return Response(
        text_data,
        mimetype="text/plain; charset=utf-8",
        headers={"Content-disposition": f"attachment; filename=Yatra_Trip_{trip_id}.txt"}
    )

@trips_bp.route('/trips/<int:trip_id>/delete', methods=['POST'])
@login_required
def delete_trip(trip_id):
    user_id = session['user_id']
    success = ItineraryService.delete_trip(trip_id, user_id)
    if success:
        flash("Pilgrimage itinerary deleted.", "info")
    else:
        flash("Could not delete itinerary.", "danger")
    return redirect(url_for('trips.my_trips'))

@trips_bp.route('/budget', methods=['GET'])
def budget():
    destinations = LocationService.get_all_destinations()
    vehicles = VehicleService.get_all_vehicles()
    return render_template(
        'budget.html',
        destinations=destinations,
        vehicles=vehicles,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@trips_bp.route('/api/budget/calculate', methods=['POST'])
def api_calculate_budget():
    data = request.get_json() or {}
    dest_ids = data.get('destination_ids', [])
    total_days = int(data.get('total_days', 3))
    travelers_count = int(data.get('travelers_count', 2))
    budget_tier = data.get('budget_tier', 'standard')
    traveler_profile = data.get('traveler_profile', 'family')
    vehicle_id = data.get('vehicle_id')
    if vehicle_id:
        vehicle_id = int(vehicle_id)

    res = BudgetService.calculate_budget(
        destination_ids=dest_ids,
        total_days=total_days,
        travelers_count=travelers_count,
        budget_tier=budget_tier,
        traveler_profile=traveler_profile,
        vehicle_id=vehicle_id
    )
    return jsonify(res)
