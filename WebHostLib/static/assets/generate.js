window.addEventListener('load', () => {
    const form = document.getElementById('generate-game-form');
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const generateButton = document.getElementById('generate-game-button');
    const cookieName = form?.dataset.race === '1' ? 'generate_race_settings' : 'generate_settings';
    const cookieMaxAge = 60 * 60 * 24 * 365;
    const excludedIds = new Set(['file-input', 'server_password']);

    function readCookie(name) {
        const prefix = name + '=';
        return document.cookie
            .split(';')
            .map(part => part.trim())
            .find(part => part.startsWith(prefix))
            ?.slice(prefix.length);
    }

    function selectHasValue(select, value) {
        return Array.from(select.options).some(option => option.value === value);
    }

    function loadStoredSettings() {
        const raw = readCookie(cookieName);
        if (!raw) return;

        let settings;
        try {
            settings = JSON.parse(decodeURIComponent(raw));
        } catch (e) {
            return;
        }

        form.querySelectorAll('input, select').forEach(el => {
            if (!el.name || excludedIds.has(el.id) || !(el.name in settings)) return;
            if (el.type === 'checkbox') {
                el.checked = !!settings[el.name];
            } else if (el.tagName === 'SELECT') {
                if (selectHasValue(el, settings[el.name])) el.value = settings[el.name];
            } else {
                el.value = settings[el.name];
            }
        });
    }

    function saveStoredSettings() {
        const settings = {};
        form.querySelectorAll('input, select').forEach(el => {
            if (!el.name || excludedIds.has(el.id)) return;
            settings[el.name] = el.type === 'checkbox' ? el.checked : el.value;
        });
        document.cookie = `${cookieName}=${encodeURIComponent(JSON.stringify(settings))}; max-age=${cookieMaxAge}; path=/; samesite=lax`;
    }

    function submitGenerateForm() {
        saveStoredSettings();
        form.submit();
    }

    loadStoredSettings();
    form.addEventListener('submit', saveStoredSettings);

    // Button click handler
    generateButton.addEventListener('click', () => {
        fileInput.click();
    });

    // File input change handler
    fileInput.addEventListener('change', () => {
        submitGenerateForm();
    });

    // Drag and drop handlers
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            submitGenerateForm();
        }
    });
});
