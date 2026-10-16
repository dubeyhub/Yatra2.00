from flask import Blueprint, render_template, request, jsonify, abort
from services.location_service import LocationService
from services.hotel_service import HotelService
from services.restaurant_service import RestaurantService
from config import Config

destinations_bp = Blueprint('destinations', __name__)

@destinations_bp.route('/')
def index():
    featured_destinations = LocationService.get_featured_destinations(6)
    circuits = LocationService.get_all_circuits()
    festivals = LocationService.get_festivals()[:4]
    stats = LocationService.get_stats()
    return render_template(
        'index.html',
        featured_destinations=featured_destinations,
        circuits=circuits,
        festivals=festivals,
        stats=stats,
        countries=Config.FOCUS_COUNTRIES,
        states=Config.FOCUS_STATES,
        categories=Config.DESTINATION_CATEGORIES
    )

@destinations_bp.route('/destinations')
def list_destinations():
    country = request.args.get('country')
    state = request.args.get('state')
    category = request.args.get('category')
    religion = request.args.get('religion')
    search = request.args.get('search')
    wheelchair = request.args.get('wheelchair')
    senior_friendly = request.args.get('senior_friendly')

    filters = {
        'country': country,
        'state': state,
        'category': category,
        'religion': religion,
        'search': search,
        'wheelchair': wheelchair,
        'senior_friendly': senior_friendly
    }

    destinations = LocationService.get_all_destinations(filters)

    return render_template(
        'destinations.html',
        destinations=destinations,
        filters=filters,
        countries=Config.FOCUS_COUNTRIES,
        states=Config.FOCUS_STATES,
        categories=Config.DESTINATION_CATEGORIES,
        religions=Config.RELIGIOUS_TRADITIONS,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@destinations_bp.route('/destinations/<int:dest_id>')
def destination_detail(dest_id):
    destination = LocationService.get_destination_by_id(dest_id)
    if not destination:
        abort(404)

    hotels = HotelService.get_hotels({'destination_id': dest_id})
    restaurants = RestaurantService.get_restaurants({'destination_id': dest_id})
    festivals = LocationService.get_festivals(destination_id=dest_id)

    return render_template(
        'destination_detail.html',
        destination=destination,
        hotels=hotels,
        restaurants=restaurants,
        festivals=festivals,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@destinations_bp.route('/circuits')
def circuits():
    all_circuits = LocationService.get_all_circuits()
    return render_template('circuits.html', circuits=all_circuits)

@destinations_bp.route('/circuits/<identifier>')
def circuit_detail(identifier):
    circuit = LocationService.get_circuit_by_slug_or_id(identifier)
    if not circuit:
        abort(404)
    return render_template('circuit_detail.html', circuit=circuit, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

@destinations_bp.route('/festivals')
def festivals():
    month = request.args.get('month')
    all_festivals = LocationService.get_festivals(month=month)
    return render_template('festivals.html', festivals=all_festivals, selected_month=month)

@destinations_bp.route('/map')
def map_view():
    return render_template(
        'map.html',
        countries=Config.FOCUS_COUNTRIES,
        states=Config.FOCUS_STATES,
        categories=Config.DESTINATION_CATEGORIES,
        religions=Config.RELIGIOUS_TRADITIONS
    )

@destinations_bp.route('/api/destinations')
def api_destinations():
    country = request.args.get('country')
    state = request.args.get('state')
    category = request.args.get('category')
    religion = request.args.get('religion')
    search = request.args.get('search')
    wheelchair = request.args.get('wheelchair')
    senior_friendly = request.args.get('senior_friendly')

    filters = {
        'country': country,
        'state': state,
        'category': category,
        'religion': religion,
        'search': search,
        'wheelchair': wheelchair,
        'senior_friendly': senior_friendly
    }
    destinations = LocationService.get_all_destinations(filters)
    return jsonify(destinations)
