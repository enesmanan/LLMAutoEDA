from openai import OpenAI
import json
from typing import Dict, Optional, Any
from .analyzer import AnalysisResult

class LLMAnalyzer:
    def __init__(self, api_key: Optional[str]):
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    def generate_insights(self, 
                         data_summary: Dict,
                         analysis_result: AnalysisResult,
                         statistical_results: Dict,
                         domain: Optional[str] = None) -> Dict[str, Any]:
        if not self.client:
            return {}

        try:
            insights = {
                'overview': self._get_completion(self._create_overview_prompt(data_summary, statistical_results, domain)),
                'distribution_insights': [],
                'correlation_insights': self._get_completion(self._create_correlations_prompt(analysis_result, domain)),
                'categorical_insights': [],
                'outlier_insights': []
            }
            
            try:
                for col in data_summary['columns']['numeric']:
                    prompt = self._create_distribution_prompt(col, statistical_results, domain)
                    insight = self._get_completion(prompt)
                    insights['distribution_insights'].append(insight)
                
                for col in data_summary['columns'].get('categorical', []):
                    prompt = self._create_categorical_prompt(col, statistical_results, domain)
                    insight = self._get_completion(prompt)
                    insights['categorical_insights'].append(insight)
                
                for col in data_summary['columns']['numeric']:
                    prompt = self._create_outlier_prompt(col, analysis_result, domain)
                    insight = self._get_completion(prompt)
                    insights['outlier_insights'].append(insight)
                    
            except Exception as e:
                print(f"Error generating insights: {str(e)}")
            
            return insights
            
        except Exception as e:
            print(f"Error during LLM analysis: {str(e)}")
            return {}
    
    def _get_completion(self, prompt: str) -> str:
        """Get response from OpenAI API"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an experienced Senior Data Scientist. "
                                               "Keep analyses concise and minimize technical jargon. "
                                               "Provide responses in markdown format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            if hasattr(response.choices[0].message, 'content'):
                return str(response.choices[0].message.content)
            return "Analysis result not found."
            
        except Exception as e:
            print(f"LLM API error: {str(e)}")
            return "Could not generate analysis."

    def _create_overview_prompt(self, data_summary: Dict, statistical_results: Dict, domain: str) -> str:
        return f"""
        Dataset summary:
        - Rows: {data_summary['shape'][0]}
        - Columns: {data_summary['shape'][1]}
        - Numeric variables: {', '.join(data_summary['columns']['numeric'])}
        - Categorical variables: {', '.join(data_summary['columns'].get('categorical', []))}
        {'- Domain: ' + domain if domain else ''}

        Provide a brief overall assessment of this dataset in markdown format.
        """

    def _create_distributions_prompt(self, statistical_results: Dict, domain: Optional[str] = None) -> str:
        return f"""
        Analyze the distributions of numerical variables in the dataset.
        
        Statistical results:
        {json.dumps(statistical_results, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please:
        1. Explain the distribution shape of each variable
        2. Highlight important statistics
        3. Point out interesting patterns if any
        4. Provide domain-specific insights
        
        Provide response in markdown format.
        """

    def _create_correlations_prompt(self, analysis_result: AnalysisResult, domain: Optional[str] = None) -> str:
        return f"""
        Analyze correlations between variables.
        
        Correlation matrix:
        {json.dumps(analysis_result.correlations, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please provide in markdown format:
        1. Highlight strongest relationships
        2. Note interesting or unexpected relationships
        3. Explain important correlations in domain context
        """

    def _create_stats_prompt(self, statistical_results: Dict, domain: Optional[str] = None) -> str:
        return f"""
        Interpret statistical analysis results.
        
        Results:
        {json.dumps(statistical_results, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please provide in markdown format:
        1. List important statistical findings
        2. Explain variable characteristics
        3. Interpret in domain context
        """

    def _create_outliers_prompt(self, analysis_result: AnalysisResult, domain: Optional[str] = None) -> str:
        return f"""
        Analyze outliers in the dataset.
        
        Analysis:
        {json.dumps(analysis_result.outliers, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please provide in markdown format:
        1. Identify significant outliers
        2. Explain potential causes
        3. Assess impact on analysis
        """

    def _create_distribution_prompt(self, column: str, statistical_results: Dict, domain: Optional[str] = None) -> str:
        """Create prompt for analyzing distribution of a numeric variable"""
        stats = statistical_results.get('descriptive_stats', {}).get(column, {})
        return f"""
        Distribution analysis for '{column}':
        
        Statistics:
        - Mean: {stats.get('mean')}
        - Median: {stats.get('median')}
        - Standard Deviation: {stats.get('std')}
        - Skewness: {stats.get('skewness')}
        - Kurtosis: {stats.get('kurtosis')}
        
        Domain: {domain if domain else 'General'}
        
        Please provide concisely in markdown format:
        1. Describe the distribution shape
        2. Highlight important statistics
        3. Note interesting patterns if any
        4. Interpret in domain context
        """

    def _create_categorical_prompt(self, column: str, statistical_results: Dict, domain: Optional[str] = None) -> str:
        """Create prompt for analyzing a categorical variable"""
        value_counts = statistical_results.get('categorical_stats', {}).get(column, {})
        return f"""
        Analysis for categorical variable '{column}':
        
        Value distribution:
        {json.dumps(value_counts, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please provide concisely in markdown format:
        1. Interpret category distribution
        2. Highlight key categories
        3. Note any imbalances
        4. Explain domain relevance
        """

    def _create_outlier_prompt(self, column: str, analysis_result: AnalysisResult, domain: Optional[str] = None) -> str:
        """Create prompt for analyzing outliers in a variable"""
        outliers = analysis_result.outliers.get(column, {})
        return f"""
        Outlier analysis for '{column}':
        
        Outlier information:
        {json.dumps(outliers, indent=2)}
        
        Domain: {domain if domain else 'General'}
        
        Please provide concisely in markdown format:
        1. Explain presence and significance of outliers
        2. Note potential causes
        3. Assess impact on analysis
        4. Interpret in domain context
        """