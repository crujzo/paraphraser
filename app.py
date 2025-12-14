"""
Simple Web Interface for AI Paraphraser
Run with: python app.py
Then open: http://localhost:5000
"""

try:
    from flask import Flask, request, jsonify, render_template_string
    from flask_cors import CORS
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Flask not installed. Run: pip install flask flask-cors")
    exit(1)

from paraphraser import AIParaphraser
import os

app = Flask(__name__)
CORS(app)

# Initialize paraphraser (loaded once at startup)
print("Loading AI Paraphraser...")
paraphraser = AIParaphraser()
print("✓ Ready to paraphrase!")

# Modern, clean HTML interface
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
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            padding: 48px;
            max-width: 800px;
            width: 100%;
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.5em;
            margin-bottom: 8px;
            text-align: center;
        }
        
        .subtitle {
            color: #666;
            text-align: center;
            margin-bottom: 32px;
            font-size: 1.1em;
        }
        
        .input-section {
            margin-bottom: 24px;
        }
        
        label {
            display: block;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
            font-size: 0.95em;
        }
        
        textarea {
            width: 100%;
            padding: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            resize: vertical;
            min-height: 120px;
            transition: all 0.3s;
        }
        
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        .controls {
            display: flex;
            gap: 16px;
            margin-bottom: 24px;
            align-items: flex-end;
        }
        
        .control-group {
            flex: 1;
        }
        
        input[type="number"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 12px;
            font-size: 16px;
            font-family: inherit;
            transition: all 0.3s;
        }
        
        input[type="number"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        button {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        button:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        button:active:not(:disabled) {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        
        .loading {
            display: none;
            text-align: center;
            padding: 24px;
            color: #667eea;
        }
        
        .loading.active {
            display: block;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            animation: spin 1s linear infinite;
            margin: 0 auto 16px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .results {
            display: none;
            margin-top: 32px;
        }
        
        .results.active {
            display: block;
        }
        
        .results-header {
            color: #333;
            font-size: 1.3em;
            font-weight: 600;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .results-count {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8em;
        }
        
        .result-item {
            background: #f8f9fa;
            padding: 16px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
            animation: slideIn 0.3s ease-out;
            display: flex;
            gap: 12px;
            transition: all 0.3s;
        }
        
        .result-item:hover {
            background: #f0f1f3;
            transform: translateX(4px);
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
            font-weight: 700;
            font-size: 1.1em;
            min-width: 24px;
        }
        
        .result-text {
            color: #333;
            line-height: 1.6;
            flex: 1;
        }
        
        .copy-btn {
            background: none;
            border: 2px solid #667eea;
            color: #667eea;
            padding: 6px 12px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.85em;
            transition: all 0.3s;
            width: auto;
        }
        
        .copy-btn:hover {
            background: #667eea;
            color: white;
            transform: none;
        }
        
        .error {
            background: #fee;
            color: #c33;
            padding: 16px;
            border-radius: 12px;
            margin-top: 20px;
            display: none;
            border-left: 4px solid #c33;
        }
        
        .error.active {
            display: block;
        }
        
        .footer {
            text-align: center;
            margin-top: 32px;
            color: #666;
            font-size: 0.9em;
        }
        
        .footer a {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        
        .footer a:hover {
            text-decoration: underline;
        }
        
        @media (max-width: 640px) {
            .container {
                padding: 32px 24px;
            }
            
            h1 {
                font-size: 2em;
            }
            
            .controls {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔄 AI Paraphraser</h1>
        <p class="subtitle">Generate multiple ways to say the same thing</p>
        
        <div class="input-section">
            <label for="text">Enter your text:</label>
            <textarea 
                id="text" 
                placeholder="Type or paste your text here... (e.g., 'The quick brown fox jumps over the lazy dog')"
                autofocus
            ></textarea>
        </div>
        
        <div class="controls">
            <div class="control-group">
                <label for="num">Number of paraphrases:</label>
                <input type="number" id="num" value="5" min="1" max="10">
            </div>
        </div>
        
        <button onclick="paraphrase()" id="generateBtn">
            Generate Paraphrases
        </button>
        
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <p>Generating paraphrases...</p>
        </div>
        
        <div class="error" id="error"></div>
        
        <div class="results" id="results">
            <div class="results-header">
                <span>Results</span>
                <span class="results-count" id="resultsCount"></span>
            </div>
            <div id="resultsList"></div>
        </div>
        
        <div class="footer">
            <p>Powered by AI • <a href="https://github.com" target="_blank">Open Source on GitHub</a></p>
        </div>
    </div>

    <script>
        // Allow Ctrl+Enter to submit
        document.getElementById('text').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                paraphrase();
            }
        });
        
        async function paraphrase() {
            const text = document.getElementById('text').value.trim();
            const num = parseInt(document.getElementById('num').value);
            
            if (!text) {
                showError('Please enter some text to paraphrase.');
                return;
            }
            
            if (num < 1 || num > 10) {
                showError('Number of paraphrases must be between 1 and 10.');
                return;
            }
            
            // Show loading
            document.getElementById('loading').classList.add('active');
            document.getElementById('results').classList.remove('active');
            document.getElementById('error').classList.remove('active');
            document.getElementById('generateBtn').disabled = true;
            
            try {
                const response = await fetch('/api/paraphrase', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        text: text,
                        num_paraphrases: num
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
                document.getElementById('loading').classList.remove('active');
                document.getElementById('generateBtn').disabled = false;
            }
        }
        
        function showResults(paraphrases) {
            const resultsDiv = document.getElementById('results');
            const resultsList = document.getElementById('resultsList');
            const resultsCount = document.getElementById('resultsCount');
            
            resultsList.innerHTML = '';
            resultsCount.textContent = paraphrases.length + ' paraphrase' + (paraphrases.length !== 1 ? 's' : '');
            
            paraphrases.forEach((para, index) => {
                const item = document.createElement('div');
                item.className = 'result-item';
                item.innerHTML = `
                    <span class="result-number">${index + 1}.</span>
                    <span class="result-text">${escapeHtml(para)}</span>
                    <button class="copy-btn" onclick="copyText('${escapeHtml(para).replace(/'/g, "\\'")}')">Copy</button>
                `;
                resultsList.appendChild(item);
            });
            
            resultsDiv.classList.add('active');
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error');
            errorDiv.textContent = message;
            errorDiv.classList.add('active');
        }
        
        function copyText(text) {
            navigator.clipboard.writeText(text).then(() => {
                // Could add a tooltip or notification here
                console.log('Copied to clipboard');
            });
        }
        
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
    </script>
</body>
</html>
"""

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
        
        # Validate parameters
        if not text.strip():
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        if num_paraphrases < 1 or num_paraphrases > 20:
            return jsonify({'error': 'num_paraphrases must be between 1 and 20'}), 400
        
        # Auto-detect if text is a paragraph and use appropriate method
        # Check for multiple sentences using periods, semicolons, and overall length
        sentence_markers = text.count('.') + text.count(';') + text.count('!')  + text.count('?')
        word_count = len(text.split())
        
        if sentence_markers >= 2 or word_count > 30:
            # Longer text with multiple sentences - use paragraph mode
            paraphrases = paraphraser.paraphrase_paragraph(
                text,
                num_paraphrases=num_paraphrases,
                temperature=1.0,
                max_length=256
            )
        else:
            # Short text or single sentence - use regular mode
            paraphrases = paraphraser.paraphrase(
                text,
                num_paraphrases=num_paraphrases,
                temperature=1.0,
                max_length=512
            )
        
        return jsonify({
            'original': text,
            'paraphrases': paraphrases,
            'count': len(paraphrases)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == "__main__":
    # Port can be set via environment variable or command line argument
    import sys
    
    # Check for command line port argument
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Error: Port must be a number")
            print("Usage: python app.py [port]")
            print("Example: python app.py 8080")
            sys.exit(1)
    else:
        port = int(os.environ.get('PORT', 8080))  # Changed default to 8080
    
    print("\n" + "=" * 70)
    print("🌐 AI Paraphraser Web Interface")
    print("=" * 70)
    print(f"\n✓ Server running at: http://localhost:{port}")
    print(f"✓ Open your browser and visit the URL above")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)
