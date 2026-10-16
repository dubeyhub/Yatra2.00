-- ====================================================================
-- TravelTales: Remaining Tables & Seeds for Supabase
-- Run this in Supabase -> SQL Editor -> New Query -> Run
-- (users, destinations, and religious_site_details are already created and live)
-- ====================================================================

-- 1. DROP REMAINING TABLES IN SAFE ORDER IF EXIST
DROP TABLE IF EXISTS bookings CASCADE;
DROP TABLE IF EXISTS trip_days CASCADE;
DROP TABLE IF EXISTS trips CASCADE;
DROP TABLE IF EXISTS circuit_destinations CASCADE;
DROP TABLE IF EXISTS circuits CASCADE;
DROP TABLE IF EXISTS festivals CASCADE;
DROP TABLE IF EXISTS restaurants CASCADE;
DROP TABLE IF EXISTS hotels CASCADE;
DROP TABLE IF EXISTS vehicles CASCADE;

-- 2. CREATE TABLES
CREATE TABLE circuits (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    states_covered VARCHAR(255) NOT NULL,
    total_days_recommended INT NOT NULL,
    theme VARCHAR(150) NOT NULL,
    image_url TEXT
);

CREATE TABLE circuit_destinations (
    id SERIAL PRIMARY KEY,
    circuit_id INT NOT NULL REFERENCES circuits(id) ON DELETE CASCADE,
    destination_id INT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    day_number INT NOT NULL,
    sequence_order INT NOT NULL,
    notes TEXT
);

CREATE TABLE festivals (
    id SERIAL PRIMARY KEY,
    destination_id INT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    dated_info_month VARCHAR(100) NOT NULL,
    typical_dates_range VARCHAR(150) NOT NULL,
    crowd_level VARCHAR(50) CHECK(crowd_level IN ('Moderate', 'High', 'Extremely Crowded')),
    key_rituals TEXT
);

CREATE TABLE hotels (
    id SERIAL PRIMARY KEY,
    destination_id INT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(100) NOT NULL CHECK(type IN ('Dharamshala / Ashram', 'Budget Hotel', 'Standard Hotel', 'Heritage Haveli', 'Luxury Resort')),
    address TEXT NOT NULL,
    contact_phone VARCHAR(50),
    price_per_night NUMERIC(10,2) NOT NULL,
    rating NUMERIC(3,2) DEFAULT 4.0,
    is_pure_veg SMALLINT DEFAULT 1,
    is_senior_friendly SMALLINT DEFAULT 1,
    has_wheelchair_ramp SMALLINT DEFAULT 0,
    has_lift SMALLINT DEFAULT 0,
    proximity_to_temple_km NUMERIC(5,2) NOT NULL,
    image_url TEXT
);

CREATE TABLE restaurants (
    id SERIAL PRIMARY KEY,
    destination_id INT NOT NULL REFERENCES destinations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    cuisine_type VARCHAR(100) NOT NULL CHECK(cuisine_type IN ('Sattvic (No Onion/Garlic)', 'Pure Vegetarian Thali', 'Temple Prasad / Mahaprasad', 'Gurudwara Langar (Seva)', 'Multi-cuisine Veg')),
    avg_cost_for_two NUMERIC(10,2) NOT NULL,
    address TEXT NOT NULL,
    special_dishes TEXT,
    opening_hours VARCHAR(255),
    is_sattvic SMALLINT DEFAULT 1
);

CREATE TABLE vehicles (
    id SERIAL PRIMARY KEY,
    vehicle_type VARCHAR(150) NOT NULL,
    capacity INT NOT NULL,
    price_per_day NUMERIC(10,2) NOT NULL,
    price_per_km NUMERIC(10,2) NOT NULL,
    driver_allowance_per_day NUMERIC(10,2) DEFAULT 400.0,
    ac_available SMALLINT DEFAULT 1,
    senior_friendly_comfort SMALLINT DEFAULT 1,
    features TEXT,
    image_url TEXT
);

