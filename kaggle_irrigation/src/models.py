"""
Model training and evaluation utilities
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import balanced_accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import StratifiedKFold
from typing import Dict, List, Tuple, Any
import joblib
from pathlib import Path

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


class ModelTrainer:
    """Train and evaluate machine learning models"""
    
    def __init__(self, random_state: int = 42):
        self.random_state = random_state
        self.models = {}
        self.cv_results = {}
        
    def get_baseline_models(self) -> Dict[str, Any]:
        """Get baseline models"""
        models = {
            'logistic_regression': LogisticRegression(
                max_iter=1000,
                random_state=self.random_state,
                class_weight='balanced'
            ),
            'decision_tree': DecisionTreeClassifier(
                max_depth=10,
                random_state=self.random_state,
                class_weight='balanced'
            ),
        }
        return models
    
    def get_ensemble_models(self) -> Dict[str, Any]:
        """Get ensemble models"""
        models = {
            'random_forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=15,
                random_state=self.random_state,
                class_weight='balanced',
                n_jobs=-1
            ),
        }
        
        if XGBOOST_AVAILABLE:
            models['xgboost'] = xgb.XGBClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                objective='multi:softmax',
                n_jobs=-1
            )
        
        if LIGHTGBM_AVAILABLE:
            models['lightgbm'] = lgb.LGBMClassifier(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                class_weight='balanced',
                n_jobs=-1,
                verbosity=-1
            )
        
        if CATBOOST_AVAILABLE:
            models['catboost'] = CatBoostClassifier(
                iterations=100,
                depth=6,
                learning_rate=0.1,
                random_state=self.random_state,
                verbose=False,
                auto_class_weights='Balanced'
            )
        
        return models
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, 
                      model_name: str, model: Any,
                      n_folds: int = 5) -> Dict[str, float]:
        """
        Perform stratified k-fold cross-validation
        
        Args:
            X: Features
            y: Target
            model_name: Name of the model
            model: Model instance
            n_folds: Number of folds
            
        Returns:
            Dictionary with CV results
        """
        skf = StratifiedKFold(n_splits=n_folds, shuffle=True, random_state=self.random_state)
        
        fold_scores = []
        
        print(f"\n{'='*60}")
        print(f"Cross-validating {model_name}...")
        print(f"{'='*60}")
        
        for fold, (train_idx, val_idx) in enumerate(skf.split(X, y), 1):
            X_train, X_val = X.iloc[train_idx], X.iloc[val_idx]
            y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
            
            # Train model
            model_clone = self._clone_model(model)
            model_clone.fit(X_train, y_train)
            
            # Predict
            y_pred = model_clone.predict(X_val)
            
            # Calculate balanced accuracy
            score = balanced_accuracy_score(y_val, y_pred)
            fold_scores.append(score)
            
            print(f"Fold {fold}: Balanced Accuracy = {score:.4f}")
        
        mean_score = np.mean(fold_scores)
        std_score = np.std(fold_scores)
        
        print(f"\nMean Balanced Accuracy: {mean_score:.4f} (+/- {std_score:.4f})")
        
        results = {
            'mean_score': mean_score,
            'std_score': std_score,
            'fold_scores': fold_scores
        }
        
        self.cv_results[model_name] = results
        
        return results
    
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series,
                   model_name: str, model: Any) -> Any:
        """
        Train a single model on full training data
        
        Args:
            X_train: Training features
            y_train: Training target
            model_name: Name of the model
            model: Model instance
            
        Returns:
            Trained model
        """
        print(f"\nTraining {model_name} on full training data...")
        model.fit(X_train, y_train)
        
        # Evaluate on training set
        y_pred = model.predict(X_train)
        train_score = balanced_accuracy_score(y_train, y_pred)
        print(f"Training Balanced Accuracy: {train_score:.4f}")
        
        self.models[model_name] = model
        
        return model
    
    def evaluate_model(self, model: Any, X: pd.DataFrame, y: pd.Series,
                      dataset_name: str = "validation") -> Dict[str, Any]:
        """
        Evaluate model performance
        
        Args:
            model: Trained model
            X: Features
            y: Target
            dataset_name: Name of dataset (for printing)
            
        Returns:
            Dictionary with evaluation metrics
        """
        y_pred = model.predict(X)
        
        # Calculate metrics
        balanced_acc = balanced_accuracy_score(y, y_pred)
        
        print(f"\n{dataset_name.upper()} SET RESULTS:")
        print(f"Balanced Accuracy: {balanced_acc:.4f}")
        print(f"\nClassification Report:")
        print(classification_report(y, y_pred))
        print(f"\nConfusion Matrix:")
        print(confusion_matrix(y, y_pred))
        
        return {
            'balanced_accuracy': balanced_acc,
            'predictions': y_pred
        }
    
    def save_model(self, model: Any, model_name: str, output_dir: str = "models"):
        """Save trained model to disk"""
        output_path = Path(output_dir) / f"{model_name}.pkl"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        joblib.dump(model, output_path)
        print(f"Model saved to {output_path}")
    
    def load_model(self, model_name: str, model_dir: str = "models") -> Any:
        """Load trained model from disk"""
        model_path = Path(model_dir) / f"{model_name}.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model not found at {model_path}")
        
        model = joblib.load(model_path)
        print(f"Model loaded from {model_path}")
        
        return model
    
    def _clone_model(self, model: Any) -> Any:
        """Clone a model for cross-validation"""
        from sklearn.base import clone
        try:
            return clone(model)
        except:
            # For models that don't support sklearn clone
            import copy
            return copy.deepcopy(model)
    
    def get_cv_summary(self) -> pd.DataFrame:
        """Get summary of cross-validation results"""
        if not self.cv_results:
            print("No cross-validation results available")
            return None
        
        summary = pd.DataFrame({
            'Model': list(self.cv_results.keys()),
            'Mean_CV_Score': [results['mean_score'] for results in self.cv_results.values()],
            'Std_CV_Score': [results['std_score'] for results in self.cv_results.values()]
        })
        
        summary = summary.sort_values('Mean_CV_Score', ascending=False)
        
        return summary


class EnsembleModel:
    """Ensemble multiple models using voting or stacking"""
    
    def __init__(self, models: Dict[str, Any], weights: List[float] = None):
        self.models = models
        self.weights = weights or [1.0] * len(models)
        
    def fit(self, X: pd.DataFrame, y: pd.Series):
        """Train all models in the ensemble"""
        for name, model in self.models.items():
            print(f"Training {name}...")
            model.fit(X, y)
        
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using weighted voting"""
        predictions = []
        
        for name, model in self.models.items():
            pred = model.predict(X)
            predictions.append(pred)
        
        # Weighted voting
        predictions = np.array(predictions)
        
        # For each sample, find the most voted class
        final_predictions = []
        for i in range(predictions.shape[1]):
            votes = predictions[:, i]
            # Count votes with weights
            unique_classes = np.unique(votes)
            weighted_votes = {}
            
            for j, vote in enumerate(votes):
                if vote not in weighted_votes:
                    weighted_votes[vote] = 0
                weighted_votes[vote] += self.weights[j]
            
            # Get class with maximum weighted votes
            final_pred = max(weighted_votes, key=weighted_votes.get)
            final_predictions.append(final_pred)
        
        return np.array(final_predictions)
