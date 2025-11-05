# src/data_processing.py

import re
import pandas as pd
import numpy as np
from pathlib import Path

def _extract_log_level(message):
    """
    (Private function) Uses regex to find a log level like [ERROR]
    in a message string. Defaults to 'INFO' if none is found.
    """
    level_pattern = r'\[(\w+)\]'
    match = re.search(level_pattern, message)
    if match:
        return match.group(1)
    else:
        return 'INFO'

def load_and_parse_logs(log_file_path):
    """
    Loads a log file, parses it with regex, and returns a
    clean, feature-rich DataFrame.
    """
    # This regex is our noise filter for the syslog format.
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
        
        # --- Convert to DataFrame ---
        df = pd.DataFrame(data, columns=['timestamp_str', 'hostname', 'process', 'message'])
        
        # --- Clean Timestamps ---
        # We add the format to make parsing fast and accurate
        df['timestamp'] = pd.to_datetime(df['timestamp_str'], format="%b %d %H:%M:%S")
        
        # Fix the year (defaults to 1900)
        current_year = pd.Timestamp.now().year
        df['timestamp'] = df['timestamp'].apply(lambda x: x.replace(year=current_year))
        
        # --- Extract Initial Features ---
        df['log_level'] = df['message'].apply(_extract_log_level)
        df['hour_of_day'] = df['timestamp'].dt.hour
        
        # Drop the original string column
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
    Takes the parsed DataFrame and the threat intel cache,
    and engineers the final (X, y) features for the model.
    """
    print("Engineering features for the model...")
    features_df = df.copy()
    
    # --- 1. Merge Threat Intel ---
    # We map the intel from our cache back to the main DataFrame
    features_df['abuse_score'] = features_df['ip_address'].map(lambda ip: ip_report_cache.get(ip, {}).get('abuse_score'))
    features_df['country'] = features_df['ip_address'].map(lambda ip: ip_report_cache.get(ip, {}).get('country'))
    
    # Fill missing scores (NaNs) with 0
    features_df['abuse_score'] = features_df['abuse_score'].fillna(0)
    # Fill missing countries (NaNs) with 'N/A'
    features_df['country'] = features_df['country'].fillna('N/A')
    
    # --- 2. Create Target Variable (y) ---
    signal_1 = features_df['message'].str.contains("Failed password")
    signal_2 = features_df['abuse_score'] > 50
    features_df['is_threat'] = np.where(signal_1 | signal_2, 1, 0)
    
    # --- 3. One-Hot Encode 'log_level' ---
    one_hot_features = pd.get_dummies(features_df['log_level'], prefix='log_level')
    features_df = pd.concat([features_df, one_hot_features], axis=1)
    
    # --- 4. Define final X and y ---
    X_columns = [
        'hour_of_day', 
        'abuse_score'
    ]
    # Find all the new 'log_level_' columns and add them
    X_columns.extend(one_hot_features.columns)
    
    # Ensure all required columns exist, even if one-hot encoding was sparse
    # This prevents errors if our sample log is missing e.g. a 'WARNING'
    all_expected_cols = ['log_level_INFO', 'log_level_ERROR', 'log_level_WARNING']
    for col in all_expected_cols:
       if col not in features_df.columns:
           features_df[col] = False # Add missing column as all False (0)
           
    # Filter X to only the columns we need, in the right order
    X = features_df[X_columns]
    y = features_df['is_threat']
    
    print(f"Feature engineering complete. X shape: {X.shape}, y shape: {y.shape}")
    
    # NEW FIX: Return the whole enriched DataFrame too
    return features_df, X, y
