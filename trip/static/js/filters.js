// Yatra Filter & Accessibility Utilities
document.addEventListener('DOMContentLoaded', function () {
    // Mobile navigation menu toggle
    const toggleBtn = document.querySelector('.mobile-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (toggleBtn && navMenu) {
        toggleBtn.addEventListener('click', function () {
            navMenu.classList.toggle('active');
        });
    }

    // Auto-dismiss alert messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });

    // Destination card instant live search filter if on listing page
    const liveSearchInput = document.getElementById('live-search-input');
    if (liveSearchInput) {
        liveSearchInput.addEventListener('input', function (e) {
            const query = e.target.value.toLowerCase().trim();
            const cards = document.querySelectorAll('.destination-card-item');

            cards.forEach(card => {
                const title = card.getAttribute('data-name') || '';
                const city = card.getAttribute('data-city') || '';
                const state = card.getAttribute('data-state') || '';

                if (title.toLowerCase().includes(query) || city.toLowerCase().includes(query) || state.toLowerCase().includes(query)) {
                    card.style.display = '';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }

    // Checkbox senior priority toggle helper
    const seniorToggle = document.getElementById('filter-senior-checkbox');
    if (seniorToggle) {
        seniorToggle.addEventListener('change', function () {
            const form = seniorToggle.closest('form');
            if (form) form.submit();
        });
    }
});
