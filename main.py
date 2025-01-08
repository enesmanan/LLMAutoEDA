from typing import Optional, Union, Dict, Any
import pandas as pd
from pathlib import Path
from IPython.display import HTML, display

from .core.data_loader import DataLoader
from .core.analyzer import DataAnalyzer
from .core.visualizer import DataVisualizer
from .core.llm_analyzer import LLMAnalyzer
from .core.report_generator import ReportGenerator
from .core.statistical_analyzer import StatisticalAnalyzer

class AutoEDA:
    """
    Automated Exploratory Data Analysis class.
    
    Features:
    - Basic data analysis
    - Statistical analysis
    - Data visualization
    - LLM-based insights (optional)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Args:
            api_key: OpenAI API key (optional)
        """
        self.api_key = api_key
        self.data_loader = DataLoader()
        self.report_generator = ReportGenerator()
        self.llm_analyzer = LLMAnalyzer(api_key) if api_key else None
        
    def analyze(self, 
                data_source: Union[str, pd.DataFrame],
                domain: Optional[str] = None,
                output_file: Optional[str] = None) -> str:
        """
        Performs comprehensive analysis on the dataset.
        
        Args:
            data_source: DataFrame or file path
            domain: Dataset domain (e.g., "finance")
            output_file: Path to save the report
            
        Returns:
            str: Analysis report in HTML format
        """
        try:
            # 1. Load Data
            print("Loading data...")
            data = self.data_loader.load_data(data_source)
            data_summary = self.data_loader.data_summary
            
            # 2. Basic Analysis
            print("Analyzing data...")
            analyzer = DataAnalyzer(data)
            analysis_result = analyzer.analyze()
            
            # 3. Statistical Analysis
            print("Performing statistical analysis...")
            statistical_analyzer = StatisticalAnalyzer(data)
            statistical_results = statistical_analyzer.to_dict()
            
            # 4. Visualizations
            print("Creating visualizations...")
            visualizer = DataVisualizer(data, analysis_result)
            plots = visualizer.generate_all_plots()
            
            # 5. LLM Analysis (optional)
            llm_insights = None
            if self.llm_analyzer:
                print("Generating LLM insights...")
                try:
                    llm_insights = self.llm_analyzer.generate_insights(
                        data_summary=data_summary,
                        analysis_result=analysis_result,
                        statistical_results=statistical_results,
                        domain=domain
                    )
                    if "error" in llm_insights:
                        print(f"Error in LLM analysis: {llm_insights['error']}")
                        llm_insights = None
                except Exception as e:
                    print(f"Error during LLM analysis: {str(e)}")
                    llm_insights = None
            
            # 6. Generate Report
            print("Generating report...")
            report = self.report_generator.generate_report(
                data_summary=data_summary,
                plots=plots,
                statistical_results=statistical_results,
                llm_insights=llm_insights
            )
            
            # 7. Save Report (optional)
            if output_file:
                output_path = Path(output_file)
                output_path.write_text(report, encoding='utf-8')
                print(f"Report saved to: {output_file}")
            
            return report
            
        except Exception as e:
            error_msg = f"Analysis error: {str(e)}"
            print(error_msg)
            return f"<h1>Error</h1><p>{error_msg}</p>"
    
    def analyze_in_notebook(self,
                          data_source: Union[str, pd.DataFrame],
                          domain: Optional[str] = None) -> None:
        """
        Performs analysis and displays results in Jupyter Notebook.
        
        Args:
            data_source: DataFrame or file path
            domain: Dataset domain
        """
        report = self.analyze(data_source, domain)
        display(HTML(report))
    
    def quick_analyze(self,
                     data_source: Union[str, pd.DataFrame],
                     domain: Optional[str] = None) -> Dict[str, Any]:
        """
        Performs quick analysis and returns results as dictionary.
        
        Args:
            data_source: DataFrame or file path
            domain: Dataset domain
            
        Returns:
            Dict: Analysis results
        """
        try:
            # Load and analyze data
            data = self.data_loader.load_data(data_source)
            data_summary = self.data_loader.data_summary
            
            # Statistical analysis
            statistical_analyzer = StatisticalAnalyzer(data)
            stats_results = statistical_analyzer.to_dict()
            
            # Basic analysis
            analyzer = DataAnalyzer(data)
            analysis_result = analyzer.analyze()
            
            return {
                "summary": data_summary,
                "shape": data.shape,
                "dtypes": data.dtypes.to_dict(),
                "missing": data.isnull().sum().to_dict(),
                "statistics": stats_results,
                "correlations": analysis_result.correlations
            }
            
        except Exception as e:
            return {"error": str(e)}

def main():
    """Command line usage main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='AutoEDA Tool')
    parser.add_argument('data_path', help='Path to data file')
    parser.add_argument('--domain', help='Dataset domain', default=None)
    parser.add_argument('--api-key', help='OpenAI API key', default=None)
    parser.add_argument('--output', help='Output file path', 
                       default='auto_eda_report.html')
    
    args = parser.parse_args()
    
    eda = AutoEDA(api_key=args.api_key)
    eda.analyze(args.data_path, domain=args.domain, output_file=args.output)

if __name__ == "__main__":
    main()