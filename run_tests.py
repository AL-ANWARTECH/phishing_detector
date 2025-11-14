import unittest
import sys
import os
from datetime import datetime

def run_tests():
    """Run all tests and generate a report"""
    print("Starting Phishing Detection System Tests...")
    print(f"Test Run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Discover and run all tests
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Create test runner with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%" if result.testsRun > 0 else "0%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"  {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"  {test}: {traceback}")
    
    # Return success status
    return len(result.failures) == 0 and len(result.errors) == 0

def run_specific_test(test_file):
    """Run a specific test file"""
    print(f"Running specific test: {test_file}")
    
    # Import and run specific test
    if test_file == "unit":
        from test_phishing_detector import TestEmailParser, TestRuleEngine, TestMLModel, TestURLAnalyzer, TestPhishingDetector, TestDatabase, TestConfiguration, TestIntegration
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestEmailParser))
        suite.addTest(unittest.makeSuite(TestRuleEngine))
        suite.addTest(unittest.makeSuite(TestMLModel))
        suite.addTest(unittest.makeSuite(TestURLAnalyzer))
        suite.addTest(unittest.makeSuite(TestPhishingDetector))
        suite.addTest(unittest.makeSuite(TestDatabase))
        suite.addTest(unittest.makeSuite(TestConfiguration))
        suite.addTest(unittest.makeSuite(TestIntegration))
    elif test_file == "integration":
        from integration_tests import TestAPIIntegration, TestCLIToAPIIntegration, TestPerformance, TestErrorHandling
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestAPIIntegration))
        suite.addTest(unittest.makeSuite(TestCLIToAPIIntegration))
        suite.addTest(unittest.makeSuite(TestPerformance))
        suite.addTest(unittest.makeSuite(TestErrorHandling))
    else:
        print(f"Unknown test type: {test_file}")
        return False
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test
        test_type = sys.argv[1]
        success = run_specific_test(test_type)
    else:
        # Run all tests
        success = run_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)