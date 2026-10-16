import json

def test_home_route(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Yatra" in res.data
    assert b"Sacred Pilgrimages" in res.data

def test_destinations_listing_and_filtering(client):
    # All destinations
    res = client.get('/destinations')
    assert res.status_code == 200
    assert b"Kashi Vishwanath" in res.data

    # Filter by state: Uttar Pradesh
    res_up = client.get('/destinations?state=Uttar+Pradesh')
    assert res_up.status_code == 200
    assert b"Ayodhya" in res_up.data or b"Mathura" in res_up.data

    # Filter by state: Punjab
    res_punjab = client.get('/destinations?state=Punjab')
    assert res_punjab.status_code == 200
    assert b"Golden Temple" in res_punjab.data

    # Filter by country: Vatican City
    res_vatican = client.get('/destinations?country=Vatican+City')
    assert res_vatican.status_code == 200
    assert b"St. Peter" in res_vatican.data

    # Filter by country: Nepal
    res_nepal = client.get('/destinations?country=Nepal')
    assert res_nepal.status_code == 200
    assert b"Lumbini" in res_nepal.data or b"Pashupatinath" in res_nepal.data

    # Filter by senior friendly
    res_senior = client.get('/destinations?senior_friendly=1')
    assert res_senior.status_code == 200

def test_destination_detail(client):
    res = client.get('/destinations/1')
    assert res.status_code == 200
    assert b"Shri Krishna Janmasthan" in res.data
    assert b"Darshan" in res.data and b"Aarti" in res.data
    assert b"Dress Code" in res.data

def test_circuits_routes(client):
    res = client.get('/circuits')
    assert res.status_code == 200
    assert b"Char Dham Yatra" in res.data

    res_detail = client.get('/circuits/chardham-uttarakhand')
    assert res_detail.status_code == 200
    assert b"Daily Stops" in res_detail.data

def test_festivals_and_map_routes(client):
    res_fest = client.get('/festivals')
    assert res_fest.status_code == 200
    assert b"Janmashtami" in res_fest.data

    res_map = client.get('/map')
    assert res_map.status_code == 200
    assert b"pilgrimage-map" in res_map.data

    res_api = client.get('/api/destinations')
    assert res_api.status_code == 200
    data = json.loads(res_api.data)
    assert len(data) >= 20

def test_hotels_and_restaurants_routes(client):
    res_h = client.get('/hotels')
    assert res_h.status_code == 200
    assert b"Ashrams" in res_h.data

    res_hd = client.get('/hotels/1')
    assert res_hd.status_code == 200

    res_r = client.get('/restaurants')
    assert res_r.status_code == 200
    assert b"Sattvic" in res_r.data

def test_vehicles_routes(client):
    res_v = client.get('/vehicles')
    assert res_v.status_code == 200
    assert b"Innova Crysta" in res_v.data

    res_vb = client.get('/vehicles/booking/1')
    assert res_vb.status_code == 200
    assert b"Book Vehicle" in res_vb.data

def test_planner_post(client):
    res = client.post('/planner', data={
        'destination_ids': [1, 2],
        'total_days': 2,
        'travelers_count': 2,
        'traveler_profile': 'seniors',
        'pace': 'relaxed',
        'budget_tier': 'standard'
    })
    assert res.status_code == 200
    assert b"Day 1:" in res.data
    assert b"Darshan" in res.data and b"Schedule" in res.data

def test_budget_calculator_route_and_api(client):
    res = client.get('/budget')
    assert res.status_code == 200
    assert b"Pilgrimage Expense" in res.data and b"Budget Calculator" in res.data

    api_res = client.post('/api/budget/calculate', json={
        'total_days': 4,
        'travelers_count': 3,
        'budget_tier': 'standard',
        'traveler_profile': 'family'
    })
    assert api_res.status_code == 200
    data = json.loads(api_res.data)
    assert data['grand_total'] > 0
    assert data['total_days'] == 4

def test_auth_workflow(client):
    # Registration
    res_reg = client.post('/register', data={
        'username': 'newpilgrim',
        'email': 'newpilgrim@test.in',
        'password': 'password123',
        'full_name': 'New Pilgrim Traveler',
        'phone': '+91 9999999999'
    }, follow_redirects=True)
    assert res_reg.status_code == 200
    assert b"Welcome to Yatra" in res_reg.data

    # Profile
    res_prof = client.get('/profile')
    assert res_prof.status_code == 200
    assert b"New Pilgrim Traveler" in res_prof.data

    # Logout
    res_logout = client.get('/logout', follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"signed out safely" in res_logout.data

def test_admin_authorization(client, auth_client, admin_client):
    # Anonymous cannot access admin
    res_anon = client.get('/admin/', follow_redirects=True)
    assert b"Access restricted to administrators" in res_anon.data

    # Normal user cannot access admin
    res_user = auth_client.get('/admin/', follow_redirects=True)
    assert b"Access restricted to administrators" in res_user.data

    # Admin user can access admin
    res_admin = admin_client.get('/admin/')
    assert res_admin.status_code == 200
    assert b"Administration" in res_admin.data
    assert b"Manage Destinations" in res_admin.data

def test_chatbot_endpoint(client):
    res = client.post('/api/chat', json={'message': 'What is the dress code for Kashi Vishwanath?'})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert 'reply' in data
    assert len(data['reply']) > 10

    # Multi-turn memory test
    res2 = client.post('/api/chat', json={
        'message': 'Are wheelchairs allowed there for my grandmother?',
        'history': [
            {'role': 'user', 'content': 'What is the dress code for Kashi Vishwanath?'},
            {'role': 'assistant', 'content': data['reply']}
        ]
    })
    assert res2.status_code == 200
    data2 = json.loads(res2.data)
    assert 'reply' in data2
    assert len(data2['reply']) > 10

def test_global_destinations_and_translator(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"yatraLangDropdown" in res.data
    assert b"yatraChatToggle" in res.data
    assert b"Global Pilgrimage Landmarks" in res.data

    res_api = client.get('/api/destinations?country=Vatican+City')
    assert res_api.status_code == 200
    data = json.loads(res_api.data)
    assert len(data) >= 1
    assert data[0]['country'] == 'Vatican City'
