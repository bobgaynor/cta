# Cyber Threat Analyzer (CTA) v1.0

This project is a complete, end-to-end data pipeline built to demonstrate key skills in Data Engineering, Machine Learning, and MLOps.

The core theme is **"Signal in the Noise."** The application ingests a raw `system.log` file (99% "noise") and uses a machine learning model to find the 1% "signal" of a brute force attack.

This repository is designed to showcase the full engineering lifecycle for my professional portfolio.

## Key Features

* **Data Pipeline:** Ingests and parses raw, unstructured log files using Python and Regex.
* **Threat Intel Enrichment:** Automatically enriches all found IP addresses with live threat data from the AbuseIPDB API (using a secure `.env` key).
* **Intelligent Caching:** Uses a JSON cache (`ip_threat_cache.json`) to avoid re-querying the API, saving time and resources.
* **ML "Noise Filter":** Trains a v1.0 Decision Tree model (`scikit-learn`) to automatically classify logs as "Noise" (0) or "Signal" (1) based on their features.
* **Reproducible Environment:** Includes a complete `environment.yml` file to build the exact Conda `cta_env` needed to run the project.
* **Modular & Clean:** All logic is refactored into the "Studio Rack" (`src/`), separating the core logic from the "Studio Notes" (`notebooks/`) and the "On Air Switch" (`main.py`).

## How to Run This Project

This project is designed to be fully reproducible.

### 1. One-Time Setup

First, clone the "project files" and set up the "studio" (the Conda environment).

```bash
# 1. Clone the project from GitHub
git clone https://github.com/bobgaynor/cta.git

# 2. Navigate into the project folder
cd cta

# 3. Build the Conda environment using the "Tech Rider"
conda env create -f environment.yml

# 4. Create your secret API key file
# (This one command creates the file and adds the line)
echo "ABUSEIPDB_KEY=YOUR_API_KEY_GOES_HERE" > .env

Note: You must get your own free API key from [AbuseIPDB](https://www.abuseipdb.com/) and replace `YOUR_API_KEY_GOES_HERE` in the `.env` file.

### 2. Run the "On Air Switch"

Anytime you want to run the full analysis:

```bash
# 1. Activate the environment
conda activate cta_env

# 2. Run the "On Air Switch"
python main.py

This will run the entire pipeline (parsing, enrichment, and ML model evaluation) and print a final Signal Report to your terminal.

## 📓 Project Structure

* **`main.py`**: The "On Air Switch" script. This is the main entry point to run the demo.
* **`environment.yml`**: The "Tech Rider" for Conda, ensuring full reproducibility.
* **`README.md`**: This instruction manual.
* **`src/`**: The "Studio Rack" containing all modular Python code.
    * `data_processing.py`: All functions for parsing logs and feature engineering.
    * `threat_intelligence.py`: All functions for API calls and IP extraction.
    * `model.py`: All functions for training and evaluating the ML model.
* **`notebooks/`**: The "Studio Notes" containing the original `01-EDA.ipynb` notebook, which now acts as a clean report.
* **`data/`**: Contains the `system.log` sample data.
* **`.gitignore`**: The "noise filter" for Git; ignores secrets, caches, and generated files.
