document.addEventListener('DOMContentLoaded', function() {
    // Check localStorage immediately and apply theme before page renders
    const isHighContrast = localStorage.getItem('high-contrast') === 'true';
    
    if (isHighContrast) {
        // Apply theme immediately to prevent flash
        document.documentElement.classList.add('high-contrast-mode');
        loadHighContrastCSS();
    }
    
    const toggleButton = document.createElement('button');
    toggleButton.innerHTML = 'Theme';
    toggleButton.title = 'Toggle High Contrast Mode';
    toggleButton.style.cssText = `
        position: fixed;
        bottom: 50px;
        right: 20px;
        z-index: 10000;
        background-color: #2d2d2d;
        color: #ffffff;
        border: 2px solid #ffffff;
        border-radius: 20px;
        width: 80px;
        height: 40px;
        cursor: pointer;
        font-size: 14px;
        font-weight: bold;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
    `;
    
    let highContrastLink = null;
    
    if (isHighContrast) {
        toggleButton.style.backgroundColor = '#00ffff';
        toggleButton.style.color = '#000000';
    }
    
    function loadHighContrastCSS() {
        if (!highContrastLink) {
            highContrastLink = document.createElement('link');
            highContrastLink.rel = 'stylesheet';
            highContrastLink.type = 'text/css';
            highContrastLink.href = '/static/styles/high-contrast.css';
            document.head.appendChild(highContrastLink);
        }
    }
    
    function enableHighContrast() {
        document.documentElement.classList.add('high-contrast-mode');
        loadHighContrastCSS();
        localStorage.setItem('high-contrast', 'true');
    }
    
    function disableHighContrast() {
        document.documentElement.classList.remove('high-contrast-mode');
        if (highContrastLink) {
            highContrastLink.remove();
            highContrastLink = null;
        }
        localStorage.setItem('high-contrast', 'false');
    }
    
    toggleButton.addEventListener('click', function() {
        const isEnabled = document.documentElement.classList.contains('high-contrast-mode');
        
        if (isEnabled) {
            disableHighContrast();
            toggleButton.style.backgroundColor = '#2d2d2d';
            toggleButton.style.color = '#ffffff';
            toggleButton.title = 'Enable High Contrast Mode';
        } else {
            enableHighContrast();
            toggleButton.style.backgroundColor = '#00ffff';
            toggleButton.style.color = '#000000';
            toggleButton.title = 'Disable High Contrast Mode';
        }
    });
    
    document.body.appendChild(toggleButton);
    
    toggleButton.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.1)';
        this.style.transition = 'transform 0.2s';
    });
    
    toggleButton.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});