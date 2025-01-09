from scipy import stats
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class StatisticalResults:
    normality_tests: Dict
    distribution_stats: Dict
    descriptive_stats: Dict

class StatisticalAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.numeric_cols = data.select_dtypes(include=[np.number]).columns
        
    def analyze(self) -> StatisticalResults:
        """Performs all statistical analyses"""
        return StatisticalResults(
            normality_tests=self._test_normality(),
            distribution_stats=self._analyze_distributions(),
            descriptive_stats=self._calculate_descriptive_stats()
        )
    
    def _test_normality(self) -> Dict:
        """Performs Shapiro-Wilk normality test"""
        normality_results = {}
        for col in self.numeric_cols:
            data = self.data[col].dropna()
            if len(data) > 2:
                shapiro_test = stats.shapiro(data)
                normality_results[col] = {
                    'shapiro_statistic': float(shapiro_test.statistic),
                    'shapiro_pvalue': float(shapiro_test.pvalue),
                    'is_normal': shapiro_test.pvalue > 0.05
                }
        return normality_results
    
    def _analyze_distributions(self) -> Dict:
        """Calculates distribution statistics"""
        distribution_stats = {}
        for col in self.numeric_cols:
            data = self.data[col].dropna()
            if len(data) > 0:
                distribution_stats[col] = {
                    'skewness': float(stats.skew(data)),
                    'kurtosis': float(stats.kurtosis(data)),
                    'mode': float(stats.mode(data, keepdims=True).mode[0]),
                    'iqr': float(np.percentile(data, 75) - np.percentile(data, 25)),
                    'range': float(data.max() - data.min()),
                    'cv': float(data.std() / data.mean() if data.mean() != 0 else np.nan)
                }
        return distribution_stats
    
    def _calculate_descriptive_stats(self) -> Dict:
        """Calculates basic descriptive statistics"""
        descriptive_stats = {}
        for col in self.numeric_cols:
            data = self.data[col].dropna()
            if len(data) > 0:
                stats_dict = {
                    'mean': float(data.mean()),
                    'median': float(data.median()),
                    'std': float(data.std()),
                    'skewness': float(stats.skew(data)),
                    'kurtosis': float(stats.kurtosis(data)),
                    'min': float(data.min()),
                    'max': float(data.max()),
                    'q1': float(np.percentile(data, 25)),
                    'q3': float(np.percentile(data, 75))
                }
                descriptive_stats[col] = stats_dict
        return descriptive_stats

    def to_dict(self) -> Dict:
        """Converts results to dictionary format"""
        results = self.analyze()
        return {
            'normality_tests': results.normality_tests,
            'distribution_stats': results.distribution_stats,
            'descriptive_stats': results.descriptive_stats
        }