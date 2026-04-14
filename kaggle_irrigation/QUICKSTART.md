# Quick Start Guide - Kaggle Irrigation Need Competition

## You Have Downloaded the Data - What's Next?

Follow these steps to train models and generate your submission:

### Step 1: Place the Data Files

Place the downloaded files in the correct location:
```bash
kaggle_irrigation/data/train.csv
kaggle_irrigation/data/test.csv
kaggle_irrigation/data/sample_submission.csv
```

### Step 2: Install Dependencies

```bash
cd kaggle_irrigation
pip install -r requirements.txt
```

### Step 3: Exploratory Data Analysis (EDA)

Run EDA to understand the data:
```bash
python kaggle_irrigation/eda.py
```

This will:
- Display data statistics and information
- Show target distribution
- Generate visualization plots
- Identify missing values
- Show correlation matrices

### Step 4: Train Models

Train all models with cross-validation:
```bash
python kaggle_irrigation/train.py
```

Options:
- `--baseline-only`: Train only baseline models (faster)
- `--ensemble-only`: Train only ensemble models
- `--n-folds 5`: Set number of CV folds (default: 5)
- `--save-models`: Save trained models to disk

Example:
```bash
# Train all models and save them
python kaggle_irrigation/train.py --save-models --n-folds 5

# Train only ensemble models
python kaggle_irrigation/train.py --ensemble-only --save-models
```

### Step 5: Generate Predictions

After training, generate predictions for the test set:
```bash
python kaggle_irrigation/predict.py --model xgboost --cv-score 0.85
```

Available models:
- `xgboost` (recommended)
- `lightgbm` (recommended)
- `catboost` (recommended)
- `random_forest`
- `logistic_regression`
- `decision_tree`

The submission file will be saved to `kaggle_irrigation/submissions/`

### Step 6 (Optional): Hyperparameter Optimization

For better performance, optimize hyperparameters:
```bash
python kaggle_irrigation/optimize.py --model xgboost --n-trials 100
```

This uses Optuna to find the best hyperparameters. Results are saved to `kaggle_irrigation/models/`

### Step 7: Submit to Kaggle

1. Go to the competition page
2. Click "Submit Predictions"
3. Upload the CSV file from `kaggle_irrigation/submissions/`
4. Check your leaderboard score

### Complete Workflow Example

```bash
# 1. Install dependencies
pip install -r kaggle_irrigation/requirements.txt

# 2. Explore the data
python kaggle_irrigation/eda.py

# 3. Train models with cross-validation
python kaggle_irrigation/train.py --save-models

# 4. Generate predictions with best model
python kaggle_irrigation/predict.py --model xgboost --cv-score 0.85

# 5. (Optional) Optimize hyperparameters
python kaggle_irrigation/optimize.py --model xgboost --n-trials 50

# 6. Train with optimized parameters and predict again
python kaggle_irrigation/train.py --ensemble-only --save-models
python kaggle_irrigation/predict.py --model xgboost --cv-score 0.87
```

## Tips for Better Performance

1. **Start Simple**: Run baseline models first to establish a baseline score
2. **Cross-Validation**: Use 5-10 fold CV to get reliable performance estimates
3. **Feature Engineering**: The pipeline automatically creates interaction features
4. **Ensemble**: Combine predictions from multiple models for better results
5. **Hyperparameter Tuning**: Use optimize.py to find optimal parameters
6. **Iterate**: Based on leaderboard feedback, adjust features and models

## Directory Structure After Running

```
kaggle_irrigation/
├── data/
│   ├── train.csv              # Your training data
│   ├── test.csv               # Your test data
│   └── sample_submission.csv  # Sample submission format
├── models/
│   ├── xgboost.pkl           # Saved models
│   ├── lightgbm.pkl
│   └── feature_engineer.pkl   # Saved feature transformations
├── submissions/
│   └── submission_xgboost_cv0.8500_20260414_205530.csv
└── src/                       # Source code modules
```

## Troubleshooting

### Missing Libraries
If you get import errors, install the specific library:
```bash
pip install xgboost lightgbm catboost optuna
```

### Data Not Found
Make sure files are in `kaggle_irrigation/data/`:
```bash
ls kaggle_irrigation/data/
# Should show: train.csv  test.csv  sample_submission.csv
```

### Memory Issues
If you run out of memory:
- Use `--baseline-only` flag
- Reduce `--n-folds` to 3
- Use fewer features (modify feature_engineering.py)

## Next Steps

After your first submission:
1. Check leaderboard score
2. Compare with CV score (if very different, you may have overfitting/underfitting)
3. Try different models or ensembles
4. Engineer more domain-specific features
5. Tune hyperparameters
6. Submit improved predictions
