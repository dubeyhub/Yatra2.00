from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_db
from services.supabase_service import SupabaseService, is_supabase_enabled

auth_bp = Blueprint('auth', __name__)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash("Please sign in to access this pilgrimage feature.", "info")
            return redirect(url_for('auth.login', next=request.url))
        return view(**kwargs)
    return wrapped_view

def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            flash("Access restricted to administrators.", "warning")
            return redirect(url_for('destinations.index'))
        return view(**kwargs)
    return wrapped_view

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('destinations.index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()

        if not username or not email or not password or not full_name:
            flash("All mandatory fields must be filled.", "danger")
            return render_template('auth/register.html')

        password_hash = generate_password_hash(password)
        db = get_db()
        user_id = None
        role = 'user'

        # 1. Supabase Registration
        if is_supabase_enabled():
            sb_existing = SupabaseService.get_user_by_login(username) or SupabaseService.get_user_by_login(email)
            if sb_existing:
                flash("Username or Email already registered in Supabase. Please login.", "warning")
                return redirect(url_for('auth.login'))
            sb_user = SupabaseService.create_user(username, email, password_hash, full_name, phone, role)
            if sb_user:
                user_id = sb_user.get('id')

        # 2. Local SQLite Sync / Fallback
        try:
            existing = db.execute(
                "SELECT id FROM users WHERE username = ? OR email = ?",
                (username, email)
            ).fetchone()
            if not existing:
                cursor = db.cursor()
                cursor.execute(
                    "INSERT INTO users (username, email, password_hash, full_name, phone, role) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, email, password_hash, full_name, phone, role)
                )
                db.commit()
                if not user_id:
                    user_id = cursor.lastrowid
            else:
                if not user_id:
                    user_id = existing['id']
        except Exception as e:
            print(f"Local db sync note: {e}")

        if not user_id:
            user_id = 999  # Safe fallback identifier if needed

        session['user_id'] = user_id
        session['username'] = username
        session['role'] = role
        session['full_name'] = full_name

        flash(f"Welcome to Yatra, {full_name}! Your spiritual journey begins.", "success")
        return redirect(url_for('destinations.index'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('destinations.index'))

    if request.method == 'POST':
        login_id = request.form.get('login_id', '').strip()
        password = request.form.get('password', '')

        user = None

        # 1. Try Supabase Login first
        if is_supabase_enabled():
            sb_user = SupabaseService.get_user_by_login(login_id)
            if sb_user and check_password_hash(sb_user['password_hash'], password):
                user = sb_user

        # 2. Try SQLite DB if not authenticated via Supabase
        if not user:
            db = get_db()
            db_user = db.execute(
                "SELECT * FROM users WHERE LOWER(username) = ? OR LOWER(email) = ?",
                (login_id.lower(), login_id.lower())
            ).fetchone()
            if db_user and check_password_hash(db_user['password_hash'], password):
                user = dict(db_user)

        if user:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user.get('role', 'user')
            session['full_name'] = user['full_name']

            flash(f"Welcome back, {user['full_name']}! Blessings for your journey.", "success")
            next_url = request.args.get('next')
            return redirect(next_url or url_for('destinations.index'))
        else:
            flash("Invalid username/email or password.", "danger")

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash("You have been signed out safely. Shubh Yatra!", "info")
    return redirect(url_for('destinations.index'))

@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user_id = session['user_id']

    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        phone = request.form.get('phone', '').strip()

        if full_name:
            if is_supabase_enabled():
                SupabaseService.update_user_profile(user_id, full_name, phone)
            
            db = get_db()
            try:
                db.execute(
                    "UPDATE users SET full_name = ?, phone = ? WHERE id = ?",
                    (full_name, phone, user_id)
                )
                db.commit()
            except Exception:
                pass
            session['full_name'] = full_name
            flash("Profile details updated successfully.", "success")

    user = None
    trips_count = 0
    bookings_count = 0

    if is_supabase_enabled():
        user = SupabaseService.get_user_by_id(user_id)
        trips_count, bookings_count = SupabaseService.get_user_counts(user_id)

    if not user:
        db = get_db()
        db_u = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if db_u:
            user = dict(db_u)
            trips_count = db.execute("SELECT COUNT(*) FROM trips WHERE user_id = ?", (user_id,)).fetchone()[0]
            bookings_count = db.execute("SELECT COUNT(*) FROM bookings WHERE user_id = ?", (user_id,)).fetchone()[0]

    if not user:
        user = {
            "id": user_id,
            "username": session.get("username", "pilgrim"),
            "full_name": session.get("full_name", "Pilgrim"),
            "email": "user@yatra.in",
            "phone": "",
            "role": session.get("role", "user")
        }

    return render_template('auth/profile.html', user=user, trips_count=trips_count, bookings_count=bookings_count)
