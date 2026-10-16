from werkzeug.security import generate_password_hash

def seed_all(conn):
    cursor = conn.cursor()
    
    # Check if already seeded
    cursor.execute("SELECT COUNT(*) FROM destinations")
    if cursor.fetchone()[0] > 0:
        return

    # Seed Users (Admin & Demo Pilgrim)
    users_data = [
        ('admin', 'admin@yatra.in', generate_password_hash('admin123'), 'Yatra Administrator', '+91 9876543210', 'admin'),
        ('pilgrim', 'pilgrim@yatra.in', generate_password_hash('pilgrim123'), 'Aarav & Sunita Sharma', '+91 9812345678', 'user'),
        ('admin_legacy', 'admin@traveltales.in', generate_password_hash('admin123'), 'TravelTales Administrator', '+91 9876543210', 'admin'),
        ('pilgrim_legacy', 'pilgrim@traveltales.in', generate_password_hash('pilgrim123'), 'Aarav & Sunita Sharma', '+91 9812345678', 'user')
    ]
    cursor.executemany(
        "INSERT INTO users (username, email, password_hash, full_name, phone, role) VALUES (?, ?, ?, ?, ?, ?)",
        users_data
    )

    # Seed Destinations across all specified regions
    # (id, name, city, state, category, religion_tradition, description, history, significance, best_time_to_visit, latitude, longitude, image_url, verified)
    destinations_data = [
        # --- Uttar Pradesh ---
        (
            1,
            'Shri Krishna Janmasthan Temple Complex',
            'Mathura',
            'Uttar Pradesh',
            'temple',
            'Hinduism',
            'The revered birthplace of Lord Krishna. The prison cell (Garbha Griha) where Lord Krishna was born is enshrined here with high spiritual vibrancy.',
            'Built over the ancient prison cell of King Kamsa, rebuilt several times across centuries, with major restoration by the Dalmia Trust in the 1950s.',
            'Supreme pilgrimage destination for Vaishnavites and devotees of Lord Krishna worldwide.',
            'October to March (especially Janmashtami & Holi)',
            27.5050, 77.6710,
            'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            2,
            'Banke Bihari Mandir',
            'Vrindavan',
            'Uttar Pradesh',
            'temple',
            'Hinduism',
            'Dedicated to Lord Krishna in the Tribhanga posture. The curtain before the deity is drawn open and shut periodically so devotees are not overwhelmed by the divine gaze.',
            'Established in 1864 by Swami Haridas, the spiritual guru of Tansen, who manifested the deity of Kunj Bihari.',
            'Heart of Braj devotion, where divine love and seva are performed without ringing bells to keep Bihariji peaceful.',
            'October to April (Holi of flowers & Janmashtami are magnificent)',
            27.5815, 77.7005,
            'https://images.unsplash.com/photo-1609137144822-0d19fbe1e367?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            3,
            'Shri Ram Janmabhoomi Mandir',
            'Ayodhya',
            'Uttar Pradesh',
            'temple',
            'Hinduism',
            'The grand Nagara-style temple at the birthplace of Lord Shri Ram on the banks of the holy Saryu river in Ayodhya.',
            'Consecrated in January 2024, constructed using carved pink sandstone from Bansi Paharpur with no iron or steel used in the superstructure.',
            'One of the holiest tirthas in Sanatana Dharma, embodying Maryada Purushottam Shri Ram.',
            'October to March (Ram Navami in April, Deepotsav in November)',
            26.7956, 82.1944,
            'https://images.unsplash.com/photo-1600100397608-f010f443b740?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            4,
            'Shri Kashi Vishwanath Temple (Jyotirlinga)',
            'Varanasi',
            'Uttar Pradesh',
            'temple',
            'Hinduism',
            'One of the 12 sacred Jyotirlingas of Lord Shiva, located in the eternal city of Varanasi beside the holy River Ganga with the magnificent Vishwanath Corridor.',
            'Mentioned in the Skanda Purana; the gilded dome was donated by Maharaja Ranjit Singh in 1835. The modern corridor connects the sanctum directly to the Ganga Ghats.',
            'Regarded as the gateway to Moksha (liberation) where Lord Shiva whispers the Taraka mantra.',
            'October to March (Dev Deepawali and Maha Shivratri are peak times)',
            25.3109, 83.0107,
            'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            5,
            'Dashashwamedh Ghat & Holy Ganga Aarti',
            'Varanasi',
            'Uttar Pradesh',
            'sacred_river',
            'Hinduism',
            'The primary and oldest sacred ghat along the Ganges in Varanasi, renowned for the spectacular evening Maha Ganga Aarti performed by priests.',
            'According to legend, Lord Brahma sacrificed ten horses (Dasa-Ashwamedha) here in a grand ritual.',
            'Center of spiritual rituals, sacred Ganga snan (holy bath), and transcendent twilight prayers.',
            'All year round; pleasant weather from October to March',
            25.3075, 83.0104,
            'https://images.unsplash.com/photo-1571536802807-30451e3955d8?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            6,
            'Triveni Sangam & Kumbh Kshetra',
            'Prayagraj',
            'Uttar Pradesh',
            'sacred_river',
            'Hinduism',
            'The sacred confluence of three holy rivers: Ganga, Yamuna, and the invisible Saraswati. Site of the world-famous Maha Kumbh and Magh Mela.',
            'Celebrated in the Rigveda and Puranas as Tirtharaj (King of all Pilgrimage Sites).',
            'A holy dip here is believed to wash away all sins and grant liberation from rebirth.',
            'November to March (Magh Mela in Jan-Feb, Kumbh cycle)',
            25.4282, 81.8845,
            'https://images.unsplash.com/photo-1610444584288-0b5368a2d126?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Uttarakhand ---
        (
            7,
            'Har Ki Pauri Ghat',
            'Haridwar',
            'Uttarakhand',
            'sacred_river',
            'Hinduism',
            'The famous ghat on the banks of the Ganges where drops of Amrit (nectar of immortality) fell. The evening Ganga Aarti here is a hypnotic spiritual experience.',
            'Built by King Vikramaditya in memory of his brother Bhatrihari. The footprint of Lord Vishnu is enshrined on the stone wall.',
            'Starting point of the holy Char Dham Yatra and prime site for Kumbh Mela.',
            'September to April (Maha Shivratri & Ganga Dussehra)',
            29.9567, 78.1706,
            'https://images.unsplash.com/photo-1598977123418-454555aa166b?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            8,
            'Triveni Ghat & Parmarth Niketan',
            'Rishikesh',
            'Uttarakhand',
            'sacred_river',
            'Hinduism',
            'Sacred bathing ghat where Ganga, Yamuna and Saraswati rivers meet subtily, renowned for evening aarti, meditation ashrams, and spiritual seekers.',
            'Spiritual sanctuary for saints and sages for thousands of years in the Himalayan foothills.',
            'Yoga Capital of the World and gateway to inner peace and Char Dham pilgrimages.',
            'September to May',
            30.1033, 78.2948,
            'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            9,
            'Shri Kedarnath Jyotirlinga Mandir',
            'Kedarnath',
            'Uttarakhand',
            'temple',
            'Hinduism',
            'The highest of the 12 Jyotirlingas, nestled in the snow-capped Garhwal Himalayas at 3,583 meters above sea level beside the Mandakini river.',
            'Originally established by the Pandavas and revived by Adi Shankaracharya in the 8th century CE.',
            'Supreme shrine of Lord Shiva and pinnacle of the Char Dham pilgrimage.',
            'May to October (Opens on Akshaya Tritiya, closes on Bhai Dooj in autumn)',
            30.7352, 79.0669,
            'https://images.unsplash.com/photo-1626014303757-6466336e4f3a?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            10,
            'Shri Badrinath Temple',
            'Badrinath',
            'Uttarakhand',
            'temple',
            'Hinduism',
            'Dedicated to Lord Vishnu (Badri Vishal), situated between Nar and Narayana mountain ranges along the Alaknanda River at 3,133 meters.',
            'Established by Adi Shankaracharya who retrieved the Saligram idol from Narad Kund. One of the primary Char Dham shrines.',
            'The seat of Moksha where sages performed millennia of tapasya.',
            'May to November (Opens early May, closes late autumn)',
            30.7433, 79.4938,
            'https://images.unsplash.com/photo-1588668214407-6ea9a6d8c272?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Gujarat ---
        (
            11,
            'Dwarkadhish Temple (Jagat Mandir)',
            'Dwarka',
            'Gujarat',
            'temple',
            'Hinduism',
            'The 5-story 72-pillared temple of Lord Krishna as the King of Dwarka, located where the Gomti River meets the Arabian Sea.',
            'Believed to have been originally established 2,500 years ago by Vajranabha, great-grandson of Lord Krishna. Current grand structure dates back to 16th century.',
            'One of the four major Char Dham of India and Saptapuri holy cities.',
            'October to March (Janmashtami is celebrated with royal splendor)',
            22.2376, 68.9678,
            'https://images.unsplash.com/photo-1609137144822-0d19fbe1e367?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            12,
            'Somnath Jyotirlinga Temple',
            'Somnath',
            'Gujarat',
            'temple',
            'Hinduism',
            'The first of the twelve sacred Aadi Jyotirlingas, perched grandly on the western shore of Gujarat overlooking the endless Arabian Sea.',
            'Built by the Moon God Soma in gold, rebuilt multiple times in history, and finally restored to majestic Chalukyan architecture in 1951 by Sardar Patel.',
            'Symbol of timeless Sanatana faith and the infinite cosmic presence of Lord Shiva.',
            'October to March (Maha Shivratri is grandly celebrated)',
            20.8880, 70.4012,
            'https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Rajasthan ---
        (
            13,
            'Dargah Sharif of Khwaja Moinuddin Chishti',
            'Ajmer',
            'Rajasthan',
            'mosque_dargah',
            'Islam',
            'The world-renowned Sufi shrine of Gharib Nawaz Khwaja Moinuddin Chishti, drawing millions of pilgrims across all faiths seeking divine blessings and inner peace.',
            'Khwaja Moinuddin Chishti came to Ajmer in 1192 CE spreading the Chishti order of Sufism emphasizing universal love, equality, and compassion.',
            'Epicenter of Sufi spiritual harmony; famous for the sacred Degs (giant cauldrons) cooking sweet rice for thousands.',
            'October to March (Annual Urs festival is globally celebrated)',
            26.4562, 74.6283,
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            14,
            'Brahma Temple & Sacred Pushkar Lake',
            'Pushkar',
            'Rajasthan',
            'temple',
            'Hinduism',
            'One of the very few surviving ancient temples dedicated to Lord Brahma in the world, surrounded by 52 holy ghats of the tranquil Pushkar Lake.',
            'Legend holds that Lord Brahma dropped a lotus flower which gave birth to Pushkar Lake. The 14th-century temple rests on a high raised platform.',
            'A sacred dip in Pushkar lake followed by Brahma darshan is considered necessary to complete any pilgrimage in India.',
            'October to March (Pushkar Fair in Kartik Purnima is world renowned)',
            26.4883, 74.5558,
            'https://images.unsplash.com/photo-1599839575945-a9e5af0c3fa5?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Punjab ---
        (
            15,
            'Sri Harmandir Sahib (The Golden Temple)',
            'Amritsar',
            'Punjab',
            'gurudwara',
            'Sikhism',
            'The central spiritual sanctum of Sikhism, surrounded by the sacred Amrit Sarovar. Four open doors in all directions symbolize welcoming everyone regardless of caste, creed, or faith.',
            'Founded by Guru Ram Das Ji in 1577; Guru Arjan Dev Ji installed the Adi Granth in 1604; gilded with pure gold foil by Maharaja Ranjit Singh in 1830.',
            'The holiest Gurudwara in the world, home to the Akal Takht and Guru Ka Langar serving over 100,000 free hot meals daily.',
            'October to March (Baisakhi, Guru Nanak Jayanti, Diwali lightings)',
            31.6200, 74.8765,
            'https://images.unsplash.com/photo-1584551246679-0daf3d275d0f?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Andhra Pradesh ---
        (
            16,
            'Sri Venkateswara Swamy Temple (Tirumala)',
            'Tirupati',
            'Andhra Pradesh',
            'temple',
            'Hinduism',
            'Perched atop the sacred Seshachalam Seven Hills in Tirumala, dedicated to Lord Venkateswara (Balaji), an incarnation of Lord Vishnu who relieves suffering in Kali Yuga.',
            'Dravidian architecture dating from Pallava, Chola, and Vijayanagara dynasties; managed by Tirumala Tirupati Devasthanams (TTD).',
            'Most visited sacred temple in the world; famous for the holy Tirupati Laddu Prasadam, tonsuring ritual, and deep bhakti.',
            'September to March (Annual Brahmotsavam in Sept/Oct)',
            13.6833, 79.3472,
            'https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Tamil Nadu ---
        (
            17,
            'Sri Ramanathaswamy Temple & Theerthams',
            'Rameswaram',
            'Tamil Nadu',
            'temple',
            'Hinduism',
            'One of the four Char Dham shrines and home to a sacred Jyotirlinga, renowned for the world’s longest pillared corridors and 22 holy bathing wells (Theerthams).',
            'Lord Rama worshipped Lord Shiva here to atone for killing Ravana, consecrating the Ramalingam built by Mother Sita.',
            'Essential Southern pillar of Char Dham; sacred bath in Agni Theertham and 22 inner temple wells cleanses all karmic burdens.',
            'October to April (Maha Shivratri, Thirukalyanam)',
            9.2881, 79.3174,
            'https://images.unsplash.com/photo-1609137144822-0d19fbe1e367?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            18,
            'Meenakshi Amman Temple',
            'Madurai',
            'Tamil Nadu',
            'temple',
            'Hinduism',
            'Masterpiece of Dravidian architecture with 14 soaring Gopurams covered in thousands of colorful sculptures, dedicated to Goddess Meenakshi (Parvati) and Sundareswarar (Shiva).',
            'Mentioned in Sangam literature dating back over 2,500 years; rebuilt by the Nayak rulers in the 16th–17th centuries.',
            'Spiritual heart of Tamil culture; celebrated for the Hall of Thousand Pillars and nightly ceremonial procession of Sundareswarar.',
            'October to March (Chithirai Festival in April is legendary)',
            9.9195, 78.1193,
            'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Maharashtra ---
        (
            19,
            'Sai Baba Samadhi Mandir',
            'Shirdi',
            'Maharashtra',
            'temple',
            'Interfaith / Multi-faith',
            'The holy shrine housing the Samadhi of the 19th-century saint Sai Baba of Shirdi, who taught "Sabka Malik Ek" (One God governs all) and devotion through faith (Shraddha) and patience (Saburi).',
            'Sai Baba lived and performed miracles in Shirdi until Mahasamadhi in 1918. The complex includes Dwarkamai mosque, Chavadi, and Gurusthan.',
            'Beacon of universal love and communal harmony attracting devotees of all religions worldwide.',
            'All year round; pleasantly cool from October to March (Guru Purnima & Sai Punyatithi)',
            19.7667, 74.4764,
            'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            20,
            'Trimbakeshwar Shiva Temple (Jyotirlinga)',
            'Trimbakeshwar',
            'Maharashtra',
            'temple',
            'Hinduism',
            'One of the 12 sacred Jyotirlingas, extraordinary for featuring a three-faced Linga representing Brahma, Vishnu, and Rudra, located at the origin of the sacred Godavari River.',
            'Constructed in black stone by Peshwa Balaji Baji Rao in the 18th century near the Kushavarta kund.',
            'Revered site for Pitru Tarpan rituals, Narayan Nagbali pooja, and Maha Kumbh Mela (Nashik-Trimbakeshwar cycle).',
            'October to March (Maha Shivratri & Shravan Mondays)',
            19.9324, 73.5308,
            'https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Bihar ---
        (
            21,
            'Mahabodhi Temple Complex & Sacred Bodhi Tree',
            'Bodh Gaya',
            'Bihar',
            'monastery',
            'Buddhism',
            'UNESCO World Heritage Site marking the exact location where Siddhartha Gautama attained supreme enlightenment under the sacred Bodhi Tree and became the Buddha.',
            'Originally built by Emperor Ashoka in 260 BCE; features the Vajrasana (diamond throne) and the 50-meter high pyramidal grand stone temple.',
            'Supreme pilgrimage center for Buddhists across Sri Lanka, Thailand, Tibet, Japan, Myanmar, and pilgrims of all faiths worldwide.',
            'October to March (Buddha Purnima in May is profound)',
            24.6959, 84.9913,
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Odisha ---
        (
            22,
            'Shree Jagannath Temple',
            'Puri',
            'Odisha',
            'temple',
            'Hinduism',
            'Ancient Char Dham temple of Lord Jagannath (Lord of the Universe), along with His siblings Balabhadra and Subhadra. World-famous for the annual Ratha Yatra and Mahaprasad.',
            'Built in Kalinga architectural style by King Anantavarman Chodaganga Deva in the 12th century CE on the Nilachala hill.',
            'Supreme tirtha where the Lord Himself partakes in 56 daily offerings (Chhappan Bhog) cooked in the largest traditional temple kitchen.',
            'October to March (Rath Yatra in June/July, Chandan Yatra)',
            19.8049, 85.8179,
            'https://images.unsplash.com/photo-1600100397608-f010f443b740?auto=format&fit=crop&w=1200&q=80',
            1
        ),

        # --- Christian Heritage & Additional Multifaith ---
        (
            23,
            'Basilica of Our Lady of Good Health',
            'Velankanni',
            'Tamil Nadu',
            'church',
            'Christianity',
            'Renowned Catholic pilgrimage sanctuary known as the "Lourdes of the East", situated on the shores of the Bay of Bengal.',
            'Origins date back to 16th-century apparitions of the Blessed Virgin Mary and the Infant Jesus to a shepherd boy and buttermilk vendor.',
            'Major pilgrimage center visited by millions of Christian, Hindu, and Muslim devotees seeking miraculous healings.',
            'September to March (Annual Feast of Our Lady in late August - early September)',
            10.6806, 79.8499,
            'https://images.unsplash.com/photo-1548625361-195fe5787e98?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            24,
            'Sarnath Deer Park & Dhamek Stupa',
            'Sarnath',
            'Uttar Pradesh',
            'heritage_site',
            'Buddhism',
            'The holy park where Gautama Buddha delivered His first sermon (Dhammacakkappavattana Sutta) and set the Wheel of Dhamma in motion.',
            'Founded in the 6th century BCE; Emperor Ashoka erected monuments and the Lion Capital of Ashoka (now the National Emblem of India) here.',
            'One of the four prime Buddhist pilgrimage destinations, offering profound stillness and meditation gardens.',
            'October to March',
            25.3811, 83.0232,
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        # --- Global Sacred Pilgrimage Landmarks ---
        (
            25,
            "St. Peter's Basilica & Vatican City",
            'Vatican City',
            'Rome Region',
            'Vatican City',
            'church',
            'Christianity',
            "The pinnacle of the Roman Catholic Church, built over the tomb of Saint Peter the Apostle. Renowned for Michelangelo's dome, Bernini's Baldachin, and the spiritual heart of Christendom.",
            'Original basilica commissioned by Emperor Constantine in the 4th century; reconstructed in the 16th and 17th centuries by masters including Michelangelo and Bernini.',
            'Supreme Catholic pilgrimage site and official Papal sanctuary welcoming believers from every continent.',
            'October to April (Easter and Christmas seasons are profoundly festive)',
            41.9022, 12.4539,
            'https://images.unsplash.com/photo-1543429776-2782fc8e1acd?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            26,
            'Maya Devi Temple (Birthplace of Lord Buddha)',
            'Lumbini',
            'Lumbini Province',
            'Nepal',
            'monastery',
            'Buddhism',
            'UNESCO World Heritage sanctuary commemorating the exact sacred birthplace of Siddhartha Gautama (Lord Buddha). Features the ancient Marker Stone, Nativity Sculpture, and Puskarini holy pond.',
            "Discovered in 1896 along with Emperor Ashoka's inscribed pillar dating back to 249 BCE verifying the divine birthplace.",
            'Supreme Buddhist pilgrimage center marking where the Buddha took His first seven lotus steps.',
            'October to March (especially Buddha Purnima in May)',
            27.4697, 83.2755,
            'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            27,
            'Pashupatinath Temple',
            'Kathmandu',
            'Bagmati Province',
            'Nepal',
            'temple',
            'Hinduism',
            'Sprawling sacred pagoda temple complex dedicated to Lord Shiva as Pashupati (Lord of All Beings) on the holy banks of the Bagmati River.',
            'Mentioned in the Mahabharata and Lichhavi inscriptions dating to the 5th century CE; current pagoda structure constructed by King Bhupatindra Malla.',
            'One of the eight supreme Paada Tirtha shrines in Sanatana Dharma; revered for liberation (Moksha) and cosmic Shiva worship.',
            'September to April (Maha Shivratri and Teej festivals)',
            27.7105, 85.3487,
            'https://images.unsplash.com/photo-1600100397608-f010f443b740?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            28,
            'Church of the Holy Sepulchre & Western Wall',
            'Jerusalem',
            'Jerusalem District',
            'Israel',
            'heritage_site',
            'Interfaith / Multi-faith',
            "The sacred crossroads of Abrahamic faiths: the Church of the Holy Sepulchre (site of Jesus's crucifixion and resurrection) and the Western Wall (Kotel - holiest remnant of the Second Temple).",
            "The Holy Sepulchre was consecrated in 335 CE by Saint Helena; the Western Wall dates back over 2,000 years to Herod the Great's Second Temple.",
            'Epicenter of profound prayer and solace for Christian and Jewish devotees from every continent.',
            'October to November & March to May',
            31.7785, 35.2296,
            'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            29,
            'Masjid al-Haram & The Holy Kaaba',
            'Mecca',
            'Makkah Province',
            'Saudi Arabia',
            'mosque_dargah',
            'Islam',
            'The Great Mosque of Mecca surrounding the sacred Kaaba, the Qibla towards which Muslims around the world pray five times daily. Destination for the sacred Hajj and Umrah pilgrimages.',
            'Originally built by Prophet Ibrahim (Abraham) and Ismail (Ishmael); expanded extensively across centuries with modern pilgrim infrastructure.',
            'The holiest sanctuary in Islam, home to the Black Stone (Hajr al-Aswad) and Maqam Ibrahim.',
            'November to February (Cooler season; Dhul Hijjah for Hajj)',
            21.4225, 39.8262,
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            30,
            'Fushimi Inari-Taisha Sacred Shrine',
            'Kyoto',
            'Kansai Region',
            'Japan',
            'heritage_site',
            'Shinto',
            'The principal Shinto shrine dedicated to Inari, the deity of rice, agriculture, and prosperity. Famous for the Senbon Torii—over 10,000 vermilion wooden gates winding up sacred Mount Inari.',
            "Founded in 711 CE by the Hata family, predating Kyoto's elevation as Imperial capital.",
            'A profound mountain pilgrimage of gratitude, mindfulness, and sacred harmony with nature.',
            'October to April (Autumn foliage & Cherry Blossom season)',
            34.9671, 135.7727,
            'https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80',
            1
        ),
        (
            31,
            'Cathedral of Santiago de Compostela',
            'Santiago de Compostela',
            'Galicia',
            'Spain',
            'church',
            'Christianity',
            'The legendary culmination of the historic Camino de Santiago (Way of Saint James) pilgrimage route. Enshrines the relics of Saint James the Greater.',
            'Construction began in 1075 during the reign of King Alfonso VI; features the Romanesque Pórtico de la Gloria and the famous Botafumeiro swinging incense censer.',
            'One of the three major Christian pilgrimages since the Middle Ages, welcoming hundreds of thousands of backpack pilgrims annually.',
            'May to October (Feast of St. James on July 25)',
            42.8806, -8.5446,
            'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80',
            1
        )
    ]

    formatted_destinations = []
    for d in destinations_data:
        if len(d) == 14:
            # (id, name, city, state, country, category, religion_tradition, description, history, significance, best_time_to_visit, latitude, longitude, image_url, verified)
            formatted_destinations.append((
                d[0], d[1], d[2], d[3], 'India', d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13]
            ))
        else:
            formatted_destinations.append(d)

    cursor.executemany(
        """
        INSERT INTO destinations (
            id, name, city, state, country, category, religion_tradition, description, 
            history, significance, best_time_to_visit, latitude, longitude, image_url, verified
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        formatted_destinations
    )

    # Seed Religious Site Details (Verified Darshan timings, Aarti, Dress Code, Accessibility)
    # (id, destination_id, opening_hours, morning_aarti_time, evening_aarti_time, darshan_timings, special_darshan_info, entry_fee_info, dress_code, footwear_rules, phone_camera_rules, security_info, non_hindu_entry_rules, wheelchair_accessible, senior_priority_darshan, battery_car_available, walking_distance_meters, medical_facility_nearby, official_booking_url)
    site_details_data = [
        (
            1, 1,
            '05:00 AM - 12:00 PM & 04:00 PM - 09:30 PM',
            '05:30 AM (Mangala Aarti)',
            '07:00 PM (Sandhya Aarti)',
            'General Darshan: 05:30 AM - 11:45 AM, 04:00 PM - 09:00 PM',
            'Special queue assistance available for senior citizens and differently abled. No VIP token charges needed.',
            'Entry is Free. Sample Prasad Box: ₹50 - ₹100. Sample Special Archana: ₹101.',
            'Modest Indian attire recommended. Shoulders and knees must be fully covered. Avoid western shorts.',
            'Free footwear token counters available outside main gate. Footwear strictly prohibited inside.',
            'Mobile phones, cameras, smartwatches, and electronic gadgets are strictly banned inside. Free/paid cloakrooms provided.',
            'High security metal detector checks. Valid government photo ID is recommended to carry.',
            'Devotees of all backgrounds are welcome with respectful adherence to temple customs.',
            1, 1, 1, 150, 1,
            'https://mathura.nic.in/'
        ),
        (
            2, 2,
            '07:45 AM - 12:00 PM & 05:30 PM - 09:30 PM (Summer: 07:00 AM - 11:30 AM, 05:00 PM - 09:00 PM)',
            '07:45 AM (Shringar Aarti - No bells)',
            '09:00 PM (Shayan Aarti)',
            'Darshan operates in continuous waves with curtain intervals every few minutes.',
            'Special early entry assistance for seniors via Gate No. 2 with volunteer help during non-peak hours.',
            'Entry is Free. Sample Peda Prasad: ₹60 - ₹120. Sample Phool Mala offering: ₹50.',
            'Modest traditional clothing. Kurtas, dhotis, sarees, or salwar suits preferred.',
            'Leave footwear at outer gali cloakrooms. Walk through temple lane barefoot.',
            'Strictly prohibited inside the sanctum. Keep in safe bag or at authorized locker.',
            'Narrow traditional alleys; police and temple marshals manage crowd surges.',
            'Open to all devotees showing devotion to Thakur Banke Bihari.',
            0, 1, 0, 350, 1,
            'https://www.bihariji.org/'
        ),
        (
            3, 3,
            '06:30 AM - 12:00 PM & 02:00 PM - 09:30 PM',
            '06:30 AM (Shringar Aarti)',
            '07:00 PM (Sandhya Aarti)',
            'General Darshan: 07:00 AM - 11:30 AM, 02:00 PM - 09:00 PM',
            'Aarti passes (Sugam Darshan) can be booked online via Shri Ram Janmabhoomi Teerth Kshetra portal. Senior citizen battery cart assistance available.',
            'Entry is completely Free. Online Sugam Darshan pass is Free upon slot availability. Sample Prasad Packet: Free distribution.',
            'Traditional attire encouraged. Decent, respectful clothing mandatory. Leather belts should be removed if requested.',
            'Massive mechanized computerized shoe deposit counters at the Pilgrim Facilitation Centre.',
            'Smartphones, electronic keys, earphones, bags are prohibited inside sanctum. Central Pilgrim Lockers available free of cost.',
            'Multi-layer CISF and UP Police security screening. Carry original Aadhaar/Passport.',
            'Devotees of all peaceful traditions are welcome to experience the sacred heritage.',
            1, 1, 1, 200, 1,
            'https://srjbtkshetra.org/'
        ),
        (
            4, 4,
            '03:00 AM - 11:00 PM',
            '03:00 AM (Mangala Aarti), 11:15 AM (Bhog Aarti)',
            '07:00 PM (Sandhya Aarti), 10:30 PM (Shayan Aarti)',
            'General Queue: 04:00 AM - 11:00 AM, 12:00 PM - 06:30 PM, 08:30 PM - 10:30 PM',
            'Sugam Darshan (VIP pass) available online for ₹300 per person. Senior citizen priority queue available at Gate 4.',
            'General Entry: Free. Sugam Darshan pass: ₹300 (sample official fee). Rudrabhishek pooja: ₹450 - ₹1,500.',
            'Dhoti/Kurta for men and Saree/Salwar for women strongly advised for Sparsh Darshan (touching lingam) during morning hours.',
            'Free electronic shoe lockers at Corridor entrance Gates 1, 2, 3 and 4.',
            'Mobiles and cameras not permitted in the inner Sanctum. Allowed in the outer corridor areas subject to token deposit rules.',
            'Corridor is well guarded. Modern baggage scanners and biometric verification for special darshan tickets.',
            'Visitors from all cultures and nations are warmly welcomed through the Vishwanath Corridor.',
            1, 1, 1, 150, 1,
            'https://shrikashivishwanath.org/'
        ),
        (
            5, 5,
            'Open 24 hours daily. Evening Maha Aarti starts around 06:45 PM (Summer) / 06:00 PM (Winter).',
            '05:30 AM (Subah-e-Banaras Morning Aarti)',
            '06:45 PM (Grand Dashashwamedh Maha Ganga Aarti)',
            'Visitors can witness Aarti from stairs or reserved boats on the river.',
            'Boat viewing available. Hand-rowed and electric bajra boats can be chartered.',
            'Ghat viewing is Free. Boat viewing: Sample ₹150 - ₹300 per person on shared boat; ₹1,500 - ₹3,500 for private boat.',
            'Modest, casual comfortable clothing. Shawl recommended during winter evenings.',
            'Footwear allowed on upper ghats; remove shoes when descending close to holy water.',
            'Photography and videography permitted from ghats and boats. Drone flying strictly prohibited without official clearance.',
            'Tourist police presence. Beware of unauthorized touts offering overpriced rituals.',
            'Universal access. Travelers of all beliefs and nations gather harmoniously at the Ghat.',
            0, 0, 0, 300, 1,
            'https://varanasi.nic.in/'
        ),
        (
            6, 6,
            '04:00 AM - 08:00 PM (Boat rides operate until sunset)',
            '05:00 AM (Morning Sangam Aarti)',
            '06:30 PM (Triveni Sandhya Aarti)',
            'Bathing and boat darshan open continuously through the day.',
            'Motorized and manual pilgrim boats take devotees directly to the confluence point for holy snan with safety life jackets.',
            'Ghat access: Free. Boat to Sangam point: Sample ₹100 - ₹200 per head (shared) or ₹800 - ₹1,500 (private boat for family).',
            'Decent modest attire. Bring change of clothes for after holy dip. Changing rooms available at Sangam ghats.',
            'Remove shoes before boarding boats or stepping on holy sand near the water.',
            'Allowed for personal photography. Avoid filming other pilgrims bathing.',
            'Jal Police and SDRF rescue boats deployed on the river 24x7 with life buoys.',
            'Open to all seekers of peace and holy river blessings.',
            1, 1, 1, 400, 1,
            'https://prayagraj.nic.in/'
        ),
        (
            7, 7,
            'Open 24 hours. Peak evening Aarti: 06:00 PM (Winter) / 06:45 PM (Summer).',
            '05:30 AM (Prabhat Ganga Aarti)',
            '06:30 PM (Maha Ganga Aarti Har Ki Pauri)',
            'Best to reach the ghat 1 hour prior to Aarti to secure comfortable seating on the steps.',
            'Separate seating area available on Malviya Dweep for senior citizens and families.',
            'Ghat access is completely Free. Diyas and flower leaf cups: ₹20 - ₹50.',
            'Respectful clothing. Shoulders and knees covered.',
            'Remove footwear when stepping onto the marble ghat steps. Footwear stalls operate at token rates (₹5 - ₹10).',
            'Photography allowed on ghat steps. Respect devotees taking holy bath.',
            'Police personnel and Ganga Sabha volunteers manage crowd safety.',
            'All faiths are welcome to witness the tranquil spiritual spectacle.',
            1, 1, 1, 200, 1,
            'https://haridwar.nic.in/'
        ),
        (
            8, 8,
            '05:00 AM - 09:00 PM',
            '05:30 AM (Morning Yoga & Havan)',
            '06:00 PM (Parmarth Niketan Ganga Aarti)',
            'Open for morning meditation, yoga sessions, and evening prayer along the Ganges.',
            'Wheelchair ramp available at Parmarth Niketan Ashram entrance.',
            'Free entry to ghat and aarti. Donations welcome for ashram seva.',
            'Comfortable modest attire. White or light clothing common for yoga/meditation.',
            'Remove shoes at designated ashram shoe counters.',
            'Allowed; respectful filming permitted.',
            'Very safe, tranquil spiritual atmosphere with active ashram security.',
            'Global center for interfaith seekers and yoga practitioners worldwide.',
            1, 1, 0, 150, 1,
            'https://www.parmarth.org/'
        ),
        (
            9, 9,
            '04:00 AM - 09:00 PM (Seasonal: May to November)',
            '04:00 AM (Maha Abhishek & Rawal Aarti)',
            '06:30 PM (Shayan Aarti)',
            'Darshan opens after 06:00 AM till 03:00 PM, and 05:00 PM till 08:30 PM.',
            'Priority queue for senior citizens and pilgrims with disabilities. Helicopter booking available from Phata/Guptkashi via IRCTC Heli Yatra portal.',
            'General Darshan: Free. Helicopter shuttle: Approx ₹5,500 - ₹8,500 roundtrip (IRCTC regulated sample price). Special Pooja: ₹1,500+.',
            'Warm woollen clothing mandatory. Traditional modest garments under warm jackets.',
            'Deposit shoes at temple shoe stand outside the stone courtyard.',
            'Strictly prohibited inside the stone sanctum. Allowed in the temple courtyard and mountain plateau.',
            'ITBP and Uttarakhand Police deployed. Mandatory biometric medical registration on Chardham Yatra portal before travel.',
            'Welcoming to all pilgrims of Sanatana faith and respectful spiritual seekers.',
            0, 1, 0, 50, 1,
            'https://badrinath-kedarnath.gov.in/'
        ),
        (
            10, 10,
            '04:30 AM - 09:00 PM (Seasonal: May to November)',
            '04:30 AM (Maha Abhishek)',
            '06:00 PM (Geet Govind & Shayan Aarti)',
            'Darshan: 06:30 AM - 12:00 PM, 03:00 PM - 09:00 PM.',
            'Special Pooja booking available online via BKTC portal. Tapt Kund natural hot sulphur spring bath before entering temple.',
            'General Darshan: Free. Special Abhishek tickets: Sample ₹1,200 - ₹2,500 per person.',
            'Warm traditional attire. Woollen jackets and thermals advised due to cold altitude.',
            'Shoe counters beside Tapt Kund and before temple steps.',
            'Mobile phones not permitted inside the inner Garbhagriha.',
            'Disaster management teams, SDRF, and local police on round-the-clock duty.',
            'Open to all devotees and spiritual travelers.',
            1, 1, 1, 100, 1,
            'https://badrinath-kedarnath.gov.in/'
        ),
        (
            11, 11,
            '06:30 AM - 01:00 PM & 05:00 PM - 09:30 PM',
            '06:30 AM (Mangala Aarti)',
            '07:30 PM (Sandhya Aarti)',
            'General Darshan operates continuously with brief bhog curtain intervals.',
            'VIP passes and senior citizen direct entry lane accessible via Moksha Dwar (Gate 2).',
            'General Entry: Free. Special Darshan / Flag hoisting ceremony (Dhwajaji): Booked through temple trust.',
            'Traditional clothes preferred. Pants/jeans allowed for general queue; dhotis/sarees preferred for inner darshan.',
            'Shoe deposit counter near the main entrance steps.',
            'Mobile phones, cameras, smart devices prohibited inside. Lockers available outside.',
            'Gujarat Police security checkpoint at entry gates.',
            'Warmly open to all devotees of Lord Krishna.',
            1, 1, 1, 150, 1,
            'https://dwarkadhish.org/'
        ),
        (
            12, 12,
            '06:00 AM - 10:00 PM',
            '07:00 AM (Pratah Aarti)',
            '07:00 PM (Sandhya Aarti followed by Light & Sound Show)',
            'Darshan continuously available throughout the day.',
            'Wheelchair accessibility throughout the seafront promenade and temple hall. Electric carts for elderly.',
            'Entry is Free. Light & Sound Show (Jay Somnath): Sample ₹30 (general), ₹50 (VIP seat).',
            'Decent traditional clothing. Shorts, mini skirts, and sleeveless shirts strictly not allowed.',
            'Shoe counter at the entrance square with clean token management.',
            'Cameras, mobile phones, electronics strictly prohibited inside. Free digital lockers available.',
            'Comprehensive CISF and Gujarat Police security with modern baggage scanners.',
            'Devotees of all backgrounds are welcome; non-Hindus register briefly at office desk as per longstanding temple trust protocol.',
            1, 1, 1, 100, 1,
            'https://somnath.org/'
        ),
        (
            13, 13,
            '05:00 AM - 10:00 PM (Winter) / 04:00 AM - 10:00 PM (Summer)',
            '05:00 AM (Khidmat ceremony - morning prayer)',
            '07:00 PM (Dua ceremony - evening prayer)',
            'Ziyarat (Darshan) available throughout the day inside the silver sanctum.',
            'Senior assistance through authorized Khadims; golf carts available from inner parking to Dargah chowk.',
            'Entry is Free. Chaddar offering: Sample ₹200 - ₹500 (optional). Tabarruk (Prasad/sweet rice): Free.',
            'Head must be covered at all times (scarf, rumal, topi). Modest clothing covering arms and legs.',
            'Shoe keepers at Dargah gates (Nizam Gate & Buland Darwaza) for ₹10 - ₹20.',
            'Photography permitted in open courtyards; strictly prohibited inside the inner tomb sanctum.',
            'Rajasthan Police checkpoint; beware of unofficial brokers insisting on forced donations.',
            'Universal welcome to people of all religions, castes, and nationalities in true Sufi spirit.',
            1, 1, 1, 150, 1,
            'https://ajmerdargah.info/'
        ),
        (
            14, 14,
            '06:30 AM - 08:30 PM (Afternoon break 01:30 PM - 03:00 PM)',
            '06:30 AM (Mangala Aarti)',
            '07:00 PM (Sandhya Aarti)',
            'Darshan queue leads up silver-plated steps to the four-faced idol of Lord Brahma.',
            'Senior citizen entry via side ramp to bypass main high staircase.',
            'Entry: Free. Pushkar Lake Ghat Pooja: Sample ₹51 - ₹201 (optional Brahmin blessing).',
            'Modest clothing. Modesty respected throughout the holy city of Pushkar.',
            'Footwear must be taken off at the foot of temple stairs.',
            'Mobile phones allowed outside; photography inside the inner Garbha Griha is prohibited.',
            'Local temple committee and police monitoring.',
            'Devotees and travelers of all paths are welcome.',
            1, 1, 0, 100, 1,
            'https://rajasthan.gov.in/'
        ),
        (
            15, 15,
            'Open 24 hours daily. Guru Granth Sahib Prakash at 04:00 AM, Sukhasan at 10:00 PM.',
            '04:00 AM (Prakash Sri Guru Granth Sahib Ji)',
            '10:00 PM (Sukhasan Ceremony & Palki Sahib Procession)',
            'Darshan inside the Golden Sanctum runs through day and night as Gurbani Kirtan is sung live continuously.',
            'Wheelchairs provided free of cost at the main information office. Volunteer Sevadaars assist seniors through special elderly queues.',
            'Entry is 100% Free. Guru Ka Langar is 100% Free for everyone 24/7. Karah Prasad: ₹10 - ₹50 token.',
            'Head must be covered at all times (rumal/scarf available for free at entrance). Shoes and socks must be removed. Feet washed in holy foot-bath. Tobacco and alcohol strictly forbidden in the entire precinct.',
            'Massive free shoe and luggage storage counters (Joda Ghar) run with extreme devotion and care.',
            'Photography permitted around the outer Parikrama (marble walkway). Strictly prohibited inside the Golden Sanctum.',
            'SGPC Task Force ensures safety, peace, and serenity.',
            'All humans of every faith, nationality, gender, and social status are welcomed with open arms and immense love.',
            1, 1, 1, 100, 1,
            'https://sgpc.net/'
        ),
        (
            16, 16,
            '02:30 AM - 11:30 PM',
            '02:30 AM (Suprabhatam)',
            '11:00 PM (Ekanta Seva)',
            'Sarva Darshan (Free queue) and Special Entry Darshan (₹300 SEE ticket).',
            'Dedicated queue line for Senior Citizens (above 65) and Physically Challenged with free prasadam and battery car pickup.',
            'Free Sarva Darshan. Special Entry Darshan: ₹300 per person (sample official TTD price). Extra Laddus: ₹50 each.',
            'Strict traditional dress code: Men must wear Dhoti with Uttareeyam / Kurta Pyjama. Women must wear Saree or Salwar Kameez with Dupatta. Western jeans/trousers not permitted.',
            'Free shoe deposit counters at Vaikuntam Queue Complex and ATC.',
            'Strictly prohibited on Tirumala hill queue and sanctum. High-tech scanning and deposit counters.',
            'Multi-tier TTD Vigilance and Andhra Pradesh Special Police security checks.',
            'Non-Hindus can have darshan after signing a faith declaration form affirming reverence for Lord Venkateswara at TTD office.',
            1, 1, 1, 150, 1,
            'https://tirupatibalaji.ap.gov.in/'
        ),
        (
            17, 17,
            '05:00 AM - 01:00 PM & 03:00 PM - 09:00 PM',
            '05:30 AM (Spadika Linga Darshan & Aarti)',
            '08:30 PM (Ardha Jama Pooja & Palliyarai)',
            'Morning Spadika (Crystal) Linga darshan from 05:00 AM - 06:00 AM is highly auspicious.',
            'Wheelchair assistance available through the East Gopuram entrance.',
            'General Entry: Free. 22 Well Theertham Bathing guide assistance: Sample ₹25 per head (official) or ₹150 for family assistance.',
            'Men: Dhoti or pants with shirt/kurta. Women: Saree or Salwar suit. Drenched clothes after 22 Theertham bath must be changed before entering the sanctum.',
            'Shoe counters outside the East and West Gopuram gates.',
            'Cameras and phones prohibited inside the inner temple corridors. Safe lockers available.',
            'Tamil Nadu temple police and CISF monitors.',
            'All respectful visitors can witness the architectural wonder and obtain darshan.',
            1, 1, 1, 200, 1,
            'https://ramanathaswamy.hrce.tn.gov.in/'
        ),
        (
            18, 18,
            '05:00 AM - 12:30 PM & 04:00 PM - 10:00 PM',
            '05:00 AM (Thiruvanandal Pooja)',
            '09:30 PM (Palliarai Procession of Sundareswarar to Meenakshi shrine)',
            'Darshan of Goddess Meenakshi followed by Lord Sundareswarar.',
            'Special senior citizen queue tickets and battery cart assistance from parking to South Gopuram.',
            'General Darshan: Free. Special Darshan Queue: Sample ₹50 - ₹100. Thousand Pillar Hall: ₹10.',
            'Traditional attire mandatory. Men in dhotis/trousers with shirt. Women in sarees/salwar with dupatta. No shorts, caps, or sleeveless attire.',
            'Cloakrooms and shoe stands at all four majestic Gopuram entrances.',
            'Smartphones and cameras strictly banned inside the entire temple complex by High Court directive. Deposit in lockers outside.',
            'High level biometric and metal detector security at Gopuram portals.',
            'All visitors can visit the temple museum and corridors; inner sanctum darshan according to HR&CE Tamil Nadu regulations.',
            1, 1, 1, 150, 1,
            'https://maduraimeenakshi.hrce.tn.gov.in/'
        ),
        (
            19, 19,
            '04:30 AM - 10:30 PM',
            '04:30 AM (Kakad Aarti)',
            '06:00 PM (Dhoop Aarti), 10:00 PM (Shej Aarti)',
            'Continuous darshan of Sai Baba Samadhi in the main hall and Dwarkamai.',
            'Senior citizens (above 60) and physically challenged devotees get free VIP lane entry with one attendant via Gate 3.',
            'General Darshan: Free. Online VIP Aarti pass: Sample ₹400 - ₹600. Online VIP Darshan: Sample ₹200.',
            'Modest, decent clothing. All respectful casual and traditional attire welcomed.',
            'Huge centralized multi-counter shoe stands operated efficiently by the Sansthan.',
            'Mobiles permitted in premises on silent mode; photography inside Samadhi hall strictly prohibited.',
            'Shirdi Sansthan security and Maharashtra Police ensure seamless queue movement.',
            'Universal temple where followers of all world religions pray side-by-side.',
            1, 1, 1, 100, 1,
            'https://online.sai.org.in/'
        ),
        (
            20, 20,
            '05:30 AM - 09:00 PM',
            '05:30 AM (Mangal Aarti)',
            '07:00 PM (Sandhya Aarti followed by Ratri Pooja)',
            'Sparsh Darshan allowed in early morning hours (with traditional dress); Mukh Darshan continuous.',
            'VIP passes available for elders and pilgrims performing specialized Vedic rituals.',
            'General Entry: Free. VIP Darshan Pass: Sample ₹200. Special Pooja (Narayan Nagbali / Kalsarpa): Handled by authorized Gurujis.',
            'Traditional attire required for sanctum entry (Dhoti without shirt for men). Decent attire for outer darshan.',
            'Shoe counters located outside the stone boundary wall.',
            'Mobile phones not permitted inside sanctum.',
            'Local temple trust security and Nashik district administration.',
            'Open to all devotees wishing to seek the grace of Lord Shiva.',
            1, 1, 0, 150, 1,
            'https://trimbakeshwartrust.com/'
        ),
        (
            21, 21,
            '05:00 AM - 09:00 PM',
            '05:30 AM (Morning Chanting & Meditation)',
            '06:30 PM (Evening Chanting & Bodhi Tree Lighting)',
            'Continuous access to inner sanctum, Bodhi Tree meditation zone, and the diamond throne (Vajrasana).',
            'Full wheelchair ramps provided throughout the monument and park paths.',
            'Entry is Free. Camera permit fee: Sample ₹100. Video camera fee: Sample ₹300.',
            'Decent, modest attire. Shoulders and knees covered. Monastic robes or white/light clothing appreciated.',
            'Deposit footwear at the secure entrance kiosk before entering the inner park.',
            'Mobile phones are restricted inside during meditation hours or must be placed on silent mode.',
            'Peaceful presence of tourism security personnel and Buddhist monastic attendants.',
            'Open to pilgrims and travelers of every faith, nationality, and background.',
            1, 1, 1, 80, 1,
            'https://mahabodhi.com/'
        ),
        (
            22, 22,
            '05:00 AM - 11:00 PM',
            '05:00 AM (Mangala Alati)',
            '07:00 PM (Sandhya Alati), 10:30 PM (Pahuda Alati)',
            'Darshan through the Lion Gate (Singhadwara) into the Jagamohan and sanctum.',
            'Senior citizens and disabled devotees have designated queues during specific daytime slots.',
            'General Entry: Free. Special Paramanik Darshan: Regulated by Temple Administration. Mahaprasad (Khadya): Sample ₹150 - ₹300 for wholesome thali at Anand Bazar.',
            'Strict traditional Indian dress code: Dhoti/Kurta or Pyjama for men; Saree or Salwar suit for women. Western clothing strictly barred.',
            'Shoe counters outside Singhadwara (Lion’s Gate) and Western Gate.',
            'Smartphones, electronic cameras, leather products (wallets, belts) are strictly banned inside temple premises.',
            'Odisha Police and JTP (Jagannath Temple Police) command high security surveillance.',
            'In accordance with ancient tradition, orthodox Hindu practice is maintained inside the temple walls; all visitors of all cultures can view the deities during the world-famous Ratha Yatra and experience the grand heritage from the Raghunandan Library roof / surrounding complexes.',
            0, 1, 0, 200, 1,
            'https://jagannath.nic.in/'
        ),
        (
            23, 23,
            '05:00 AM - 09:30 PM',
            '05:30 AM (Morning Mass in Tamil)',
            '06:00 PM (Rosary & Evening Mass in English & Hindi)',
            'Mass services conducted daily in Tamil, Malayalam, Telugu, Hindi, and English.',
            'Fully accessible campus with wide paved paths, ramps, and sea breeze.',
            'Entry is completely Free. Candles and offering flowers: Sample ₹20 - ₹100.',
            'Decent modest attire covering shoulders and knees.',
            'Footwear can be removed at church entrance steps or kept in personal bags.',
            'Photography permitted on grounds; silence and respect required inside the sanctuary during Holy Mass.',
            'Peaceful coastal shrine with round-the-clock basilica security.',
            'Welcomes millions of pilgrims of all religions and communities seeking healing and blessings.',
            1, 1, 1, 100, 1,
            'https://velankannichurch.com/'
        ),
        (
            24, 24,
            '06:00 AM - 06:00 PM',
            '06:30 AM (Morning Meditation at Chaukhandi Stupa)',
            '05:30 PM (Sunset Chanting at Mulagandhakuti Vihara)',
            'Walking trails through ancient archaeological excavations and Dhamek Stupa park.',
            'Wheelchair accessible pathways through the ASI monument gardens.',
            'ASI Entry Ticket: Sample ₹25 (Indian citizens), ₹300 (Foreign nationals). Children under 15: Free.',
            'Casual, modest and respectful clothing suited for garden walking.',
            'Footwear allowed in the archaeological park; remove shoes when entering Buddhist shrines/temples.',
            'Photography permitted outdoors; video filming rules per Archaeological Survey of India.',
            'ASI monuments security and local Uttar Pradesh tourism police.',
            'Universally open to tourists, history enthusiasts, and spiritual seekers of all beliefs.',
            1, 1, 1, 100, 1,
            'https://asi.nic.in/'
        ),
        (
            25, 25,
            '07:00 AM - 07:00 PM (April-Sept) / 07:00 AM - 06:30 PM (Oct-March)',
            '08:30 AM (Morning Mass at Altar of the Chair)',
            '05:00 PM (Evening Solemn Mass)',
            'General Entry: 07:00 AM - 06:30 PM continuously',
            'Papal General Audiences on Wednesday mornings in St. Peter’s Square. Dome climb requires admission ticket (lift + stairs).',
            'Basilica Entry is Free. Dome Climb: €8 (stairs) / €10 (lift). Treasury Museum: €5.',
            'Strict Christian Modesty Dress Code: Shoulders and knees must be covered. Sleeveless shirts, short skirts, and low-cut tops strictly forbidden.',
            'Footwear required at all times. Comfortable walking shoes recommended for vast marble halls.',
            'Photography permitted without flash. Mobile phones must be on silent. Video tripods prohibited without press credential.',
            'Airport-style metal detector and x-ray screening at security colonnade.',
            'Pilgrims and visitors of all faiths and nations are warmly welcomed to pray and admire the sacred heritage.',
            1, 1, 0, 100, 1,
            'https://www.vatican.va/'
        ),
        (
            26, 26,
            '06:00 AM - 06:00 PM daily',
            '06:30 AM (Morning Buddhist Chanting)',
            '05:30 PM (Sunset Meditation & Butter Lamp Lighting)',
            'Continuous peaceful circumambulation (Parikrama) around the sacred Marker Stone and Puskarini pond.',
            'Wheelchair accessible pathways and electric rickshaws available through the Sacred Garden monastic zone.',
            'Entry Ticket: NPR 200 (SAARC nationals) / NPR 500 (Foreign nationals). Mahabodhi Society meditation center is open to all.',
            'Modest attire. White or light colors preferred. Shoulders and knees covered.',
            'Footwear strictly prohibited inside the inner Maya Devi Temple compound. Free shoe stand outside.',
            'Photography prohibited directly over the sacred Marker Stone. Allowed in outer Sacred Garden and Puskarini pond.',
            'UNESCO World Heritage security and Nepal Armed Police Force monitor peace and serenity.',
            'Universal welcome to monks, pilgrims, and peaceful travelers of all religions worldwide.',
            1, 1, 1, 120, 1,
            'https://lumbinidevtrust.gov.np/'
        ),
        (
            27, 27,
            '04:00 AM - 09:00 PM (Inner Sanctum doors open 05:00 AM - 12:00 PM & 05:00 PM - 07:00 PM)',
            '05:30 AM (Pratah Mahasnana & Aarti)',
            '06:30 PM (Grand Bagmati Ganga-style Sandhya Maha Aarti)',
            'Continuous darshan from western and eastern courtyard; evening Bagmati aarti is spectacular with lamps and Vedic music.',
            'Special queue assistance for elderly pilgrims and Sadhus; resting pavilions available along holy ghats.',
            'Temple Entry for Hindu devotees is Free. ASI heritage fee for foreign nationals to view courtyard: NPR 1,000.',
            'Traditional modest Indian/Nepali attire encouraged (Dhoti/Kurta, Saree/Kurtha). Leather belts and items not allowed in inner sanctum.',
            'Shoe deposit counters available outside the Western Gate.',
            'Photography strictly prohibited inside inner courtyard; permitted along the eastern ghats across the river.',
            'Nepal Police and Pashupati Area Development Trust (PADT) security.',
            'Orthodox inner sanctum traditions maintained; non-Hindu visitors can view the majestic pagoda and Aarti from the eastern bank of Bagmati River.',
            1, 1, 0, 150, 1,
            'https://pashupati.org.np/'
        ),
        (
            28, 28,
            'Church of Holy Sepulchre: 05:00 AM - 08:00 PM; Western Wall: Open 24 hours daily',
            '06:00 AM (Holy Sepulchre Morning Liturgy)',
            '06:00 PM (Evening Vespers & Shabbat twilight prayers)',
            'Access to Golgotha, the Tomb of Christ (Aedicule), and the Western Wall plaza operates continuously.',
            'Ramps for wheelchair access lead to Western Wall plaza and main Church of Holy Sepulchre courtyard.',
            'Entry to both sacred landmarks is completely Free.',
            'Modest dress required: Shoulders and knees covered. At the Western Wall, men must wear a head covering (kippah/hat, free kippahs available).',
            'Footwear permitted throughout; respectful quiet conduct required.',
            'Photography permitted outside Shabbat; strictly prohibited at the Western Wall on Friday night through Saturday night (Shabbat).',
            'Comprehensive security checkpoints with metal detectors at all Old City quarter entrances.',
            'Visitors and pilgrims of all faiths and traditions are welcomed to pray and witness sacred history.',
            1, 1, 0, 100, 1,
            'https://thekotel.org/'
        ),
        (
            29, 29,
            'Open 24 hours continuously every day',
            '05:00 AM (Fajr Morning Prayer)',
            '08:00 PM (Isha Evening Prayer)',
            'Continuous Tawaf (circumambulation of Kaaba) and Sa\'i between Safa and Marwah for Umrah and Hajj.',
            'Free electric golf carts and manual wheelchair assistance available on upper Tawaf and Sa\'i floors for seniors and disabled pilgrims.',
            'Entry for pilgrimage is Free under authorized Nusuk pilgrimage permits.',
            'Men in Ihram (two unstitched white towels) for Umrah; modest Islamic attire for regular prayer. Women in loose modest Abaya covering entire body except face and hands.',
            'Shoe racks provided at all majestic King Abdulaziz and King Fahd gates with digital locator numbers.',
            'Smartphones allowed for personal memory; commercial filming and tripods strictly barred.',
            'General Directorate of Public Security and Special Emergency Forces ensure world-class safety.',
            'In accordance with Islamic law, entry into Mecca sanctuary is reserved for Muslim pilgrims; all global seekers can study and appreciate its spiritual heritage.',
            1, 1, 1, 80, 1,
            'https://www.nusuk.sa/'
        ),
        (
            30, 30,
            'Open 24 hours daily. Main shrine ceremonies: 08:30 AM - 04:30 PM',
            '08:30 AM (Morning Shinto Prayer & Flute Offering)',
            '04:00 PM (Sunset Kagura Ritual)',
            'Hike through the Senbon Torii mountain trail open day and night with serene lantern lighting.',
            'Lower shrine precinct is flat and accessible; upper mountain path consists of stone steps.',
            'Entry to shrine grounds and Torii gate trails is completely Free.',
            'Respectful, comfortable casual attire. Modesty appreciated during sacred bowing ceremonies.',
            'Footwear worn on trails; remove shoes only when stepping onto tatami shrine pavilions.',
            'Photography permitted along the torii trails. Refrain from filming priests during sacred inner ceremonies.',
            'Very safe, tranquil mountain paths with emergency call boxes.',
            'Welcoming to people of all backgrounds, cultures, and beliefs to experience Shinto nature reverence.',
            1, 1, 0, 200, 1,
            'https://inari.jp/'
        ),
        (
            31, 31,
            '07:00 AM - 09:00 PM daily',
            '07:30 AM (Morning Pilgrim Mass)',
            '07:30 PM (Evening Pilgrim Blessing Mass & Botafumeiro Ceremony)',
            'Continuous visits to the Crypt of Saint James and ceremonial embracing of the statue of the Apostle.',
            'Ramp entrance via the Quintana Square (Plaza de la Quintana) and elevator to museum areas.',
            'Entry to Cathedral is Free. Cathedral Museum, Pórtico de la Gloria, and Roof tour tickets: €12 - €15.',
            'Modest, respectful attire. Backpacks from Camino pilgrims must be deposited in nearby luggage lockers before entering.',
            'Footwear worn throughout cathedral.',
            'Photography without flash permitted; silence during Holy Mass.',
            'Galician police and cathedral wardens.',
            'Welcomes hundreds of thousands of backpackers, hikers, and pilgrims of all faiths walking the Camino.',
            1, 1, 0, 80, 1,
            'https://catedraldesantiago.es/'
        )
    ]

    cursor.executemany(
        """
        INSERT INTO religious_site_details (
            id, destination_id, opening_hours, morning_aarti_time, evening_aarti_time, darshan_timings,
            special_darshan_info, entry_fee_info, dress_code, footwear_rules, phone_camera_rules,
            security_info, non_hindu_entry_rules, wheelchair_accessible, senior_priority_darshan,
            battery_car_available, walking_distance_meters, medical_facility_nearby, official_booking_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        site_details_data
    )

    # Seed Pilgrimage Circuits
    # (id, name, slug, description, states_covered, total_days_recommended, theme, image_url)
    circuits_data = [
        (
            1,
            'Uttarakhand Char Dham Yatra',
            'chardham-uttarakhand',
            'The holy Himalayan pilgrimage to the sacred shrines of Haridwar, Rishikesh, Kedarnath, and Badrinath nestled in the majestic peaks.',
            'Uttarakhand',
            10,
            'Moksha & Himalayan Divine Grace',
            'https://images.unsplash.com/photo-1626014303757-6466336e4f3a?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            2,
            'Braj Bhoomi Krishna Circuit',
            'braj-bhoomi-krishna',
            'Walk in the divine steps of Lord Krishna through Mathura, Vrindavan, Goverdhan, and sacred Yamuna ghats with enchanting aartis and devotion.',
            'Uttar Pradesh',
            3,
            'Vaishnava Bhakti & Divine Love',
            'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            3,
            'Kashi - Prayagraj - Ayodhya Moksha Circuit',
            'kashi-prayagraj-ayodhya',
            'The eternal sacred triangle of Sanatana Dharma: Lord Shiva in Kashi, the holy Triveni Sangam in Prayagraj, and Lord Rama’s birthplace in Ayodhya.',
            'Uttar Pradesh',
            5,
            'Tirtharaj, Moksha & Ram Lalla Darshan',
            'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            4,
            'Gujarat Coastal Sacred Circuit',
            'gujarat-coastal-circuit',
            'Visit the western jewel of Char Dham at Dwarkadhish Jagat Mandir and the premier Jyotirlinga at Somnath on the azure Arabian seacoast.',
            'Gujarat',
            4,
            'Coastal Jyotirlinga & Krishna Capital',
            'https://images.unsplash.com/photo-1621847468516-1ed5d0df56fe?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            5,
            'Sufi & Brahma Spiritual Circuit (Rajasthan)',
            'rajasthan-ajmer-pushkar',
            'A harmonious spiritual odyssey blending the timeless Sufi devotion at Ajmer Sharif Dargah with the cosmic reverence of Pushkar Brahma Temple.',
            'Rajasthan',
            3,
            'Interfaith Harmony, Sufi Love & Vedic Antiquity',
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            6,
            'Tamil Nadu Divine Dravidian Circuit',
            'tamilnadu-madurai-rameswaram',
            'Marvel at the ancient architecture of Madurai Meenakshi Amman Temple and complete the Char Dham sacred bath across 22 Theerthams in Rameswaram.',
            'Tamil Nadu',
            4,
            'Dravidian Temple Grandeur & Jyotirlinga Snan',
            'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            7,
            'Maharashtra Jyotirlinga & Sai Bhakti',
            'maharashtra-shirdi-trimbakeshwar',
            'Seek peace and miracles at the Samadhi of Sai Baba in Shirdi, coupled with the ancient Godavari Jyotirlinga at Trimbakeshwar.',
            'Maharashtra',
            3,
            'Shraddha, Saburi & Trimbakeshwar Mahadev',
            'https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=1200&q=80'
        ),
        (
            8,
            'Buddhist Enlightenment Pilgrimage',
            'buddhist-circuit-bodhgaya',
            'Trace the enlightened footsteps of Lord Buddha from Bodh Gaya’s sacred Bodhi Tree to Sarnath Deer Park where the first Dhamma sermon was delivered.',
            'Bihar, Uttar Pradesh',
            4,
            'Inner Peace, Dhamma & Mindfulness',
            'https://images.unsplash.com/photo-1590766940554-634a7ed41450?auto=format&fit=crop&w=1200&q=80'
        )
    ]

    cursor.executemany(
        "INSERT INTO circuits (id, name, slug, description, states_covered, total_days_recommended, theme, image_url) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        circuits_data
    )

    # Seed Circuit Destinations mapping
    # (id, circuit_id, destination_id, day_number, sequence_order, notes)
    circuit_destinations_data = [
        # Char Dham Yatra
        (1, 1, 7, 1, 1, 'Haridwar: Holy dip at Har Ki Pauri and evening Ganga Aarti'),
        (2, 1, 8, 2, 2, 'Rishikesh: Triveni Ghat aarti and ashram meditation'),
        (3, 1, 9, 4, 3, 'Kedarnath: Helicopter/Trek to sacred Jyotirlinga'),
        (4, 1, 10, 7, 4, 'Badrinath: Badri Vishal darshan and Tapt Kund holy bath'),
        
        # Braj Bhoomi
        (5, 2, 1, 1, 1, 'Mathura: Krishna Janmasthan and Dwarkadhish morning darshan'),
        (6, 2, 2, 2, 2, 'Vrindavan: Banke Bihari, ISKCON and evening Prem Mandir musical fountains'),
        
        # Kashi - Prayagraj - Ayodhya
        (7, 3, 4, 1, 1, 'Varanasi: Kashi Vishwanath Jyotirlinga & Golden Temple corridor'),
        (8, 3, 5, 2, 2, 'Varanasi: Dashashwamedh Ghat sunrise boat ride & evening Maha Aarti'),
        (9, 3, 6, 3, 3, 'Prayagraj: Holy Snan at Triveni Sangam & Bade Hanuman Ji darshan'),
        (10, 3, 3, 4, 4, 'Ayodhya: Shri Ram Janmabhoomi Mandir & Saryu Aarti'),

        # Gujarat
        (11, 4, 11, 1, 1, 'Dwarka: Dwarkadhish Jagat Mandir, Gomti Sangam and Bet Dwarka boat ride'),
        (12, 4, 12, 3, 2, 'Somnath: First Jyotirlinga darshan and Sound & Light evening show'),

        # Rajasthan
        (13, 5, 13, 1, 1, 'Ajmer: Ziyarat at Khwaja Moinuddin Chishti Dargah and Sufi Qawwali'),
        (14, 5, 14, 2, 2, 'Pushkar: Holy bath at Pushkar Lake and sacred Brahma Temple darshan'),

        # Tamil Nadu
        (15, 6, 18, 1, 1, 'Madurai: Meenakshi Amman Temple exploration and Hall of Thousand Pillars'),
        (16, 6, 17, 3, 2, 'Rameswaram: Ramanathaswamy 22 Theertham holy dip, Agni Theertham, and Dhanushkodi'),

        # Maharashtra
        (17, 7, 19, 1, 1, 'Shirdi: Sai Baba Samadhi darshan, Dwarkamai and Gurusthan'),
        (18, 7, 20, 2, 2, 'Trimbakeshwar: Trimbakeshwar Jyotirlinga darshan and Kushavarta Kund'),

        # Buddhist Circuit
        (19, 8, 21, 1, 1, 'Bodh Gaya: Mahabodhi Temple, meditation under the Bodhi Tree & monasteries'),
        (20, 8, 24, 3, 2, 'Sarnath: Dhamek Stupa, Deer Park and Archaeological Museum')
    ]

    cursor.executemany(
        "INSERT INTO circuit_destinations (id, circuit_id, destination_id, day_number, sequence_order, notes) VALUES (?, ?, ?, ?, ?, ?)",
        circuit_destinations_data
    )

    # Seed Festivals with verified dates and crowd information
    festivals_data = [
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
        (19, 22, 'Puri Ratha Yatra (Festival of Chariots)', 'The supreme spectacle of Sanatana Dharma where Lord Jagannath, Balabhadra, and Subhadra journey on majestic wooden chariots to Gundicha Temple.', 'June - July', 'Ashadha Shukla Dwitiya (June/July)', 'Extremely Crowded', 'Pulling of Nandighosha chariot, Chhera Pahanra sweep by Puri Gajapati Maharaja')
    ]

    cursor.executemany(
        "INSERT INTO festivals (id, destination_id, name, description, dated_info_month, typical_dates_range, crowd_level, key_rituals) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        festivals_data
    )

    # Seed Hotels & Dharamshalas (Authentic pure-veg, ashrams, senior-accessible stays)
    # (id, destination_id, name, type, address, contact_phone, price_per_night, rating, is_pure_veg, is_senior_friendly, has_wheelchair_ramp, has_lift, proximity_to_temple_km, image_url)
    hotels_data = [
        # Mathura & Vrindavan
        (1, 1, 'Shri Krishna Janmasthan Yatri Niwas', 'Dharamshala / Ashram', 'Opposite Janmasthan Gate 3, Mathura', '+91 565 2423888', 850.0, 4.4, 1, 1, 1, 1, 0.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (2, 2, 'MVT Guesthouse & Ashram', 'Dharamshala / Ashram', 'Bhakti Vedanta Swami Marg, Raman Reti, Vrindavan', '+91 565 2540050', 1600.0, 4.7, 1, 1, 1, 1, 0.8, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
        (3, 2, 'Brij View Premier Suites', 'Standard Hotel', 'Near Prem Mandir, Chhatikara Road, Vrindavan', '+91 9897012345', 2800.0, 4.5, 1, 1, 1, 1, 0.5, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),

        # Ayodhya
        (4, 3, 'Birla Yatri Niwas Dharamshala', 'Dharamshala / Ashram', 'Near Ram Janmabhoomi Complex, Ayodhya', '+91 5278 232230', 950.0, 4.3, 1, 1, 1, 1, 0.4, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (5, 3, 'Shri Ram Hotel & Heritage Suites', 'Standard Hotel', 'Tedhi Bazar, Near Saryu Ghat, Ayodhya', '+91 5278 232555', 2400.0, 4.4, 1, 1, 1, 1, 0.6, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),

        # Varanasi
        (6, 4, 'Shri Kashi Vishwanath Yatri Nivas (Trust)', 'Dharamshala / Ashram', 'Vishwanath Corridor Gate 4, Varanasi', '+91 542 2392629', 1100.0, 4.6, 1, 1, 1, 1, 0.1, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (7, 4, 'BrijRama Palace Heritage Hotel', 'Heritage Haveli', 'Darbhanga Ghat, Dashashwamedh, Varanasi', '+91 542 2452222', 12500.0, 4.9, 1, 1, 1, 1, 0.3, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
        (8, 5, 'Hotel Ganges View & Retreat', 'Standard Hotel', 'Assi Ghat Road, Varanasi', '+91 542 2313218', 3200.0, 4.5, 1, 1, 0, 1, 1.2, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),

        # Prayagraj
        (9, 6, 'Kumbh Divine Sangam Tent & Guest Suites', 'Standard Hotel', 'Near Sangam Marg, Daraganj, Prayagraj', '+91 532 2500123', 2200.0, 4.3, 1, 1, 1, 1, 0.8, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),

        # Haridwar & Rishikesh
        (10, 7, 'Bhagirathi Atithi Griha (GMVN)', 'Budget Hotel', 'Near Har Ki Pauri, Haridwar', '+91 1334 227370', 1400.0, 4.2, 1, 1, 1, 1, 0.3, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (11, 8, 'Parmarth Niketan Ashram Stay', 'Dharamshala / Ashram', 'Swargashram, Rishikesh', '+91 135 2440077', 900.0, 4.8, 1, 1, 1, 1, 0.1, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),

        # Kedarnath & Badrinath
        (12, 9, 'GMVN Kedarnath Temple Colony Cottages', 'Dharamshala / Ashram', 'Near Kedarnath Temple Plateau, Kedarnath', '+91 135 2740896', 1800.0, 4.1, 1, 0, 0, 0, 0.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (13, 10, 'Shri Badrinath Guest House (Devasthanam)', 'Dharamshala / Ashram', 'Near Temple Gate, Badrinath', '+91 1381 222212', 1200.0, 4.3, 1, 1, 1, 1, 0.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),

        # Dwarka & Somnath
        (14, 11, 'Dwarkadhish Kokila Dhirubhai Ambani Yatri Niwas', 'Dharamshala / Ashram', 'Near ISKCON Gate, Dwarka', '+91 2892 234125', 1200.0, 4.6, 1, 1, 1, 1, 0.6, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (15, 12, 'Somnath Sagar Darshan Guest House (Trust)', 'Standard Hotel', 'Directly Facing Somnath Seafront, Somnath', '+91 2876 231212', 2100.0, 4.7, 1, 1, 1, 1, 0.2, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),

        # Ajmer & Pushkar
        (16, 13, 'Khwaja Heritage Haveli Stay', 'Heritage Haveli', 'Near Dargah Sharif Gate 2, Ajmer', '+91 145 2420999', 2600.0, 4.3, 0, 1, 0, 1, 0.3, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
        (17, 14, 'Brahma Horizon Resort & Suites', 'Standard Hotel', 'Panchkund Road, Pushkar', '+91 145 2772500', 3100.0, 4.5, 1, 1, 1, 1, 0.8, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),

        # Amritsar
        (18, 15, 'Sri Guru Ram Das Niwas (SGPC)', 'Dharamshala / Ashram', 'Golden Temple Complex, Amritsar', '+91 183 2553957', 500.0, 4.7, 1, 1, 1, 1, 0.1, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (19, 15, 'Ramada by Wyndham Amritsar', 'Luxury Resort', 'Hall Bazar, Near Golden Temple, Amritsar', '+91 183 5025555', 4800.0, 4.6, 1, 1, 1, 1, 0.9, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),

        # Tirupati
        (20, 16, 'Srinivasam Complex (TTD)', 'Dharamshala / Ashram', 'Near Tirupati Railway Station, Tirupati', '+91 877 2277777', 600.0, 4.5, 1, 1, 1, 1, 1.5, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (21, 16, 'Fortune Select Grand Ridge', 'Luxury Resort', 'Shilparamam Tirupati', '+91 877 6688888', 4900.0, 4.6, 1, 1, 1, 1, 3.2, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),

        # Rameswaram & Madurai
        (22, 17, 'Goswami Math Dharamshala', 'Dharamshala / Ashram', 'West Car Street, Rameswaram', '+91 4573 221234', 800.0, 4.2, 1, 1, 0, 1, 0.2, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (23, 17, 'Hotel Daiwik Rameswaram', 'Standard Hotel', 'NH 49, Near Rameswaram Temple, Rameswaram', '+91 4573 301222', 3600.0, 4.5, 1, 1, 1, 1, 1.0, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=800&q=80'),
        (24, 18, 'Heritage Madurai', 'Luxury Resort', 'Kochadai, Madurai', '+91 452 2385455', 5500.0, 4.7, 1, 1, 1, 1, 4.0, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),

        # Shirdi & Trimbakeshwar
        (25, 19, 'Shirdi Sai Ashram Bhakta Niwas (Sansthan)', 'Dharamshala / Ashram', 'Dindori Road, Shirdi', '+91 2423 258500', 500.0, 4.6, 1, 1, 1, 1, 0.7, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),
        (26, 20, 'Gajanan Maharaj Sansthan Bhakta Nivas', 'Dharamshala / Ashram', 'Near Trimbakeshwar Temple, Trimbakeshwar', '+91 2594 233215', 750.0, 4.4, 1, 1, 1, 1, 0.3, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80'),

        # Bodh Gaya & Puri
        (27, 21, 'Daijokyo Buddhist Monastery Guest House', 'Dharamshala / Ashram', 'Near Japanese Temple, Bodh Gaya', '+91 631 2200747', 1000.0, 4.7, 1, 1, 1, 1, 0.4, 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'),
        (28, 22, 'Shri Jagannath Bhakta Nivas', 'Dharamshala / Ashram', 'VIP Road, Puri', '+91 6752 222053', 900.0, 4.5, 1, 1, 1, 1, 0.8, 'https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=800&q=80')
    ]

    cursor.executemany(
        """
        INSERT INTO hotels (
            id, destination_id, name, type, address, contact_phone, price_per_night,
            rating, is_pure_veg, is_senior_friendly, has_wheelchair_ramp, has_lift,
            proximity_to_temple_km, image_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        hotels_data
    )

    # Seed Restaurants & Sattvic / Prasad / Langar Dining
    # (id, destination_id, name, cuisine_type, avg_cost_for_two, address, special_dishes, opening_hours, is_sattvic)
    restaurants_data = [
        (1, 1, 'Brijwasi Mithai & Bhojanalaya', 'Pure Vegetarian Thali', 350.0, 'Near Janmasthan, Mathura', 'Mathura Ke Special Pede, Hing Kachori with Dubki Aloo, Rabdi', '07:00 AM - 10:30 PM', 1),
        (2, 2, 'Govinda Restaurant (ISKCON)', 'Sattvic (No Onion/Garlic)', 450.0, 'ISKCON Temple Campus, Raman Reti, Vrindavan', 'Pure Sattvic Thali, Khichdi Prasadam, Paneer Makhanwala (No onion/garlic)', '08:00 AM - 09:30 PM', 1),
        (3, 3, 'Shri Ram Rasoi & Bhojanalaya', 'Sattvic (No Onion/Garlic)', 300.0, 'Near Ram Janmabhoomi Path, Ayodhya', 'Awadhi Sattvic Thali, Baati Chokha, Kheer', '07:30 AM - 10:00 PM', 1),
        (4, 4, 'Shri Annapurna Temple Rasoi', 'Temple Prasad / Mahaprasad', 0.0, 'Annapurna Mandir, Vishwanath Gali, Varanasi', 'Free Mahaprasad (Dal, Bhaat, Tarkari, Kheer) served with boundless love to all pilgrims', '11:00 AM - 03:00 PM', 1),
        (5, 4, 'Keshari Restaurant & Sattvic Bhoj', 'Pure Vegetarian Thali', 400.0, 'Near Dashashwamedh Ghat, Varanasi', 'Banarasi Thali, Baati Chokha, Malaiyyo (Winter seasonal sweet)', '08:00 AM - 11:00 PM', 1),
        (6, 6, 'Netram Mulchand Pure Veg Bhoj', 'Pure Vegetarian Thali', 350.0, 'Katla Road, Prayagraj', 'Traditional Desi Ghee Puri, Subzi, Jalebi and Dahi', '07:00 AM - 10:00 PM', 1),
        (7, 7, 'Mathura Walo Ki Pracheen Dukan', 'Pure Vegetarian Thali', 250.0, 'Moti Bazar, Haridwar', 'Puri Chhole, Halwa, Rabdi, Lassi', '06:30 AM - 10:30 PM', 1),
        (8, 8, 'Chotiwala Restaurant Since 1958', 'Pure Vegetarian Thali', 500.0, 'Swargashram, Ram Jhula, Rishikesh', 'Garhwali Thali, Paneer Butter Masala, Special Kheer', '07:30 AM - 10:30 PM', 1),
        (9, 10, 'Badri Vishal Prasad Bhandar', 'Temple Prasad / Mahaprasad', 150.0, 'Near Temple Gate, Badrinath', 'Poha, Khichdi, Laddu Prasadam, Herbal Himalayan Tea', '06:00 AM - 08:30 PM', 1),
        (10, 11, 'Toran Dining Hall (Gujarat Tourism)', 'Pure Vegetarian Thali', 350.0, 'Near Dwarkadhish Temple, Dwarka', 'Authentic Kathiyawadi Gujarati Thali, Kadhi, Bajra Rotla, Khichdi', '11:00 AM - 03:30 PM & 07:00 PM - 10:30 PM', 1),
        (11, 12, 'Somnath Trust Prasadam Bhojanalaya', 'Temple Prasad / Mahaprasad', 100.0, 'Somnath Temple Complex, Somnath', 'Traditional Gujarati Prasad Thali (Subzi, Dal, Roti, Rice, Sweet)', '11:00 AM - 03:00 PM & 06:30 PM - 09:30 PM', 1),
        (12, 13, 'Dargah Sharif Langar Khana', 'Multi-cuisine Veg', 0.0, 'Inside Dargah Sharif Courtyard, Ajmer', 'Sweet Saffron Rice (Zarda) & Tabarruk distributed freely from the historic Big Deg', '12:00 PM - 02:00 PM & 07:00 PM - 09:00 PM', 1),
        (13, 14, 'Pushkar Brahma Sattvic Kitchen', 'Sattvic (No Onion/Garlic)', 350.0, 'Main Market, Near Brahma Temple, Pushkar', 'Rajasthani Dal Baati Churma, Ker Sangri, Malpua', '08:00 AM - 10:00 PM', 1),
        (14, 15, 'Guru Ka Langar (Sri Harmandir Sahib)', 'Gurudwara Langar (Seva)', 0.0, 'Golden Temple Complex, Amritsar', 'Universal hot meals: Fresh hot rotis (served directly by sevadaars), Dal, Kheer, Subzi. 100% Free for everyone.', 'Open 24 hours continuously', 1),
        (15, 15, 'Bharawan Da Dhaba Since 1912', 'Pure Vegetarian Thali', 450.0, 'Near Town Hall, Amritsar', 'Amritsari Kulcha with Chhole, Dal Makhani, Fresh Sweet Lassi', '07:30 AM - 11:30 PM', 1),
        (16, 16, 'TTD Annaprasadam Complex', 'Temple Prasad / Mahaprasad', 0.0, 'Matrusri Tarigonda Vengamamba Complex, Tirumala', 'Sacred Tirumala Anna Prasadam: Hot rice, Sambar, Rasam, Chutney, Payasam served with supreme devotion to tens of thousands daily. 100% Free.', '09:00 AM - 11:00 PM', 1),
        (17, 16, 'Hotel Saravana Bhavan Tirupati', 'Pure Vegetarian Thali', 400.0, 'TP Area, Tirupati', 'Authentic South Indian Filter Coffee, Ghee Roast Dosa, Mini Tiffin', '06:00 AM - 10:30 PM', 1),
        (18, 17, 'Ram Nivas Traditional South Thali', 'Pure Vegetarian Thali', 250.0, 'South Car Street, Rameswaram', 'Chettinad Veg Thali on fresh Banana leaf, Rasam, Appalam', '07:00 AM - 09:30 PM', 1),
        (19, 18, 'Murugan Idli Shop', 'Pure Vegetarian Thali', 300.0, 'West Masi Street, Madurai', 'World-famous Melt-in-mouth Steamed Idlis with four fresh chutneys and Podi Ghee', '06:30 AM - 11:00 PM', 1),
        (20, 19, 'Shri Sai Sansthan Prasadalaya', 'Temple Prasad / Mahaprasad', 20.0, 'Nimgaon Road, Shirdi', 'Asia’s largest solar-powered kitchen serving wholesome Sattvic Mahaprasad: Dal, Rice, 2 Sabzis, Roti, Sweet for ₹20 (Free for children)', '10:00 AM - 10:00 PM', 1),
        (21, 21, 'Bodhi Tree Monastery Vegetarian Cafe', 'Sattvic (No Onion/Garlic)', 350.0, 'Near Mahabodhi Temple, Bodh Gaya', 'Tibetan Thukpa, Momos, Herbal Teas, Sattvic Rice bowls', '07:00 AM - 09:00 PM', 1),
        (22, 22, 'Ananda Bazar (Jagannath Temple Mahaprasad)', 'Temple Prasad / Mahaprasad', 200.0, 'Outer Courtyard, Jagannath Temple, Puri', 'Sacred Chhappan Bhog Mahaprasad: Kanika (sweet fragrant rice), Dalma, Besara, Khaja sweet cooked in earthenware pots', '12:00 PM - 05:00 PM', 1)
    ]

    cursor.executemany(
        """
        INSERT INTO restaurants (
            id, destination_id, name, cuisine_type, avg_cost_for_two, address,
            special_dishes, opening_hours, is_sattvic
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        restaurants_data
    )

    # Seed Vehicles for Pilgrimage & Senior travel
    # (id, vehicle_type, capacity, price_per_day, price_per_km, driver_allowance_per_day, ac_available, senior_friendly_comfort, features, image_url)
    vehicles_data = [
        (
            1,
            'Sedan (Maruti Dzire / Toyota Etios)',
            4,
            2400.0,
            12.0,
            400.0,
            1, 1,
            'Ideal for couples and small families. Boot space for 2 large luggage bags, air conditioned, sanitized, gentle driving guaranteed.',
            'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'
        ),
        (
            2,
            'SUV (Toyota Innova Crysta - Senior Recommended)',
            7,
            3800.0,
            17.0,
            500.0,
            1, 1,
            'Recommended for senior citizens: High seating, captain seats with lumbar support, smooth shock absorbers, low step board for easy entry, rear AC vents.',
            'https://images.unsplash.com/photo-1549399542-7e3f8b79c341?auto=format&fit=crop&w=800&q=80'
        ),
        (
            3,
            'Tempo Traveller (12-14 Seater Family Group)',
            13,
            5200.0,
            23.0,
            600.0,
            1, 1,
            'Perfect for extended family pilgrimage groups. Pushback reclining seats, LED screen with devotional audio/bhajans, ample luggage carrier, dual AC.',
            'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80'
        ),
        (
            4,
            'Tempo Traveller Deluxe (17-20 Seater Large Group)',
            19,
            6800.0,
            28.0,
            700.0,
            1, 1,
            'Spacious 2x1 luxury seating, high headroom, wide panoramic windows, air suspension, PA audio microphone for tour guide / kirtan.',
            'https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80'
        ),
        (
            5,
            'Electric Darshan Rickshaw (Local City Tour)',
            4,
            900.0,
            0.0,
            0.0,
            0, 1,
            'Eco-friendly battery-operated rickshaw specifically licensed for inner temple galis and ghat pathways where regular cars are prohibited (e.g. Vrindavan, Ayodhya, Varanasi).',
            'https://images.unsplash.com/photo-1596707255140-520e17621be0?auto=format&fit=crop&w=800&q=80'
        )
    ]

    cursor.executemany(
        """
        INSERT INTO vehicles (
            id, vehicle_type, capacity, price_per_day, price_per_km,
            driver_allowance_per_day, ac_available, senior_friendly_comfort, features, image_url
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        vehicles_data
    )

    # Seed Sample Demo Trips and Bookings for the Demo User
    trips_data = [
        (
            1, 2, 'Sacred Kashi & Ayodhya Family Tirth Yatra', 3,
            '[4, 5, 3]', '2026-11-10', 4, 3, 'seniors', 'relaxed', 'standard',
            24500.0, 'Senior-friendly pilgrimage for parents. Battery car passes required for Ayodhya Ram Mandir and Kashi Vishwanath Sugam Darshan.'
        )
    ]
    cursor.executemany(
        """
        INSERT INTO trips (
            id, user_id, title, circuit_id, destination_ids_json, start_date, total_days,
            travelers_count, traveler_profile, pace, budget_tier, estimated_total_cost, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        trips_data
    )

    trip_days_data = [
        (1, 1, 1, '2026-11-10', 'Day 1: Arrival in Kashi & Evening Ganga Aarti',
         'Arrival at Varanasi Airport / Railway Station. Check-in at wheelchair-friendly hotel near Dashashwamedh. Afternoon rest.',
         'Visit Sarnath Deer Park and Dhamek Stupa (gentle walking on paved garden paths).',
         'Attend the world-famous Maha Ganga Aarti at Dashashwamedh Ghat from a comfortable reserved family boat.', 4500.0),
        (2, 1, 2, '2026-11-11', 'Day 2: Kashi Vishwanath Jyotirlinga Darshan',
         'Early morning Sugam Darshan at Shri Kashi Vishwanath Temple via Corridor Gate 4 with battery car transit for parents.',
         'Sattvic lunch at Annapurna Rasoi followed by temple rest and visit to Sankat Mochan Hanuman Temple.',
         'Quiet twilight boat cruise along Manikarnika and Assi Ghats with Banarasi Thali dinner.', 5800.0),
        (3, 1, 3, '2026-11-12', 'Day 3: Journey to Ayodhya & Saryu Aarti',
         'Comfortable Innova Crysta drive to Ayodhya (approx 4 hours with tea stop). Hotel check-in.',
         'Relaxed visit to Kanak Bhawan and Hanuman Garhi temple with volunteer assistance.',
         'Peaceful evening Saryu River Aarti and illuminated Ram Ki Paidi walk.', 6200.0),
        (4, 1, 4, '2026-11-13', 'Day 4: Shri Ram Janmabhoomi Darshan & Departure',
         'Morning Sugam Darshan of Ram Lalla at Shri Ram Janmabhoomi Mandir using Senior Facilitation Center golf carts.',
         'Collect sacred Prasad, lunch at Shri Ram Rasoi, purchase local souvenirs and souvenirs.',
         'Return transfer to Ayodhya Dham Railway Station / Ayodhya Airport for departure with cherished memories.', 8000.0)
    ]
    cursor.executemany(
        """
        INSERT INTO trip_days (
            id, trip_id, day_number, date, title, morning_plan, afternoon_plan, evening_plan, estimated_cost
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        trip_days_data
    )

    # Sample Bookings
    bookings_data = [
        (1, 2, 'hotel', 6, '2026-11-10', '2026-11-12', 3, 2200.0, 'confirmed', 'Ground floor room requested for elderly parents. Need wheelchair assistance at check-in.'),
        (2, 2, 'vehicle', 2, '2026-11-10', '2026-11-13', 3, 15200.0, 'confirmed', 'Innova Crysta with senior-friendly captain seats and experienced polite driver.')
    ]
    cursor.executemany(
        """
        INSERT INTO bookings (
            id, user_id, booking_type, reference_id, start_date, end_date,
            guests_count, total_amount, status, special_requests
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        bookings_data
    )

    conn.commit()
    print("Database successfully seeded with comprehensive religious tourism data!")
