"""
Data loading utilities for Kaggle Irrigation Need competition
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Tuple, Optional


class DataLoader:
    """Load and validate competition data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        
    def load_train_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load training data
        
        Returns:
            Tuple of (features, target)
        """
        train_path = self.data_dir / "train.csv"
        if not train_path.exists():
            raise FileNotFoundError(
                f"Training data not found at {train_path}. "
                "Please download from Kaggle and place in data/ directory."
            )
        
        df = pd.read_csv(train_path)
        print(f"Loaded training data: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        
        # Separate features and target
        if 'Irrigation_Need' not in df.columns:
            raise ValueError("Target column 'Irrigation_Need' not found in training data")
        
        X = df.drop(['Irrigation_Need'], axis=1)
        y = df['Irrigation_Need']
        
        # Remove ID column if present
        if 'id' in X.columns:
            X = X.drop('id', axis=1)
        
        print(f"Features shape: {X.shape}")
        print(f"Target distribution:\n{y.value_counts()}")
        
        return X, y
    
    def load_test_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Load test data
        
        Returns:
            Tuple of (features, ids)
        """
        test_path = self.data_dir / "test.csv"
        if not test_path.exists():
            raise FileNotFoundError(
                f"Test data not found at {test_path}. "
                "Please download from Kaggle and place in data/ directory."
            )
        
        df = pd.read_csv(test_path)
        print(f"Loaded test data: {df.shape}")
        
        # Extract IDs
        if 'id' not in df.columns:
            raise ValueError("ID column not found in test data")
        
        ids = df['id']
        X = df.drop('id', axis=1)
        
        print(f"Test features shape: {X.shape}")
        
        return X, ids
    
    def load_sample_submission(self) -> pd.DataFrame:
        """Load sample submission file"""
        sample_path = self.data_dir / "sample_submission.csv"
        if not sample_path.exists():
            print(f"Warning: Sample submission not found at {sample_path}")
            return None
        
        return pd.read_csv(sample_path)
    
    def get_data_info(self, X: pd.DataFrame, y: Optional[pd.Series] = None) -> dict:
        """
        Get comprehensive data information
        
        Args:
            X: Feature dataframe
            y: Optional target series
            
        Returns:
            Dictionary with data statistics
        """
        info = {
            'n_samples': len(X),
            'n_features': X.shape[1],
            'feature_names': X.columns.tolist(),
            'feature_types': X.dtypes.to_dict(),
            'missing_values': X.isnull().sum().to_dict(),
            'missing_percentage': (X.isnull().sum() / len(X) * 100).to_dict(),
        }
        
        if y is not None:
            info['target_distribution'] = y.value_counts().to_dict()
            info['target_percentage'] = (y.value_counts() / len(y) * 100).to_dict()
        
        return info
    
    def validate_data(self, X_train: pd.DataFrame, X_test: pd.DataFrame):
        """
        Validate training and test data consistency
        
        Args:
            X_train: Training features
            X_test: Test features
        """
        # Check column consistency
        train_cols = set(X_train.columns)
        test_cols = set(X_test.columns)
        
        if train_cols != test_cols:
            missing_in_test = train_cols - test_cols
            missing_in_train = test_cols - train_cols
            
            if missing_in_test:
                print(f"Warning: Columns in train but not in test: {missing_in_test}")
            if missing_in_train:
                print(f"Warning: Columns in test but not in train: {missing_in_train}")
        else:
            print("✓ Column names match between train and test")
        
        # Check data types
        for col in train_cols & test_cols:
            if X_train[col].dtype != X_test[col].dtype:
                print(f"Warning: Data type mismatch for column '{col}': "
                      f"train={X_train[col].dtype}, test={X_test[col].dtype}")
        
        print(f"✓ Data validation complete")


def create_submission(ids: pd.Series, predictions: np.ndarray, 
                     output_path: str = "submissions/submission.csv"):
    """
    Create submission file in required format
    
    Args:
        ids: Test set IDs
        predictions: Predicted class labels
        output_path: Path to save submission file
    """
    submission = pd.DataFrame({
        'id': ids,
        'Irrigation_Need': predictions
    })
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save submission
    submission.to_csv(output_path, index=False)
    print(f"Submission saved to {output_path}")
    print(f"Submission shape: {submission.shape}")
    print(f"Prediction distribution:\n{submission['Irrigation_Need'].value_counts()}")
    
    return submission
