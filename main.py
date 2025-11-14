from flask import Flask, request, jsonify, render_template_string
from phishing_detector import PhishingDetector

app = Flask(__name__)
detector = PhishingDetector()

# Simple HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Detection System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        textarea { width: 100%; height: 200px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .phishing { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .safe { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phishing Detection System</h1>
        <p>Paste an email content below to analyze for phishing indicators:</p>
        <textarea id="emailContent" placeholder="Paste email content here..."></textarea>
        <br>
        <button onclick="analyzeEmail()">Analyze Email</button>
        <div id="result" class="result" style="display:none;"></div>
    </div>

    <script>
        async function analyzeEmail() {
            const emailContent = document.getElementById('emailContent').value;
            if (!emailContent.trim()) {
                alert('Please enter email content to analyze');
                return;
            }
            
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '<p>Analyzing email...</p>';
            resultDiv.className = 'result info';
            resultDiv.style.display = 'block';
            
            try {
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({email_content: emailContent})
                });
                
                const result = await response.json();
                
                if (result.error) {
                    resultDiv.className = 'result info';
                    resultDiv.innerHTML = `<h3>⚠️ Error</h3><p>${result.error}</p>`;
                } else if (result.is_phishing) {
                    resultDiv.className = 'result phishing';
                    resultDiv.innerHTML = `
                        <h3>⚠️ PHISHING DETECTED!</h3>
                        <p><strong>Confidence Score:</strong> ${result.confidence_score.toFixed(2)}%</p>
                        <p><strong>Rule Score:</strong> ${result.rule_score}%</p>
                        <p><strong>ML Prediction:</strong> ${result.ml_prediction} (Confidence: ${(result.ml_confidence*100).toFixed(2)}%)</p>
                        <p><strong>Reasons:</strong> ${result.rule_reasons.join(', ')}</p>
                    `;
                } else {
                    resultDiv.className = 'result safe';
                    resultDiv.innerHTML = `
                        <h3>✅ SAFE EMAIL</h3>
                        <p><strong>Confidence Score:</strong> ${result.confidence_score.toFixed(2)}%</p>
                        <p><strong>Rule Score:</strong> ${result.rule_score}%</p>
                        <p><strong>ML Prediction:</strong> ${result.ml_prediction} (Confidence: ${(result.ml_confidence*100).toFixed(2)}%)</p>
                    `;
                }
            } catch (error) {
                resultDiv.className = 'result info';
                resultDiv.innerHTML = `<h3>⚠️ Error</h3><p>Failed to analyze email: ${error.message}</p>`;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze_email():
    try:
        data = request.json
        email_content = data.get('email_content', '')
        
        if not email_content:
            return jsonify({'error': 'No email content provided'}), 400
        
        result = detector.analyze_email(email_content)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy', 
        'ml_model_trained': detector.ml_model.is_trained,
        'system': 'phishing_detector'
    })

if __name__ == '__main__':
    print("Starting Phishing Detection System...")
    print("Visit http://localhost:5000 to use the web interface")
    print("API endpoints:")
    print("  - GET / - Web interface")
    print("  - POST /analyze - Analyze email content")
    print("  - GET /health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)