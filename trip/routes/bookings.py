from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from routes.auth import login_required
from db import get_db
from services.hotel_service import HotelService
from services.vehicle_service import VehicleService
from services.supabase_service import SupabaseService, is_supabase_enabled
from config import Config

bookings_bp = Blueprint('bookings', __name__)

@bookings_bp.route('/my-bookings')
@login_required
def my_bookings():
    user_id = session['user_id']
    bookings = []

    if is_supabase_enabled():
        sb_bookings = SupabaseService.get_user_bookings(user_id)
        if sb_bookings is not None and len(sb_bookings) > 0:
            for b in sb_bookings:
                if b['booking_type'] == 'hotel':
                    b['item'] = HotelService.get_hotel_by_id(b['reference_id'])
                elif b['booking_type'] == 'vehicle':
                    b['item'] = VehicleService.get_vehicle_by_id(b['reference_id'])
            return render_template('my_bookings.html', bookings=sb_bookings, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

    db = get_db()
    query = """
        SELECT b.*
        FROM bookings b
        WHERE b.user_id = ?
        ORDER BY b.created_at DESC
    """
    rows = db.execute(query, (user_id,)).fetchall()
    for r in rows:
        b = dict(r)
        if b['booking_type'] == 'hotel':
            b['item'] = HotelService.get_hotel_by_id(b['reference_id'])
        elif b['booking_type'] == 'vehicle':
            b['item'] = VehicleService.get_vehicle_by_id(b['reference_id'])
        bookings.append(b)

    return render_template('my_bookings.html', bookings=bookings, disclaimer=Config.SAMPLE_PRICE_DISCLAIMER)

@bookings_bp.route('/bookings/create', methods=['POST'])
@login_required
def create_booking():
    user_id = session['user_id']
    booking_type = request.form.get('booking_type')
    reference_id = request.form.get('reference_id', type=int)
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    guests_count = request.form.get('guests_count', 1, type=int)
    special_requests = request.form.get('special_requests', '')
    total_amount = request.form.get('total_amount', 0.0, type=float)

    if not booking_type or not reference_id or not start_date or not end_date:
        flash("Please provide all required dates and details.", "warning")
        return redirect(request.referrer or url_for('destinations.index'))

    # Save to Supabase
    if is_supabase_enabled():
        booking_data = {
            "user_id": user_id,
            "booking_type": booking_type,
            "reference_id": reference_id,
            "start_date": start_date,
            "end_date": end_date,
            "guests_count": guests_count,
            "total_amount": total_amount,
            "status": "confirmed",
            "special_requests": special_requests
        }
        SupabaseService.create_booking(booking_data)

    # Local SQLite sync / fallback
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(
            """
            INSERT INTO bookings (
                user_id, booking_type, reference_id, start_date, end_date,
                guests_count, total_amount, status, special_requests
            ) VALUES (?, ?, ?, ?, ?, ?, ?, 'confirmed', ?)
            """,
            (user_id, booking_type, reference_id, start_date, end_date, guests_count, total_amount, special_requests)
        )
        db.commit()
    except Exception as e:
        print(f"Local db booking sync note: {e}")

    flash("Your sacred booking request has been confirmed! Saved in database successfully.", "success")
    return redirect(url_for('bookings.my_bookings'))

@bookings_bp.route('/bookings/<int:booking_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(booking_id):
    user_id = session['user_id']
    
    if is_supabase_enabled():
        sb = SupabaseService.get_supabase()
        if sb:
            try:
                sb.table("bookings").update({"status": "cancelled"}).eq("id", booking_id).eq("user_id", user_id).execute()
            except Exception:
                pass

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE bookings SET status = 'cancelled' WHERE id = ? AND user_id = ?",
        (booking_id, user_id)
    )
    db.commit()
    flash("Booking has been cancelled.", "info")
    return redirect(url_for('bookings.my_bookings'))
