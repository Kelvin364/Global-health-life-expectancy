"""
Comprehensive API Testing Suite
Tests all endpoints of the Life Expectancy Prediction API
"""

import requests
import json
import sys
from typing import Dict, Any
import time

# API Base URL - change this when testing deployed version
BASE_URL = "http://localhost:8000"

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.BLUE}ℹ {text}{Colors.END}")


class APITester:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.results = {
            'passed': 0,
            'failed': 0,
            'warnings': 0
        }
    
    def test_endpoint(self, method: str, endpoint: str, data: Dict = None, 
                     expected_status: int = 200, test_name: str = "") -> bool:
        """Generic endpoint tester"""
        try:
            url = f"{self.base_url}{endpoint}"
            print_info(f"Testing: {test_name or endpoint}")
            print_info(f"URL: {url}")
            
            if method.upper() == "GET":
                response = requests.get(url, timeout=10)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, timeout=10)
            else:
                print_error(f"Unsupported method: {method}")
                return False
            
            # Check status code
            if response.status_code == expected_status:
                print_success(f"Status Code: {response.status_code} ✓")
            else:
                print_error(f"Status Code: {response.status_code} (Expected: {expected_status})")
                self.results['failed'] += 1
                return False
            
            # Try to parse JSON
            try:
                response_data = response.json()
                print_success(f"Valid JSON Response ✓")
                print(f"Response: {json.dumps(response_data, indent=2)[:500]}...")
            except:
                print_error("Invalid JSON Response")
                self.results['failed'] += 1
                return False
            
            self.results['passed'] += 1
            return True
            
        except requests.exceptions.ConnectionError:
            print_error(f"Connection Error: Could not connect to {url}")
            print_warning("Make sure the server is running: python main.py")
            self.results['failed'] += 1
            return False
        except requests.exceptions.Timeout:
            print_error("Request Timeout")
            self.results['failed'] += 1
            return False
        except Exception as e:
            print_error(f"Unexpected Error: {str(e)}")
            self.results['failed'] += 1
            return False
    
    def print_summary(self):
        """Print test summary"""
        print_header("TEST SUMMARY")
        total = self.results['passed'] + self.results['failed']
        
        print(f"Total Tests: {total}")
        print_success(f"Passed: {self.results['passed']}")
        print_error(f"Failed: {self.results['failed']}")
        print_warning(f"Warnings: {self.results['warnings']}")
        
        success_rate = (self.results['passed'] / total * 100) if total > 0 else 0
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        if self.results['failed'] == 0:
            print_success("\n🎉 ALL TESTS PASSED! API is ready for deployment!")
            return True
        else:
            print_error(f"\n⚠ {self.results['failed']} test(s) failed. Fix issues before deploying!")
            return False


def test_root_endpoint(tester: APITester):
    """Test 1: Root endpoint"""
    print_header("TEST 1: Root Endpoint (/)")
    
    success = tester.test_endpoint(
        method="GET",
        endpoint="/",
        test_name="Root endpoint"
    )
    
    if success:
        print_success("Root endpoint is working correctly")
    else:
        print_error("Root endpoint test failed")
    
    return success


def test_health_endpoint(tester: APITester):
    """Test 2: Health check endpoint"""
    print_header("TEST 2: Health Check Endpoint (/health)")
    
    success = tester.test_endpoint(
        method="GET",
        endpoint="/health",
        test_name="Health check"
    )
    
    if success:
        # Additional validation for health check
        try:
            response = requests.get(f"{tester.base_url}/health")
            data = response.json()
            
            if data.get('model_loaded') == True:
                print_success("Model is loaded ✓")
            else:
                print_error("Model is NOT loaded!")
                tester.results['warnings'] += 1
            
            if data.get('status') == 'healthy':
                print_success("API status is healthy ✓")
            else:
                print_warning(f"API status: {data.get('status')}")
                tester.results['warnings'] += 1
                
        except Exception as e:
            print_error(f"Error validating health check: {e}")
    
    return success


