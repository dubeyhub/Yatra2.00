from db import get_db

def test_create_and_manage_booking(client, auth_client, app):
    with app.app_context():
        # Create hotel booking via route
        res = auth_client.post('/bookings/create', data={
            'booking_type': 'hotel',
            'reference_id': 1,
            'start_date': '2026-11-15',
            'end_date': '2026-11-18',
            'guests_count': 2,
            'total_amount': 2550.0,
            'special_requests': 'Ground floor room preferred for senior parents.'
        }, follow_redirects=True)

        assert res.status_code == 200
        assert b"Your sacred booking request has been confirmed" in res.data
        assert b"Ground floor room preferred" in res.data

        # Check in DB
        db = get_db()
        booking = db.execute("SELECT * FROM bookings WHERE special_requests LIKE '%Ground floor%'").fetchone()
        assert booking is not None
        assert booking['status'] == 'confirmed'

        # Cancel booking
        res_cancel = auth_client.post(f'/bookings/{booking["id"]}/cancel', follow_redirects=True)
        assert res_cancel.status_code == 200
        assert b"Booking has been cancelled" in res_cancel.data

        # Verify status in DB
        db.commit()
        updated = db.execute("SELECT status FROM bookings WHERE id = ?", (booking['id'],)).fetchone()
        assert updated['status'] == 'cancelled'
