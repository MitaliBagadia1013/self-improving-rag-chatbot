# Kaggle Competition: Predicting Irrigation Need

This directory contains the solution for the Kaggle Tabular Playground Series competition "Predicting Irrigation Need Evaluation".

## Competition Details

- **Task**: Multi-class classification (Low, Medium, High)
- **Metric**: Balanced Accuracy
- **Timeline**: April 1-30, 2026
- **Competition Link**: https://kaggle.com/competitions/playground-series-s6e4

## Directory Structure

```
kaggle_irrigation/
├── data/              # Competition data files (train.csv, test.csv, sample_submission.csv)
├── notebooks/         # Jupyter notebooks for exploration and analysis
├── models/           # Saved model files
├── submissions/      # Generated submission files
├── src/              # Source code modules
│   ├── data_loader.py
│   ├── feature_engineering.py
│   ├── models.py
│   └── utils.py
├── train.py          # Main training script
├── predict.py        # Prediction and submission generation
└── requirements.txt  # Python dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download competition data from Kaggle and place in `data/` directory:
   - train.csv
   - test.csv
   - sample_submission.csv

3. Run exploratory data analysis:
```bash
python src/eda.py
```

4. Train models:
```bash
python train.py
```

5. Generate predictions:
```bash
python predict.py
```

## Approach

### Phase 1: Data Exploration
- Dataset profiling and statistics
- Target distribution analysis
- Feature correlation analysis
- Missing value detection

### Phase 2: Feature Engineering
- Missing value imputation
- Feature scaling and normalization
- Interaction features
- Domain-specific features

### Phase 3: Model Development
- Baseline models (Logistic Regression, Decision Tree)
- Ensemble models (Random Forest, XGBoost, LightGBM, CatBoost)
- Model stacking/blending

### Phase 4: Validation
- Stratified K-Fold cross-validation
- Balanced accuracy metric
- Overfitting monitoring

### Phase 5: Optimization
- Hyperparameter tuning (Optuna)
- Feature selection
- Class imbalance handling

### Phase 6: Submission
- Test set predictions
- Submission file generation
- Leaderboard tracking
