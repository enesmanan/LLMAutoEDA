import pandas as pd
import numpy as np
from typing import Dict, Union, Tuple, Optional
from pathlib import Path
import re

class DataLoader:
    def __init__(self):
        self.data = None
        self.data_summary = None
        self.dropped_columns = []  # Track dropped columns
        
    def load_data(self, data_source: Union[str, pd.DataFrame]) -> pd.DataFrame:
        if isinstance(data_source, str):
            if data_source.endswith('.csv'):
                self.data = pd.read_csv(data_source)
            elif data_source.endswith('.xlsx'):
                self.data = pd.read_excel(data_source)
            else:
                raise ValueError("Unsupported file format")
        elif isinstance(data_source, pd.DataFrame):
            self.data = data_source.copy()
        else:
            raise ValueError("Unsupported data source")
        
        self.data = self._remove_id_columns(self.data)
        self._generate_summary()
        return self.data
    
    def _remove_id_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Detects and removes ID columns based on patterns and uniqueness"""
        id_patterns = [
            r'.*_id$', r'^id_.*', r'^id$', r'.*id.*',  # ID patterns
            r'.*_key$', r'^key_.*', r'^key$',          # Key patterns
            r'.*_no$', r'^no_.*', r'^no$',             # Number patterns
            r'.*index.*', r'.*identifier.*'            # Other common patterns
        ]
        
        potential_id_columns = []
        
        for col in df.columns:
            col_lower = col.lower()
            
            # Name-based check
            if any(re.match(pattern, col_lower) for pattern in id_patterns):
                if (df[col].nunique() / len(df) > 0.9 and  # >90% unique values
                    (pd.api.types.is_numeric_dtype(df[col]) or  
                     pd.api.types.is_string_dtype(df[col]))):   
                    potential_id_columns.append(col)
            
            # Content-based check
            elif (pd.api.types.is_numeric_dtype(df[col]) or 
                  pd.api.types.is_string_dtype(df[col])):
                if df[col].nunique() / len(df) > 0.95:  # >95% unique values
                    potential_id_columns.append(col)
        
        self.dropped_columns = potential_id_columns
        if potential_id_columns:
            print(f"Detected and removed ID columns: {', '.join(potential_id_columns)}")
            return df.drop(columns=potential_id_columns)
        
        return df
    
    def _generate_summary(self) -> Dict:
        """Generates a comprehensive summary of the dataset"""
        self.data_summary = {
            "shape": self.data.shape,
            "columns": {
                "numeric": self.data.select_dtypes(include=[np.number]).columns.tolist(),
                "categorical": self.data.select_dtypes(include=['object', 'category']).columns.tolist(),
                "datetime": self.data.select_dtypes(include=['datetime64']).columns.tolist()
            },
            "missing_values": self.data.isnull().sum().to_dict(),
            "unique_counts": {col: self.data[col].nunique() for col in self.data.columns},
            "dropped_id_columns": self.dropped_columns
        }
        return self.data_summary