# src/threat_intelligence.py

import os
import re
import json
import requests
from dotenv import load_dotenv

def extract_ip(log_message):
    """
    Finds the first valid, non-private IPv4 address in a log message.

    This function uses a regular expression to find potential IPv4 addresses
    and filters out common private IP ranges (e.g., 192.168.x.x).
    """
    # This regex is our "Signal Filter" for IPv4 addresses.
    ip_pattern = r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    
    match = re.search(ip_pattern, log_message)
    
    # If an IP is found, check if it is a private (internal) address.
    if match:
        ip = match.group(1)
        if ip.startswith(('192.168.', '10.', '127.0.0.1')):
            return None # Ignore internal or localhost IPs.
        return ip
    
    return None # No public IP address found.

def check_ip(ip_address, api_key):
    """
    Checks a single IP address against the AbuseIPDB API.

    This function queries the AbuseIPDB API for a given IP address and
    returns key threat intelligence data, such as the abuse score.
    """
    url = 'https://api.abuseipdb.com/api/v2/check'
    params = {
        'ipAddress': ip_address,
        'maxAgeInDays': '90', # Check reports from the last 90 days.
        'verbose': 'true'
    }
    headers = {
        'Accept': 'application/json',
        'Key': api_key
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Raise an HTTPError for bad responses.
        
        data = response.json()
        
        # Extract the most important "Signal" data from the API response.
        if 'data' in data:
            return {
                'abuse_score': data['data'].get('abuseConfidenceScore', 0),
                'country': data['data'].get('countryCode', 'N/A'),
                'domain': data['data'].get('domain', 'N/A')
            }
            
    except requests.exceptions.RequestException as e:
        print(f"Error checking IP {ip_address}: {e}")
        
    return None # Return None if the API call fails or returns no data.

def build_threat_cache(ip_list, api_key, cache_file='ip_threat_cache.json'):
    """
    Builds and uses a local cache to avoid redundant API queries.

    This function checks for a local JSON cache file. If an IP address is
    not in the cache, it queries the API and saves the new data.
    """
    # Load existing threat intelligence from the cache file if it exists.
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            threat_cache = json.load(f)
    else:
        threat_cache = {}

    # Note: This cache is persistent.
    
    # Process each IP address in the provided list.
    for ip in ip_list:
        # If the IP is not in our cache, we need to query the API.
        if ip not in threat_cache:
            print(f"Cache miss. Querying new IP: {ip}")
            intel = check_ip(ip, api_key)
            if intel:
                threat_cache[ip] = intel
            else:
                # If the API fails, store a default entry to avoid re-querying.
                threat_cache[ip] = {'abuse_score': 0, 'country': 'N/A', 'domain': 'N/A'}
        
    # Save the updated threat intelligence data back to the cache file.
    with open(cache_file, 'w') as f:
        json.dump(threat_cache, f, indent=4)
        
    print("Threat Intel Cache is up to date.")
    return threat_cache