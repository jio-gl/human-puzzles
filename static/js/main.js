new Vue({
    el: '#app',
    data() {
        return {
            captchaImage: null,
            captchaId: null,
            userCoords: {
                x: [7, 9],
                y: [7, 9]
            },
            result: null,
            loading: false
        };
    },
    mounted() {
        if (window.initialUserCoords) {
            this.userCoords = {
                x: [Number(window.initialUserCoords.x[0]), Number(window.initialUserCoords.x[1])],
                y: [Number(window.initialUserCoords.y[0]), Number(window.initialUserCoords.y[1])]
            };
        }
        this.generateCaptcha();
    },
    methods: {
        adjustCoord(axis, index, delta) {
            this.userCoords[axis][index] += delta;
            this.drawLines();
        },
        drawLines() {
            if (!this.$refs.captchaImage || !this.$refs.lineOverlay) return;

            const img = this.$refs.captchaImage;
            const canvas = this.$refs.lineOverlay;
            const ctx = canvas.getContext('2d');

            // Set canvas size to match container
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;

            // Clear previous lines
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Calculate pixel positions including padding
            const imageWidth = img.width;
            const imageHeight = img.height;
            const cellWidth = imageWidth / 16;
            const cellHeight = imageHeight / 16;

            // Draw lines
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;

            // Vertical lines - extend beyond image bounds
            ctx.beginPath();
            ctx.moveTo(this.userCoords.x[0] * cellWidth, -10); // Start above
            ctx.lineTo(this.userCoords.x[0] * cellWidth, canvas.height + 10); // End below
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(this.userCoords.x[1] * cellWidth, -10);
            ctx.lineTo(this.userCoords.x[1] * cellWidth, canvas.height + 10);
            ctx.stroke();

            // Horizontal lines - extend beyond image bounds
            ctx.beginPath();
            ctx.moveTo(-10, this.userCoords.y[0] * cellHeight);
            ctx.lineTo(canvas.width + 10, this.userCoords.y[0] * cellHeight);
            ctx.stroke();

            ctx.beginPath();
            ctx.moveTo(-10, this.userCoords.y[1] * cellHeight);
            ctx.lineTo(canvas.width + 10, this.userCoords.y[1] * cellHeight);
            ctx.stroke();
        },
        generateCaptcha() {
            this.loading = true;
            this.captchaImage = null;
            this.result = null;
            
            // Reset coordinates to middle ranges
            this.userCoords = {
                x: [7, 9],
                y: [7, 9]
            };
            
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
                // Draw lines after image loads
                this.$nextTick(() => {
                    this.drawLines();
                });
            })
            .catch(error => {
                console.error('Error generating CAPTCHA:', error);
                this.loading = false;
            });
        },
        verifyCaptcha() {
            this.loading = true;
            
            fetch('/verify-captcha', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    position: {
                        x: [Number(this.userCoords.x[0]), Number(this.userCoords.x[1])],
                        y: [Number(this.userCoords.y[0]), Number(this.userCoords.y[1])]
                    }
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