CREATE TABLE trips (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    circuit_id INT REFERENCES circuits(id) ON DELETE SET NULL,
    destination_ids_json TEXT NOT NULL,
    start_date VARCHAR(50),
    total_days INT NOT NULL,
    travelers_count INT DEFAULT 2,
    traveler_profile VARCHAR(50) CHECK(traveler_profile IN ('solo', 'couple', 'family', 'seniors')),
    pace VARCHAR(50) CHECK(pace IN ('relaxed', 'balanced', 'active')),
    budget_tier VARCHAR(50) CHECK(budget_tier IN ('economy', 'standard', 'comfort')),
    estimated_total_cost NUMERIC(12,2) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trip_days (
    id SERIAL PRIMARY KEY,
    trip_id INT NOT NULL REFERENCES trips(id) ON DELETE CASCADE,
    day_number INT NOT NULL,
    date VARCHAR(100),
    title VARCHAR(255) NOT NULL,
    morning_plan TEXT NOT NULL,
    afternoon_plan TEXT NOT NULL,
    evening_plan TEXT NOT NULL,
    estimated_cost NUMERIC(10,2) DEFAULT 0.0
);

CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    booking_type VARCHAR(50) NOT NULL CHECK(booking_type IN ('hotel', 'vehicle', 'puja_darshan_assistance')),
    reference_id INT NOT NULL,
    booking_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    start_date VARCHAR(50) NOT NULL,
    end_date VARCHAR(50) NOT NULL,
    guests_count INT DEFAULT 1,
    total_amount NUMERIC(12,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'confirmed' CHECK(status IN ('confirmed', 'pending', 'cancelled')),
    special_requests TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 3. SEED INSERTIONS

-- Circuits (8 pilgrimage circuits)
INSERT INTO circuits (id, name, slug, description, states_covered, total_days_recommended, theme, image_url) VALUES
(1, 'Uttarakhand Char Dham Yatra', 'chardham-uttarakhand', 'The holy Himalayan pilgrimage to the sacred shrines of Haridwar, Rishikesh, Kedarnath, and Badrinath nestled in the majestic peaks.', 'Uttarakhand', 10, 'Moksha & Himalayan Divine Grace', 'https://images.unsplash.com/photo-1626014303757-6466336e4f3a?auto=format&fit=crop&w=1200&q=80'),
(2, 'Braj Bhoomi Krishna Circuit', 'braj-bhoomi-krishna', 'Walk in the divine steps of Lord Krishna through Mathura, Vrindavan, Goverdhan, and sacred Yamuna ghats with enchanting aartis and devotion.', 'Uttar Pradesh', 3, 'Vaishnava Bhakti & Divine Love', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80'),
(3, 'Kashi - Prayagraj - Ayodhya Moksha Circuit', 'kashi-prayagraj-ayodhya', 'The eternal sacred triangle of Sanatana Dharma: Lord Shiva in Kashi, the holy Triveni Sangam in Prayagraj, and Lord Rama’s birthplace in Ayodhya.', 'Uttar Pradesh', 5, 'Tirtharaj, Moksha & Ram Lalla Darshan', 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80'),
(4, 'Gujarat Coastal Sacred Circuit', 'gujarat-coastal-circuit', 'Visit the western jewel of Char Dham at Dwarkadhish Jagat Mandir and the premier Jyotirlinga at Somnath on the azure Arabian seacoast.', 'Gujarat', 4, 'Coastal Jyotirlinga & Krishna Capital', 'https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe?auto=format&fit=crop&w=1200&q=80'),
(5, 'Sufi & Brahma Spiritual Circuit (Rajasthan)', 'rajasthan-ajmer-pushkar', 'A harmonious spiritual odyssey blending the timeless Sufi devotion at Ajmer Sharif Dargah with the cosmic reverence of Pushkar Brahma Temple.', 'Rajasthan', 3, 'Interfaith Harmony, Sufi Love & Vedic Antiquity', 'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80'),
(6, 'Tamil Nadu Divine Dravidian Circuit', 'tamilnadu-madurai-rameswaram', 'Marvel at the ancient architecture of Madurai Meenakshi Amman Temple and complete the Char Dham sacred bath across 22 Theerthams in Rameswaram.', 'Tamil Nadu', 4, 'Dravidian Temple Grandeur & Jyotirlinga Snan', 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80'),
(7, 'Maharashtra Jyotirlinga & Sai Bhakti', 'maharashtra-shirdi-trimbakeshwar', 'Seek peace and miracles at the Samadhi of Sai Baba in Shirdi, coupled with the ancient Godavari Jyotirlinga at Trimbakeshwar.', 'Maharashtra', 3, 'Shraddha, Saburi & Trimbakeshwar Mahadev', 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80'),
(8, 'Buddhist Enlightenment Pilgrimage', 'buddhist-circuit-bodhgaya', 'Trace the enlightened footsteps of Lord Buddha from Bodh Gaya’s sacred Bodhi Tree to Sarnath Deer Park where the first Dhamma sermon was delivered.', 'Bihar, Uttar Pradesh', 4, 'Inner Peace, Dhamma & Mindfulness', 'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80');

-- Circuit Destinations
INSERT INTO circuit_destinations (id, circuit_id, destination_id, day_number, sequence_order, notes) VALUES
(1, 1, 7, 1, 1, 'Haridwar: Holy dip at Har Ki Pauri and evening Ganga Aarti'),
(2, 1, 8, 2, 2, 'Rishikesh: Triveni Ghat aarti and ashram meditation'),
(3, 1, 9, 4, 3, 'Kedarnath: Helicopter/Trek to sacred Jyotirlinga'),
(4, 1, 10, 7, 4, 'Badrinath: Badri Vishal darshan and Tapt Kund holy bath'),
(5, 2, 1, 1, 1, 'Mathura: Krishna Janmasthan and Dwarkadhish morning darshan'),
(6, 2, 2, 2, 2, 'Vrindavan: Banke Bihari, ISKCON and evening Prem Mandir musical fountains'),
(7, 3, 4, 1, 1, 'Varanasi: Kashi Vishwanath Jyotirlinga & Golden Temple corridor'),
(8, 3, 5, 2, 2, 'Varanasi: Dashashwamedh Ghat sunrise boat ride & evening Maha Aarti'),
(9, 3, 6, 3, 3, 'Prayagraj: Holy Snan at Triveni Sangam & Bade Hanuman Ji darshan'),
(10, 3, 3, 4, 4, 'Ayodhya: Shri Ram Janmabhoomi Mandir & Saryu Aarti'),
(11, 4, 11, 1, 1, 'Dwarka: Dwarkadhish Jagat Mandir, Gomti Sangam and Bet Dwarka boat ride'),
(12, 4, 12, 3, 2, 'Somnath: First Jyotirlinga darshan and Sound & Light evening show'),
(13, 5, 13, 1, 1, 'Ajmer: Ziyarat at Khwaja Moinuddin Chishti Dargah and Sufi Qawwali'),
(14, 5, 14, 2, 2, 'Pushkar: Holy bath at Pushkar Lake and sacred Brahma Temple darshan'),
(15, 6, 18, 1, 1, 'Madurai: Meenakshi Amman Temple exploration and Hall of Thousand Pillars'),
(16, 6, 17, 3, 2, 'Rameswaram: Ramanathaswamy 22 Theertham holy dip, Agni Theertham, and Dhanushkodi'),
(17, 7, 19, 1, 1, 'Shirdi: Sai Baba Samadhi darshan, Dwarkamai and Gurusthan'),
(18, 7, 20, 2, 2, 'Trimbakeshwar: Trimbakeshwar Jyotirlinga darshan and Kushavarta Kund'),
(19, 8, 21, 1, 1, 'Bodh Gaya: Mahabodhi Temple, meditation under the Bodhi Tree & monasteries'),
(20, 8, 24, 3, 2, 'Sarnath: Dhamek Stupa, Deer Park and Archaeological Museum');

-- Festivals
INSERT INTO festivals (id, destination_id, name, description, dated_info_month, typical_dates_range, crowd_level, key_rituals) VALUES
(1, 1, 'Shri Krishna Janmashtami', 'Grand midnight celebration of Lord Krishna’s divine appearance with ecstatic kirtan, Chhappan Bhog, and flower decorations.', 'August - September', 'Bhadrapada Krishna Ashtami (Aug/Sep)', 'Extremely Crowded', 'Midnight Maha Abhishek, Makhan Mishri distribution, 24-hr Akhand Kirtan'),
(2, 2, 'Holi of Flowers (Phoolon ki Holi)', 'World-famous celebration where devotees and priests shower fresh fragrant flower petals on the deities and each other in ecstatic joy.', 'March', 'Phalguna Ekadashi to Purnima (March)', 'Extremely Crowded', 'Flower shower, Samaj Gayan devotional singing, Raas Leela'),
(3, 3, 'Ayodhya Deepotsav & Ram Navami', 'Illumination of millions of earthen lamps (diyas) on the banks of Saryu River during Diwali, and grand celebration of Lord Ram’s birth during Chaitra Navami.', 'April & November', 'Ram Navami (March/April) & Deepotsav (Oct/Nov)', 'Extremely Crowded', 'Record-breaking Guinness diya lighting, laser show, chariot procession'),
(4, 4, 'Dev Deepawali in Kashi', 'The Gods descend to bathe in the Ganga; all 84 ghats are illuminated with over one million sparkling earthen lamps in an ethereal spectacle.', 'November', 'Kartik Purnima (Nov 2026)', 'Extremely Crowded', 'Ghat-wide diya illumination, Maha Ganga Aarti, floating lamps on river'),
(5, 4, 'Maha Shivratri in Kashi', 'The night of Lord Shiva’s wedding. Special 4-Prahar Pooja conducted all night with continuous Bilva patra and milk offerings.', 'February - March', 'Phalguna Krishna Chaturdashi (Feb/Mar)', 'Extremely Crowded', 'Continuous 24-hour Darshan, Shiv Baraat procession through ancient streets'),
(6, 6, 'Maha Kumbh / Magh Mela Prayagraj', 'The greatest spiritual gathering on Earth where tens of millions take the nectarous dip at Triveni Sangam during auspicious Shahi Snan dates.', 'January - February', 'Magh Mela annually (Jan-Feb); Purna Kumbh every 12 years', 'Extremely Crowded', 'Shahi Snan of Akhadas, Kalpavas ascetic camping, spiritual discourses'),
(7, 7, 'Ganga Dussehra Haridwar', 'Celebrates the sacred descent of River Ganga from Heaven to Earth. Hundreds of thousands of devotees gather for holy bath and floating deepas.', 'May - June', 'Jyeshtha Shukla Dashami (May/June)', 'High', 'Maha Aarti at Har Ki Pauri, melon and lassi distribution, milk abhishek'),
(8, 9, 'Kedarnath Dham Opening Ceremony', 'Auspicious opening of the temple doors in early summer marked by the arrival of the Utsav Doli from Omkareshwar Temple, Ukhimath.', 'April - May', 'Akshaya Tritiya (April/May annually)', 'High', 'Vedic rituals, ceremonial key turning, flower shower from helicopters'),
(9, 11, 'Dwarka Janmashtami & Flag Hoisting', 'Solemn ceremonial changing of the 52-yard sacred flag (Dhwaja) atop the temple pinnacle 5 times daily amidst royal celebrations.', 'August - September', 'Janmashtami week (Aug/Sep)', 'Extremely Crowded', 'Dhwaja Arohan, midnight Krishna Janma aarti, traditional Ras dance'),
(10, 12, 'Somnath Maha Shivratri Mahotsav', 'Three-day grand spiritual festival featuring Palki Yatra of Somnath Mahadev and all-night musical and classical dance tributes.', 'February - March', 'Maha Shivratri (Feb/Mar)', 'Extremely Crowded', 'Four prahar continuous Jalabhishek, beachfront laser and sound show'),
(11, 13, 'Annual Urs of Khwaja Gharib Nawaz', 'Commemoration of the death anniversary of Khwaja Moinuddin Chishti. The sacred Jannati Darwaza is opened for pilgrims from all corners of the world.', 'January - February', '1st to 6th Rajab (Islamic Lunar Calendar)', 'Extremely Crowded', 'Opening of Jannati Darwaza, giant Deg cooking of Kheer, all-night Qawwali'),
(12, 14, 'Pushkar Camel & Spiritual Fair', 'Vibrant amalgamation of sacred lake pilgrimage with colorful cultural traditions, folk music, and desert festivities.', 'November', 'Kartik Purnima (November)', 'Extremely Crowded', 'Holy Kartik Purnima snan, Maha Aarti at Brahma Ghat, folk dance & music'),
(13, 15, 'Guru Nanak Dev Ji Gurpurab', 'Commemorates the birth of Guru Nanak Dev Ji. The Golden Temple is illuminated with hundreds of thousands of lights and dazzling fireworks.', 'November', 'Kartik Purnima (November)', 'Extremely Crowded', 'Akhand Path recitation, Nagar Kirtan procession, grand fireworks over Sarovar'),
(14, 16, 'Tirumala Salakatla Brahmotsavam', 'Nine-day celestial festival where Lord Malayappa Swamy is carried out on magnificent golden Vahanams (Garuda, Hanuman, Sesha Vahanams).', 'September - October', 'Ashwin month (September/October)', 'Extremely Crowded', 'Garuda Seva day with over 300,000 pilgrims, Rathotsavam car festival'),
(15, 17, 'Rameswaram Maha Shivratri & Thirukalyanam', 'Celebrates the divine marriage of Lord Ramanathaswamy and Goddess Parvathavardhini followed by temple car procession.', 'February - March & July', 'Maha Shivratri & Aadi Thirukalyanam', 'High', 'Sacred bath in 22 Theerthams, silver chariot procession along sea coast'),
(16, 18, 'Meenakshi Thirukalyanam (Chithirai Festival)', 'Spectacular 10-day carnival commemorating the divine wedding of Goddess Meenakshi and Lord Sundareswarar with Lord Alagar entering the Vaigai River.', 'April - May', 'Chithirai Tamil month (April/May)', 'Extremely Crowded', 'Celestial Wedding ceremony, golden car procession, 1 million attendees'),
(17, 19, 'Shirdi Sai Baba Punyatithi', 'Commemoration of Sai Baba’s Mahasamadhi on Vijayadashami day with continuous Bhiksha, Palanquin procession, and Bhajans.', 'October', 'Vijayadashami / Dussehra (October)', 'Extremely Crowded', 'Palki procession, Khandoba temple march, continuous 24-hr Akhand Dhuni'),
(18, 21, 'Buddha Purnima Mahotsav', 'Celebrates the thrice-blessed day of Gautama Buddha’s Birth, Supreme Enlightenment, and Mahaparinirvana under the Bodhi Tree.', 'May', 'Vaisakha Purnima (May)', 'High', 'Peace march by international monks, chanting of Tipitaka, Bodhi Tree water blessing'),
(19, 22, 'Puri Ratha Yatra (Festival of Chariots)', 'The supreme spectacle of Sanatana Dharma where Lord Jagannath, Balabhadra, and Subhadra journey on majestic wooden chariots to Gundicha Temple.', 'June - July', 'Ashadha Shukla Dwitiya (June/July)', 'Extremely Crowded', 'Pulling of Nandighosha chariot, Chhera Pahanra sweep by Puri Gajapati Maharaja');

-- Hotels & Dharamshalas
INSERT INTO hotels (id, destination_id, name, type, address, contact_phone, price_per_night, rating, is_pure_veg, is_senior_friendly, has_wheelchair_ramp, has_lift, proximity_to_temple_km, image_url) VALUES
(1, 1, 'Shri Krishna Janmasthan Yatri Niwas', 'Dharamshala / Ashram', 'Opposite Janmasthan Gate 3, Mathura', '+91 565 2423888', 850.00, 4.40, 1, 1, 1, 1, 0.20, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(2, 2, 'MVT Guesthouse & Ashram', 'Dharamshala / Ashram', 'Bhakti Vedanta Swami Marg, Raman Reti, Vrindavan', '+91 565 2540050', 1600.00, 4.70, 1, 1, 1, 1, 0.80, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(3, 2, 'Brij View Premier Suites', 'Standard Hotel', 'Near Prem Mandir, Chhatikara Road, Vrindavan', '+91 9897012345', 2800.00, 4.50, 1, 1, 1, 1, 0.50, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(4, 3, 'Birla Yatri Niwas Dharamshala', 'Dharamshala / Ashram', 'Near Ram Janmabhoomi Complex, Ayodhya', '+91 5278 232230', 950.00, 4.30, 1, 1, 1, 1, 0.40, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(5, 3, 'Shri Ram Hotel & Heritage Suites', 'Standard Hotel', 'Tedhi Bazar, Near Saryu Ghat, Ayodhya', '+91 5278 232555', 2400.00, 4.40, 1, 1, 1, 1, 0.60, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(6, 4, 'Shri Kashi Vishwanath Yatri Nivas (Trust)', 'Dharamshala / Ashram', 'Vishwanath Corridor Gate 4, Varanasi', '+91 542 2392629', 1100.00, 4.60, 1, 1, 1, 1, 0.10, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(7, 4, 'BrijRama Palace Heritage Hotel', 'Heritage Haveli', 'Darbhanga Ghat, Dashashwamedh, Varanasi', '+91 542 2452222', 12500.00, 4.90, 1, 1, 1, 1, 0.30, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(8, 5, 'Hotel Ganges View & Retreat', 'Standard Hotel', 'Assi Ghat Road, Varanasi', '+91 542 2313218', 3200.00, 4.50, 1, 1, 0, 1, 1.20, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(9, 6, 'Kumbh Divine Sangam Tent & Guest Suites', 'Standard Hotel', 'Near Sangam Marg, Daraganj, Prayagraj', '+91 532 2500123', 2200.00, 4.30, 1, 1, 1, 1, 0.80, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(10, 7, 'Bhagirathi Atithi Griha (GMVN)', 'Budget Hotel', 'Near Har Ki Pauri, Haridwar', '+91 1334 227370', 1400.00, 4.20, 1, 1, 1, 1, 0.30, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(11, 8, 'Parmarth Niketan Ashram Stay', 'Dharamshala / Ashram', 'Swargashram, Rishikesh', '+91 135 2440077', 900.00, 4.80, 1, 1, 1, 1, 0.10, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(12, 9, 'GMVN Kedarnath Temple Colony Cottages', 'Dharamshala / Ashram', 'Near Kedarnath Temple Plateau, Kedarnath', '+91 135 2740896', 1800.00, 4.10, 1, 0, 0, 0, 0.20, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(13, 10, 'Shri Badrinath Guest House (Devasthanam)', 'Dharamshala / Ashram', 'Near Temple Gate, Badrinath', '+91 1381 222212', 1200.00, 4.30, 1, 1, 1, 1, 0.20, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(14, 11, 'Dwarkadhish Kokila Dhirubhai Ambani Yatri Niwas', 'Dharamshala / Ashram', 'Near ISKCON Gate, Dwarka', '+91 2892 234125', 1200.00, 4.60, 1, 1, 1, 1, 0.60, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(15, 12, 'Somnath Sagar Darshan Guest House (Trust)', 'Standard Hotel', 'Directly Facing Somnath Seafront, Somnath', '+91 2876 231212', 2100.00, 4.70, 1, 1, 1, 1, 0.20, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(16, 13, 'Khwaja Heritage Haveli Stay', 'Heritage Haveli', 'Near Dargah Sharif Gate 2, Ajmer', '+91 145 2420999', 2600.00, 4.30, 0, 1, 0, 1, 0.30, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(17, 14, 'Brahma Horizon Resort & Suites', 'Standard Hotel', 'Panchkund Road, Pushkar', '+91 145 2772500', 3100.00, 4.50, 1, 1, 1, 1, 0.80, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(18, 15, 'Sri Guru Ram Das Niwas (SGPC)', 'Dharamshala / Ashram', 'Golden Temple Complex, Amritsar', '+91 183 2553957', 500.00, 4.70, 1, 1, 1, 1, 0.10, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(19, 15, 'Ramada by Wyndham Amritsar', 'Luxury Resort', 'Hall Bazar, Near Golden Temple, Amritsar', '+91 183 5025555', 4800.00, 4.60, 1, 1, 1, 1, 0.90, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(20, 16, 'Srinivasam Complex (TTD)', 'Dharamshala / Ashram', 'Near Tirupati Railway Station, Tirupati', '+91 877 2277777', 600.00, 4.50, 1, 1, 1, 1, 1.50, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(21, 16, 'Fortune Select Grand Ridge', 'Luxury Resort', 'Shilparamam Tirupati', '+91 877 6688888', 4900.00, 4.60, 1, 1, 1, 1, 3.20, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(22, 17, 'Goswami Math Dharamshala', 'Dharamshala / Ashram', 'West Car Street, Rameswaram', '+91 4573 221234', 800.00, 4.20, 1, 1, 0, 1, 0.20, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(23, 17, 'Hotel Daiwik Rameswaram', 'Standard Hotel', 'NH 49, Near Rameswaram Temple, Rameswaram', '+91 4573 301222', 3600.00, 4.50, 1, 1, 1, 1, 1.00, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
(24, 18, 'Heritage Madurai', 'Luxury Resort', 'Kochadai, Madurai', '+91 452 2385455', 5500.00, 4.70, 1, 1, 1, 1, 4.00, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(25, 19, 'Shirdi Sai Ashram Bhakta Niwas (Sansthan)', 'Dharamshala / Ashram', 'Dindori Road, Shirdi', '+91 2423 258500', 500.00, 4.60, 1, 1, 1, 1, 0.70, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(26, 20, 'Gajanan Maharaj Sansthan Bhakta Nivas', 'Dharamshala / Ashram', 'Near Trimbakeshwar Temple, Trimbakeshwar', '+91 2594 233215', 750.00, 4.40, 1, 1, 1, 1, 0.30, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
(27, 21, 'Daijokyo Buddhist Monastery Guest House', 'Dharamshala / Ashram', 'Near Japanese Temple, Bodh Gaya', '+91 631 2200747', 1000.00, 4.70, 1, 1, 1, 1, 0.40, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
(28, 22, 'Shri Jagannath Bhakta Nivas', 'Dharamshala / Ashram', 'VIP Road, Puri', '+91 6752 222053', 900.00, 4.50, 1, 1, 1, 1, 0.80, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80');

-- Restaurants & Sattvic / Prasad / Langar Dining
INSERT INTO restaurants (id, destination_id, name, cuisine_type, avg_cost_for_two, address, special_dishes, opening_hours, is_sattvic) VALUES
(1, 1, 'Brijwasi Mithai & Bhojanalaya', 'Pure Vegetarian Thali', 350.00, 'Near Janmasthan, Mathura', 'Mathura Ke Special Pede, Hing Kachori with Dubki Aloo, Rabdi', '07:00 AM - 10:30 PM', 1),
(2, 2, 'Govinda Restaurant (ISKCON)', 'Sattvic (No Onion/Garlic)', 450.00, 'ISKCON Temple Campus, Raman Reti, Vrindavan', 'Pure Sattvic Thali, Khichdi Prasadam, Paneer Makhanwala (No onion/garlic)', '08:00 AM - 09:30 PM', 1),
(3, 3, 'Shri Ram Rasoi & Bhojanalaya', 'Sattvic (No Onion/Garlic)', 300.00, 'Near Ram Janmabhoomi Path, Ayodhya', 'Awadhi Sattvic Thali, Baati Chokha, Kheer', '07:30 AM - 10:00 PM', 1),
(4, 4, 'Shri Annapurna Temple Rasoi', 'Temple Prasad / Mahaprasad', 0.00, 'Annapurna Mandir, Vishwanath Gali, Varanasi', 'Free Mahaprasad (Dal, Bhaat, Tarkari, Kheer) served with boundless love to all pilgrims', '11:00 AM - 03:00 PM', 1),
(5, 4, 'Keshari Restaurant & Sattvic Bhoj', 'Pure Vegetarian Thali', 400.00, 'Near Dashashwamedh Ghat, Varanasi', 'Banarasi Thali, Baati Chokha, Malaiyyo (Winter seasonal sweet)', '08:00 AM - 11:00 PM', 1),
(6, 6, 'Netram Mulchand Pure Veg Bhoj', 'Pure Vegetarian Thali', 350.00, 'Katla Road, Prayagraj', 'Traditional Desi Ghee Puri, Subzi, Jalebi and Dahi', '07:00 AM - 10:00 PM', 1),
(7, 7, 'Mathura Walo Ki Pracheen Dukan', 'Pure Vegetarian Thali', 250.00, 'Moti Bazar, Haridwar', 'Puri Chhole, Halwa, Rabdi, Lassi', '06:30 AM - 10:30 PM', 1),
(8, 8, 'Chotiwala Restaurant Since 1958', 'Pure Vegetarian Thali', 500.00, 'Swargashram, Ram Jhula, Rishikesh', 'Garhwali Thali, Paneer Butter Masala, Special Kheer', '07:30 AM - 10:30 PM', 1),
(9, 10, 'Badri Vishal Prasad Bhandar', 'Temple Prasad / Mahaprasad', 150.00, 'Near Temple Gate, Badrinath', 'Poha, Khichdi, Laddu Prasadam, Herbal Himalayan Tea', '06:00 AM - 08:30 PM', 1),
(10, 11, 'Toran Dining Hall (Gujarat Tourism)', 'Pure Vegetarian Thali', 350.00, 'Near Dwarkadhish Temple, Dwarka', 'Authentic Kathiyawadi Gujarati Thali, Kadhi, Bajra Rotla, Khichdi', '11:00 AM - 03:30 PM & 07:00 PM - 10:30 PM', 1),
(11, 12, 'Somnath Trust Prasadam Bhojanalaya', 'Temple Prasad / Mahaprasad', 100.00, 'Somnath Temple Complex, Somnath', 'Traditional Gujarati Prasad Thali (Subzi, Dal, Roti, Rice, Sweet)', '11:00 AM - 03:00 PM & 06:30 PM - 09:30 PM', 1),
(12, 13, 'Dargah Sharif Langar Khana', 'Multi-cuisine Veg', 0.00, 'Inside Dargah Sharif Courtyard, Ajmer', 'Sweet Saffron Rice (Zarda) & Tabarruk distributed freely from the historic Big Deg', '12:00 PM - 02:00 PM & 07:00 PM - 09:00 PM', 1),
(13, 14, 'Pushkar Brahma Sattvic Kitchen', 'Sattvic (No Onion/Garlic)', 350.00, 'Main Market, Near Brahma Temple, Pushkar', 'Rajasthani Dal Baati Churma, Ker Sangri, Malpua', '08:00 AM - 10:00 PM', 1),
(14, 15, 'Guru Ka Langar (Sri Harmandir Sahib)', 'Gurudwara Langar (Seva)', 0.00, 'Golden Temple Complex, Amritsar', 'Universal hot meals: Fresh hot rotis (served directly by sevadaars), Dal, Kheer, Subzi. 100% Free for everyone.', 'Open 24 hours continuously', 1),
(15, 15, 'Bharawan Da Dhaba Since 1912', 'Pure Vegetarian Thali', 450.00, 'Near Town Hall, Amritsar', 'Amritsari Kulcha with Chhole, Dal Makhani, Fresh Sweet Lassi', '07:30 AM - 11:30 PM', 1),
(16, 16, 'TTD Annaprasadam Complex', 'Temple Prasad / Mahaprasad', 0.00, 'Matrusri Tarigonda Vengamamba Complex, Tirumala', 'Sacred Tirumala Anna Prasadam: Hot rice, Sambar, Rasam, Chutney, Payasam served with supreme devotion to tens of thousands daily. 100% Free.', '09:00 AM - 11:00 PM', 1),
(17, 16, 'Hotel Saravana Bhavan Tirupati', 'Pure Vegetarian Thali', 400.00, 'TP Area, Tirupati', 'Authentic South Indian Filter Coffee, Ghee Roast Dosa, Mini Tiffin', '06:00 AM - 10:30 PM', 1),
(18, 17, 'Ram Nivas Traditional South Thali', 'Pure Vegetarian Thali', 250.00, 'South Car Street, Rameswaram', 'Chettinad Veg Thali on fresh Banana leaf, Rasam, Appalam', '07:00 AM - 09:30 PM', 1),
(19, 18, 'Murugan Idli Shop', 'Pure Vegetarian Thali', 300.00, 'West Masi Street, Madurai', 'World-famous Melt-in-mouth Steamed Idlis with four fresh chutneys and Podi Ghee', '06:30 AM - 11:00 PM', 1),
(20, 19, 'Shri Sai Sansthan Prasadalaya', 'Temple Prasad / Mahaprasad', 20.00, 'Nimgaon Road, Shirdi', 'Asia’s largest solar-powered kitchen serving wholesome Sattvic Mahaprasad: Dal, Rice, 2 Sabzis, Roti, Sweet for ₹20 (Free for children)', '10:00 AM - 10:00 PM', 1),
(21, 21, 'Bodhi Tree Monastery Vegetarian Cafe', 'Sattvic (No Onion/Garlic)', 350.00, 'Near Mahabodhi Temple, Bodh Gaya', 'Tibetan Thukpa, Momos, Herbal Teas, Sattvic Rice bowls', '07:00 AM - 09:00 PM', 1),
(22, 22, 'Ananda Bazar (Jagannath Temple Mahaprasad)', 'Temple Prasad / Mahaprasad', 200.00, 'Outer Courtyard, Jagannath Temple, Puri', 'Sacred Chhappan Bhog Mahaprasad: Kanika (sweet fragrant rice), Dalma, Besara, Khaja sweet cooked in earthenware pots', '12:00 PM - 05:00 PM', 1);

-- Vehicles
INSERT INTO vehicles (id, vehicle_type, capacity, price_per_day, price_per_km, driver_allowance_per_day, ac_available, senior_friendly_comfort, features, image_url) VALUES
(1, 'Sedan (Maruti Dzire / Toyota Etios)', 4, 2400.00, 12.00, 400.00, 1, 1, 'Ideal for couples and small families. Boot space for 2 large luggage bags, air conditioned, sanitized, gentle driving guaranteed.', 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'),
(2, 'SUV (Toyota Innova Crysta - Senior Recommended)', 7, 3800.00, 17.00, 500.00, 1, 1, 'Recommended for senior citizens: High seating, captain seats with lumbar support, smooth shock absorbers, low step board for easy entry, rear AC vents.', 'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'),
(3, 'Tempo Traveller (12-14 Seater Family Group)', 13, 5200.00, 23.00, 600.00, 1, 1, 'Perfect for extended family pilgrimage groups. Pushback reclining seats, LED screen with devotional audio/bhajans, ample luggage carrier, dual AC.', 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80'),
(4, 'Tempo Traveller Deluxe (17-20 Seater Large Group)', 19, 6800.00, 28.00, 700.00, 1, 1, 'Spacious 2x1 luxury seating, high headroom, wide panoramic windows, air suspension, PA audio microphone for tour guide / kirtan.', 'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80'),
(5, 'Electric Darshan Rickshaw (Local City Tour)', 4, 900.00, 0.00, 0.00, 0, 1, 'Eco-friendly battery-operated rickshaw specifically licensed for inner temple galis and ghat pathways where regular cars are prohibited (e.g. Vrindavan, Ayodhya, Varanasi).', 'https://images.unsplash.com/photo-1596707255140-520e17621be0?auto=format&fit=crop&w=800&q=80');

-- Sample Trips & Days
INSERT INTO trips (id, user_id, title, circuit_id, destination_ids_json, start_date, total_days, travelers_count, traveler_profile, pace, budget_tier, estimated_total_cost, notes) VALUES
(1, 2, 'Sacred Kashi & Ayodhya Family Tirth Yatra', 3, '[4, 5, 3]', '2026-11-10', 4, 3, 'seniors', 'relaxed', 'standard', 24500.00, 'Senior-friendly pilgrimage for parents. Battery car passes required for Ayodhya Ram Mandir and Kashi Vishwanath Sugam Darshan.');

INSERT INTO trip_days (id, trip_id, day_number, date, title, morning_plan, afternoon_plan, evening_plan, estimated_cost) VALUES
(1, 1, 1, '2026-11-10', 'Day 1: Arrival in Kashi & Evening Ganga Aarti', 'Arrival at Varanasi Airport / Railway Station. Check-in at wheelchair-friendly hotel near Dashashwamedh. Afternoon rest.', 'Visit Sarnath Deer Park and Dhamek Stupa (gentle walking on paved garden paths).', 'Attend the world-famous Maha Ganga Aarti at Dashashwamedh Ghat from a comfortable reserved family boat.', 4500.00),
(2, 1, 2, '2026-11-11', 'Day 2: Kashi Vishwanath Jyotirlinga Darshan', 'Early morning Sugam Darshan at Shri Kashi Vishwanath Temple via Corridor Gate 4 with battery car transit for parents.', 'Sattvic lunch at Annapurna Rasoi followed by temple rest and visit to Sankat Mochan Hanuman Temple.', 'Quiet twilight boat cruise along Manikarnika and Assi Ghats with Banarasi Thali dinner.', 5800.00),
(3, 1, 3, '2026-11-12', 'Day 3: Journey to Ayodhya & Saryu Aarti', 'Comfortable Innova Crysta drive to Ayodhya (approx 4 hours with tea stop). Hotel check-in.', 'Relaxed visit to Kanak Bhawan and Hanuman Garhi temple with volunteer assistance.', 'Peaceful evening Saryu River Aarti and illuminated Ram Ki Paidi walk.', 6200.00),
(4, 1, 4, '2026-11-13', 'Day 4: Shri Ram Janmabhoomi Darshan & Departure', 'Morning Sugam Darshan of Ram Lalla at Shri Ram Janmabhoomi Mandir using Senior Facilitation Center golf carts.', 'Collect sacred Prasad, lunch at Shri Ram Rasoi, purchase local souvenirs and souvenirs.', 'Return transfer to Ayodhya Dham Railway Station / Ayodhya Airport for departure with cherished memories.', 8000.00);

-- Sample Bookings
INSERT INTO bookings (id, user_id, booking_type, reference_id, start_date, end_date, guests_count, total_amount, status, special_requests) VALUES
(1, 2, 'hotel', 6, '2026-11-10', '2026-11-12', 3, 2200.00, 'confirmed', 'Ground floor room requested for elderly parents. Need wheelchair assistance at check-in.'),
(2, 2, 'vehicle', 2, '2026-11-10', '2026-11-13', 3, 15200.00, 'confirmed', 'Innova Crysta with senior-friendly captain seats and experienced polite driver.');

-- 4. SYNCHRONIZE SEQUENCES
SELECT setval(pg_get_serial_sequence('circuits', 'id'), COALESCE((SELECT MAX(id) FROM circuits), 1));
SELECT setval(pg_get_serial_sequence('circuit_destinations', 'id'), COALESCE((SELECT MAX(id) FROM circuit_destinations), 1));
SELECT setval(pg_get_serial_sequence('festivals', 'id'), COALESCE((SELECT MAX(id) FROM festivals), 1));
SELECT setval(pg_get_serial_sequence('hotels', 'id'), COALESCE((SELECT MAX(id) FROM hotels), 1));
SELECT setval(pg_get_serial_sequence('restaurants', 'id'), COALESCE((SELECT MAX(id) FROM restaurants), 1));
SELECT setval(pg_get_serial_sequence('vehicles', 'id'), COALESCE((SELECT MAX(id) FROM vehicles), 1));
SELECT setval(pg_get_serial_sequence('trips', 'id'), COALESCE((SELECT MAX(id) FROM trips), 1));
SELECT setval(pg_get_serial_sequence('trip_days', 'id'), COALESCE((SELECT MAX(id) FROM trip_days), 1));
SELECT setval(pg_get_serial_sequence('bookings', 'id'), COALESCE((SELECT MAX(id) FROM bookings), 1));

-- 5. ROW LEVEL SECURITY (RLS) POLICIES
ALTER TABLE circuits ENABLE ROW LEVEL SECURITY;
ALTER TABLE circuit_destinations ENABLE ROW LEVEL SECURITY;
ALTER TABLE festivals ENABLE ROW LEVEL SECURITY;
ALTER TABLE hotels ENABLE ROW LEVEL SECURITY;
ALTER TABLE restaurants ENABLE ROW LEVEL SECURITY;
ALTER TABLE vehicles ENABLE ROW LEVEL SECURITY;
ALTER TABLE trips ENABLE ROW LEVEL SECURITY;
ALTER TABLE trip_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE bookings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can view circuits" ON circuits FOR SELECT USING (true);
CREATE POLICY "Public can view circuit destinations" ON circuit_destinations FOR SELECT USING (true);
CREATE POLICY "Public can view festivals" ON festivals FOR SELECT USING (true);
CREATE POLICY "Public can view hotels" ON hotels FOR SELECT USING (true);
CREATE POLICY "Public can view restaurants" ON restaurants FOR SELECT USING (true);
CREATE POLICY "Public can view vehicles" ON vehicles FOR SELECT USING (true);
CREATE POLICY "Full access on trips" ON trips FOR ALL USING (true);
CREATE POLICY "Full access on trip_days" ON trip_days FOR ALL USING (true);
CREATE POLICY "Full access on bookings" ON bookings FOR ALL USING (true);
CREATE POLICY "Full access on circuits admin" ON circuits FOR ALL USING (true);
CREATE POLICY "Full access on festivals admin" ON festivals FOR ALL USING (true);
CREATE POLICY "Full access on hotels admin" ON hotels FOR ALL USING (true);
CREATE POLICY "Full access on restaurants admin" ON restaurants FOR ALL USING (true);
CREATE POLICY "Full access on vehicles admin" ON vehicles FOR ALL USING (true);

-- Done!
