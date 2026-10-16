from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from services.vehicle_service import VehicleService
from services.location_service import LocationService
from routes.auth import login_required
from config import Config
from db import get_db

vehicles_bp = Blueprint('vehicles', __name__)

@vehicles_bp.route('/vehicles')
def list_vehicles():
    vehicles = VehicleService.get_all_vehicles()
    return render_template('vehicles.html', vehicles=vehicles, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

@vehicles_bp.route('/vehicles/booking/<int:vehicle_id>', methods=['GET'])
def vehicle_booking(vehicle_id):
    vehicle = VehicleService.get_vehicle_by_id(vehicle_id)
    if not vehicle:
        abort(404)
    circuits = LocationService.get_all_circuits()
    destinations = LocationService.get_all_destinations()
    return render_template(
        'vehicle_booking.html',
        vehicle=vehicle,
        circuits=circuits,
        destinations=destinations,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@vehicles_bp.route('/vehicles/calculate-cost', methods=['POST'])
def calculate_cost():
    vehicle_id = request.form.get('vehicle_id', type=int)
    days = request.form.get('days', 1, type=int)
    cost_info = VehicleService.calculate_vehicle_cost(vehicle_id, days)
    return cost_info