def test_feature_info_endpoint(tester: APITester):
    """Test 3: Feature info endpoint"""
    print_header("TEST 3: Feature Info Endpoint (/feature-info)")
    
    success = tester.test_endpoint(
        method="GET",
        endpoint="/feature-info",
        test_name="Feature information"
    )
    
    if success:
        try:
            response = requests.get(f"{tester.base_url}/feature-info")
            data = response.json()
            
            if 'features' in data:
                feature_count = len(data['features'])
                print_success(f"Feature info returned {feature_count} features")
                
                # Verify all expected features are present
                expected_features = [
                    'adult_mortality', 'infant_deaths', 'alcohol', 
                    'percentage_expenditure', 'hepatitis_b', 'measles',
                    'bmi', 'under_five_deaths', 'polio', 'total_expenditure',
                    'diphtheria', 'hiv_aids', 'gdp', 'population',
                    'thinness_1_19_years', 'thinness_5_9_years',
                    'income_composition_of_resources', 'schooling', 'status_numeric'
                ]
                
                missing = [f for f in expected_features if f not in data['features']]
                if missing:
                    print_warning(f"Missing features in documentation: {missing}")
                else:
                    print_success("All expected features are documented ✓")
            
        except Exception as e:
            print_error(f"Error validating feature info: {e}")
    
    return success


def test_predict_endpoint_valid(tester: APITester):
    """Test 4: Prediction endpoint with valid data"""
    print_header("TEST 4: Prediction Endpoint - Valid Data (/predict)")
    
    # Sample valid data
    valid_data = {
        "adult_mortality": 150.0,
        "infant_deaths": 20.0,
        "alcohol": 5.0,
        "percentage_expenditure": 500.0,
        "hepatitis_b": 85.0,
        "measles": 100.0,
        "bmi": 30.0,
        "under_five_deaths": 25.0,
        "polio": 90.0,
        "total_expenditure": 6.5,
        "diphtheria": 88.0,
        "hiv_aids": 1.0,
        "gdp": 5000.0,
        "population": 10000000.0,
        "thinness_1_19_years": 5.0,
        "thinness_5_9_years": 5.0,
        "income_composition_of_resources": 0.65,
        "schooling": 12.0,
        "status_numeric": 0
    }
    
    print(f"Input Data:\n{json.dumps(valid_data, indent=2)}")
    
    success = tester.test_endpoint(
        method="POST",
        endpoint="/predict",
        data=valid_data,
        test_name="Prediction with valid data"
    )
    
    if success:
        try:
            response = requests.post(f"{tester.base_url}/predict", json=valid_data)
            data = response.json()
            
            prediction = data.get('predicted_life_expectancy')
            if prediction:
                print_success(f"Prediction: {prediction} years")
                
                # Validate prediction range
                if 30 <= prediction <= 100:
                    print_success("Prediction is in reasonable range (30-100 years) ✓")
                else:
                    print_warning(f"Prediction {prediction} seems unusual")
                    tester.results['warnings'] += 1
            
            if 'input_summary' in data:
                print_success("Input summary included in response ✓")
            
        except Exception as e:
            print_error(f"Error validating prediction: {e}")
    
    return success


def test_predict_endpoint_developed_country(tester: APITester):
    """Test 5: Prediction for developed country"""
    print_header("TEST 5: Prediction - Developed Country")
    
    developed_country_data = {
        "adult_mortality": 80.0,
        "infant_deaths": 2.0,
        "alcohol": 10.0,
        "percentage_expenditure": 5000.0,
        "hepatitis_b": 99.0,
        "measles": 5.0,
        "bmi": 55.0,
        "under_five_deaths": 3.0,
        "polio": 99.0,
        "total_expenditure": 8.5,
        "diphtheria": 99.0,
        "hiv_aids": 0.1,
        "gdp": 40000.0,
        "population": 50000000.0,
        "thinness_1_19_years": 1.0,
        "thinness_5_9_years": 1.0,
        "income_composition_of_resources": 0.9,
        "schooling": 16.0,
        "status_numeric": 1
    }
    
    success = tester.test_endpoint(
        method="POST",
        endpoint="/predict",
        data=developed_country_data,
        test_name="Developed country prediction"
    )
    
    if success:
        try:
            response = requests.post(f"{tester.base_url}/predict", json=developed_country_data)
            data = response.json()
            prediction = data.get('predicted_life_expectancy')
            
            if prediction and prediction >= 70:
                print_success(f"Prediction for developed country: {prediction} years (>= 70) ✓")
            else:
                print_warning(f"Developed country prediction seems low: {prediction}")
                
        except Exception as e:
            print_error(f"Error: {e}")
    
    return success


