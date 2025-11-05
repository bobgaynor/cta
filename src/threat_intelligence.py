# src/threat_intelligence.py

import os
import re
import json
import requests
from dotenv import load_dotenv

# --- Our IP Address Signal Extractor ---

def extract_ip(log_message):
    """
    Uses regex to find the first valid IPv4 address in a log message.
    """
    # This regex is our signal filter for IPv4 addresses
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    
    match = re.search(ip_pattern, log_message)
    
    # If we find a signal, return it. Otherwise, return noise.
    if match:
        # Check if it's a boring internal IP
        ip = match.group(1)
        if ip.startswith(('192.168.', '10.', '127.0.0.1')):
            return None # Ignore internal/localhost IPs
        return ip
    
    return None # No IP found

# --- Our AbuseIPDB API Intel Analyst ---

def check_ip(ip_address, api_key):
    """
    Checks a single IP address against the AbuseIPDB API.
    """
    url = 'https://api.abuseipdb.com/api/v2/check'
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90', # Look at reports from the last 90 days
        'verbose': 'true'
    }
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise an error for bad responses
        
        data = response.json()
        
        # Extract the signal we care about
        if 'data' in data:
            return {
                'abuse_score': data['data'].get('abuseConfidenceScore', 0),
                'country': data['data'].get('countryCode', 'N/A'),
                'domain': data['data'].get('domain', 'N/A')
            }
            
    except requests.exceptions.RequestException as e:
        print(f"Error checking IP {ip_address}: {e}")
        
    return None # Return None if API fails or no data

# --- Our Threat Intel Cache Builder ---

def build_threat_cache(ip_list, api_key, cache_file='ip_threat_cache.json'):
    """
    Builds and uses a local JSON cache to avoid re-querying the API.
    """
    # Load existing intel from our cache file, if it exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            threat_cache = json.load(f)
    else:
        threat_cache = {}

    # Go through our list of IPs
    for ip in ip_list:
        # If we don't have intel on this IP, get it
        if ip not in threat_cache:
            print(f"Cache miss. Querying new IP: {ip}")
            intel = check_ip(ip, api_key)
            if intel:
                threat_cache[ip] = intel
            else:
                # If API fails, store a null to avoid re-querying
                threat_cache[ip] = {'abuse_score': 0, 'country': 'N/A', 'domain': 'N/A'}
        
    # Save our updated intel back to the cache file
    with open(cache_file, 'w') as f:
        json.dump(threat_cache, f, indent=4)
        
    print("Threat Intel Cache is up to date.")
    return threat_cache
