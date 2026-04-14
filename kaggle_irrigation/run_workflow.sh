#!/bin/bash
# Complete workflow script for Kaggle Irrigation Need competition

echo "=========================================="
echo "Kaggle Irrigation Need - Complete Workflow"
echo "=========================================="

# Check if data files exist
if [ ! -f "kaggle_irrigation/data/train.csv" ]; then
    echo "❌ Error: train.csv not found in kaggle_irrigation/data/"
    echo "Please download the data from Kaggle and place it in kaggle_irrigation/data/"
    exit 1
fi

if [ ! -f "kaggle_irrigation/data/test.csv" ]; then
    echo "❌ Error: test.csv not found in kaggle_irrigation/data/"
    exit 1
fi

echo "✓ Data files found"

# Step 1: Install dependencies
echo ""
echo "Step 1: Installing dependencies..."
pip install -q -r kaggle_irrigation/requirements.txt
echo "✓ Dependencies installed"

# Step 2: Run EDA
echo ""
echo "Step 2: Running Exploratory Data Analysis..."
python kaggle_irrigation/eda.py
echo "✓ EDA complete"

# Step 3: Train models
echo ""
echo "Step 3: Training models with cross-validation..."
python kaggle_irrigation/train.py --save-models --n-folds 5
echo "✓ Model training complete"

# Step 4: Generate predictions
echo ""
echo "Step 4: Generating predictions..."

# Try XGBoost first
if python -c "import xgboost" 2>/dev/null; then
    python kaggle_irrigation/predict.py --model xgboost --cv-score 0.85
    echo "✓ XGBoost predictions generated"
elif python -c "import lightgbm" 2>/dev/null; then
    python kaggle_irrigation/predict.py --model lightgbm --cv-score 0.85
    echo "✓ LightGBM predictions generated"
else
    python kaggle_irrigation/predict.py --model random_forest --cv-score 0.80
    echo "✓ Random Forest predictions generated"
fi

echo ""
echo "=========================================="
echo "Workflow Complete!"
echo "=========================================="
echo ""
echo "Your submission file is in: kaggle_irrigation/submissions/"
echo ""
echo "Next steps:"
echo "1. Review the submission file"
echo "2. Submit to Kaggle: https://kaggle.com/competitions/playground-series-s6e4"
echo "3. Check your leaderboard score"
echo "4. Iterate and improve!"
