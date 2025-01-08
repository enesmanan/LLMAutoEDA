import pandas as pd
import numpy as np
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class AnalysisResult:
    stats: Dict
    correlations: Dict
    distributions: Dict
    outliers: Dict

class DataAnalyzer:
    """Class for performing data analysis tasks"""
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.numeric_cols = data.select_dtypes(include=[np.number]).columns
        self.categorical_cols = data.select_dtypes(include=['object', 'category']).columns
        
    def analyze(self) -> AnalysisResult:
        """Performs all analyses and returns the results"""
        return AnalysisResult(
            stats=self._calculate_statistics(),
            correlations=self._calculate_correlations(),
            distributions=self._analyze_distributions(),
            outliers=self._detect_outliers()
        )
    
    def _calculate_statistics(self) -> Dict:
        """Calculates basic statistics for numeric and categorical variables"""
        numeric_stats = self.data[self.numeric_cols].describe()
        categorical_stats = {col: self.data[col].value_counts().to_dict() 
                           for col in self.categorical_cols}
        return {"numeric": numeric_stats.to_dict(), "categorical": categorical_stats}
    
    def _calculate_correlations(self) -> Dict:
        """Performs correlation analysis for numeric variables"""
        if len(self.numeric_cols) > 1:
            return self.data[self.numeric_cols].corr().to_dict()
        return {}
    
    def _analyze_distributions(self) -> Dict:
        """Analyzes distributions of numeric variables"""
        distributions = {}
        for col in self.numeric_cols:
            distributions[col] = {
                "skew": self.data[col].skew(),
                "kurtosis": self.data[col].kurtosis(),
                "histogram_data": np.histogram(self.data[col].dropna(), bins=30)
            }
        return distributions
    
    def _detect_outliers(self) -> Dict:
        """Detects outliers using IQR method"""
        outliers = {}
        for col in self.numeric_cols:
            q1 = self.data[col].quantile(0.25)
            q3 = self.data[col].quantile(0.75)
            iqr = q3 - q1
            outliers[col] = {
                "count": len(self.data[(self.data[col] < q1 - 1.5 * iqr) | 
                                     (self.data[col] > q3 + 1.5 * iqr)]),
                "percentage": len(self.data[(self.data[col] < q1 - 1.5 * iqr) | 
                                          (self.data[col] > q3 + 1.5 * iqr)]) / len(self.data) * 100
            }
        return outliers