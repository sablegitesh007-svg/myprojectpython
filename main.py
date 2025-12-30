"""
Main entry point for the Python project - Web Application.
"""

from flask import Flask, render_template_string

app = Flask(__name__)


@app.route('/')
def home():
    """Home page route."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Python Web App</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                text-align: center;
                max-width: 600px;
                width: 100%;
            }
            h1 {
                color: #667eea;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            p {
                color: #666;
                font-size: 1.2em;
                line-height: 1.6;
                margin-bottom: 30px;
            }
            .info {
                background: #f0f0f0;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            .info h2 {
                color: #764ba2;
                margin-bottom: 10px;
                font-size: 1.5em;
            }
            .status {
                color: #28a745;
                font-weight: bold;
                font-size: 1.1em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Python Web App</h1>
            <p>Your Python project is running successfully in the browser!</p>
            <div class="info">
                <h2>Project Status</h2>
                <p class="status">✅ Application is running</p>
                <p style="margin-top: 15px; color: #666;">
                    Flask web server is active and ready to serve your application.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/api/hello')
def api_hello():
    """API endpoint example."""
    return {"message": "Hello from Python API!", "status": "success"}


def main():
    """Main function to run the Flask app."""
    print("Starting Flask web server...")
    print("Open your browser and go to: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server")
    app.run(debug=True, host='127.0.0.1', port=5000)


if __name__ == "__main__":
    main()

