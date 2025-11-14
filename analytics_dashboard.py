from flask import Flask, render_template_string, jsonify
from performance_monitor import get_performance_monitor
import json

app = Flask(__name__)
monitor = get_performance_monitor()

# HTML template for analytics dashboard
DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Phishing Detection System - Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
        .stat-card { background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }
        .stat-value { font-size: 2em; font-weight: bold; color: #007bff; }
        .stat-label { font-size: 0.9em; color: #6c757d; }
        .chart-container { margin: 30px 0; height: 300px; }
        .refresh-btn { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 20px; }
        .refresh-btn:hover { background: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Phishing Detection System - Analytics Dashboard</h1>
            <p>Real-time monitoring and performance analytics</p>
        </div>
        
        <button class="refresh-btn" onclick="refreshDashboard()">Refresh Data</button>
        
        <div class="stats-grid" id="statsGrid">
            <!-- Stats will be populated by JavaScript -->
        </div>
        
        <div class="chart-container">
            <canvas id="cpuChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="memoryChart"></canvas>
        </div>
        
        <div class="chart-container">
            <canvas id="analysisTimeChart"></canvas>
        </div>
    </div>

    <script>
        let cpuChart, memoryChart, analysisTimeChart;
        
        async function refreshDashboard() {
            try {
                // Get performance stats
                const statsResponse = await fetch('/api/performance/stats');
                const stats = await statsResponse.json();
                
                // Update stats grid
                updateStatsGrid(stats);
                
                // Get system history
                const historyResponse = await fetch('/api/performance/history');
                const history = await historyResponse.json();
                
                // Update charts
                updateCharts(history, stats);
                
            } catch (error) {
                console.error('Error refreshing dashboard:', error);
            }
        }
        
        function updateStatsGrid(stats) {
            const statsGrid = document.getElementById('statsGrid');
            statsGrid.innerHTML = `
                <div class="stat-card">
                    <div class="stat-value">${stats.total_analyses}</div>
                    <div class="stat-label">Total Analyses</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.phishing_detected}</div>
                    <div class="stat-label">Phishing Detected</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.safe_emails}</div>
                    <div class="stat-label">Safe Emails</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.phishing_rate.toFixed(1)}%</div>
                    <div class="stat-label">Phishing Rate</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.avg_analysis_time.toFixed(3)}s</div>
                    <div class="stat-label">Avg Analysis Time</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.current_cpu}%</div>
                    <div class="stat-label">Current CPU</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.current_memory}%</div>
                    <div class="stat-label">Current Memory</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">${stats.success_rate.toFixed(1)}%</div>
                    <div class="stat-label">Success Rate</div>
                </div>
            `;
        }
        
        function updateCharts(history, stats) {
            // Update or create CPU chart
            if (cpuChart) {
                cpuChart.destroy();
            }
            const cpuCtx = document.getElementById('cpuChart').getContext('2d');
            cpuChart = new Chart(cpuCtx, {
                type: 'line',
                data: {
                    labels: history.cpu_history.map(point => new Date(point.timestamp).toLocaleTimeString()),
                    datasets: [{
                        label: 'CPU Usage (%)',
                        data: history.cpu_history.map(point => point.value),
                        borderColor: 'rgb(255, 99, 132)',
                        backgroundColor: 'rgba(255, 99, 132, 0.1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'CPU Usage Over Time'
                        }
                    }
                }
            });
            
            // Update or create Memory chart
            if (memoryChart) {
                memoryChart.destroy();
            }
            const memoryCtx = document.getElementById('memoryChart').getContext('2d');
            memoryChart = new Chart(memoryCtx, {
                type: 'line',
                data: {
                    labels: history.memory_history.map(point => new Date(point.timestamp).toLocaleTimeString()),
                    datasets: [{
                        label: 'Memory Usage (%)',
                        data: history.memory_history.map(point => point.value),
                        borderColor: 'rgb(54, 162, 235)',
                        backgroundColor: 'rgba(54, 162, 235, 0.1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Memory Usage Over Time'
                        }
                    }
                }
            });
            
            // Update or create Analysis Time chart
            if (analysisTimeChart) {
                analysisTimeChart.destroy();
            }
            const timeCtx = document.getElementById('analysisTimeChart').getContext('2d');
            analysisTimeChart = new Chart(timeCtx, {
                type: 'line',
                data: {
                    labels: history.analysis_times.map((_, i) => i + 1),
                    datasets: [{
                        label: 'Analysis Time (seconds)',
                        data: history.analysis_times,
                        borderColor: 'rgb(75, 192, 192)',
                        backgroundColor: 'rgba(75, 192, 192, 0.1)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Analysis Time Over Recent Analyses'
                        }
                    }
                }
            });
        }
        
        // Initial load
        refreshDashboard();
        
        // Refresh every 30 seconds
        setInterval(refreshDashboard, 30000);
    </script>
</body>
</html>
'''

@app.route('/analytics')
def dashboard():
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/performance/stats')
def get_performance_stats():
    stats = monitor.get_performance_stats()
    return jsonify(stats)

@app.route('/api/performance/history')
def get_performance_history():
    history = monitor.get_system_history(minutes=5)  # Last 5 minutes
    return jsonify(history)

@app.route('/api/performance/trends')
def get_performance_trends():
    trends = monitor.get_analysis_trends(hours=24)
    return jsonify(trends)

@app.route('/api/performance/current')
def get_current_metrics():
    metrics = monitor.get_current_metrics()
    return jsonify(metrics)

if __name__ == '__main__':
    print("Starting Analytics Dashboard...")
    print("Visit http://localhost:5001/analytics to view the dashboard")
    app.run(debug=True, host='0.0.0.0', port=5001)