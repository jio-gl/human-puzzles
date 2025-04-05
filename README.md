# Human Puzzles (GenAI-hard CAPTCHAs)

*Where is the largest rectangle you see in this image?*
![image](https://github.com/user-attachments/assets/cb7e82bc-e577-4944-bc2a-cfdb2305537e)


A web application that generates CAPTCHAs using geometric figures with random rotations. Users need to count emerging patterns (like triangles) to pass the verification.

## Features

- Generates random geometric patterns as CAPTCHA challenges
- Uses a "wisdom of the crowd" approach for verification
- No login required - anyone can use the web app
- Seed-based generation for reproducibility and verification

## Requirements

- Python 3.6+
- Flask
- Pillow (PIL)
- SQLite3
- Modern web browser with JavaScript enabled

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/geometric-captcha.git
   cd geometric-captcha
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install flask pillow
   ```

4. Initialize the database:
   ```bash
   export FLASK_APP=app.py
   flask init-db
   ```

## Running the Application

1. Start the Flask development server:
   ```bash
   flask run
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## How to Use

1. When the page loads, a CAPTCHA image with overlapping triangles will be displayed
2. Count the number of triangles you see in the image
3. Enter your count in the input field
4. Click "Verify" to submit your answer
5. If your count matches what most people see, the CAPTCHA is passed
6. You can click "Refresh CAPTCHA" to generate a new challenge

## Project Structure

```
geometric-captcha/
├── app.py                # Main Flask application
├── captcha_generator.py  # CAPTCHA generation logic
├── database.py           # Database setup and operations
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   └── js/
│       └── main.js       # Frontend logic
├── templates/
│   └── index.html        # Main page
├── schema.sql            # Database schema
├── README.md             # This file
└── SPECS.md              # Technical specifications
```

## Development

To run the application in development mode with auto-reloading:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

## Troubleshooting

If you encounter issues with the `init-db` command, make sure:
1. You've set the FLASK_APP environment variable: `export FLASK_APP=app.py`
2. You've installed all required dependencies: `pip install flask pillow`
3. You're running the command from the project root directory 

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
