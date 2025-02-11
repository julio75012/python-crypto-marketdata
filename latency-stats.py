import sys
import json
import numpy as np

def process_line(line):
    # Split timestamp and json data
    timestamp, json_data = line.split(' ', 1)
    timestamp = float(timestamp)
    
    # Parse JSON data
    data = json.loads(json_data)
    
    # Extract event time from data
    event_time = data['data']['E']
    
    # Calculate latency
    latency = timestamp/1000 - event_time  # Convert to milliseconds
    
    return latency

def calculate_statistics(latencies):
    stats = {
        'count': len(latencies),
        'mean': np.mean(latencies),
        'std': np.std(latencies),
        'min': np.min(latencies),
        'max': np.max(latencies),
        'percentiles': {
            '0.1': np.percentile(latencies, 0.1),
            '1': np.percentile(latencies, 1),
            '5': np.percentile(latencies, 5),
            '10': np.percentile(latencies, 10),
            '25': np.percentile(latencies, 25),
            '50': np.percentile(latencies, 50),
            '75': np.percentile(latencies, 75),
            '80': np.percentile(latencies, 80),
            '90': np.percentile(latencies, 90),
            '95': np.percentile(latencies, 95),
            '99': np.percentile(latencies, 99),
            '99.9': np.percentile(latencies, 99.9)
        }
    }
    return stats

def main(filename):
    latencies = []
    
    with open(filename, 'r') as f:
        for line in f:
            try:
                latency = process_line(line.strip())
                latencies.append(latency)
            except (ValueError, KeyError, json.JSONDecodeError):
                continue
    
    if latencies:
        stats = calculate_statistics(latencies)
        print("Latency Statistics (in milliseconds):")
        print(f"Count: {stats['count']}")
        print(f"Mean: {stats['mean']:.4f}")
        print(f"Std Dev: {stats['std']:.4f}")
        print(f"Min: {stats['min']:.4f}")
        print(f"Max: {stats['max']:.4f}")
        print("\nPercentiles:")
        for p, value in stats['percentiles'].items():
            print(f"{p}%: {value:.4f}")
    else:
        print("No valid data found in the file.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
        sys.exit(1)
    
    filename = sys.argv[1]
    main(filename)
