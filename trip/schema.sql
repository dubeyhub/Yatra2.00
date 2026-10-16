-- Yatra Database Schema
-- Focus: Global Sacred Pilgrimages & Spiritual Journeys

DROP TABLE IF EXISTS bookings;
DROP TABLE IF EXISTS trip_days;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS circuit_destinations;
DROP TABLE IF EXISTS circuits;
DROP TABLE IF EXISTS festivals;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS hotels;
DROP TABLE IF EXISTS religious_site_details;
DROP TABLE IF EXISTS destinations;
DROP TABLE IF EXISTS vehicles;
DROP TABLE IF EXISTS users;

-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name TEXT NOT NULL,
    phone TEXT,
    role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Destinations table
CREATE TABLE destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT NOT NULL,
    country TEXT DEFAULT 'India',
    category TEXT NOT NULL CHECK(category IN ('temple', 'pilgrimage_route', 'sacred_river', 'mosque_dargah', 'church', 'gurudwara', 'monastery', 'heritage_site')),
    religion_tradition TEXT NOT NULL,
    description TEXT NOT NULL,
    history TEXT,
    significance TEXT,
    best_time_to_visit TEXT,
    latitude REAL,
    longitude REAL,
    image_url TEXT,
    verified INTEGER DEFAULT 1
);

-- Specific religious site details, darshan, etiquette, accessibility
CREATE TABLE religious_site_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER UNIQUE NOT NULL,
    opening_hours TEXT NOT NULL,
    morning_aarti_time TEXT,
    evening_aarti_time TEXT,
    darshan_timings TEXT NOT NULL,
    special_darshan_info TEXT,
    entry_fee_info TEXT, -- Sample price details clearly stated
    dress_code TEXT NOT NULL,
    footwear_rules TEXT NOT NULL,
    phone_camera_rules TEXT NOT NULL,
    security_info TEXT,
    non_hindu_entry_rules TEXT,
    wheelchair_accessible INTEGER DEFAULT 0,
    senior_priority_darshan INTEGER DEFAULT 0,
    battery_car_available INTEGER DEFAULT 0,
    walking_distance_meters INTEGER DEFAULT 200,
    medical_facility_nearby INTEGER DEFAULT 1,
    official_booking_url TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations (id) ON DELETE CASCADE
);

-- Pilgrimage circuits (e.g., Char Dham, Braj Bhoomi, Jyotirlinga, Buddhist Circuit, Sangam)
CREATE TABLE circuits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    description TEXT NOT NULL,
    states_covered TEXT NOT NULL,
    total_days_recommended INTEGER NOT NULL,
    theme TEXT NOT NULL,
    image_url TEXT
);

-- Circuit stops mapping
CREATE TABLE circuit_destinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    circuit_id INTEGER NOT NULL,
    destination_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    sequence_order INTEGER NOT NULL,
    notes TEXT,
    FOREIGN KEY (circuit_id) REFERENCES circuits (id) ON DELETE CASCADE,
    FOREIGN KEY (destination_id) REFERENCES destinations (id) ON DELETE CASCADE
);

-- Festivals and seasonal dates
CREATE TABLE festivals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    dated_info_month TEXT NOT NULL,
    typical_dates_range TEXT NOT NULL,
    crowd_level TEXT CHECK(crowd_level IN ('Moderate', 'High', 'Extremely Crowded')),
    key_rituals TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations (id) ON DELETE CASCADE
);

-- Hotels and Dharamshalas
CREATE TABLE hotels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('Dharamshala / Ashram', 'Budget Hotel', 'Standard Hotel', 'Heritage Haveli', 'Luxury Resort')),
    address TEXT NOT NULL,
    contact_phone TEXT,
    price_per_night REAL NOT NULL, -- Sample price in INR
    rating REAL DEFAULT 4.0,
    is_pure_veg INTEGER DEFAULT 1,
    is_senior_friendly INTEGER DEFAULT 1,
    has_wheelchair_ramp INTEGER DEFAULT 0,
    has_lift INTEGER DEFAULT 0,
    proximity_to_temple_km REAL NOT NULL,
    image_url TEXT,
    FOREIGN KEY (destination_id) REFERENCES destinations (id) ON DELETE CASCADE
);

-- Restaurants, Sattvic Dining, Langar, Prasad
CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    destination_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    cuisine_type TEXT NOT NULL CHECK(cuisine_type IN ('Sattvic (No Onion/Garlic)', 'Pure Vegetarian Thali', 'Temple Prasad / Mahaprasad', 'Gurudwara Langar (Seva)', 'Multi-cuisine Veg')),
    avg_cost_for_two REAL NOT NULL, -- Sample price in INR (0 for Langar)
    address TEXT NOT NULL,
    special_dishes TEXT,
    opening_hours TEXT,
    is_sattvic INTEGER DEFAULT 1,
    FOREIGN KEY (destination_id) REFERENCES destinations (id) ON DELETE CASCADE
);

-- Vehicles for pilgrimage and family travel
CREATE TABLE vehicles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_type TEXT NOT NULL,
    capacity INTEGER NOT NULL,
    price_per_day REAL NOT NULL, -- Sample estimated price in INR
    price_per_km REAL NOT NULL,
    driver_allowance_per_day REAL DEFAULT 400.0,
    ac_available INTEGER DEFAULT 1,
    senior_friendly_comfort INTEGER DEFAULT 1,
    features TEXT,
    image_url TEXT
);

-- User planned trips
CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    circuit_id INTEGER,
    destination_ids_json TEXT NOT NULL,
    start_date TEXT,
    total_days INTEGER NOT NULL,
    travelers_count INTEGER DEFAULT 2,
    traveler_profile TEXT CHECK(traveler_profile IN ('solo', 'couple', 'family', 'seniors')),
    pace TEXT CHECK(pace IN ('relaxed', 'balanced', 'active')),
    budget_tier TEXT CHECK(budget_tier IN ('economy', 'standard', 'comfort')),
    estimated_total_cost REAL NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    FOREIGN KEY (circuit_id) REFERENCES circuits (id) ON DELETE SET NULL
);

-- Day-wise plan for multi-day trips
CREATE TABLE trip_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    day_number INTEGER NOT NULL,
    date TEXT,
    title TEXT NOT NULL,
    morning_plan TEXT NOT NULL,
    afternoon_plan TEXT NOT NULL,
    evening_plan TEXT NOT NULL,
    estimated_cost REAL DEFAULT 0.0,
    FOREIGN KEY (trip_id) REFERENCES trips (id) ON DELETE CASCADE
);

-- Bookings table (Hotels, Vehicles, Puja / Darshan assistance)
CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    booking_type TEXT NOT NULL CHECK(booking_type IN ('hotel', 'vehicle', 'puja_darshan_assistance')),
    reference_id INTEGER NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    guests_count INTEGER DEFAULT 1,
    total_amount REAL NOT NULL, -- Sample estimated price
    status TEXT DEFAULT 'confirmed' CHECK(status IN ('confirmed', 'pending', 'cancelled')),
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
