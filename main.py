# main.py
# The "On Air Switch" for the Cyber Threat Analyzer (CTA)

import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# --- Path Fix ---
# Add the project root to the Python path
# This allows us to import our 'src' modules
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
    print(f"Added project root to path: {project_root}")
# --- End Fix ---

# --- Import our "Toolboxes" ---
import src.data_processing as dp
import src.threat_intelligence as ti
import src.model as m

def run_pipeline():
    """
    Runs the full CTA data and ML pipeline.
    """
    print("--- [CTA] Cyber Threat Analyzer v1.0 Initializing ---")
    
    # --- 1. Load API Key ---
    load_dotenv()
    api_key = os.environ.get('ABUSEIPDB_KEY')
    if not api_key:
        print("[CTA] ERROR: ABUSEIPDB_KEY not found in .env file.")
        print("Please create a .env file in the project root.")
        return
    print("[CTA] API Key loaded successfully.")

    # --- 2. Load and Parse Logs ---
    log_file_path = project_root / "data" / "system.log"
    df = dp.load_and_parse_logs(log_file_path)
    if df.empty:
        print("[CTA] ERROR: Log file could not be parsed or was empty.")
        return
    print(f"[CTA] Parsed {len(df)} log entries.")

    # --- 3. Enrich Data ---
    df['ip_address'] = df['message'].apply(ti.extract_ip)
    unique_ips = df['ip_address'].dropna().unique()
    print(f"[CTA] Found {len(unique_ips)} unique IPs for enrichment.")
    
    ip_report_cache = ti.build_threat_cache(unique_ips, api_key)
    print("[CTA] Threat intel cache build complete.")

    # --- 4. Engineer Features ---
    df, X, y = dp.engineer_features(df, ip_report_cache)
    print(f"[CTA] Feature engineering complete. Found {y.sum()} potential threats.")

    # --- 5. Train and Evaluate Model ---
    print("[CTA] Training and evaluating v1.0 baseline model...")
    model, X_test, y_test = m.train_model(X, y)
    
    # --- 6. Print Final Report ---
    print("\n\n--- [CTA] FINAL SIGNAL REPORT ---")
    print("The v1.0 'Noise Filter' (Decision Tree) has been evaluated.")
    print("This report shows its performance on the 20% 'test' dataset.")
    m.evaluate_model(model, X_test, y_test)
    print("--- [CTA] Pipeline Run Complete ---")


# This is the standard Python "entry point"
# It means "if someone clicks 'run' on this file,
# execute the run_pipeline() function."
if __name__ == "__main__":
    run_pipeline()