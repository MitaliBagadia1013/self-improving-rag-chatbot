"""
Create sample data for testing the pipeline
This generates synthetic data similar to the competition format
"""
import pandas as pd
import numpy as np
from pathlib import Path


def generate_sample_data(n_train=1000, n_test=500, n_features=20, random_state=42):
    """
    Generate sample irrigation need dataset
    
    Args:
        n_train: Number of training samples
        n_test: Number of test samples
        n_features: Number of features
        random_state: Random seed
    """
    np.random.seed(random_state)
    
    # Feature names (simulating irrigation-related features)
    feature_names = [
        'temperature', 'humidity', 'rainfall', 'soil_moisture',
        'wind_speed', 'solar_radiation', 'evapotranspiration',
        'crop_type', 'soil_type', 'latitude', 'longitude',
        'elevation', 'days_since_rain', 'season'
    ]
    
    # Add generic features to reach n_features
    while len(feature_names) < n_features:
        feature_names.append(f'feature_{len(feature_names)}')
    
    feature_names = feature_names[:n_features]
    
    def generate_features(n_samples):
        """Generate feature values"""
        data = {}
        
        # Numerical features
        data['temperature'] = np.random.normal(25, 10, n_samples)  # Celsius
        data['humidity'] = np.random.uniform(20, 100, n_samples)  # Percentage
        data['rainfall'] = np.random.exponential(5, n_samples)  # mm
        data['soil_moisture'] = np.random.uniform(0.1, 0.5, n_samples)  # fraction
        data['wind_speed'] = np.random.uniform(0, 20, n_samples)  # km/h
        data['solar_radiation'] = np.random.uniform(100, 1000, n_samples)  # W/m^2
        data['evapotranspiration'] = np.random.uniform(2, 10, n_samples)  # mm/day
        data['latitude'] = np.random.uniform(-50, 50, n_samples)
        data['longitude'] = np.random.uniform(-180, 180, n_samples)
        data['elevation'] = np.random.uniform(0, 2000, n_samples)  # meters
        data['days_since_rain'] = np.random.randint(0, 30, n_samples)
        
        # Categorical features
        data['crop_type'] = np.random.choice(['wheat', 'corn', 'rice', 'soybean'], n_samples)
        data['soil_type'] = np.random.choice(['clay', 'sandy', 'loam', 'silt'], n_samples)
        data['season'] = np.random.choice(['spring', 'summer', 'fall', 'winter'], n_samples)
        
        # Generic features
        for i in range(14, n_features):
            data[f'feature_{i}'] = np.random.normal(0, 1, n_samples)
        
        return pd.DataFrame(data)
    
    # Generate training data
    X_train = generate_features(n_train)
    
    # Generate target based on features (simple rule-based)
    # Low irrigation need: high rainfall, high soil moisture
    # High irrigation need: low rainfall, low soil moisture, high temperature
    # Medium: everything else
    
    irrigation_score = (
        -X_train['rainfall'] * 0.3 +
        -X_train['soil_moisture'] * 50 +
        X_train['temperature'] * 0.5 +
        -X_train['humidity'] * 0.1 +
        X_train['evapotranspiration'] * 2 +
        np.random.normal(0, 5, n_train)  # Add noise
    )
    
    # Convert score to categories
    low_threshold = np.percentile(irrigation_score, 33)
    high_threshold = np.percentile(irrigation_score, 67)
    
    y_train = pd.Series(['Medium'] * n_train)
    y_train[irrigation_score < low_threshold] = 'Low'
    y_train[irrigation_score > high_threshold] = 'High'
    
    # Add ID column
    train_df = X_train.copy()
    train_df.insert(0, 'id', range(n_train))
    train_df['Irrigation_Need'] = y_train
    
    # Generate test data
    X_test = generate_features(n_test)
    test_df = X_test.copy()
    test_df.insert(0, 'id', range(n_train, n_train + n_test))
    
    # Generate sample submission
    sample_submission = pd.DataFrame({
        'id': range(n_train, n_train + n_test),
        'Irrigation_Need': ['Low'] * n_test  # Dummy predictions
    })
    
    return train_df, test_df, sample_submission


def main():
    """Generate and save sample data"""
    print("Generating sample data for testing...")
    
    train_df, test_df, sample_submission = generate_sample_data(
        n_train=5000,
        n_test=2000,
        n_features=20
    )
    
    # Create data directory
    data_dir = Path("kaggle_irrigation/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Save files
    train_df.to_csv(data_dir / "train.csv", index=False)
    test_df.to_csv(data_dir / "test.csv", index=False)
    sample_submission.to_csv(data_dir / "sample_submission.csv", index=False)
    
    print(f"✓ Sample data generated and saved to {data_dir}/")
    print(f"  - train.csv: {train_df.shape}")
    print(f"  - test.csv: {test_df.shape}")
    print(f"  - sample_submission.csv: {sample_submission.shape}")
    
    print("\nTarget distribution:")
    print(train_df['Irrigation_Need'].value_counts())
    
    print("\nYou can now run:")
    print("  python kaggle_irrigation/eda.py")
    print("  python kaggle_irrigation/train.py")
    print("  python kaggle_irrigation/predict.py --model xgboost")


if __name__ == "__main__":
    main()
