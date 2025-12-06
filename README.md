# Extending OASIS+: A Temporal, Multimodal, and Cluster-Aware Framework for ICU Mortality Prediction

This repository contains an extension of the OASIS+ model, an advanced machine learning approach to calculate the OASIS (Oxford Acute Severity of Illness Score) severity score for predicting in-hospital mortality.

## Overview

ExOASIS+ implements a multimodal deep learning architecture that integrates structured clinical variables, admission clusters, and temporal physiological features. The original OASIS+ model leveraged machine learning techniques to improve upon the traditional OASIS severity scoring system. This model is tested on synthetic patient data from Synthea and validated on clinical data from MIMIC-III and validated using.

 All modeling is implemented in PyTorch, and the pipeline is modular and reproducible, allowing each component to be developed independently and then combined into a full end-to-end system.

## Features

After preprocessing, three types of inputs are generated for each patient:
- **Structured Data**: Age, surgery indicator, diagnosis-cluster ID
- **Temporal Features**: Longitudinal ICU chart events (vitals and labs)
- **Target Label**: Binary in-hospital mortality
- **Synthea Synthetic Data**: Generate and process synthetic patient data

## Project Structure

```
.
├── oasis_plus_model.py              # Core OASIS+ model implementation
├── oasis_plus_data.py               # Data processing utilities for OASIS+ model
├── ensure_data.py                   # Data download and validation
├── extending_oasis_plus.py          # Extended model variants
├── extending_oasis_plus_cluster.py  # Clustering-based extensions
├── mortality_model.pt               # Pre-trained mortality prediction model (PyTorch)
├── synthea_mimic.py                 # Synthea and MIMIC data integration
├── running_synthea.py               # Synthea data generation pipeline
├── test.py                          # Testing and validation scripts
├── requirements.txt                 # Python dependencies
├── mimic_demo/                      # Sample MIMIC-III data files
├── output/                          # Generated outputs
│   ├── data/                        # Processed datasets (train/valid/test splits)
│   ├── metadata/                    # Metadata and configuration files
│   ├── mimic/                       # Processed MIMIC data
│   └── synthea_output/              # Generated Synthea data
├── results/                         # Trained models
│   ├── oasis_filter.joblib          # Feature filtering model
│   └── oasis_xgb200.joblib          # XGBoost classifier
└── synthea/                         # Synthea configuration and templates
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or conda package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/kkl5524/oasis-plus.git
cd oasis-plus
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### 1. Ensure Data Availability

Download and validate required data files:
```bash
python ensure_data.py
```

This script automatically downloads MIMIC-III data and prepares it for processing.

### 2. Generate Synthetic Data (Optional)

Create synthetic patient cohorts using Synthea:
```bash
python running_synthea.py
```
Note: This process will take an extended amount of time (~ 45 minutes) and is optional, as the ensure_data.py file will download pre-generated data.

### 3. Process Data

Extract OASIS+ features from clinical data:
```bash
python oasis_plus_data.py
```

### 4. Train/Evaluate Model

Run the core OASIS+ model:
```bash
python oasis_plus_model.py
```

This will:
- Load processed data
- Split into train/validation/test sets
- Train XGBoost classifier
- Generate predictions and metrics
- Save trained models

### 5. Run Tests

Validate model performance of model without cluster:
```bash
python extending_oasis_plus.py
```

Validate model performance of model with cluster:
```bash
python extending_oasis_plus_cluster.py
```


## Dependencies

Key packages used:
- **pandas & numpy**: Data manipulation and numerical computing
- **scikit-learn**: Machine learning utilities and metrics
- **xgboost**: Gradient boosting classifier
- **torch**: Deep learning framework for mortality model
- **matplotlib**: Visualization
- **joblib**: Model serialization
- **requests & gdown**: Data downloading

See `requirements.txt` for complete list with versions.

## Data

### MIMIC-III Data
Clinical data from the MIT-LCP MIMIC-III database. Sample files included in `mimic_demo/`:
- ADMISSIONS: Patient admission records
- PATIENTS: Patient demographics
- ICUSTAYS: ICU stay information
- CHARTEVENTS: Vital signs and lab values
- LABEVENTS: Laboratory test results
- And other clinical event tables

### Synthea Data
Synthetic patient data generated using Synthea. Includes:
- Patient demographics
- Medical conditions
- Medications and prescriptions
- Procedures and encounters
- Laboratory results

## Model Details

### OASIS Features

The model uses traditional OASIS components:
- Pre-ICU length of stay
- Reason for admission
- Age
- Glasgow Coma Score (GCS)
- Mean arterial pressure
- Respiratory rate
- Temperature
- Urine output
- Ventilation status
- Surgery status (optional)

Additional machine learning features derived from clinical measurements.

### Training Configuration

- **Algorithm**: XGBoost Classifier
- **Train/Valid/Test Split**: 70% / 20% / 10%
- **Target Variable**: In-hospital mortality (binary classification)
- **Cross-validation**: Included for robust evaluation

## Output Files

Generated outputs are saved in the `output/` directory:

- `output/data/oasis_plus.csv` - Complete processed dataset
- `output/data/train/oasis_train.csv` - Training set
- `output/data/valid/oasis_valid.csv` - Validation set
- `output/data/test/oasis_test.csv` - Test set
- `results/oasis_xgb200.joblib` - Trained XGBoost model
- `results/oasis_filter.joblib` - Feature selector model
- `output/metadata/*.json` - Metadata about data generation

## References

[1] OASIS+: Leveraging Machine Learning to Improve the Prognostic Accuracy of OASIS Severity Score for Predicting In-Hospital Mortality.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Contact

For questions or issues, please open a GitHub issue in the repository.

## Acknowledgments

- Data sourced from MIT-LCP MIMIC-III database
- Synthea for synthetic patient data generation
- XGBoost team for the gradient boosting framework
