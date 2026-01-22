# Project Structure

## Overview
This document describes the directory structure and organization of the Customer Purchasing Pattern Analysis project.

## Directory Tree

```
customer-purchasing-pattern-analysis-using-AI/
├── data/
│   ├── raw/                    # Raw input data
│   └── processed/              # Processed/cleaned data
├── src/                        # Source code
│   ├── __init__.py
│   ├── data_loader.py          # Data loading utilities
│   ├── preprocessing.py        # Data preprocessing functions
│   ├── utils.py                # Utility functions
│   └── models/                 # Model implementations
├── notebooks/                  # Jupyter notebooks
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_feature_engineering.ipynb
│   └── 04_model_training.ipynb
├── tests/                      # Unit tests
│   ├── __init__.py
│   └── test_data_loader.py
├── config/                     # Configuration files
│   └── config.yaml
├── scripts/                    # Standalone scripts
├── results/                    # Output results
│   ├── models/                 # Saved models
│   └── plots/                  # Generated plots
├── docs/                       # Documentation
│   └── PROJECT_STRUCTURE.md
├── LICENSE                     # License file
├── README.md                   # Project README
├── setup.py                    # Setup configuration
├── requirements.txt            # Python dependencies
└── .gitignore                  # Git ignore rules
```

## Directory Descriptions

### `/data`
- **raw/**: Original, immutable data files
- **processed/**: Cleaned and transformed data ready for analysis

### `/src`
Core Python modules for the project:
- **data_loader.py**: Functions for loading and saving data
- **preprocessing.py**: Data cleaning and preprocessing
- **utils.py**: Utility functions and configuration management
- **models/**: Machine learning model implementations

### `/notebooks`
Jupyter notebooks for exploration and experimentation:
- **01_exploratory_data_analysis.ipynb**: Initial data exploration
- **02_data_preprocessing.ipynb**: Data cleaning workflows
- **03_feature_engineering.ipynb**: Feature creation
- **04_model_training.ipynb**: Model development

### `/tests`
Unit tests for code validation:
- Test data loading functions
- Test preprocessing functions
- Test utility functions

### `/config`
Configuration files:
- **config.yaml**: Main project configuration

### `/scripts`
Standalone executable scripts:
- Data download scripts
- Model inference scripts
- Batch processing scripts

### `/results`
Output files:
- **models/**: Saved trained models
- **plots/**: Generated visualizations

### `/docs`
Project documentation:
- Architecture documentation
- API references
- User guides

## Getting Started

1. **Setup environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Prepare data**:
   - Place raw data in `data/raw/`

3. **Run analysis**:
   - Use notebooks in `notebooks/` for exploration
   - Use modules in `src/` for reproducible pipelines

4. **Run tests**:
   ```bash
   pytest tests/
   ```

## Best Practices

- Keep data files in `data/` directory
- Store all functions in `src/` modules
- Use notebooks for exploration only
- Write tests for critical functions
- Document code with docstrings
- Use configuration files for parameters