def test_predict_endpoint_developing_country(tester: APITester):
    """Test 6: Prediction for developing country"""
    print_header("TEST 6: Prediction - Developing Country")
    
    developing_country_data = {
        "adult_mortality": 300.0,
        "infant_deaths": 50.0,
        "alcohol": 2.0,
        "percentage_expenditure": 100.0,
        "hepatitis_b": 60.0,
        "measles": 1000.0,
        "bmi": 20.0,
        "under_five_deaths": 70.0,
        "polio": 65.0,
        "total_expenditure": 4.0,
        "diphtheria": 60.0,
        "hiv_aids": 5.0,
        "gdp": 1000.0,
        "population": 20000000.0,
        "thinness_1_19_years": 10.0,
        "thinness_5_9_years": 10.0,
        "income_composition_of_resources": 0.4,
        "schooling": 8.0,
        "status_numeric": 0
    }
    
    success = tester.test_endpoint(
        method="POST",
        endpoint="/predict",
        data=developing_country_data,
        test_name="Developing country prediction"
    )
    
    if success:
        try:
            response = requests.post(f"{tester.base_url}/predict", json=developing_country_data)
            data = response.json()
            prediction = data.get('predicted_life_expectancy')
            
            if prediction:
                print_success(f"Prediction for developing country: {prediction} years")
                
        except Exception as e:
            print_error(f"Error: {e}")
    
    return success


def test_predict_endpoint_edge_cases(tester: APITester):
    """Test 7: Prediction with edge cases"""
    print_header("TEST 7: Prediction - Edge Cases")
    
    edge_cases = [
        {
            "name": "Minimum values",
            "data": {
                "adult_mortality": 1.0,
                "infant_deaths": 0.0,
                "alcohol": 0.0,
                "percentage_expenditure": 0.0,
                "hepatitis_b": 0.0,
                "measles": 0.0,
                "bmi": 10.0,
                "under_five_deaths": 0.0,
                "polio": 0.0,
                "total_expenditure": 0.0,
                "diphtheria": 0.0,
                "hiv_aids": 0.0,
                "gdp": 0.0,
                "population": 1000.0,
                "thinness_1_19_years": 0.0,
                "thinness_5_9_years": 0.0,
                "income_composition_of_resources": 0.0,
                "schooling": 0.0,
                "status_numeric": 0
            }
        },
        {
            "name": "Maximum values",
            "data": {
                "adult_mortality": 500.0,
                "infant_deaths": 100.0,
                "alcohol": 15.0,
                "percentage_expenditure": 10000.0,
                "hepatitis_b": 100.0,
                "measles": 5000.0,
                "bmi": 70.0,
                "under_five_deaths": 150.0,
                "polio": 100.0,
                "total_expenditure": 15.0,
                "diphtheria": 100.0,
                "hiv_aids": 20.0,
                "gdp": 100000.0,
                "population": 1000000000.0,
                "thinness_1_19_years": 20.0,
                "thinness_5_9_years": 20.0,
                "income_composition_of_resources": 1.0,
                "schooling": 20.0,
                "status_numeric": 1
            }
        }
    ]
    
    all_passed = True
    for case in edge_cases:
        print(f"\n--- Testing: {case['name']} ---")
        success = tester.test_endpoint(
            method="POST",
            endpoint="/predict",
            data=case['data'],
            test_name=case['name']
        )
        
        if success:
            try:
                response = requests.post(f"{tester.base_url}/predict", json=case['data'])
                data = response.json()
                prediction = data.get('predicted_life_expectancy')
                print_success(f"{case['name']} prediction: {prediction} years")
            except:
                pass
        
        all_passed = all_passed and success
    
    return all_passed


def test_predict_endpoint_invalid_data(tester: APITester):
    """Test 8: Prediction with invalid data"""
    print_header("TEST 8: Prediction - Invalid Data (Should Fail)")
    
    invalid_cases = [
        {
            "name": "Missing required field",
            "data": {
                "adult_mortality": 150.0,
                # Missing other required fields
            },
            "expected_status": 422
        },
        {
            "name": "Invalid data type",
            "data": {
                "adult_mortality": "not_a_number",
                "infant_deaths": 20.0,
                "alcohol": 5.0,
                "percentage_expenditure": 500.0,
                "hepatitis_b": 85.0,
                "measles": 100.0,
                "bmi": 30.0,
                "under_five_deaths": 25.0,
                "polio": 90.0,
                "total_expenditure": 6.5,
                "diphtheria": 88.0,
                "hiv_aids": 1.0,
                "gdp": 5000.0,
                "population": 10000000.0,
                "thinness_1_19_years": 5.0,
                "thinness_5_9_years": 5.0,
                "income_composition_of_resources": 0.65,
                "schooling": 12.0,
                "status_numeric": 0
            },
            "expected_status": 422
        },
        {
            "name": "Out of range value",
            "data": {
                "adult_mortality": 150.0,
                "infant_deaths": 20.0,
                "alcohol": 5.0,
                "percentage_expenditure": 500.0,
                "hepatitis_b": 150.0,  # Out of range (max 100)
                "measles": 100.0,
                "bmi": 30.0,
                "under_five_deaths": 25.0,
                "polio": 90.0,
                "total_expenditure": 6.5,
                "diphtheria": 88.0,
                "hiv_aids": 1.0,
                "gdp": 5000.0,
                "population": 10000000.0,
                "thinness_1_19_years": 5.0,
                "thinness_5_9_years": 5.0,
                "income_composition_of_resources": 0.65,
                "schooling": 12.0,
                "status_numeric": 0
            },
            "expected_status": 422
        }
    ]
    
    all_passed = True
    for case in invalid_cases:
        print(f"\n--- Testing: {case['name']} ---")
        success = tester.test_endpoint(
            method="POST",
            endpoint="/predict",
            data=case['data'],
            expected_status=case['expected_status'],
            test_name=case['name']
        )
        
        if success:
            print_success(f"Correctly rejected: {case['name']} ✓")
        
        all_passed = all_passed and success
    
    return all_passed


