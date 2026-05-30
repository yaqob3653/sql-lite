console.log('Entrepreneur Hub loaded');

// Add any custom interactivity here in the future
document.addEventListener('DOMContentLoaded', () => {
    // Example: Fade out flash messages after 3 seconds
    const flashes = document.querySelectorAll('.glass-panel');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(flash => {
                flash.style.opacity = '0';
                setTimeout(() => flash.remove(), 500);
            });
        }, 3000);
    }
});
