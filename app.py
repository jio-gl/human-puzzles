import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from captcha_generator import generate_captcha, regenerate_captcha
from database import init_app, store_captcha, store_response, get_captcha, get_most_common_response

# Create the Flask application
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'geometric_captcha.sqlite'),
)

# Ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# Initialize the database with the app
init_app(app)

# Fix for getting real IP behind proxies
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-captcha', methods=['POST'])
def create_captcha():
    captcha_data = generate_captcha()
    captcha_id = store_captcha(captcha_data['seed'], captcha_data['expected_count'])
    
    # Store the captcha ID in the session
    session['captcha_id'] = captcha_id
    
    return jsonify({
        'captcha_id': captcha_id,
        'image_data': captcha_data['image_data']
    })

@app.route('/verify-captcha', methods=['POST'])
def verify_captcha():
    user_count = request.json.get('count')
    captcha_id = session.get('captcha_id')
    
    if not captcha_id:
        return jsonify({'success': False, 'message': 'No CAPTCHA session found'})
    
    # Get the user's IP address
    ip_address = request.remote_addr
    
    # Store the user's response
    store_response(captcha_id, user_count, ip_address)
    
    # Get the captcha details
    captcha = get_captcha(captcha_id)
    
    # Get the most common response from other users
    most_common = get_most_common_response(captcha_id)
    
    # If there aren't enough responses yet, use the expected count
    if most_common is None:
        most_common = captcha['expected_count']
    
    # Check if the user's count matches the most common response
    success = user_count == most_common
    
    return jsonify({
        'success': success,
        'message': 'CAPTCHA verification successful' if success else 'CAPTCHA verification failed',
        'expected': most_common
    })

# This allows the app to be run directly with 'python app.py'
if __name__ == '__main__':
    app.run(debug=True) 