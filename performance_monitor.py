import time
import psutil
import threading
from datetime import datetime, timedelta
from collections import deque, defaultdict
import json
import os

class PerformanceMonitor:
    def __init__(self, max_samples=100):
        self.max_samples = max_samples
        self.cpu_history = deque(maxlen=max_samples)
        self.memory_history = deque(maxlen=max_samples)
        self.analysis_times = deque(maxlen=max_samples)
        self.analysis_results = deque(maxlen=max_samples)
        self.start_time = datetime.now()
        self.is_monitoring = False
        self.monitoring_thread = None
        
        # Statistics
        self.total_analyses = 0
        self.phishing_detected = 0
        self.safe_emails = 0
        self.error_count = 0
        
        # Performance metrics
        self.avg_analysis_time = 0
        self.max_analysis_time = 0
        self.min_analysis_time = float('inf')
    
    def start_monitoring(self):
        """Start performance monitoring in a separate thread"""
        if not self.is_monitoring:
            self.is_monitoring = True
            self.monitoring_thread = threading.Thread(target=self._monitor_system, daemon=True)
            self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
    
    def _monitor_system(self):
        """Monitor system resources in a separate thread"""
        while self.is_monitoring:
            try:
                # Get current system metrics
                cpu_percent = psutil.cpu_percent(interval=1)
                memory_percent = psutil.virtual_memory().percent
                
                # Store in history
                self.cpu_history.append({
                    'timestamp': datetime.now(),
                    'value': cpu_percent
                })
                
                self.memory_history.append({
                    'timestamp': datetime.now(),
                    'value': memory_percent
                })
                
                time.sleep(1)  # Monitor every second
            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(1)
    
    def record_analysis(self, analysis_time, is_phishing, success=True):
        """Record an analysis event"""
        self.total_analyses += 1
        
        if success:
            if is_phishing:
                self.phishing_detected += 1
            else:
                self.safe_emails += 1
            
            # Update analysis time metrics
            self.analysis_times.append(analysis_time)
            self.avg_analysis_time = sum(self.analysis_times) / len(self.analysis_times)
            self.max_analysis_time = max(self.max_analysis_time, analysis_time)
            self.min_analysis_time = min(self.min_analysis_time, analysis_time) if self.min_analysis_time != float('inf') else analysis_time
        else:
            self.error_count += 1
    
    def get_current_metrics(self):
        """Get current system metrics"""
        return {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent,
            'process_count': len(psutil.pids()),
            'uptime': (datetime.now() - self.start_time).total_seconds()
        }
    
    def get_performance_stats(self):
        """Get performance statistics"""
        return {
            'total_analyses': self.total_analyses,
            'phishing_detected': self.phishing_detected,
            'safe_emails': self.safe_emails,
            'error_count': self.error_count,
            'phishing_rate': (self.phishing_detected / self.total_analyses * 100) if self.total_analyses > 0 else 0,
            'success_rate': ((self.total_analyses - self.error_count) / self.total_analyses * 100) if self.total_analyses > 0 else 0,
            'avg_analysis_time': self.avg_analysis_time,
            'max_analysis_time': self.max_analysis_time,
            'min_analysis_time': self.min_analysis_time if self.min_analysis_time != float('inf') else 0,
            'current_cpu': psutil.cpu_percent(),
            'current_memory': psutil.virtual_memory().percent
        }
    
    def get_system_history(self, minutes=10):
        """Get system metrics history for the last N minutes"""
        cutoff_time = datetime.now() - timedelta(minutes=minutes)
        
        cpu_data = [point for point in self.cpu_history if point['timestamp'] > cutoff_time]
        memory_data = [point for point in self.memory_history if point['timestamp'] > cutoff_time]
        
        return {
            'cpu_history': cpu_data,
            'memory_history': memory_data,
            'analysis_times': list(self.analysis_times)[-len(cpu_data):]  # Match the time window
        }
    
    def get_analysis_trends(self, hours=24):
        """Get analysis trends over time"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # This would be enhanced in a real implementation with database integration
        return {
            'total_analyses': self.total_analyses,
            'phishing_over_time': self.phishing_detected,  # Simplified for now
            'safe_over_time': self.safe_emails,
            'error_over_time': self.error_count
        }

# Global performance monitor instance
performance_monitor = PerformanceMonitor()

def get_performance_monitor():
    """Get the global performance monitor instance"""
    return performance_monitor

# Test function
def test_performance_monitor():
    monitor = PerformanceMonitor()
    monitor.start_monitoring()
    
    # Simulate some analysis times
    import random
    for i in range(10):
        analysis_time = random.uniform(0.1, 1.0)  # 0.1 to 1.0 seconds
        is_phishing = random.choice([True, False])
        monitor.record_analysis(analysis_time, is_phishing)
        time.sleep(0.1)
    
    stats = monitor.get_performance_stats()
    print("=== Performance Monitor Test Results ===")
    print(f"Total Analyses: {stats['total_analyses']}")
    print(f"Phishing Rate: {stats['phishing_rate']:.2f}%")
    print(f"Average Analysis Time: {stats['avg_analysis_time']:.3f}s")
    print(f"Current CPU: {stats['current_cpu']}%")
    print(f"Current Memory: {stats['current_memory']}%")
    
    monitor.stop_monitoring()

if __name__ == "__main__":
    test_performance_monitor()