def test_docs_endpoint(tester: APITester):
    """Test 9: Swagger docs endpoint"""
    print_header("TEST 9: API Documentation (/docs)")
    
    try:
        response = requests.get(f"{tester.base_url}/docs", timeout=10)
        
        if response.status_code == 200:
            print_success("Swagger documentation is accessible ✓")
            print_info(f"Docs URL: {tester.base_url}/docs")
            tester.results['passed'] += 1
            return True
        else:
            print_error(f"Docs endpoint returned status {response.status_code}")
            tester.results['failed'] += 1
            return False
            
    except Exception as e:
        print_error(f"Error accessing docs: {e}")
        tester.results['failed'] += 1
        return False


def test_response_time(tester: APITester):
    """Test 10: Response time check"""
    print_header("TEST 10: Response Time Check")
    
    test_data = {
        "adult_mortality": 150.0,
        "infant_deaths": 20.0,
        "alcohol": 5.0,
        "percentage_expenditure": 500.0,
        "hepatitis_b": 85.0,
        "measles": 100.0,
        "bmi": 30.0,
        "under_five_deaths": 25.0,
        "polio": 90.0,
        "total_expenditure": 6.5,
        "diphtheria": 88.0,
        "hiv_aids": 1.0,
        "gdp": 5000.0,
        "population": 10000000.0,
        "thinness_1_19_years": 5.0,
        "thinness_5_9_years": 5.0,
        "income_composition_of_resources": 0.65,
        "schooling": 12.0,
        "status_numeric": 0
    }
    
    try:
        start_time = time.time()
        response = requests.post(f"{tester.base_url}/predict", json=test_data, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        print_info(f"Response Time: {response_time:.2f}ms")
        
        if response_time < 1000:
            print_success("Response time is good (< 1 second) ✓")
        elif response_time < 5000:
            print_warning(f"Response time is acceptable but could be better")
            tester.results['warnings'] += 1
        else:
            print_warning(f"Response time is slow (> 5 seconds)")
            tester.results['warnings'] += 1
        
        tester.results['passed'] += 1
        return True
        
    except Exception as e:
        print_error(f"Error measuring response time: {e}")
        tester.results['failed'] += 1
        return False


def main():
    """Run all tests"""
    print_header("LIFE EXPECTANCY API - COMPREHENSIVE TEST SUITE")
    
    print_info(f"Testing API at: {BASE_URL}")
    print_info("Make sure the API is running: python main.py\n")
    
    # Initialize tester
    tester = APITester(BASE_URL)
    
    # Run all tests
    tests = [
        ("Root Endpoint", test_root_endpoint),
        ("Health Check", test_health_endpoint),
        ("Feature Info", test_feature_info_endpoint),
        ("Prediction - Valid Data", test_predict_endpoint_valid),
        ("Prediction - Developed Country", test_predict_endpoint_developed_country),
        ("Prediction - Developing Country", test_predict_endpoint_developing_country),
        ("Prediction - Edge Cases", test_predict_endpoint_edge_cases),
        ("Prediction - Invalid Data", test_predict_endpoint_invalid_data),
        ("API Documentation", test_docs_endpoint),
        ("Response Time", test_response_time)
    ]
    
    for test_name, test_func in tests:
        try:
            test_func(tester)
        except KeyboardInterrupt:
            print_error("\n\nTests interrupted by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Test '{test_name}' crashed: {e}")
            tester.results['failed'] += 1
    
    # Print summary
    success = tester.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()