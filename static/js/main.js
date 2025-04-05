new Vue({
    el: '#app',
    data: {
        captchaImage: null,
        captchaId: null,
        userCoords: [null, null, null, null, null, null, null, null],  // Array for 4 corners (x,y)
        result: null,
        loading: false
    },
    mounted() {
        this.generateCaptcha();
    },
    methods: {
        generateCaptcha() {
            this.loading = true;
            this.captchaImage = null;
            this.result = null;
            this.userCoords = [null, null, null, null, null, null, null, null];
            
            fetch('/generate-captcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                this.captchaImage = data.image_data;
                this.captchaId = data.captcha_id;
                this.loading = false;
            })
            .catch(error => {
                console.error('Error generating CAPTCHA:', error);
                this.loading = false;
            });
        },
        
        verifyCaptcha() {
            // Check if all coordinates are filled
            if (this.userCoords.some(coord => coord === null)) {
                alert('Please enter all corner coordinates.');
                return;
            }
            
            this.loading = true;
            
            fetch('/verify-captcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    coordinates: this.userCoords
                })
            })
            .then(response => response.json())
            .then(data => {
                this.result = data;
                this.loading = false;
            })
            .catch(error => {
                console.error('Error verifying CAPTCHA:', error);
                this.loading = false;
            });
        }
    }
}); 