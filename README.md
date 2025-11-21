# Cyber Threat Analyzer (CTA)

Machine-learning pipeline for detecting brute-force activity by revealing the signal hidden in noisy log data.

This project is a complete, end-to-end data workflow designed to demonstrate key skills in machine learning, security analysis, and data-driven engineering.

The core theme is **“finding the signal in the noise.”** The application ingests a raw system.log file (99% noise) and uses a machine-learning model to find the 1% signal of security-relevant activity (demonstrated here using brute-force patterns).

This repository is part of my professional portfolio, showcasing the full engineering lifecycle of a reproducible ML-for-security project.


<!-- Core Technologies -->
![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/ML-scikit--learn-F7931E?logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Data-Pandas-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Viz-Matplotlib-11557c)
![Seaborn](https://img.shields.io/badge/Viz-Seaborn-4c78a8)

<!-- APIs & Tools -->
![AbuseIPDB](https://img.shields.io/badge/API-AbuseIPDB-red)
![Requests](https://img.shields.io/badge/HTTP-Requests-blue)
![dotenv](https://img.shields.io/badge/Config-python--dotenv-yellowgreen)

<!-- Environment -->
![Conda](https://img.shields.io/badge/Conda-44A833?logo=anaconda&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)

<!-- Project Info -->
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-v1.0%20Complete-brightgreen)

---

## Project Motivation

As a cybersecurity professional, I often analyze noisy system and network logs where meaningful signals are buried in routine activity. This project demonstrates how machine learning can uncover meaningful patterns hidden in noisy operational data and support predictive detection approaches.

It showcases my ability to:

- Design end-to-end ML pipelines from raw data to model evaluation  
- Apply machine learning to real-world security problems  
- Build production-quality code with clean structure and engineering discipline  

## Pipeline Overview

```
Raw Logs → Parse & Extract → Threat Intelligence Enrichment → Feature Engineering → ML Classification Model → Signal Report
```

## Key Features

* **Data Pipeline:** Ingests and parses raw, unstructured log files using Python and Regex.
* **Threat Intel Enrichment:** Automatically enriches all found IP addresses with live threat data from the AbuseIPDB API (using a secure `env` key).
* **Intelligent Caching:** Uses a JSON cache (`ip_threat_cache.json`) to avoid re-querying the API, saving time and resources.
* **ML Noise Filter:** Trains a v1.0 Decision Tree model to separate noise from signal by classifying logs as "Noise" (0) or "Signal" (1) based on their features.
* **Reproducible Environment:** Includes a complete `environment.yml` file to build the exact Conda `cta_env` needed to run the project.
* **Modular & Clean:** All logic is refactored into the "Studio Rack" (`src/`), separating the core logic from the "Studio Notes" (`notebooks`) and the "On Air Switch" (`main.py`).

## Development Approach: Modern ML Engineering

This project was built using a modern, human-in-the-loop workflow. I led all architectural decisions, designed the full pipeline, and implemented the core system end-to-end. I used AI tools throughout the process for targeted assistance with refactoring, debugging, and automated code review, similar to how engineers use pair programming or linting automation.

The goal was not only to build a functional ML pipeline, but to demonstrate a modern engineering approach where AI accelerates development while the human engineer remains fully in control of design, structure, and correctness.

## How to Run This Project

This project is designed to be fully reproducible.

### 1. One-Time Setup

First, clone the project files and set up the studio (the Conda environment).
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
```

**Note:** You must get your own free API key from [AbuseIPDB](https://www.abuseipdb.com/) and replace `YOUR_API_KEY_GOES_HERE` in the `.env` file.

The echo command above creates the .env file for you, but you can also just copy the config_template.env file (included in this repo) to .env and paste your key there.

### 2. Run the "On Air Switch"

Anytime you want to run the full analysis:
```bash
# 1. Activate the environment
conda activate cta_env

# 2. Run the "On Air Switch"
python main.py
```

This will run the entire pipeline (parsing, enrichment, and ML model evaluation) and print a final Signal Report to your terminal.

## Example Output

When you run the pipeline, it will fetch live threat intel (or use the cache) and train the v1.0 "Noise Filter." The final output will be a "Signal Report" showing how well the model performed on the test data:
```text
(cta_env) blue@harlem cta % python main.py
--- [CTA] Cyber Threat Analyzer v1.0 Initializing ---
[CTA] API Key loaded successfully.
Starting log parsing from: /Users/bg/projects/cta/data/system.log
[CTA] Parsed 76 log entries.
[CTA] Found 9 unique IPs for enrichment.
Threat Intel Cache is up to date.
[CTA] Threat intel cache build complete.
Engineering features for the model...
[CTA] Feature engineering complete. Found 35 potential threats.
[CTA] Training and evaluating v1.0 baseline model...
Splitting data for training and testing...
Training set size: 60 logs
Test set size: 16 logs
--- Model Training Complete ---
--- [CTA] FINAL SIGNAL REPORT ---
The v1.0 'Noise Filter' (Decision Tree) has been evaluated.
This report shows its performance on the 20% 'test' dataset.
Evaluating model performance on test data...
--- Classification Report ---
              precision    recall  f1-score   support
           0       0.64      0.78      0.70         9
           1       0.60      0.43      0.50         7
    accuracy                           0.62        16
   macro avg       0.62      0.60      0.60        16
weighted avg       0.62      0.62      0.61        16
--- Confusion Matrix ---
--- Readable Confusion Matrix ---
                 PREDICTED
                 Noise (0)   Signal (1)
ACTUAL Noise (0)    7          2         
ACTUAL Signal (1)   4          3         
--- Model Evaluation Complete ---
--- [CTA] Pipeline Run Complete ---
```

## Key Results

* **Dataset:** 76 log entries, 9 unique IPs analyzed
* **Threat Detection Accuracy:** 62% on test set (v1.0 prototype)
* **API Efficiency:** Intelligent caching reduced queries by ~90%
* **Processing Time:** <2 seconds for full pipeline execution

## Project Structure

The layout is modeled after a recording session, aligning with the process of isolating signal from noise in security data.

* **`main.py`**: The **"Session Start"** script, serving as the main entry point to run the pipeline.
* **`src/`**: The **"Signal Chain"**, containing all modular Python code.
* **`notebooks/`**: The **"Scratch Tracks"**, including the original `01-EDA.ipynb`.
* **`data/`**: The **"Raw Takes"** (`system.log`) waiting to be mixed.
* **`environment.yml`**: The **"Studio Setup"** for Conda, ensuring full reproducibility.
* **`.gitignore`**: The **"Noise Filter"** for Git; ignores secrets, caches, and generated files.

## Future Enhancements

This v1.0 prototype is a solid foundation, and my roadmap for this project includes several key MLOps and ML engineering goals:

* **Improve the Model:** Explore more advanced models beyond the v1.0 Decision Tree (like Random Forests) to improve the 62% baseline accuracy.
* **Expand Feature Engineering:** Add new data sources to the model to make it "smarter"—for example, looking at the *time between* failed logins, not just the failures themselves.
* **Deploy as an API:** This is my next major learning block. I plan to containerize this pipeline using **Docker** and deploy the model as a live, real-time web API using **FastAPI** so other tools could use it.
* **Build a Test Suite:** Add a formal `tests/` folder with `pytest` to automatically verify that the data parsing and API logic work as expected, ensuring the pipeline is reliable.
* **Automate the Pipeline:** Integrate the project with GitHub Actions (CI/CD) to automatically test and run the pipeline, moving it from a manual script to a continuous, automated service.
