// Function to refresh the CAPTCHA
function refreshCaptcha() {
    fetch('/generate_captcha', {
        method: 'GET'
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the image
            document.getElementById('captcha-image').src = data.captcha.image_data;
            
            // Update the hidden seed field
            document.querySelector('input[name="captcha_seed"]').value = data.captcha.seed;
            
            // Clear all input fields
            const inputs = document.querySelectorAll('.coordinates-input input[type="number"]');
            inputs.forEach(input => input.value = '');
        }
    })
    .catch(error => console.error('Error refreshing CAPTCHA:', error));
}

// Handle form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            
            fetch('/verify_captcha', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Show success message and proceed
                    alert('CAPTCHA verification successful!');
                    // Here you could redirect or enable form submission
                } else {
                    // Show error message and refresh CAPTCHA
                    alert('CAPTCHA verification failed. Please try again.');
                    refreshCaptcha();
                }
            })
            .catch(error => console.error('Error verifying CAPTCHA:', error));
        });
    }
});

// Add visual helpers to better explain the corner order
document.addEventListener('DOMContentLoaded', function() {
    const cornerInputs = document.querySelectorAll('.corner');
    cornerInputs.forEach(corner => {
        const label = corner.querySelector('label').textContent;
        const helperTip = document.createElement('div');
        helperTip.className = 'helper-tip';
        helperTip.textContent = "↑ Enter the grid coordinates (x,y) for this corner";
        corner.appendChild(helperTip);
    });
}); 