// Yatra Interactive Pilgrimage Budget Calculator
document.addEventListener('DOMContentLoaded', function () {
    const budgetForm = document.getElementById('budget-calculator-form');
    if (!budgetForm) return;

    const daysInput = document.getElementById('calc-days');
    const travelersInput = document.getElementById('calc-travelers');
    const tierRadios = document.querySelectorAll('input[name="budget_tier"]');
    const profileRadios = document.querySelectorAll('input[name="traveler_profile"]');
    const vehicleSelect = document.getElementById('calc-vehicle');

    const totalDisplay = document.getElementById('calc-grand-total');
    const perPersonDisplay = document.getElementById('calc-per-person');
    const accomDisplay = document.getElementById('calc-breakdown-accom');
    const foodDisplay = document.getElementById('calc-breakdown-food');
    const transportDisplay = document.getElementById('calc-breakdown-transport');
    const darshanDisplay = document.getElementById('calc-breakdown-darshan');
    const miscDisplay = document.getElementById('calc-breakdown-misc');
    const bufferDisplay = document.getElementById('calc-breakdown-buffer');

    function formatINR(val) {
        return '₹' + Number(val).toLocaleString('en-IN', { maximumFractionDigits: 0 });
    }

    function calculateBudget() {
        const totalDays = parseInt(daysInput ? daysInput.value : 3) || 1;
        const travelersCount = parseInt(travelersInput ? travelersInput.value : 2) || 1;

        let selectedTier = 'standard';
        tierRadios.forEach(r => {
            if (r.checked) selectedTier = r.value;
        });

        let selectedProfile = 'family';
        profileRadios.forEach(r => {
            if (r.checked) selectedProfile = r.value;
        });

        const vehicleId = vehicleSelect && vehicleSelect.value ? parseInt(vehicleSelect.value) : null;

        fetch('/api/budget/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                total_days: totalDays,
                travelers_count: travelersCount,
                budget_tier: selectedTier,
                traveler_profile: selectedProfile,
                vehicle_id: vehicleId
            })
        })
        .then(res => res.json())
        .then(data => {
            if (totalDisplay) totalDisplay.textContent = formatINR(data.grand_total);
            if (perPersonDisplay) perPersonDisplay.textContent = formatINR(data.per_person_cost) + ' per pilgrim';

            const b = data.breakdown;
            if (accomDisplay) accomDisplay.textContent = formatINR(b.accommodation.amount);
            if (foodDisplay) foodDisplay.textContent = formatINR(b.food.amount);
            if (transportDisplay) transportDisplay.textContent = formatINR(b.transport.amount);
            if (darshanDisplay) darshanDisplay.textContent = formatINR(b.darshan_pooja.amount);
            if (miscDisplay) miscDisplay.textContent = formatINR(b.accessibility_misc.amount);
            if (bufferDisplay) bufferDisplay.textContent = formatINR(b.emergency_buffer.amount);
        })
        .catch(err => console.error("Error calculating budget:", err));
    }

    // Bind event listeners
    if (daysInput) daysInput.addEventListener('input', calculateBudget);
    if (travelersInput) travelersInput.addEventListener('input', calculateBudget);
    tierRadios.forEach(r => r.addEventListener('change', calculateBudget));
    profileRadios.forEach(r => r.addEventListener('change', calculateBudget));
    if (vehicleSelect) vehicleSelect.addEventListener('change', calculateBudget);

    // Initial calculation
    calculateBudget();
});
