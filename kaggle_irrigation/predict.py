"""
Prediction and submission generation script
"""
import sys
from pathlib import Path
import argparse
import joblib
import numpy as np

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import DataLoader, create_submission
from src.feature_engineering import FeatureEngineer, DomainFeatureEngineer
from src.models import ModelTrainer
from src.utils import save_predictions_with_metadata


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Generate predictions for test set")
    parser.add_argument('--model', type=str, required=True,
                       help='Model name to use for predictions (e.g., xgboost, lightgbm)')
    parser.add_argument('--cv-score', type=float, default=0.0,
                       help='CV score to include in filename')
    parser.add_argument('--ensemble', action='store_true',
                       help='Use ensemble of multiple models')
    
    return parser.parse_args()


def main():
    """Generate predictions and create submission file"""
    args = parse_args()
    
    print("=" * 80)
    print("KAGGLE IRRIGATION NEED - PREDICTION GENERATION")
    print("=" * 80)
    
    # Load data
    print("\n" + "=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    loader = DataLoader(data_dir="kaggle_irrigation/data")
    
    try:
        X_train, y_train = loader.load_train_data()
        X_test, test_ids = loader.load_test_data()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Feature engineering
    print("\n" + "=" * 80)
    print("FEATURE ENGINEERING")
    print("=" * 80)
    
    # Try to load saved feature engineer
    fe_path = Path("kaggle_irrigation/models/feature_engineer.pkl")
    
    if fe_path.exists():
        print(f"Loading saved feature engineer from {fe_path}")
        fe = joblib.load(fe_path)
    else:
        print("No saved feature engineer found, creating new one...")
        fe = FeatureEngineer()
        fe.fit(X_train)
    
    domain_fe = DomainFeatureEngineer()
    
    # Transform training and test data
    print("Transforming training data...")
    X_train_transformed = fe.transform(X_train, create_interactions=True)
    X_train_transformed = domain_fe.create_irrigation_features(X_train_transformed)
    
    print("Transforming test data...")
    X_test_transformed = fe.transform(X_test, create_interactions=True)
    X_test_transformed = domain_fe.create_irrigation_features(X_test_transformed)
    
    print(f"Training features shape: {X_train_transformed.shape}")
    print(f"Test features shape: {X_test_transformed.shape}")
    
    # Load or train model
    print("\n" + "=" * 80)
    print("MODEL LOADING/TRAINING")
    print("=" * 80)
    
    trainer = ModelTrainer(random_state=42)
    model_path = Path(f"kaggle_irrigation/models/{args.model}.pkl")
    
    if model_path.exists():
        print(f"Loading saved model from {model_path}")
        model = trainer.load_model(args.model)
    else:
        print(f"No saved model found, training {args.model}...")
        
        # Get model
        if args.model in ['logistic_regression', 'decision_tree']:
            models = trainer.get_baseline_models()
        else:
            models = trainer.get_ensemble_models()
        
        if args.model not in models:
            print(f"❌ Error: Model '{args.model}' not found")
            print(f"Available models: {list(models.keys())}")
            return
        
        model = models[args.model]
        
        # Train model
        model = trainer.train_model(X_train_transformed, y_train, args.model, model)
        
        # Save model
        trainer.save_model(model, args.model)
    
    # Generate predictions
    print("\n" + "=" * 80)
    print("GENERATING PREDICTIONS")
    print("=" * 80)
    
    predictions = model.predict(X_test_transformed)
    
    print(f"Predictions generated: {len(predictions)}")
    print(f"Prediction distribution:")
    import pandas as pd
    print(pd.Series(predictions).value_counts())
    
    # Create submission
    print("\n" + "=" * 80)
    print("CREATING SUBMISSION FILE")
    print("=" * 80)
    
    if args.cv_score > 0:
        submission_path = save_predictions_with_metadata(
            predictions, test_ids, args.model, args.cv_score,
            output_dir="kaggle_irrigation/submissions"
        )
    else:
        submission_path = create_submission(
            test_ids, predictions,
            output_path=f"kaggle_irrigation/submissions/submission_{args.model}.csv"
        )
    
    print("\n" + "=" * 80)
    print("SUBMISSION READY")
    print("=" * 80)
    print(f"\n✓ Submission file created: {submission_path}")
    print("\nNext steps:")
    print("1. Review the submission file")
    print("2. Submit to Kaggle competition")
    print("3. Check leaderboard score")
    print("4. Iterate and improve!")


if __name__ == "__main__":
    main()
