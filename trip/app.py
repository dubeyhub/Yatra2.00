import os
from flask import Flask, render_template, session, g
from config import Config
import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    from routes.auth import auth_bp
    from routes.destinations import destinations_bp
    from routes.hotels import hotels_bp
    from routes.restaurants import restaurants_bp
    from routes.vehicles import vehicles_bp
    from routes.trips import trips_bp
    from routes.bookings import bookings_bp
    from routes.admin import admin_bp
    from routes.chatbot import chatbot_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(destinations_bp)
    app.register_blueprint(hotels_bp)
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(trips_bp)
    app.register_blueprint(bookings_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chatbot_bp)

    # Context processor to inject global variables into templates
    @app.context_processor
    def inject_globals():
        current_user = None
        if 'user_id' in session:
            current_user = {
                'id': session.get('user_id'),
                'username': session.get('username'),
                'full_name': session.get('full_name'),
                'role': session.get('role')
            }
        return {
            'current_user': current_user,
            'app_name': Config.APP_NAME,
            'tagline': Config.TAGLINE,
            'currency_symbol': Config.CURRENCY_SYMBOL,
            'focus_countries': Config.FOCUS_COUNTRIES,
            'focus_states': Config.FOCUS_STATES,
            'categories': Config.DESTINATION_CATEGORIES,
            'religions': Config.RELIGIOUS_TRADITIONS,
            'sample_price_disclaimer': Config.SAMPLE_PRICE_DISCLAIMER
        }

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
