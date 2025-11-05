# src/data_processing.py

import re
import pandas as pd
import numpy as np
from pathlib import Path

def _extract_log_level(message):
    """
    Extracts a log level (e.g., ERROR, INFO) from a log message string.

    This is a private helper function that uses a regular expression to find
    a log level enclosed in square brackets. If no level is found, it
    defaults to 'INFO'.
    """
    level_pattern = r'\[(\w+)\]'
    match = re.search(level_pattern, message)
    if match:
        return match.group(1)
    else:
        return 'INFO'

def load_and_parse_logs(log_file_path):
    """
    Loads a log file, parses it line-by-line, and returns a DataFrame.

    This function is designed to handle a syslog-style format and extracts
    key information like timestamps, hostnames, processes, and messages.
    """
    # This regex acts as a "Noise Filter" for the syslog format.
    log_pattern = re.compile(r'^(.{15})\s+([\w\d\.-]+)\s+([^:]+):\s+(.*)$')
    
    data = []
    print(f"Starting log parsing from: {log_file_path}")
    
    try:
        with open(log_file_path, 'r') as f:
            for line in f:
                match = log_pattern.match(line)
                if match:
                    data.append({
                        'timestamp_str': match.group(1),
                        'hostname': match.group(2),
                        'process': match.group(3).strip(),
                        'message': match.group(4).strip()
                    })
        
        if not data:
            print("No log entries matched the pattern. Check regex.")
            return pd.DataFrame()

        print(f"--- CTA Parser finished. Found {len(data)} log entries. ---")
        
        df = pd.DataFrame(data, columns=['timestamp_str', 'hostname', 'process', 'message'])
        
        # --- Timestamp Cleaning ---
        # Explicitly setting the format improves parsing speed and accuracy.
        df['timestamp'] = pd.to_datetime(df['timestamp_str'], format="%b %d %H:%M:%S")
        
        # Syslog timestamps often lack a year, so we add the current one.
        current_year = pd.Timestamp.now().year
        df['timestamp'] = df['timestamp'].apply(lambda x: x.replace(year=current_year))
        
        # --- Initial Feature Extraction ---
        df['log_level'] = df['message'].apply(_extract_log_level)
        df['hour_of_day'] = df['timestamp'].dt.hour
        
        # Drop the original timestamp string column.
        df = df.drop(columns=['timestamp_str'])
        
        return df

    except FileNotFoundError:
        print(f"--- ERROR: File Not Found ---")
        print(f"Could not find the log file at this path: {log_file_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"An unexpected error occurred during parsing: {e}")
        return pd.DataFrame()

def engineer_features(df, ip_report_cache):
    """
    Engineers the final features (X, y) for model training.

    This function takes the parsed log DataFrame and the threat intelligence
    cache, and creates the final feature set for the machine learning model.
    """
    print("Engineering features for the model...")
    features_df = df.copy()
    
    # --- 1. Merge Threat Intelligence Data ---
    # Map the abuse score and country from the cache to the DataFrame.
    features_df['abuse_score'] = features_df['ip_address'].map(lambda ip: ip_report_cache.get(ip, {}).get('abuse_score'))
    features_df['country'] = features_df['ip_address'].map(lambda ip: ip_report_cache.get(ip, {}).get('country'))
    
    # Replace missing (NaN) values with appropriate defaults.
    features_df['abuse_score'] = features_df['abuse_score'].fillna(0)
    features_df['country'] = features_df['country'].fillna('N/A')
    
    # --- 2. Create Target Variable (y) ---
    # Define our "Signal" by looking for threat indicators.
    signal_1 = features_df['message'].str.contains("Failed password")
    signal_2 = features_df['abuse_score'] > 50
    features_df['is_threat'] = np.where(signal_1 | signal_2, 1, 0)
    
    # --- 3. One-Hot Encode Categorical Features ---
    one_hot_features = pd.get_dummies(features_df['log_level'], prefix='log_level')
    features_df = pd.concat([features_df, one_hot_features], axis=1)
    
    # --- 4. Define Final Feature Set (X) and Target (y) ---
    X_columns = [
        'hour_of_day', 
        'abuse_score'
    ]
    X_columns.extend(one_hot_features.columns)
    
    # Ensure all expected one-hot encoded columns exist.
    # This prevents errors if a log sample is missing a specific log level.
    all_expected_cols = ['log_level_INFO', 'log_level_ERROR', 'log_level_WARNING']
    for col in all_expected_cols:
       if col not in features_df.columns:
           features_df[col] = False # Add missing column as False (0).
           
    # Select the final columns for the feature matrix.
    X = features_df[X_columns]
    y = features_df['is_threat']
    
    print(f"Feature engineering complete. X shape: {X.shape}, y shape: {y.shape}")
    
    # Return the enriched DataFrame along with X and y.
    return features_df, X, y
