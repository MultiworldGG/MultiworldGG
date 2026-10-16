document.addEventListener('DOMContentLoaded', () => {
    const controls = document.getElementById('lobby-filters');
    if (!controls) return;

    const search = document.getElementById('lobby-title-search');
    const hideFullButton = document.getElementById('hide-full-lobbies');
    const hidePasswordButton = document.getElementById('hide-password-lobbies');
    const emptyMessage = document.getElementById('lobby-filter-empty');
    const lobbies = Array.from(document.querySelectorAll('#lobby-table tbody tr'), row => ({
        row,
        title: row.querySelector('[data-label="Lobby"]').textContent.toLowerCase(),
        full: row.dataset.full === 'true',
        password: row.dataset.password === 'true',
    }));
    const cookieName = 'lobby_filters';
    const cookieMaxAge = 60 * 60 * 24 * 365;
    const filters = {hideFull: false, hidePassword: false};

    try {
        const prefix = cookieName + '=';
        const raw = document.cookie.split(';').map(part => part.trim())
            .find(part => part.startsWith(prefix))?.slice(prefix.length);
        if (raw) {
            const stored = JSON.parse(decodeURIComponent(raw));
            filters.hideFull = stored?.hideFull === true;
            filters.hidePassword = stored?.hidePassword === true;
        }
    } catch (e) {
        // Keep the defaults if cookies are unavailable or the saved value is invalid.
    }

    function applyFilters() {
        const query = search.value.toLowerCase();
        let visibleCount = 0;
        lobbies.forEach(lobby => {
            lobby.row.hidden = !lobby.title.includes(query)
                || (filters.hideFull && lobby.full)
                || (filters.hidePassword && lobby.password);
            if (!lobby.row.hidden) visibleCount++;
        });
        hideFullButton.setAttribute('aria-pressed', String(filters.hideFull));
        hidePasswordButton.setAttribute('aria-pressed', String(filters.hidePassword));
        emptyMessage.hidden = visibleCount > 0;
    }

    function toggleFilter(name) {
        filters[name] = !filters[name];
        applyFilters();
        try {
            document.cookie = `${cookieName}=${encodeURIComponent(JSON.stringify(filters))}; max-age=${cookieMaxAge}; path=/; samesite=lax`;
        } catch (e) {
            // Filtering still works when the browser blocks cookie storage.
        }
    }

    search.addEventListener('input', applyFilters);
    hideFullButton.addEventListener('click', () => toggleFilter('hideFull'));
    hidePasswordButton.addEventListener('click', () => toggleFilter('hidePassword'));
    applyFilters();
    controls.hidden = false;
});
