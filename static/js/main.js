new Vue({
    el: '#app',
    data: {
        captchaImage: null,
        captchaId: null,
        userCount: null,
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
            this.userCount = null;
            
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
            if (this.userCount === null) {
                alert('Please enter the number of triangles you see.');
                return;
            }
            
            this.loading = true;
            
            fetch('/verify-captcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    count: parseInt(this.userCount)
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