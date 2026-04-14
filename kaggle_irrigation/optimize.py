"""
Hyperparameter optimization using Optuna
"""
import sys
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import balanced_accuracy_score

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.feature_engineering import FeatureEngineer, DomainFeatureEngineer
from src.models import ModelTrainer

try:
    import optuna
    OPTUNA_AVAILABLE = True
except ImportError:
    OPTUNA_AVAILABLE = False
    print("Warning: Optuna not installed. Install with: pip install optuna")

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

try:
    import lightgbm as lgb
    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

try:
    from catboost import CatBoostClassifier
    CATBOOST_AVAILABLE = True
except ImportError:
    CATBOOST_AVAILABLE = False


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Hyperparameter optimization")
    parser.add_argument('--model', type=str, required=True,
                       choices=['xgboost', 'lightgbm', 'catboost', 'random_forest'],
                       help='Model to optimize')
    parser.add_argument('--n-trials', type=int, default=50,
                       help='Number of Optuna trials (default: 50)')
    parser.add_argument('--n-folds', type=int, default=5,
                       help='Number of CV folds (default: 5)')
    
    return parser.parse_args()


def objective_xgboost(trial, X, y, n_folds=5):
    """Optuna objective for XGBoost"""
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0, 5),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 2),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 2),
        'objective': 'multi:softmax',
        'random_state': 42,
        'n_jobs': -1
    }
    
    return cross_validate_score(xgb.XGBClassifier(**param), X, y, n_folds)


def objective_lightgbm(trial, X, y, n_folds=5):
    """Optuna objective for LightGBM"""
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'num_leaves': trial.suggest_int('num_leaves', 20, 150),
        'subsample': trial.suggest_float('subsample', 0.6, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.6, 1.0),
        'min_child_samples': trial.suggest_int('min_child_samples', 5, 100),
        'reg_alpha': trial.suggest_float('reg_alpha', 0, 2),
        'reg_lambda': trial.suggest_float('reg_lambda', 0, 2),
        'class_weight': 'balanced',
        'random_state': 42,
        'n_jobs': -1,
        'verbosity': -1
    }
    
    return cross_validate_score(lgb.LGBMClassifier(**param), X, y, n_folds)


def objective_catboost(trial, X, y, n_folds=5):
    """Optuna objective for CatBoost"""
    param = {
        'iterations': trial.suggest_int('iterations', 100, 1000),
        'depth': trial.suggest_int('depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3, log=True),
        'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
        'border_count': trial.suggest_int('border_count', 32, 255),
        'random_strength': trial.suggest_float('random_strength', 0, 10),
        'bagging_temperature': trial.suggest_float('bagging_temperature', 0, 1),
        'auto_class_weights': 'Balanced',
        'random_state': 42,
        'verbose': False
    }
    
    return cross_validate_score(CatBoostClassifier(**param), X, y, n_folds)


def objective_random_forest(trial, X, y, n_folds=5):
    """Optuna objective for Random Forest"""
    from sklearn.ensemble import RandomForestClassifier
    
    param = {
        'n_estimators': trial.suggest_int('n_estimators', 100, 500),
        'max_depth': trial.suggest_int('max_depth', 5, 30),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None]),
        'class_weight': 'balanced',
        'random_state': 42,
        'n_jobs': -1
    }
    
    return cross_validate_score(RandomForestClassifier(**param), X, y, n_folds)


def cross_validate_score(model, X, y, n_folds=5):
    """Cross-validate and return mean balanced accuracy"""
    skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=42)
    scores = []
    
    for train_idx, val_idx in skf.split(X, y):
        X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
        y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
        
        model.fit(X_train, y_train)
        y_pred = model.predict(X_val)
        score = balanced_accuracy_score(y_val, y_pred)
        scores.append(score)
    
    return np.mean(scores)


def main():
    """Main optimization pipeline"""
    args = parse_args()
    
    if not OPTUNA_AVAILABLE:
        print("❌ Optuna is required for hyperparameter optimization")
        print("Install with: pip install optuna")
        return
    
    print("=" * 80)
    print(f"HYPERPARAMETER OPTIMIZATION - {args.model.upper()}")
    print("=" * 80)
    
    # Load data
    print("\nLoading data...")
    loader = DataLoader(data_dir="kaggle_irrigation/data")
    
    try:
        X_train, y_train = loader.load_train_data()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return
    
    # Feature engineering
    print("\nApplying feature engineering...")
    fe = FeatureEngineer()
    domain_fe = DomainFeatureEngineer()
    
    X_train_transformed = fe.fit_transform(X_train, create_interactions=True)
    X_train_transformed = domain_fe.create_irrigation_features(X_train_transformed)
    
    print(f"Transformed features shape: {X_train_transformed.shape}")
    
    # Select objective function
    print(f"\nOptimizing {args.model}...")
    
    if args.model == 'xgboost' and XGBOOST_AVAILABLE:
        objective_fn = lambda trial: objective_xgboost(trial, X_train_transformed, y_train, args.n_folds)
    elif args.model == 'lightgbm' and LIGHTGBM_AVAILABLE:
        objective_fn = lambda trial: objective_lightgbm(trial, X_train_transformed, y_train, args.n_folds)
    elif args.model == 'catboost' and CATBOOST_AVAILABLE:
        objective_fn = lambda trial: objective_catboost(trial, X_train_transformed, y_train, args.n_folds)
    elif args.model == 'random_forest':
        objective_fn = lambda trial: objective_random_forest(trial, X_train_transformed, y_train, args.n_folds)
    else:
        print(f"❌ Model {args.model} not available or not installed")
        return
    
    # Create and run study
    study = optuna.create_study(direction='maximize', study_name=f'{args.model}_optimization')
    study.optimize(objective_fn, n_trials=args.n_trials, show_progress_bar=True)
    
    # Print results
    print("\n" + "=" * 80)
    print("OPTIMIZATION RESULTS")
    print("=" * 80)
    
    print(f"\nBest trial:")
    trial = study.best_trial
    
    print(f"  Value (Balanced Accuracy): {trial.value:.4f}")
    print(f"\n  Params:")
    for key, value in trial.params.items():
        print(f"    {key}: {value}")
    
    # Save best parameters
    import json
    output_path = Path(f"kaggle_irrigation/models/{args.model}_best_params.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(trial.params, f, indent=2)
    
    print(f"\n✓ Best parameters saved to {output_path}")
    
    # Plot optimization history
    try:
        import matplotlib.pyplot as plt
        
        fig = optuna.visualization.matplotlib.plot_optimization_history(study)
        plt.tight_layout()
        plt.savefig(f"kaggle_irrigation/models/{args.model}_optimization_history.png", dpi=300)
        print(f"✓ Optimization history saved to kaggle_irrigation/models/{args.model}_optimization_history.png")
        
        fig = optuna.visualization.matplotlib.plot_param_importances(study)
        plt.tight_layout()
        plt.savefig(f"kaggle_irrigation/models/{args.model}_param_importances.png", dpi=300)
        print(f"✓ Parameter importances saved to kaggle_irrigation/models/{args.model}_param_importances.png")
    except Exception as e:
        print(f"Warning: Could not save plots: {e}")


if __name__ == "__main__":
    main()
