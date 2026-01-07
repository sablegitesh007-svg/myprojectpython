"""
Main entry point for the Python project - Service Request Resolution Time Prediction using AI.
"""

from flask import Flask, render_template_string, request, jsonify
from prediction_model import predictor
import json

app = Flask(__name__)


def format_time(hours):
    """Format hours into readable time string."""
    if hours < 1:
        return f"{int(hours * 60)} minutes"
    elif hours < 24:
        return f"{hours:.1f} hours" if hours != int(hours) else f"{int(hours)} hours"
    else:
        days = int(hours // 24)
        remaining_hours = hours % 24
        if remaining_hours < 1:
            return f"{days} day{'s' if days > 1 else ''}"
        else:
            return f"{days} day{'s' if days > 1 else ''} {int(remaining_hours)} hour{'s' if remaining_hours > 1 else ''}"


@app.route('/')
def home():
    """Home page with prediction form."""
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Service Request Resolution Time Predictor</title>
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
                padding: 20px;
            }
            .container {
                max-width: 900px;
                margin: 0 auto;
                background: white;
                border-radius: 20px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
                text-align: center;
            }
            .subtitle {
                text-align: center;
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .form-group {
                margin-bottom: 25px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
                font-size: 0.95em;
            }
            select, input[type="number"] {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            select:focus, input[type="number"]:focus {
                outline: none;
                border-color: #667eea;
            }
            .range-input {
                display: flex;
                align-items: center;
                gap: 15px;
            }
            input[type="range"] {
                flex: 1;
                height: 8px;
                border-radius: 5px;
                background: #e0e0e0;
                outline: none;
            }
            input[type="range"]::-webkit-slider-thumb {
                appearance: none;
                width: 20px;
                height: 20px;
                border-radius: 50%;
                background: #667eea;
                cursor: pointer;
            }
            .range-value {
                min-width: 60px;
                text-align: center;
                font-weight: bold;
                color: #667eea;
            }
            .btn {
                width: 100%;
                padding: 15px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
                margin-top: 10px;
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            .btn:active {
                transform: translateY(0);
            }
            .result {
                margin-top: 30px;
                padding: 25px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 5px solid #667eea;
                display: none;
            }
            .result.show {
                display: block;
                animation: fadeIn 0.5s;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .result h2 {
                color: #667eea;
                margin-bottom: 15px;
            }
            .prediction-value {
                font-size: 2.5em;
                font-weight: bold;
                color: #764ba2;
                margin: 15px 0;
            }
            .prediction-details {
                margin-top: 20px;
                padding-top: 20px;
                border-top: 2px solid #e0e0e0;
            }
            .detail-item {
                display: flex;
                justify-content: space-between;
                padding: 10px 0;
                border-bottom: 1px solid #e0e0e0;
            }
            .detail-item:last-child {
                border-bottom: none;
            }
            .detail-label {
                color: #666;
            }
            .detail-value {
                font-weight: 600;
                color: #333;
            }
            .loading {
                display: none;
                text-align: center;
                margin-top: 20px;
            }
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto;
            }
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            .grid {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
            }
            @media (max-width: 768px) {
                .grid {
                    grid-template-columns: 1fr;
                }
                h1 {
                    font-size: 2em;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Service Request Predictor</h1>
            <p class="subtitle">Predict resolution time using Machine Learning</p>
            
            <form id="predictionForm">
                <div class="grid">
                    <div class="form-group">
                        <label for="category">Category *</label>
                        <select id="category" name="category" required>
                            <option value="">Select Category</option>
                            <option value="Hardware">Hardware</option>
                            <option value="Software">Software</option>
                            <option value="Network">Network</option>
                            <option value="Database">Database</option>
                            <option value="Security">Security</option>
                            <option value="Application">Application</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label for="priority">Priority *</label>
                        <select id="priority" name="priority" required>
                            <option value="">Select Priority</option>
                            <option value="Low">Low</option>
                            <option value="Medium">Medium</option>
                            <option value="High">High</option>
                            <option value="Critical">Critical</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="assigned_team">Assigned Team *</label>
                    <select id="assigned_team" name="assigned_team" required>
                        <option value="">Select Team</option>
                        <option value="IT Support">IT Support</option>
                        <option value="Development">Development</option>
                        <option value="Network Team">Network Team</option>
                        <option value="Database Team">Database Team</option>
                        <option value="Security Team">Security Team</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="complexity_score">Complexity Score (1-10) *</label>
                    <div class="range-input">
                        <input type="range" id="complexity_score" name="complexity_score" 
                               min="1" max="10" value="5" step="0.1" required>
                        <span class="range-value" id="complexity_display">5.0</span>
                    </div>
                </div>
                
                <div class="grid">
                    <div class="form-group">
                        <label for="request_age_hours">Request Age (hours)</label>
                        <input type="number" id="request_age_hours" name="request_age_hours" 
                               value="0" min="0" step="0.5">
                    </div>
                    
                    <div class="form-group">
                        <label for="previous_interactions">Previous Interactions</label>
                        <input type="number" id="previous_interactions" name="previous_interactions" 
                               value="0" min="0" step="1">
                    </div>
                </div>
                
                <button type="submit" class="btn">🔮 Predict Resolution Time</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p style="margin-top: 10px; color: #666;">Predicting...</p>
            </div>
            
            <div class="result" id="result">
                <h2>Predicted Resolution Time</h2>
                <div class="prediction-value" id="predictionValue"></div>
                <div class="prediction-details" id="predictionDetails"></div>
            </div>
        </div>
        
        <script>
            // Update complexity score display
            const complexitySlider = document.getElementById('complexity_score');
            const complexityDisplay = document.getElementById('complexity_display');
            
            complexitySlider.addEventListener('input', function() {
                complexityDisplay.textContent = parseFloat(this.value).toFixed(1);
            });
            
            // Handle form submission
            document.getElementById('predictionForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                
                const formData = new FormData(this);
                const data = {
                    category: formData.get('category'),
                    priority: formData.get('priority'),
                    assigned_team: formData.get('assigned_team'),
                    complexity_score: parseFloat(formData.get('complexity_score')),
                    request_age_hours: parseFloat(formData.get('request_age_hours')) || 0,
                    previous_interactions: parseInt(formData.get('previous_interactions')) || 0
                };
                
                // Show loading
                document.getElementById('loading').style.display = 'block';
                document.getElementById('result').classList.remove('show');
                
                try {
                    const response = await fetch('/api/predict', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(data)
                    });
                    
                    const result = await response.json();
                    
                    // Hide loading
                    document.getElementById('loading').style.display = 'none';
                    
                    // Show result
                    document.getElementById('predictionValue').textContent = result.formatted_time;
                    document.getElementById('predictionDetails').innerHTML = `
                        <div class="detail-item">
                            <span class="detail-label">Category:</span>
                            <span class="detail-value">${result.category}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Priority:</span>
                            <span class="detail-value">${result.priority}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Assigned Team:</span>
                            <span class="detail-value">${result.assigned_team}</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Complexity Score:</span>
                            <span class="detail-value">${result.complexity_score}/10</span>
                        </div>
                        <div class="detail-item">
                            <span class="detail-label">Resolution Time (hours):</span>
                            <span class="detail-value">${result.prediction_hours.toFixed(2)} hours</span>
                        </div>
                    `;
                    document.getElementById('result').classList.add('show');
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('loading').style.display = 'none';
                    alert('Error making prediction.  keep trying.');
                }
            });
        </script>
    </body>
    </html>
    """
    return render_template_string(html)


@app.route('/api/predict', methods=['POST'])
def predict():
    """API endpoint for prediction."""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['category', 'priority', 'assigned_team', 'complexity_score']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Make prediction
        prediction_hours = predictor.predict(
            category=data['category'],
            priority=data['priority'],
            assigned_team=data['assigned_team'],
            complexity_score=float(data['complexity_score']),
            request_age_hours=float(data.get('request_age_hours', 0)),
            previous_interactions=int(data.get('previous_interactions', 0))
        )
        
        return jsonify({
            'prediction_hours': prediction_hours,
            'formatted_time': format_time(prediction_hours),
            'category': data['category'],
            'priority': data['priority'],
            'assigned_team': data['assigned_team'],
            'complexity_score': data['complexity_score']
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
