import argparse
import sys
import os
from phishing_detector import PhishingDetector
from database import Database
from training_system import TrainingSystem
from email_processor import EmailProcessor
from logger import get_logger
from config import Config
import json

class PhishingDetectorCLI:
    def __init__(self):
        self.detector = PhishingDetector()
        self.db = Database()
        self.training_system = TrainingSystem()
        self.email_processor = EmailProcessor()
        self.logger = get_logger()
        self.config = Config()
        
        # Initialize with sample training data
        sample_data = self.training_system.load_sample_data()
        self.detector.train_model(sample_data)
        self.training_system.train_advanced_model(sample_data)
    
    def analyze_single_email(self, email_content, verbose=False):
        """Analyze a single email"""
        try:
            result = self.detector.analyze_email(email_content)
            
            if verbose:
                print("=== Detailed Analysis ===")
                print(f"Is Phishing: {result['is_phishing']}")
                print(f"Confidence Score: {result['confidence_score']:.2f}%")
                print(f"Rule Score: {result['rule_score']}")
                print(f"ML Prediction: {result['ml_prediction']} (Confidence: {result['ml_confidence']:.2f})")
                print(f"URL Score: {result['url_score']}")
                print(f"Rule Reasons: {', '.join(result['rule_reasons'])}")
                print(f"URL Reasons: {', '.join(result['url_reasons'])}")
            else:
                if result['is_phishing']:
                    print(f"⚠️  PHISHING DETECTED! (Confidence: {result['confidence_score']:.2f}%)")
                else:
                    print(f"✅ SAFE EMAIL (Confidence: {result['confidence_score']:.2f}%)")
            
            # Save to database
            self.db.save_analysis_result(email_content, result)
            
            return result
        except Exception as e:
            print(f"Error analyzing email: {str(e)}")
            return {'error': str(e)}
    
    def analyze_file(self, file_path, verbose=False):
        """Analyze email from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                email_content = f.read()
            
            print(f"Analyzing email from: {file_path}")
            return self.analyze_single_email(email_content, verbose)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
            return {'error': f"File not found: {file_path}"}
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            return {'error': str(e)}
    
    def analyze_directory(self, dir_path, verbose=False):
        """Analyze all email files in a directory"""
        results = []
        
        for filename in os.listdir(dir_path):
            if filename.lower().endswith(('.txt', '.eml', '.email')):
                file_path = os.path.join(dir_path, filename)
                print(f"\nAnalyzing: {filename}")
                result = self.analyze_file(file_path, verbose)
                results.append((filename, result))
        
        print(f"\n=== Directory Analysis Complete ===")
        print(f"Processed {len(results)} files")
        
        phishing_count = sum(1 for _, result in results if result.get('is_phishing', False))
        print(f"Phishing emails detected: {phishing_count}")
        
        return results
    
    def show_history(self, limit=10):
        """Show analysis history"""
        try:
            history = self.db.get_analysis_history(limit)
            
            if not history:
                print("No analysis history available.")
                return
            
            print(f"=== Last {len(history)} Analysis Results ===")
            for i, item in enumerate(history, 1):
                phishing_status = "PHISHING" if item[2] else "SAFE"
                print(f"{i}. {phishing_status} - Score: {item[3]:.2f}% - {item[10]}")
                print(f"   Rule: {item[4]}, ML: {item[5]} ({item[6]:.2f}), URL: {item[7]}")
        except Exception as e:
            print(f"Error retrieving history: {str(e)}")
    
    def train_model(self, training_file=None):
        """Train the model"""
        try:
            if training_file:
                # Load training data from file
                training_data = self.training_system.load_training_data(training_file)
                if not training_data:
                    print(f"Error loading training data from {training_file}")
                    return
            else:
                # Use sample training data
                training_data = self.training_system.load_sample_data()
            
            print(f"Training model with {len(training_data)} samples...")
            success = self.training_system.train_advanced_model(training_data)
            
            if success:
                print("Model training completed successfully!")
            else:
                print("Model training failed!")
        except Exception as e:
            print(f"Error training model: {str(e)}")
    
    def evaluate_model(self):
        """Evaluate model performance"""
        try:
            sample_data = self.training_system.load_sample_data()
            evaluation = self.training_system.evaluate_model(sample_data)
            
            if evaluation:
                print("=== Model Evaluation Results ===")
                for metric, value in evaluation.items():
                    print(f"{metric}: {value:.3f}")
            else:
                print("Model evaluation failed!")
        except Exception as e:
            print(f"Error evaluating model: {str(e)}")
    
    def batch_process(self, input_file, output_file=None):
        """Batch process multiple emails from a JSON file"""
        try:
            with open(input_file, 'r') as f:
                emails = json.load(f)
            
            results = []
            for i, email_content in enumerate(emails):
                print(f"Processing email {i+1}/{len(emails)}...")
                result = self.analyze_single_email(email_content)
                results.append(result)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"Results saved to {output_file}")
            else:
                print(f"Processed {len(emails)} emails")
            
            return results
        except Exception as e:
            print(f"Error in batch processing: {str(e)}")
            return []

def main():
    parser = argparse.ArgumentParser(
        description='Phishing Detection System - Command Line Interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s analyze --file email.txt
  %(prog)s analyze --file email.txt --verbose
  %(prog)s history
  %(prog)s train
  %(prog)s evaluate
  %(prog)s process-dir /path/to/emails
        '''
    )
    
    parser.add_argument('--version', action='version', version='Phishing Detector CLI 1.0')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an email')
    analyze_parser.add_argument('--file', '-f', help='Path to email file')
    analyze_parser.add_argument('--text', '-t', help='Email content as text')
    analyze_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # History command
    history_parser = subparsers.add_parser('history', help='Show analysis history')
    history_parser.add_argument('--limit', '-l', type=int, default=10, help='Number of results to show')
    
    # Train command
    train_parser = subparsers.add_parser('train', help='Train the model')
    train_parser.add_argument('--file', help='Training data file')
    
    # Evaluate command
    evaluate_parser = subparsers.add_parser('evaluate', help='Evaluate model performance')
    
    # Process directory command
    dir_parser = subparsers.add_parser('process-dir', help='Process all emails in a directory')
    dir_parser.add_argument('dir_path', help='Path to directory containing email files')
    dir_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Batch process command
    batch_parser = subparsers.add_parser('batch', help='Batch process emails from JSON file')
    batch_parser.add_argument('input_file', help='Input JSON file with emails')
    batch_parser.add_argument('--output', '-o', help='Output file for results')
    
    args = parser.parse_args()
    
    # Initialize CLI
    cli = PhishingDetectorCLI()
    
    if args.command == 'analyze':
        if args.file:
            cli.analyze_file(args.file, args.verbose)
        elif args.text:
            cli.analyze_single_email(args.text, args.verbose)
        else:
            print("Error: Please specify either --file or --text")
            parser.print_help()
    
    elif args.command == 'history':
        cli.show_history(args.limit)
    
    elif args.command == 'train':
        cli.train_model(args.file)
    
    elif args.command == 'evaluate':
        cli.evaluate_model()
    
    elif args.command == 'process-dir':
        cli.analyze_directory(args.dir_path, args.verbose)
    
    elif args.command == 'batch':
        cli.batch_process(args.input_file, args.output)
    
    elif args.command is None:
        parser.print_help()
    
    else:
        print(f"Unknown command: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()