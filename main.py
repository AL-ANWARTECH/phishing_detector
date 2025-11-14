from flask import Flask, request, jsonify, render_template_string
from phishing_detector import PhishingDetector
from database import Database
from config import Config
from logger import get_logger
from performance_monitor import get_performance_monitor  
import time  

app = Flask(__name__)
detector = PhishingDetector()
db = Database()
logger = get_logger()
performance_monitor = get_performance_monitor()  

# Enhanced HTML template with history view
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Detection System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        textarea { width: 100%; height: 200px; margin: 10px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; margin: 5px; }
        button:hover { background: #0056b3; }
        .result { margin-top: 20px; padding: 15px; border-radius: 5px; }
        .phishing { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .safe { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .info { background: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        .history { margin-top: 30px; }
        .history-item { padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 3px; }
        .tabs { margin-bottom: 20px; }
        .tab { display: none; }
        .tab.active { display: block; }
        .tab-links { margin-bottom: 10px; }
        .tab-link { padding: 10px 15px; background: #e9ecef; cursor: pointer; border: 1px solid #ddd; }
        .tab-link.active { background: #007bff; color: white; }
        .stats { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Phishing Detection System</h1>
        
        <div class="stats">
            <strong>System Status:</strong> Active | 
            <strong>Threshold:</strong> {{config.PHISHING_THRESHOLD}}% | 
            <strong>ML Weight:</strong> {{config.ML_WEIGHT}} | 
            <strong>Rule Weight:</strong> {{config.RULE_WEIGHT}}
        </div>
        
        <div class="tabs">
            <div class="tab-links">
                <div class="tab-link active" onclick="switchTab('analyze')">Analyze Email</div>
                <div class="tab-link" onclick="switchTab('history')">Analysis History</div>
            </div>
            
            <div id="analyze" class="tab active">
                <p>Paste an email content below to analyze for phishing indicators:</p>
                <textarea id="emailContent" placeholder="Paste email content here..."></textarea>
                <br>
                <button onclick="analyzeEmail()">Analyze Email</button>
                <div id="result" class="result" style="display:none;"></div>
            </div>
            
            <div id="history" class="tab">
                <h3>Recent Analysis History</h3>
                <div id="historyContent"></div>
                <button onclick="loadHistory()">Load History</button>
            </div>
        </div>
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
                        <p><strong>URL Score:</strong> ${result.url_score}%</p>
                        <p><strong>Rule Reasons:</strong> ${result.rule_reasons.join(', ')}</p>
                        <p><strong>URL Reasons:</strong> ${result.url_reasons.join(', ')}</p>
                    `;
                } else {
                    resultDiv.className = 'result safe';
                    resultDiv.innerHTML = `
                        <h3>✅ SAFE EMAIL</h3>
                        <p><strong>Confidence Score:</strong> ${result.confidence_score.toFixed(2)}%</p>
                        <p><strong>Rule Score:</strong> ${result.rule_score}%</p>
                        <p><strong>ML Prediction:</strong> ${result.ml_prediction} (Confidence: ${(result.ml_confidence*100).toFixed(2)}%)</p>
                        <p><strong>URL Score:</strong> ${result.url_score}%</p>
                    `;
                }
            } catch (error) {
                resultDiv.className = 'result info';
                resultDiv.innerHTML = `<h3>⚠️ Error</h3><p>Failed to analyze email: ${error.message}</p>`;
            }
        }
        
        async function loadHistory() {
            try {
                const response = await fetch('/history');
                const history = await response.json();
                
                const historyDiv = document.getElementById('historyContent');
                if (history.length === 0) {
                    historyDiv.innerHTML = '<p>No analysis history available.</p>';
                    return;
                }
                
                let html = '<div class="history">';
                history.forEach(item => {
                    const phishingClass = item.is_phishing ? 'phishing' : 'safe';
                    const phishingText = item.is_phishing ? '⚠️ PHISHING' : '✅ SAFE';
                    
                    html += `
                        <div class="history-item ${phishingClass}">
                            <strong>${phishingText}</strong> - Score: ${item.confidence_score.toFixed(2)}% 
                            (${new Date(item.analyzed_at).toLocaleString()})
                            <br><small>Rule: ${item.rule_score}%, ML: ${item.ml_prediction} (${(item.ml_confidence*100).toFixed(2)}%), URL: ${item.url_score}%</small>
                        </div>
                    `;
                });
                html += '</div>';
                
                historyDiv.innerHTML = html;
            } catch (error) {
                document.getElementById('historyContent').innerHTML = `<p>Error loading history: ${error.message}</p>`;
            }
        }
        
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all tab links
            document.querySelectorAll('.tab-link').forEach(link => {
                link.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Add active class to clicked tab link
            event.target.classList.add('active');
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    # Pass config to template (simplified - in real app you'd use proper template engine)
    config_html = HTML_TEMPLATE.replace('{{config.PHISHING_THRESHOLD}}', str(Config.PHISHING_THRESHOLD))
    config_html = config_html.replace('{{config.ML_WEIGHT}}', str(Config.ML_WEIGHT))
    config_html = config_html.replace('{{config.RULE_WEIGHT}}', str(Config.RULE_WEIGHT))
    return config_html

@app.route('/analyze', methods=['POST'])
def analyze_email():
    start_time = time.time()  # Add timing
    
    try:
        data = request.json
        email_content = data.get('email_content', '')
        
        if not email_content:
            performance_monitor.record_analysis(time.time() - start_time, False, success=False)  # Record error
            logger.warning("Empty email content received for analysis")
            return jsonify({'error': 'No email content provided'}), 400
        
        logger.info(f"Analyzing email of length {len(email_content)} characters")
        result = detector.analyze_email(email_content)
        
        # Save result to database if enabled
        if Config.ENABLE_DATABASE_LOGGING:
            db.save_analysis_result(email_content, result)
            logger.info("Analysis result saved to database")
        
        # Record performance
        analysis_time = time.time() - start_time
        performance_monitor.record_analysis(analysis_time, result.get('is_phishing', False), success=True)
        
        return jsonify(result)
    
    except Exception as e:
        analysis_time = time.time() - start_time
        performance_monitor.record_analysis(analysis_time, False, success=False)  # Record error
        logger.error(f"Error in analyze_email endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/history')
def get_history():
    try:
        if Config.ENABLE_HISTORY_TRACKING:
            history = db.get_analysis_history(10)
            # Convert tuples to dictionaries for JSON
            history_dict = []
            for item in history:
                history_dict.append({
                    'id': item[0],
                    'email_content': item[1][:100] + '...' if len(item[1]) > 100 else item[1],  # Truncate for display
                    'is_phishing': bool(item[2]),
                    'confidence_score': item[3],
                    'rule_score': item[4],
                    'ml_prediction': item[5],
                    'ml_confidence': item[6],
                    'url_score': item[7],
                    'rule_reasons': item[8],
                    'url_reasons': item[9],
                    'analyzed_at': item[10]
                })
            logger.info(f"Retrieved {len(history_dict)} history items")
            return jsonify(history_dict)
        else:
            logger.warning("History tracking is disabled")
            return jsonify([])
    except Exception as e:
        logger.error(f"Error in get_history endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health_check():
    status = {
        'status': 'healthy', 
        'ml_model_trained': detector.ml_model.is_trained,
        'system': 'phishing_detector',
        'database': 'connected',
        'config': {
            'phishing_threshold': Config.PHISHING_THRESHOLD,
            'ml_weight': Config.ML_WEIGHT,
            'rule_weight': Config.RULE_WEIGHT
        }
    }
    logger.info("Health check requested")
    return jsonify(status)

@app.route('/stats')
def get_stats():
    """Get system statistics"""
    try:
        if Config.ENABLE_HISTORY_TRACKING:
            history = db.get_analysis_history(100)  # Get last 100 records for stats
            total_analyses = len(history)
            phishing_count = sum(1 for item in history if item[2])  # item[2] is is_phishing
            safe_count = total_analyses - phishing_count
            
            stats = {
                'total_analyses': total_analyses,
                'phishing_detected': phishing_count,
                'safe_emails': safe_count,
                'phishing_percentage': (phishing_count / total_analyses * 100) if total_analyses > 0 else 0
            }
        else:
            stats = {'total_analyses': 0, 'phishing_detected': 0, 'safe_emails': 0, 'phishing_percentage': 0}
        
        logger.info("Statistics retrieved")
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error in get_stats endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info("Starting Phishing Detection System...")
    print("Starting Phishing Detection System...")
    print("Visit http://localhost:5000 to use the web interface")
    print("API endpoints:")
    print("  - GET / - Web interface")
    print("  - POST /analyze - Analyze email content")
    print("  - GET /history - Get analysis history")
    print("  - GET /stats - Get system statistics")
    print("  - GET /health - Health check")
    app.run(debug=True, host='0.0.0.0', port=5000)