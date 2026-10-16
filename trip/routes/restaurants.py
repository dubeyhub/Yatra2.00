from flask import Blueprint, render_template, request
from services.restaurant_service import RestaurantService
from services.location_service import LocationService
from config import Config

restaurants_bp = Blueprint('restaurants', __name__)

@restaurants_bp.route('/restaurants')
def list_restaurants():
    destination_id = request.args.get('destination_id')
    state = request.args.get('state')
    cuisine_type = request.args.get('cuisine_type')
    is_sattvic = request.args.get('is_sattvic')
    search = request.args.get('search')

    filters = {
        'destination_id': destination_id,
        'state': state,
        'cuisine_type': cuisine_type,
        'is_sattvic': is_sattvic,
        'search': search
    }

    restaurants = RestaurantService.get_restaurants(filters)
    destinations = LocationService.get_all_destinations()

    return render_template(
        'restaurants.html',
        restaurants=restaurants,
        filters=filters,
        destinations=destinations,
        states=Config.FOCUS_STATES,
        disclaimer=Config.SAMPLE_PRICE_DISCLAIMER
    )
