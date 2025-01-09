import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Dict, List
from .analyzer import AnalysisResult

class DataVisualizer:
    def __init__(self, data: pd.DataFrame, analysis_result: AnalysisResult):
        self.data = data
        self.analysis = analysis_result
        self.default_layout = {
            'height': 420,  # Fixed height for plot section
            'width': None,  # None for responsive design
            'margin': dict(l=40, r=40, t=50, b=40),
            'template': 'plotly_white',
            'showlegend': True,
            'font': {'size': 11, 'family': 'Roboto, "Segoe UI", Arial, sans-serif'},
            'title': {
                'font': {'size': 14, 'family': 'Roboto, "Segoe UI", Arial, sans-serif'},
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'xaxis': {
                'gridcolor': 'rgba(0,0,0,0.1)',
                'showline': True,
                'linewidth': 1,
                'linecolor': 'rgba(0,0,0,0.2)',
                'title': {'standoff': 15}
            },
            'yaxis': {
                'gridcolor': 'rgba(0,0,0,0.1)',
                'showline': True,
                'linewidth': 1,
                'linecolor': 'rgba(0,0,0,0.2)',
                'title': {'standoff': 15}
            }
        }
    
    def generate_all_plots(self) -> Dict[str, List[str]]:
        """Generates all visualization plots"""
        return {
            "distributions": self._create_distribution_plots(),
            "correlations": self._create_correlation_plot(),
            "categorical": self._create_categorical_plots(),
            "outliers": self._create_outlier_plots()
        }
    
    def _create_plot_config(self):
        """Common configuration for all plots"""
        return {
            'displayModeBar': False,  # Remove plotly buttons
            'responsive': True,
            'showTips': False  # Remove tooltips
        }
    
    def _create_distribution_plots(self) -> List[str]:
        """Creates distribution plots for numeric variables"""
        plots = []
        for col in self.data.select_dtypes(include=[np.number]).columns:
            fig = px.histogram(
                self.data, 
                x=col, 
                title=f'Distribution of {col}'
            )
            fig.update_layout(**self.default_layout)
            plots.append(fig.to_html(
                full_html=False,
                include_plotlyjs=False,
                config=self._create_plot_config()
            ))
        return plots
    
    def _create_correlation_plot(self) -> str:
        """Creates correlation matrix plot"""
        if not self.analysis.correlations:
            return ""
        
        corr_df = pd.DataFrame(self.analysis.correlations)
        
        corr_layout = self.default_layout.copy()
        corr_layout.update({
            'height': 450,
            'width': None,
            'margin': dict(l=50, r=50, t=50, b=50),
            'annotations': [{
                'x': i,
                'y': j,
                'text': f'{corr_df.iloc[i, j]:.2f}',
                'font': {'size': 11, 'color': 'white' if abs(corr_df.iloc[i, j]) > 0.4 else 'black'},
                'showarrow': False
            } for i in range(len(corr_df.columns)) for j in range(len(corr_df.index))],
            'coloraxis': {
                'colorbar': {
                    'title': 'Correlation',
                    'titleside': 'right',
                    'thickness': 15,
                    'len': 0.9,
                    'tickformat': '.2f'
                },
                'colorscale': [
                    [0.0, '#c41e3a'],
                    [0.5, '#f8f9fa'],
                    [1.0, '#1e88e5']
                ]
            }
        })
        
        fig = px.imshow(
            corr_df,
            title="Correlation Matrix",
            color_continuous_scale=[
                [0.0, '#c41e3a'],
                [0.5, '#f8f9fa'],
                [1.0, '#1e88e5']
            ],
            aspect='auto'
        )
        
        fig.update_traces(text=corr_df.values, texttemplate='%{text:.2f}')
        fig.update_layout(**corr_layout)
        
        return fig.to_html(
            full_html=False,
            include_plotlyjs=False,
            config=self._create_plot_config()
        )
    
    def _create_categorical_plots(self) -> List[str]:
        """Creates bar plots for categorical variables"""
        plots = []
        for col in self.data.select_dtypes(include=['object', 'category']).columns:
            if self.data[col].nunique() <= 30:  # Only plot if 30 or fewer unique values
                value_counts = self.data[col].value_counts()
                fig = px.bar(
                    x=value_counts.index,
                    y=value_counts.values,
                    title=f'Distribution of {col}'
                )
                fig.update_layout(**self.default_layout)
                plots.append(fig.to_html(
                    full_html=False,
                    include_plotlyjs=False,
                    config=self._create_plot_config()
                ))
        return plots
    
    def _create_outlier_plots(self) -> List[str]:
        """Creates box plots for outlier detection"""
        plots = []
        numeric_columns = [col for col in self.data.select_dtypes(include=[np.number]).columns 
                          if col not in self.data.select_dtypes(include=['object', 'category']).columns]
        
        for col in numeric_columns:
            fig = px.box(
                self.data,
                y=col,
                title=f'Box Plot of {col}'
            )
            fig.update_layout(**self.default_layout)
            plots.append(fig.to_html(
                full_html=False,
                include_plotlyjs=False,
                config=self._create_plot_config()
            ))
        return plots