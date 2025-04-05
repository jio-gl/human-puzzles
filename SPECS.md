# Geometric CAPTCHA - Technical Specifications

## Overview
The Geometric CAPTCHA system generates verification challenges using geometric shapes with random rotations. Users must count the number of emerging patterns (like triangles) to pass the verification. The system compares the user's answer with the most common answer from other users to determine if the CAPTCHA is passed.

## Architecture

### Backend
- **Framework**: Flask (Python web framework)
- **Database**: SQLite
- **Image Generation**: Pillow (PIL)

### Frontend
- **HTML/CSS**: Standard web interface
- **JavaScript**: Vue.js for reactivity and user interactions

## Components

### 1. CAPTCHA Generator
- Generates random geometric shapes (currently triangles)
- Uses a seed-based approach for reproducibility
- Creates PNG images with semi-transparent shapes
- Calculates an expected count of shapes

### 2. Database Schema
- **captchas**: Stores CAPTCHA challenges with seeds and expected counts
- **responses**: Records user responses for statistical verification

### 3. API Endpoints
- **/generate-captcha**: Creates a new CAPTCHA challenge
- **/verify-captcha**: Verifies user responses against common answers

### 4. Verification Logic
- Primary verification: User's count matches the most common response from other users
- Fallback verification: User's count matches the system's expected count

## CAPTCHA Generation Algorithm
1. Create a blank canvas (400x300 pixels)
2. Generate 10 triangles with:
   - Random positions
   - Random sizes (30-70 pixels)
   - Random rotations (0-360 degrees)
   - Semi-transparent random colors
3. Calculate an expected count based on the number of shapes plus a random factor
4. Convert the image to a data URL for embedding in HTML

## Verification Algorithm
1. Store the user's response in the database
2. Retrieve the most common response for this CAPTCHA
3. If no other responses exist, use the system's expected count
4. Compare the user's count with the reference count
5. Return success/failure status

## Security Considerations
- Uses session-based tracking for CAPTCHA challenges
- Records IP addresses to prevent abuse
- Seed-based generation allows for verification of expected results
- Random factors make automated solving difficult

## Future Improvements
- Add more shape types (circles, squares, etc.)
- Implement more sophisticated pattern detection
- Add rate limiting to prevent abuse
- Improve accessibility features
- Enhance the algorithm for determining the "correct" answer 