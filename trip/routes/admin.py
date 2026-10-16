from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from routes.auth import admin_required
from db import get_db
from config import Config

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/')
@admin_required
def dashboard():
    db = get_db()
    total_destinations = db.execute("SELECT COUNT(*) FROM destinations").fetchone()[0]
    total_hotels = db.execute("SELECT COUNT(*) FROM hotels").fetchone()[0]
    total_restaurants = db.execute("SELECT COUNT(*) FROM restaurants").fetchone()[0]
    total_bookings = db.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
    total_users = db.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_trips = db.execute("SELECT COUNT(*) FROM trips").fetchone()[0]

    recent_bookings = db.execute(
        """
        SELECT b.*, u.full_name as user_name, u.email as user_email
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
        LIMIT 8
        """
    ).fetchall()

    return render_template(
        'admin/dashboard.html',
        stats={
            'destinations': total_destinations,
            'hotels': total_hotels,
            'restaurants': total_restaurants,
            'bookings': total_bookings,
            'users': total_users,
            'trips': total_trips
        },
        recent_bookings=[dict(r) for r in recent_bookings]
    )

@admin_bp.route('/destinations')
@admin_required
def manage_destinations():
    db = get_db()
    rows = db.execute("SELECT * FROM destinations ORDER BY state, name").fetchall()
    return render_template('admin/manage_destinations.html', destinations=[dict(r) for r in rows], states=Config.FOCUS_STATES, categories=Config.DESTINATION_CATEGORIES)

@admin_bp.route('/destinations/new', methods=['GET', 'POST'])
@admin_required
def create_destination():
    db = get_db()
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country') or 'India'
        category = request.form.get('category')
        religion = request.form.get('religion_tradition')
        desc = request.form.get('description')
        history = request.form.get('history', '')
        significance = request.form.get('significance', '')
        best_time = request.form.get('best_time_to_visit', '')
        lat = request.form.get('latitude', type=float) or 0.0
        lng = request.form.get('longitude', type=float) or 0.0
        image_url = request.form.get('image_url', '')

        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO destinations (name, city, state, country, category, religion_tradition, description, history, significance, best_time_to_visit, latitude, longitude, image_url, verified)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
            """,
            (name, city, state, country, category, religion, desc, history, significance, best_time, lat, lng, image_url)
        )
        dest_id = cursor.lastrowid

        # Insert default religious site details
        cursor.execute(
            """
            INSERT INTO religious_site_details (
                destination_id, opening_hours, morning_aarti_time, evening_aarti_time,
                darshan_timings, special_darshan_info, entry_fee_info, dress_code,
                footwear_rules, phone_camera_rules, security_info, non_hindu_entry_rules,
                wheelchair_accessible, senior_priority_darshan, battery_car_available,
                walking_distance_meters, medical_facility_nearby, official_booking_url
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                dest_id,
                request.form.get('opening_hours', '06:00 AM - 09:00 PM'),
                request.form.get('morning_aarti_time', '06:00 AM'),
                request.form.get('evening_aarti_time', '07:00 PM'),
                request.form.get('darshan_timings', '06:30 AM - 08:30 PM'),
                request.form.get('special_darshan_info', 'Senior citizen queue available'),
                request.form.get('entry_fee_info', 'Entry is Free. Sample Prasad Box: ₹50 - ₹100.'),
                request.form.get('dress_code', 'Modest traditional Indian clothing'),
                request.form.get('footwear_rules', 'Deposit shoes at temple shoe counter'),
                request.form.get('phone_camera_rules', 'Prohibited inside sanctum; lockers available'),
                request.form.get('security_info', 'Metal detector and physical inspection'),
                request.form.get('non_hindu_entry_rules', 'Devotees of all peaceful traditions welcomed'),
                1 if request.form.get('wheelchair_accessible') else 0,
                1 if request.form.get('senior_priority_darshan') else 0,
                1 if request.form.get('battery_car_available') else 0,
                request.form.get('walking_distance_meters', 150, type=int),
                1 if request.form.get('medical_facility_nearby') else 0,
                request.form.get('official_booking_url', '')
            )
        )
        db.commit()
        flash(f"Destination '{name}' created successfully!", "success")
        return redirect(url_for('admin.manage_destinations'))

    return render_template('admin/edit_destination.html', destination=None, countries=Config.FOCUS_COUNTRIES, states=Config.FOCUS_STATES, categories=Config.DESTINATION_CATEGORIES, religions=Config.RELIGIOUS_TRADITIONS)

