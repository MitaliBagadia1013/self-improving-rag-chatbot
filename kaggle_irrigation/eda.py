"""
Exploratory Data Analysis for Kaggle Irrigation Need competition
"""
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.data_loader import DataLoader
from src.utils import (
    setup_plotting_style, plot_target_distribution, 
    plot_correlation_matrix, plot_missing_values, print_data_summary
)


def main():
    """Run exploratory data analysis"""
    print("=" * 80)
    print("KAGGLE IRRIGATION NEED - EXPLORATORY DATA ANALYSIS")
    print("=" * 80)
    
    # Setup plotting
    setup_plotting_style()
    
    # Load data
    loader = DataLoader(data_dir="kaggle_irrigation/data")
    
    try:
        X_train, y_train = loader.load_train_data()
        X_test, test_ids = loader.load_test_data()
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease download the competition data from Kaggle and place in kaggle_irrigation/data/")
        print("Required files: train.csv, test.csv, sample_submission.csv")
        return
    
    # Validate data consistency
    print("\n" + "=" * 80)
    print("DATA VALIDATION")
    print("=" * 80)
    loader.validate_data(X_train, X_test)
    
    # Print data summary
    print("\n" + "=" * 80)
    print("TRAINING DATA SUMMARY")
    print("=" * 80)
    print_data_summary(X_train, y_train)
    
    print("\n" + "=" * 80)
    print("TEST DATA SUMMARY")
    print("=" * 80)
    print_data_summary(X_test)
    
    # Get detailed info
    train_info = loader.get_data_info(X_train, y_train)
    test_info = loader.get_data_info(X_test)
    
    # Plot target distribution
    print("\n" + "=" * 80)
    print("VISUALIZATIONS")
    print("=" * 80)
    print("Generating plots...")
    
    plot_target_distribution(y_train, title="Training Set - Irrigation Need Distribution")
    
    # Plot missing values
    plot_missing_values(X_train)
    
    # Plot correlation matrix
    plot_correlation_matrix(X_train, top_n=20)
    
    # Check for class imbalance
    print("\n" + "=" * 80)
    print("CLASS IMBALANCE ANALYSIS")
    print("=" * 80)
    
    class_counts = y_train.value_counts()
    imbalance_ratio = class_counts.max() / class_counts.min()
    
    print(f"Class counts:")
    print(class_counts)
    print(f"\nImbalance ratio (max/min): {imbalance_ratio:.2f}")
    
    if imbalance_ratio > 1.5:
        print("⚠️  Significant class imbalance detected!")
        print("   Consider using: class weights, SMOTE, or stratified sampling")
    else:
        print("✓ Classes are relatively balanced")
    
    # Feature statistics
    print("\n" + "=" * 80)
    print("FEATURE STATISTICS")
    print("=" * 80)
    
    numerical_features = X_train.select_dtypes(include=['number']).columns
    categorical_features = X_train.select_dtypes(include=['object', 'category']).columns
    
    print(f"Numerical features: {len(numerical_features)}")
    if len(numerical_features) > 0:
        print(f"Numerical feature names: {', '.join(numerical_features[:10])}...")
    
    print(f"\nCategorical features: {len(categorical_features)}")
    if len(categorical_features) > 0:
        print(f"Categorical feature names: {', '.join(categorical_features)}")
    
    # Check for high cardinality categorical features
    if len(categorical_features) > 0:
        print(f"\nCategorical feature cardinality:")
        for col in categorical_features:
            n_unique = X_train[col].nunique()
            print(f"  {col}: {n_unique} unique values")
    
    print("\n" + "=" * 80)
    print("EDA COMPLETE")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Review the visualizations and statistics")
    print("2. Identify important features and patterns")
    print("3. Plan feature engineering strategies")
    print("4. Run: python kaggle_irrigation/train.py")


if __name__ == "__main__":
    main()
