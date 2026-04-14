"""
Utility functions for the Kaggle competition
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from typing import Optional, Dict, Any


def setup_plotting_style():
    """Set up matplotlib and seaborn styling"""
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 10


def plot_target_distribution(y: pd.Series, title: str = "Target Distribution",
                            save_path: Optional[str] = None):
    """
    Plot target variable distribution
    
    Args:
        y: Target series
        title: Plot title
        save_path: Optional path to save figure
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Count plot
    y.value_counts().plot(kind='bar', ax=ax1, color='skyblue', edgecolor='black')
    ax1.set_title(f"{title} - Counts")
    ax1.set_xlabel("Irrigation Need")
    ax1.set_ylabel("Count")
    ax1.tick_params(axis='x', rotation=0)
    
    # Percentage plot
    (y.value_counts() / len(y) * 100).plot(kind='bar', ax=ax2, color='lightcoral', edgecolor='black')
    ax2.set_title(f"{title} - Percentage")
    ax2.set_xlabel("Irrigation Need")
    ax2.set_ylabel("Percentage (%)")
    ax2.tick_params(axis='x', rotation=0)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_feature_importance(importances: np.ndarray, feature_names: list,
                           top_n: int = 20, save_path: Optional[str] = None):
    """
    Plot feature importance
    
    Args:
        importances: Feature importance values
        feature_names: Feature names
        top_n: Number of top features to show
        save_path: Optional path to save figure
    """
    # Create dataframe
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    # Plot top N features
    plt.figure(figsize=(10, 8))
    sns.barplot(data=importance_df.head(top_n), x='importance', y='feature', palette='viridis')
    plt.title(f'Top {top_n} Feature Importances')
    plt.xlabel('Importance')
    plt.ylabel('Feature')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()
    
    return importance_df


def plot_correlation_matrix(X: pd.DataFrame, top_n: int = 30,
                           save_path: Optional[str] = None):
    """
    Plot correlation matrix heatmap
    
    Args:
        X: Feature dataframe
        top_n: Number of features to include
        save_path: Optional path to save figure
    """
    # Select numerical features only
    numerical_features = X.select_dtypes(include=[np.number]).columns
    
    if len(numerical_features) == 0:
        print("No numerical features to plot")
        return
    
    # Limit to top_n features
    features_to_plot = numerical_features[:min(top_n, len(numerical_features))]
    
    # Calculate correlation matrix
    corr_matrix = X[features_to_plot].corr()
    
    # Plot heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Feature Correlation Matrix')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_missing_values(X: pd.DataFrame, save_path: Optional[str] = None):
    """
    Plot missing value statistics
    
    Args:
        X: Feature dataframe
        save_path: Optional path to save figure
    """
    missing = X.isnull().sum()
    missing_pct = (missing / len(X) * 100).sort_values(ascending=False)
    
    # Filter features with missing values
    missing_pct = missing_pct[missing_pct > 0]
    
    if len(missing_pct) == 0:
        print("No missing values found")
        return
    
    plt.figure(figsize=(10, 6))
    missing_pct.plot(kind='bar', color='salmon', edgecolor='black')
    plt.title('Missing Values by Feature')
    plt.xlabel('Feature')
    plt.ylabel('Missing Percentage (%)')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def plot_cv_results(cv_results: Dict[str, Dict], save_path: Optional[str] = None):
    """
    Plot cross-validation results comparison
    
    Args:
        cv_results: Dictionary with CV results for each model
        save_path: Optional path to save figure
    """
    models = list(cv_results.keys())
    mean_scores = [cv_results[model]['mean_score'] for model in models]
    std_scores = [cv_results[model]['std_score'] for model in models]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    x_pos = np.arange(len(models))
    ax.bar(x_pos, mean_scores, yerr=std_scores, capsize=5, 
           color='steelblue', edgecolor='black', alpha=0.7)
    
    ax.set_xlabel('Model')
    ax.set_ylabel('Balanced Accuracy')
    ax.set_title('Cross-Validation Results Comparison')
    ax.set_xticks(x_pos)
    ax.set_xticklabels(models, rotation=45, ha='right')
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (mean, std) in enumerate(zip(mean_scores, std_scores)):
        ax.text(i, mean + std + 0.01, f'{mean:.4f}', 
               ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    plt.show()


def print_data_summary(X: pd.DataFrame, y: Optional[pd.Series] = None):
    """
    Print comprehensive data summary
    
    Args:
        X: Feature dataframe
        y: Optional target series
    """
    print("=" * 80)
    print("DATA SUMMARY")
    print("=" * 80)
    
    print(f"\nDataset Shape: {X.shape}")
    print(f"Number of Features: {X.shape[1]}")
    print(f"Number of Samples: {X.shape[0]}")
    
    # Feature types
    print(f"\nFeature Types:")
    print(X.dtypes.value_counts())
    
    # Missing values
    missing = X.isnull().sum()
    if missing.sum() > 0:
        print(f"\nFeatures with Missing Values:")
        missing_features = missing[missing > 0].sort_values(ascending=False)
        for feat, count in missing_features.items():
            pct = count / len(X) * 100
            print(f"  {feat}: {count} ({pct:.2f}%)")
    else:
        print(f"\n✓ No missing values found")
    
    # Numerical features statistics
    numerical_features = X.select_dtypes(include=[np.number]).columns
    if len(numerical_features) > 0:
        print(f"\nNumerical Features Summary:")
        print(X[numerical_features].describe())
    
    # Target distribution
    if y is not None:
        print(f"\nTarget Distribution:")
        print(y.value_counts())
        print(f"\nTarget Percentages:")
        print((y.value_counts() / len(y) * 100).round(2))
    
    print("=" * 80)


def save_predictions_with_metadata(predictions: np.ndarray, ids: pd.Series,
                                  model_name: str, cv_score: float,
                                  output_dir: str = "submissions"):
    """
    Save predictions with metadata in filename
    
    Args:
        predictions: Predicted labels
        ids: Test IDs
        model_name: Name of model
        cv_score: Cross-validation score
        output_dir: Output directory
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"submission_{model_name}_cv{cv_score:.4f}_{timestamp}.csv"
    output_path = Path(output_dir) / filename
    
    submission = pd.DataFrame({
        'id': ids,
        'Irrigation_Need': predictions
    })
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    submission.to_csv(output_path, index=False)
    
    print(f"Submission saved to {output_path}")
    
    return output_path


def compare_predictions(pred1: np.ndarray, pred2: np.ndarray,
                       label1: str = "Model 1", label2: str = "Model 2"):
    """
    Compare predictions from two models
    
    Args:
        pred1: Predictions from model 1
        pred2: Predictions from model 2
        label1: Label for model 1
        label2: Label for model 2
    """
    agreement = (pred1 == pred2).sum() / len(pred1) * 100
    
    print(f"\n{label1} vs {label2} Comparison:")
    print(f"Agreement: {agreement:.2f}%")
    print(f"Disagreement: {100-agreement:.2f}%")
    
    # Distribution comparison
    print(f"\n{label1} distribution:")
    print(pd.Series(pred1).value_counts(normalize=True) * 100)
    
    print(f"\n{label2} distribution:")
    print(pd.Series(pred2).value_counts(normalize=True) * 100)
