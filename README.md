# Cyber Threat Analyzer (CTA) v1.0

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
![OMSCS](https://img.shields.io/badge/Built%20For-OMSCS%20Application-B3A369)

---

This project is a complete, end-to-end data pipeline built to demonstrate key skills in Data Engineering, Machine Learning, and MLOps.

The core theme is **"Signal in the Noise."** The application ingests a raw `system.log` file (99% "noise") and uses a machine learning model to find the 1% "signal" of a brute force attack.

This repository is designed to showcase the full engineering lifecycle for my professional portfolio.

## Key Features

* **Data Pipeline:** Ingests and parses raw, unstructured log files using Python and Regex.
* **Threat Intel Enrichment:** Automatically enriches all found IP addresses with live threat data from the AbuseIPDB API (using a secure `.env` key).
* **Intelligent Caching:** Uses a JSON cache (`ip_threat_cache.json`) to avoid re-querying the API, saving time and resources.
* **ML Noise Filter:** Trains a v1.0 Decision Tree model (`scikit-learn`) to automatically classify logs as "Noise" (0) or "Signal" (1) based on their features.
* **Reproducible Environment:** Includes a complete `environment.yml` file to build the exact Conda `cta_env` needed to run the project.
* **Modular & Clean:** All logic is refactored into the "Studio Rack" (`src/`), separating the core logic from the "Studio Notes" (`notebooks/`) and the "On Air Switch" (`main.py`).

## Development Philosophy: Human-AI Collaboration

This project, the **Cyber Threat Analyzer (CTA)**, was designed to master and demonstrate a modern, MLOps-driven workflow.

It was built using an intensive **Human-AI collaboration**.

* **My Role (Bob Gaynor): The Architect & Tech Lead**
    As the project owner, I served as the "Tech Lead." I defined the entire roadmap, set all project goals, and was the "human-in-the-loop" who debugged, tested, and made all final architectural decisions (like refactoring into `src/` and managing the `git` history).

* **AI Role 1: The "Senior Mentor" / "Pair Programmer" (Google Gemini)**
    I used Google Gemini as my "on-demand senior mentor." I bounced ideas off it, asked it to help "pair program" and refactor functions, and used it as a "debugger" to find errors. This demonstrates a modern workflow of using AI to accelerate *learning* and *development*.

* **AI Role 2: The "Code Reviewer" (Google Jules)**
    After the core logic was completed, I used the `google-labs-jules[bot]` agent to perform an automated "style and linting" review. This is why the bot appears as a contributor (for fixing whitespace, improving docstrings, etc.). This demonstrates using AI for *automated quality assurance*.

This project's value is not just in the final code, but in the *process*. It's a "Top-Down" showcase of how a modern engineer can *lead and orchestrate* AI tools to build, debug, and ship a reproducible ML pipeline from scratch.

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
(cta_env) bg@AirBG cta % python main.py
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

## Project Structure (The "Studio")

As a nod to audio engineering, the project is structured like a recording studio:

* **`main.py`**: The **"On Air Switch"** script. This is the main entry point to run the demo.
* **`src/`**: The **"Studio Rack"** containing all modular Python code.
* **`notebooks/`**: The **"Studio Notes"** (my "scratchpad") containing the original `01-EDA.ipynb`.
* **`data/`**: The "raw audio" (`system.log`) waiting to be mixed.
* **`environment.yml`**: The "Tech Rider" for Conda, ensuring full reproducibility.
* **`.gitignore`**: The "noise filter" for Git; ignores secrets, caches, and generated files.
