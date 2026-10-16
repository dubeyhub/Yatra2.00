// Yatra Interactive Global Pilgrimage Map
document.addEventListener('DOMContentLoaded', function () {
    const mapElement = document.getElementById('pilgrimage-map');
    if (!mapElement) return;

    // Global view centered across sacred regions
    const map = L.map('pilgrimage-map').setView([24.0, 50.0], 4);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors | Yatra Global Sacred Pilgrimages'
    }).addTo(map);

    let markersLayer = L.layerGroup().addTo(map);

    // Color icons by category
    function getCategoryColor(category) {
        switch (category) {
            case 'temple': return '#c44d18'; // Saffron
            case 'sacred_river': return '#117864'; // Teal
            case 'gurudwara': return '#e67e22'; // Ochre Orange
            case 'mosque_dargah': return '#27ae60'; // Emerald Green
            case 'monastery': return '#8e44ad'; // Maroon/Purple
            case 'church': return '#2980b9'; // Blue
            default: return '#7f8c8d';
        }
    }

    function createCustomMarker(dest) {
        const color = getCategoryColor(dest.category);
        const markerHtml = `
            <div style="background-color: ${color}; width: 28px; height: 28px; border-radius: 50%; border: 3px solid #fff; box-shadow: 0 2px 6px rgba(0,0,0,0.3); display: flex; align-items: center; justify-content: center; color: #fff; font-size: 13px; font-weight: bold;">
                ✦
            </div>
        `;

        const icon = L.divIcon({
            html: markerHtml,
            className: 'custom-div-icon',
            iconSize: [28, 28],
            iconAnchor: [14, 14]
        });

        const marker = L.marker([dest.latitude, dest.longitude], { icon: icon });

        const seniorBadge = dest.senior_priority_darshan ? '<span class="amenity-pill">👴 Senior Priority</span>' : '';
        const wheelchairBadge = dest.wheelchair_accessible ? '<span class="amenity-pill">♿ Wheelchair</span>' : '';
        const batteryBadge = dest.battery_car_available ? '<span class="amenity-pill">🛺 Battery Car</span>' : '';
        const countryLabel = dest.country && dest.country !== 'India' ? `, ${dest.country}` : '';

        const popupContent = `
            <div style="font-family: inherit; max-width: 270px;">
                <h4 style="margin: 0 0 4px 0; color: #922b21; font-size: 1.1rem;">${dest.name}</h4>
                <div style="font-size: 0.85rem; color: #666; margin-bottom: 8px;">📍 ${dest.city}, ${dest.state}${countryLabel}</div>
                <div style="margin-bottom: 8px;">
                    ${seniorBadge} ${wheelchairBadge} ${batteryBadge}
                </div>
                <p style="font-size: 0.88rem; margin-bottom: 8px; line-height: 1.4;">${dest.description.substring(0, 100)}...</p>
                <a href="/destinations/${dest.id}" style="display: inline-block; background-color: #c44d18; color: #fff; padding: 4px 10px; border-radius: 4px; font-size: 0.82rem; font-weight: bold; text-decoration: none;">View Darshan & Timings →</a>
            </div>
        `;

        marker.bindPopup(popupContent);
        return marker;
    }

    function loadDestinations(country = '', state = '', category = '', seniorOnly = false) {
        markersLayer.clearLayers();
        let url = `/api/destinations?`;
        if (country) url += `country=${encodeURIComponent(country)}&`;
        if (state) url += `state=${encodeURIComponent(state)}&`;
        if (category) url += `category=${encodeURIComponent(category)}&`;
        if (seniorOnly) url += `senior_friendly=1&`;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                if (!data || data.length === 0) return;
                const bounds = [];
                data.forEach(dest => {
                    if (dest.latitude && dest.longitude) {
                        const marker = createCustomMarker(dest);
                        markersLayer.addLayer(marker);
                        bounds.push([dest.latitude, dest.longitude]);
                    }
                });
                if (bounds.length > 0 && !state && !country) {
                    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 12 });
                } else if (bounds.length > 0) {
                    map.fitBounds(bounds, { padding: [40, 40], maxZoom: 14 });
                }
            })
            .catch(err => console.error("Error loading map points:", err));
    }

    // Initial load
    loadDestinations();

    // Listen to map filter changes if filters present
    const mapCountryFilter = document.getElementById('map-country-filter');
    const mapStateFilter = document.getElementById('map-state-filter');
    const mapCategoryFilter = document.getElementById('map-category-filter');
    const mapSeniorFilter = document.getElementById('map-senior-filter');

    function applyMapFilters() {
        const country = mapCountryFilter ? mapCountryFilter.value : '';
        const state = mapStateFilter ? mapStateFilter.value : '';
        const category = mapCategoryFilter ? mapCategoryFilter.value : '';
        const seniorOnly = mapSeniorFilter ? mapSeniorFilter.checked : false;
        loadDestinations(country, state, category, seniorOnly);
    }

    if (mapCountryFilter) mapCountryFilter.addEventListener('change', applyMapFilters);
    if (mapStateFilter) mapStateFilter.addEventListener('change', applyMapFilters);
    if (mapCategoryFilter) mapCategoryFilter.addEventListener('change', applyMapFilters);
    if (mapSeniorFilter) mapSeniorFilter.addEventListener('change', applyMapFilters);
});