@admin_bp.route('/destinations/<int:dest_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_destination(dest_id):
    db = get_db()
    dest = db.execute(
        """
        SELECT d.*, rsd.*
        FROM destinations d
        LEFT JOIN religious_site_details rsd ON d.id = rsd.destination_id
        WHERE d.id = ?
        """,
        (dest_id,)
    ).fetchone()

    if not dest:
        abort(404)

    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country') or 'India'
        category = request.form.get('category')
        religion = request.form.get('religion_tradition')
        desc = request.form.get('description')
        history = request.form.get('history', '')
        significance = request.form.get('significance', '')
        best_time = request.form.get('best_time_to_visit', '')
        lat = request.form.get('latitude', type=float) or 0.0
        lng = request.form.get('longitude', type=float) or 0.0
        image_url = request.form.get('image_url', '')
        verified = 1 if request.form.get('verified') else 0

        db.execute(
            """
            UPDATE destinations
            SET name = ?, city = ?, state = ?, country = ?, category = ?, religion_tradition = ?,
                description = ?, history = ?, significance = ?, best_time_to_visit = ?,
                latitude = ?, longitude = ?, image_url = ?, verified = ?
            WHERE id = ?
            """,
            (name, city, state, country, category, religion, desc, history, significance, best_time, lat, lng, image_url, verified, dest_id)
        )

        db.execute(
            """
            UPDATE religious_site_details
            SET opening_hours = ?, morning_aarti_time = ?, evening_aarti_time = ?,
                darshan_timings = ?, special_darshan_info = ?, entry_fee_info = ?,
                dress_code = ?, footwear_rules = ?, phone_camera_rules = ?,
                security_info = ?, non_hindu_entry_rules = ?, wheelchair_accessible = ?,
                senior_priority_darshan = ?, battery_car_available = ?, walking_distance_meters = ?,
                medical_facility_nearby = ?, official_booking_url = ?
            WHERE destination_id = ?
            """,
            (
                request.form.get('opening_hours'),
                request.form.get('morning_aarti_time'),
                request.form.get('evening_aarti_time'),
                request.form.get('darshan_timings'),
                request.form.get('special_darshan_info'),
                request.form.get('entry_fee_info'),
                request.form.get('dress_code'),
                request.form.get('footwear_rules'),
                request.form.get('phone_camera_rules'),
                request.form.get('security_info'),
                request.form.get('non_hindu_entry_rules'),
                1 if request.form.get('wheelchair_accessible') else 0,
                1 if request.form.get('senior_priority_darshan') else 0,
                1 if request.form.get('battery_car_available') else 0,
                request.form.get('walking_distance_meters', 150, type=int),
                1 if request.form.get('medical_facility_nearby') else 0,
                request.form.get('official_booking_url'),
                dest_id
            )
        )
        db.commit()
        flash(f"Destination '{name}' updated successfully!", "success")
        return redirect(url_for('admin.manage_destinations'))

    return render_template('admin/edit_destination.html', destination=dict(dest), countries=Config.FOCUS_COUNTRIES, states=Config.FOCUS_STATES, categories=Config.DESTINATION_CATEGORIES, religions=Config.RELIGIOUS_TRADITIONS)

@admin_bp.route('/destinations/<int:dest_id>/delete', methods=['POST'])
@admin_required
def delete_destination(dest_id):
    db = get_db()
    db.execute("DELETE FROM destinations WHERE id = ?", (dest_id,))
    db.commit()
    flash("Destination deleted.", "info")
    return redirect(url_for('admin.manage_destinations'))

@admin_bp.route('/bookings')
@admin_required
def manage_bookings():
    db = get_db()
    rows = db.execute(
        """
        SELECT b.*, u.full_name as user_name, u.email as user_email, u.phone as user_phone
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        ORDER BY b.created_at DESC
        """
    ).fetchall()
    return render_template('admin/manage_bookings.html', bookings=[dict(r) for r in rows])

@admin_bp.route('/bookings/<int:booking_id>/update-status', methods=['POST'])
@admin_required
def update_booking_status(booking_id):
    status = request.form.get('status')
    if status in ['confirmed', 'pending', 'cancelled']:
        db = get_db()
        db.execute("UPDATE bookings SET status = ? WHERE id = ?", (status, booking_id))
        db.commit()
        flash(f"Booking #{booking_id} status updated to {status}.", "success")
    return redirect(url_for('admin.manage_bookings'))
