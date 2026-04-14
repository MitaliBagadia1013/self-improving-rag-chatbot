"""
Main training script for Kaggle Irrigation Need competition
"""
import sys
from pathlib import Path
import numpy as np
import argparse

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.feature_engineering import FeatureEngineer, DomainFeatureEngineer
from src.models import ModelTrainer, EnsembleModel
from src.utils import plot_cv_results, print_data_summary, setup_plotting_style


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Train models for Irrigation Need prediction")
    parser.add_argument('--baseline-only', action='store_true', 
                       help='Train only baseline models')
    parser.add_argument('--ensemble-only', action='store_true',
                       help='Train only ensemble models')
    parser.add_argument('--n-folds', type=int, default=5,
                       help='Number of cross-validation folds (default: 5)')
    parser.add_argument('--no-interactions', action='store_true',
                       help='Skip interaction feature creation')
    parser.add_argument('--save-models', action='store_true',
                       help='Save trained models to disk')
    
    return parser.parse_args()


def main():
    """Main training pipeline"""
    args = parse_args()
    
    print("=" * 80)
    print("KAGGLE IRRIGATION NEED - MODEL TRAINING")
    print("=" * 80)
    
    # Setup
    setup_plotting_style()
    
    # Load data
    print("\n" + "=" * 80)
    print("LOADING DATA")
    print("=" * 80)
    
    loader = DataLoader(data_dir="kaggle_irrigation/data")
    
    try:
        X_train, y_train = loader.load_train_data()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease download the competition data from Kaggle and place in kaggle_irrigation/data/")
        return
    
    # Feature engineering
    print("\n" + "=" * 80)
    print("FEATURE ENGINEERING")
    print("=" * 80)
    
    fe = FeatureEngineer()
    domain_fe = DomainFeatureEngineer()
    
    print("Fitting feature transformations...")
    fe.fit(X_train)
    
    print("Transforming features...")
    X_train_transformed = fe.transform(X_train, create_interactions=not args.no_interactions)
    
    # Apply domain-specific features
    X_train_transformed = domain_fe.create_irrigation_features(X_train_transformed)
    
    print(f"Transformed features shape: {X_train_transformed.shape}")
    print(f"Number of features created: {X_train_transformed.shape[1]}")
    
    # Initialize trainer
    trainer = ModelTrainer(random_state=42)
    
    # Train baseline models
    if not args.ensemble_only:
        print("\n" + "=" * 80)
        print("TRAINING BASELINE MODELS")
        print("=" * 80)
        
        baseline_models = trainer.get_baseline_models()
        
        for name, model in baseline_models.items():
            trainer.cross_validate(X_train_transformed, y_train, name, model, n_folds=args.n_folds)
            
            if args.save_models:
                # Train on full data and save
                trained_model = trainer.train_model(X_train_transformed, y_train, name, model)
                trainer.save_model(trained_model, name)
    
    # Train ensemble models
    if not args.baseline_only:
        print("\n" + "=" * 80)
        print("TRAINING ENSEMBLE MODELS")
        print("=" * 80)
        
        ensemble_models = trainer.get_ensemble_models()
        
        for name, model in ensemble_models.items():
            trainer.cross_validate(X_train_transformed, y_train, name, model, n_folds=args.n_folds)
            
            if args.save_models:
                # Train on full data and save
                trained_model = trainer.train_model(X_train_transformed, y_train, name, model)
                trainer.save_model(trained_model, name)
    
    # Display results summary
    print("\n" + "=" * 80)
    print("CROSS-VALIDATION RESULTS SUMMARY")
    print("=" * 80)
    
    cv_summary = trainer.get_cv_summary()
    print(cv_summary.to_string(index=False))
    
    # Plot results
    plot_cv_results(trainer.cv_results)
    
    # Recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    best_model = cv_summary.iloc[0]['Model']
    best_score = cv_summary.iloc[0]['Mean_CV_Score']
    
    print(f"\n✓ Best Model: {best_model}")
    print(f"✓ Best CV Score: {best_score:.4f}")
    
    print("\nNext steps:")
    print("1. Review model performance and CV results")
    print("2. Consider hyperparameter tuning for best models")
    print("3. Train ensemble/stacking of top models")
    print("4. Generate predictions: python kaggle_irrigation/predict.py")
    
    # Save feature engineer
    if args.save_models:
        import joblib
        fe_path = Path("kaggle_irrigation/models/feature_engineer.pkl")
        fe_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(fe, fe_path)
        print(f"\n✓ Feature engineer saved to {fe_path}")


if __name__ == "__main__":
    main()
