from flask import Blueprint, render_template, request, abort
from services.hotel_service import HotelService
from services.location_service import LocationService
from config import Config

hotels_bp = Blueprint('hotels', __name__)

@hotels_bp.route('/hotels')
def list_hotels():
    destination_id = request.args.get('destination_id')
    state = request.args.get('state')
    hotel_type = request.args.get('type')
    is_pure_veg = request.args.get('is_pure_veg')
    is_senior_friendly = request.args.get('is_senior_friendly')
    max_price = request.args.get('max_price')
    sort_by = request.args.get('sort_by')

    filters = {
        'destination_id': destination_id,
        'state': state,
        'type': hotel_type,
        'is_pure_veg': is_pure_veg,
        'is_senior_friendly': is_senior_friendly,
        'max_price': max_price,
        'sort_by': sort_by
    }

    hotels = HotelService.get_hotels(filters)
    destinations = LocationService.get_all_destinations()

    return render_template(
        'hotels.html',
        hotels=hotels,
        filters=filters,
        destinations=destinations,
        states=Config.FOCUS_STATES,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )

@hotels_bp.route('/hotels/<int:hotel_id>')
def hotel_details(hotel_id):
    hotel = HotelService.get_hotel_by_id(hotel_id)
    if not hotel:
        abort(404)
    return render_template('hotel_details.html', hotel=hotel, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)
