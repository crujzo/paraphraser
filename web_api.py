"""
Simple Flask Web API for the paraphraser
Optional: Install Flask with 'pip install flask flask-cors'
"""

try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Run: pip install flask flask-cors")

from paraphraser import AIParaphraser
import os


# HTML template for web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Paraphraser</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
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
        }
        .subtitle {
            color: #666;
            margin-bottom: 30px;
        }
        .input-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
        }
        textarea, input, select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        textarea:focus, input:focus, select:focus {
            outline: none;
            border-color: #667eea;
        }
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        .controls {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
        }
        .controls > div {
            flex: 1;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
        }
        button:active {
            transform: translateY(0);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
            display: none;
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .results {
            margin-top: 30px;
            display: none;
        }
        .result-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 10px;
            border-left: 4px solid #667eea;
            animation: slideIn 0.3s ease-out;
        }
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateX(-20px);
            }
            to {
                opacity: 1;
                transform: translateX(0);
            }
        }
        .result-number {
            color: #667eea;
            font-weight: 600;
            margin-right: 8px;
        }
        .error {
            background: #fee;
            color: #c33;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 AI Paraphraser</h1>
        <p class="subtitle">Generate multiple diverse paraphrases of any text</p>
        
        <div class="input-group">
            <label for="text">Enter your text:</label>
            <textarea id="text" placeholder="Type or paste your text here..."></textarea>
        </div>
        
        <div class="controls">
            <div>
                <label for="num">Number of paraphrases:</label>
                <input type="number" id="num" value="5" min="1" max="20">
            </div>
            <div>
                <label for="temperature">Creativity:</label>
                <select id="temperature">
                    <option value="0.7">Conservative</option>
                    <option value="1.2">Balanced</option>
                    <option value="1.5" selected>Creative</option>
                    <option value="2.0">Very Creative</option>
                </select>
            </div>
        </div>
        
        <button onclick="paraphrase()">Generate Paraphrases</button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating paraphrases...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results"></div>
    </div>

    <script>
        async function paraphrase() {
            const text = document.getElementById('text').value.trim();
            const num = document.getElementById('num').value;
            const temperature = document.getElementById('temperature').value;
            
            if (!text) {
                showError('Please enter some text to paraphrase.');
                return;
            }
            
            document.getElementById('loading').style.display = 'block';
            document.getElementById('results').style.display = 'none';
            document.getElementById('error').style.display = 'none';
            
            try {
                const response = await fetch('/api/paraphrase', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        num_paraphrases: parseInt(num),
                        temperature: parseFloat(temperature)
                    })
                });
                
                const data = await response.json();
                
                if (data.error) {
                    showError(data.error);
                } else {
                    showResults(data.paraphrases);
                }
            } catch (error) {
                showError('Error: ' + error.message);
            } finally {
                document.getElementById('loading').style.display = 'none';
            }
        }
        
        function showResults(paraphrases) {
            const resultsDiv = document.getElementById('results');
            resultsDiv.innerHTML = '<h2 style="margin-bottom: 20px; color: #333;">Results:</h2>';
            
            paraphrases.forEach((para, index) => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.innerHTML = `<span class="result-number">${index + 1}.</span>${para}`;
                resultsDiv.appendChild(item);
            });
            
            resultsDiv.style.display = 'block';
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        // Allow Enter key in textarea
        document.getElementById('text').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && e.ctrlKey) {
                paraphrase();
            }
        });
    </script>
</body>
</html>
"""


if FLASK_AVAILABLE:
    app = Flask(__name__)
    CORS(app)  # Enable CORS for API access
    
    # Initialize paraphraser (loaded once at startup)
    print("Loading AI model...")
    paraphraser = AIParaphraser(model_name="t5-base")
    print("Model loaded! Server ready.")
    
    
    @app.route('/')
    def home():
        """Serve the web interface"""
        return render_template_string(HTML_TEMPLATE)
    
    
    @app.route('/api/paraphrase', methods=['POST'])
    def api_paraphrase():
        """API endpoint for paraphrasing"""
        try:
            data = request.json
            
            if not data or 'text' not in data:
                return jsonify({'error': 'No text provided'}), 400
            
            text = data['text']
            num_paraphrases = data.get('num_paraphrases', 5)
            temperature = data.get('temperature', 1.5)
            diversity_penalty = data.get('diversity_penalty', 1.0)
            max_length = data.get('max_length', 128)
            
            # Validate parameters
            if not text.strip():
                return jsonify({'error': 'Text cannot be empty'}), 400
            
            if num_paraphrases < 1 or num_paraphrases > 20:
                return jsonify({'error': 'num_paraphrases must be between 1 and 20'}), 400
            
            # Generate paraphrases
            paraphrases = paraphraser.paraphrase(
                text,
                num_paraphrases=num_paraphrases,
                temperature=temperature,
                diversity_penalty=diversity_penalty,
                max_length=max_length
            )
            
            return jsonify({
                'original': text,
                'paraphrases': paraphrases,
                'count': len(paraphrases)
            })
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    
    @app.route('/api/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'healthy', 'model': 't5-base'})


def main():
    """Run the web server"""
    if not FLASK_AVAILABLE:
        print("\nFlask is not installed.")
        print("To use the web API, install Flask:")
        print("  pip install flask flask-cors")
        print("\nThen run this script again.")
        return
    
    print("\n" + "=" * 80)
    print("🌐 AI Paraphraser Web API")
    print("=" * 80)
    print("\nStarting server...")
    print("\nAccess the web interface at: http://localhost:5000")
    print("API endpoint: http://localhost:5000/api/paraphrase")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 80 + "\n")
    
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == "__main__":
    main()
