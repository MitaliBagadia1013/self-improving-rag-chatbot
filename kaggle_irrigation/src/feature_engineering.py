"""
Feature engineering for Kaggle Irrigation Need competition
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, RobustScaler, LabelEncoder
from sklearn.impute import SimpleImputer
from typing import Tuple, List, Optional


class FeatureEngineer:
    """Feature engineering pipeline"""
    
    def __init__(self):
        self.scaler = None
        self.imputer = None
        self.label_encoders = {}
        self.feature_names = None
        self.numerical_features = []
        self.categorical_features = []
        
    def fit(self, X: pd.DataFrame) -> 'FeatureEngineer':
        """
        Fit feature engineering transformations
        
        Args:
            X: Training features
            
        Returns:
            self
        """
        X = X.copy()
        
        # Identify feature types
        self.numerical_features = X.select_dtypes(include=[np.number]).columns.tolist()
        self.categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        print(f"Numerical features: {len(self.numerical_features)}")
        print(f"Categorical features: {len(self.categorical_features)}")
        
        # Fit imputer for numerical features
        if self.numerical_features:
            self.imputer = SimpleImputer(strategy='median')
            self.imputer.fit(X[self.numerical_features])
        
        # Fit label encoders for categorical features
        for col in self.categorical_features:
            le = LabelEncoder()
            # Handle missing values
            valid_mask = X[col].notna()
            if valid_mask.any():
                le.fit(X[col][valid_mask].astype(str))
                self.label_encoders[col] = le
        
        # Fit scaler after imputation
        if self.numerical_features:
            X_imputed = pd.DataFrame(
                self.imputer.transform(X[self.numerical_features]),
                columns=self.numerical_features,
                index=X.index
            )
            self.scaler = RobustScaler()
            self.scaler.fit(X_imputed)
        
        return self
    
    def transform(self, X: pd.DataFrame, create_interactions: bool = True) -> pd.DataFrame:
        """
        Transform features
        
        Args:
            X: Input features
            create_interactions: Whether to create interaction features
            
        Returns:
            Transformed features
        """
        X = X.copy()
        
        # Impute numerical features
        if self.numerical_features and self.imputer is not None:
            X[self.numerical_features] = self.imputer.transform(X[self.numerical_features])
        
        # Encode categorical features
        for col in self.categorical_features:
            if col in self.label_encoders:
                le = self.label_encoders[col]
                # Handle unseen categories
                X[col] = X[col].fillna('missing').astype(str)
                X[col] = X[col].apply(
                    lambda x: le.transform([x])[0] if x in le.classes_ else -1
                )
        
        # Create additional features
        if create_interactions and len(self.numerical_features) >= 2:
            X = self._create_interaction_features(X)
        
        # Create statistical features
        if len(self.numerical_features) >= 3:
            X = self._create_statistical_features(X)
        
        # Scale numerical features
        num_cols = [col for col in X.columns if col in self.numerical_features or 
                   col.endswith('_interaction') or col.endswith('_stat')]
        
        if num_cols and self.scaler is not None:
            # Only scale original numerical features with the fitted scaler
            original_num_cols = [col for col in num_cols if col in self.numerical_features]
            if original_num_cols:
                X[original_num_cols] = self.scaler.transform(X[original_num_cols])
            
            # Scale new features separately (simple standardization)
            new_cols = [col for col in num_cols if col not in self.numerical_features]
            if new_cols:
                scaler_new = StandardScaler()
                X[new_cols] = scaler_new.fit_transform(X[new_cols])
        
        return X
    
    def fit_transform(self, X: pd.DataFrame, create_interactions: bool = True) -> pd.DataFrame:
        """Fit and transform in one step"""
        return self.fit(X).transform(X, create_interactions)
    
    def _create_interaction_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features between important variables"""
        X = X.copy()
        
        # Get top numerical features (limit to avoid explosion)
        num_features = [col for col in self.numerical_features if col in X.columns]
        
        if len(num_features) >= 2:
            # Create pairwise interactions for top features
            # Limit to first 10 features to avoid too many combinations
            top_features = num_features[:min(10, len(num_features))]
            
            for i in range(len(top_features)):
                for j in range(i + 1, min(i + 4, len(top_features))):  # Limit interactions
                    feat1, feat2 = top_features[i], top_features[j]
                    
                    # Multiplicative interaction
                    X[f'{feat1}_x_{feat2}_interaction'] = X[feat1] * X[feat2]
                    
                    # Ratio (avoid division by zero)
                    with np.errstate(divide='ignore', invalid='ignore'):
                        ratio = X[feat1] / (X[feat2] + 1e-5)
                        X[f'{feat1}_div_{feat2}_interaction'] = np.where(
                            np.isfinite(ratio), ratio, 0
                        )
        
        return X
    
    def _create_statistical_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Create statistical aggregation features"""
        X = X.copy()
        
        num_features = [col for col in self.numerical_features if col in X.columns]
        
        if len(num_features) >= 3:
            # Statistical aggregations across all numerical features
            X['mean_stat'] = X[num_features].mean(axis=1)
            X['std_stat'] = X[num_features].std(axis=1)
            X['min_stat'] = X[num_features].min(axis=1)
            X['max_stat'] = X[num_features].max(axis=1)
            X['range_stat'] = X['max_stat'] - X['min_stat']
            X['median_stat'] = X[num_features].median(axis=1)
        
        return X
    
    def get_feature_names(self, X: pd.DataFrame) -> List[str]:
        """Get list of all feature names after transformation"""
        return X.columns.tolist()


class DomainFeatureEngineer:
    """
    Domain-specific feature engineering for irrigation prediction
    This can be customized based on the actual features in the dataset
    """
    
    def __init__(self):
        pass
    
    def create_irrigation_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """
        Create domain-specific features related to irrigation needs
        
        Note: This is a template - actual implementation depends on available features
        Common irrigation-related features might include:
        - Temperature and humidity combinations
        - Moisture deficit calculations
        - Evapotranspiration estimates
        - Seasonal indicators
        - Soil-weather interactions
        """
        X = X.copy()
        
        # Example: If temperature and humidity columns exist
        if 'temperature' in X.columns and 'humidity' in X.columns:
            # Heat index approximation
            X['heat_index'] = X['temperature'] + 0.5 * (X['temperature'] - X['humidity'])
            
        # Example: If rainfall and temperature exist
        if 'rainfall' in X.columns and 'temperature' in X.columns:
            # Moisture availability indicator
            X['moisture_indicator'] = X['rainfall'] / (X['temperature'] + 1)
            
        # Example: If soil moisture exists
        if 'soil_moisture' in X.columns:
            # Moisture deficit
            optimal_moisture = 0.3  # Example threshold
            X['moisture_deficit'] = optimal_moisture - X['soil_moisture']
            X['moisture_deficit_abs'] = np.abs(X['moisture_deficit'])
        
        return X
