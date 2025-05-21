"""
Script to test the Mobile Price Classification API
"""
import requests
import argparse
import json
import sys
import random

def generate_random_mobile_data():
    """
    Generate random mobile features for testing
    """
    return {
        "battery_power": random.randint(500, 2000),
        "blue": random.randint(0, 1),
        "clock_speed": round(random.uniform(0.5, 3.0), 1),
        "dual_sim": random.randint(0, 1),
        "fc": random.randint(0, 20),
        "four_g": random.randint(0, 1),
        "int_memory": random.randint(2, 64),
        "m_dep": round(random.uniform(0.1, 1.0), 1),
        "mobile_wt": random.randint(80, 200),
        "n_cores": random.randint(1, 8),
        "pc": random.randint(0, 20),
        "px_height": random.randint(0, 2000),
        "px_width": random.randint(0, 2000),
        "ram": random.randint(256, 4000),
        "sc_h": random.randint(5, 20),
        "sc_w": random.randint(0, 20),
        "talk_time": random.randint(2, 20),
        "three_g": random.randint(0, 1),
        "touch_screen": random.randint(0, 1),
        "wifi": random.randint(0, 1)
    }

def main():
    parser = argparse.ArgumentParser(description='Test the Mobile Price Classification API')
    parser.add_argument('--url', type=str, default='http://localhost:8000', help='API server URL')
    parser.add_argument('--batch', action='store_true', help='Test batch prediction')
    parser.add_argument('--batch-size', type=int, default=5, help='Batch size for batch prediction')
    args = parser.parse_args()
    
    # Verify API is running
    try:
        response = requests.get(f"{args.url}/health")
        if response.status_code != 200:
            print(f"Error: API server returned status code {response.status_code}")
            sys.exit(1)
        
        health_check = response.json()
        if not health_check["status"] == "ok":
            print(f"Error: API server health check failed: {health_check}")
            sys.exit(1)
            
        print("API server is running and healthy")
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API server at {args.url}")
        print("Make sure the server is running and the URL is correct")
        sys.exit(1)
    
    if args.batch:
        # Generate random data for batch prediction
        mobile_data_list = [generate_random_mobile_data() for _ in range(args.batch_size)]
        
        print(f"Sending batch of {args.batch_size} mobile devices to {args.url}/predict_batch...")
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f"{args.url}/predict_batch",
                json=mobile_data_list,
                headers=headers
            )
            
            if response.status_code != 200:
                print(f"Error: API server returned status code {response.status_code}")
                print(response.text)
                sys.exit(1)
            
            results = response.json()
            
            print(f"\nBatch Prediction Results ({len(results)} devices):")
            
            for i, result in enumerate(results):
                print(f"\nDevice {i+1}:")
                print(f"Price Category: {result['price_category']} - {result['category_name']}")
                print("Probabilities:")
                for class_idx, prob in result['probabilities'].items():
                    print(f"  Class {class_idx}: {prob:.4f}")
                
        except Exception as e:
            print(f"Error during batch prediction: {e}")
            sys.exit(1)
            
    else:
        # Generate random data for single prediction
        mobile_data = generate_random_mobile_data()
        
        print(f"Mobile features to be evaluated:")
        for feature, value in mobile_data.items():
            print(f"  {feature}: {value}")
            
        print(f"\nSending request to {args.url}/predict...")
        
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(
                f"{args.url}/predict",
                json=mobile_data,
                headers=headers
            )
            
            if response.status_code != 200:
                print(f"Error: API server returned status code {response.status_code}")
                print(response.text)
                sys.exit(1)
            
            result = response.json()
            
            # Display results
            print("\nPrediction Result:")
            print(f"Price Category: {result['price_category']} - {result['category_name']}")
            
            print("\nClass probabilities:")
            for class_idx, prob in result['probabilities'].items():
                print(f"  Class {class_idx}: {prob:.4f}")
                
        except Exception as e:
            print(f"Error during prediction: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main() 