from jinja2 import Template
from typing import Dict, Optional, Any
import markdown2
from datetime import datetime

class ReportGenerator:
    """HTML report generation class"""
    
    def __init__(self):
        self.css = self._get_css()
        self.template = self._get_template()
    
    def generate_report(self,
                       data_summary: Dict,
                       plots: Dict,
                       statistical_results: Dict,
                       llm_insights: Optional[Dict] = None) -> str:
        """Generates HTML report"""
        
        # Safe markdown to HTML conversion
        if llm_insights:
            try:
                for key, value in llm_insights.items():
                    if isinstance(value, str):
                        llm_insights[key] = markdown2.markdown(value)
                    elif isinstance(value, list):
                        llm_insights[key] = [
                            markdown2.markdown(item) if isinstance(item, str) else ""
                            for item in value
                        ]
            except Exception as e:
                print(f"Markdown conversion error: {str(e)}")
        
        # Generate report
        try:
            report = self.template.render(
                timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                data_summary=data_summary,
                plots=plots,
                statistical_results=statistical_results,
                llm_insights=llm_insights,
                css=self.css
            )
            return report
        except Exception as e:
            print(f"Report generation error: {str(e)}")
            return f"<h1>Error</h1><p>An error occurred while generating the report: {str(e)}</p>"
    
    def _get_css(self) -> str:
        return """
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #34495e;
            --accent-color: #3498db;
            --background-color: #f8f9fa;
            --card-background: #ffffff;
            --header-height: 60px;
        }

        body {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            line-height: 1.6;
            color: var(--primary-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 0;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .main-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            margin: -20px -20px 2rem -20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0));
            z-index: 1;
        }

        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 300;
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .main-header p {
            margin: 0.5rem 0 0;
            font-size: 1.1rem;
            opacity: 0.9;
            text-align: center;
            position: relative;
            z-index: 2;
        }

        .analysis-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .analysis-card {
            background: var(--card-background);
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s, box-shadow 0.2s;
            overflow: hidden;
            height: fit-content;
        }

        .analysis-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .section-header {
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 12px 12px 0 0;
            position: relative;
            overflow: hidden;
        }

        .section-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(45deg, rgba(52, 152, 219, 0.1), rgba(52, 152, 219, 0));
            z-index: 1;
        }

        .section-header h2 {
            margin: 0;
            font-size: 1.2rem;
            font-weight: 500;
            position: relative;
            z-index: 2;
        }

        .plot-section {
            padding: 1rem;
            background: white;
            height: 450px;
            position: relative;
            overflow: visible !important;
        }

        .plot-section > div {
            width: 100% !important;
            height: 100% !important;
        }

        .js-plotly-plot .plotly .modebar {
            top: -40px !important;
            right: 0 !important;
        }

        .js-plotly-plot .plotly .modebar-btn {
            font-size: 12px !important;
            opacity: 0.5 !important;
        }

        .js-plotly-plot .plotly .modebar-btn:hover {
            opacity: 1 !important;
        }

        .insight-section {
            background: linear-gradient(45deg, #f8f9fa, #ffffff);
            padding: 1.5rem;
            border-top: 2px solid var(--accent-color);
        }

        .insight-header {
            font-weight: 600;
            color: var(--primary-color);
            margin-bottom: 0.8rem;
            font-size: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .insight-header::before {
            content: '💡';
            font-size: 1.2rem;
        }

        .insight-text {
            font-size: 0.95rem;
            color: var(--secondary-color);
            line-height: 1.6;
        }

        .overview-section {
            grid-column: 1 / -1;
        }

        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            padding: 1.5rem;
        }

        .metric-card {
            background: white;
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            transition: transform 0.2s;
        }

        .metric-card:hover {
            transform: translateY(-2px);
        }

        .metric-value {
            font-size: 2rem;
            font-weight: 600;
            color: var(--accent-color);
            margin-bottom: 0.5rem;
        }

        .metric-label {
            font-size: 0.9rem;
            color: var(--secondary-color);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .timestamp {
            text-align: center;
            font-size: 0.9rem;
            color: #666;
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }

        @media (max-width: 1200px) {
            .analysis-grid {
                grid-template-columns: 1fr;
            }

            .plot-section {
                height: 400px;
            }
        }

        @media (max-width: 768px) {
            .plot-section {
                min-height: 350px;
            }
        }
        """

    def _get_template(self) -> Template:
        return Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Automated EDA Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                {{ css }}
            </style>
        </head>
        <body>
            <div class="main-header">
                <h1>Automated EDA Report</h1>
                <p>Data Analysis Results</p>
            </div>

            <div class="container">
                <!-- Dataset Summary -->
                <div class="analysis-card overview-section">
                    <div class="section-header">
                        <h2>Dataset Summary</h2>
                    </div>
                    <div class="metric-grid">
                        <div class="metric-card">
                            <div class="metric-value">{{ data_summary.shape[0] }}</div>
                            <div class="metric-label">Number of Rows</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{{ data_summary.shape[1] }}</div>
                            <div class="metric-label">Number of Columns</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{{ data_summary.columns.numeric|length }}</div>
                            <div class="metric-label">Numeric Variables</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">{{ data_summary.columns.categorical|length }}</div>
                            <div class="metric-label">Categorical Variables</div>
                        </div>
                    </div>
                </div>

                {% if llm_insights and llm_insights.overview %}
                <!-- General Assessment -->
                <div class="analysis-card overview-section">
                    <div class="section-header">
                        <h2>General Assessment</h2>
                    </div>
                    <div class="insight-section">
                        <div class="insight-text">
                            {{ llm_insights.overview }}
                        </div>
                    </div>
                </div>
                {% endif %}

                <!-- Main Analysis Grid -->
                <div class="analysis-grid">
                    {% for plot in plots.distributions %}
                    <div class="analysis-card">
                        <div class="section-header">
                            <h2>Distribution of {{ data_summary.columns.numeric[loop.index0] }}</h2>
                        </div>
                        <div class="plot-section">
                            {{ plot }}
                        </div>
                        {% if llm_insights and llm_insights.distribution_insights %}
                        <div class="insight-section">
                            <div class="insight-text">
                                {{ llm_insights.distribution_insights[loop.index0] }}
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}

                    <!-- Correlation Matrix -->
                    {% if plots.correlations %}
                    <div class="analysis-card">
                        <div class="section-header">
                            <h2>Variable Correlations</h2>
                        </div>
                        <div class="plot-section">
                            {{ plots.correlations }}
                        </div>
                        {% if llm_insights and llm_insights.correlation_insights %}
                        <div class="insight-section">
                            <div class="insight-text">
                                {{ llm_insights.correlation_insights }}
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    {% endif %}

                    <!-- Categorical Variable Plots -->
                    {% for plot in plots.categorical %}
                    <div class="analysis-card">
                        <div class="section-header">
                            <h2>Analysis of {{ data_summary.columns.categorical[loop.index0] }}</h2>
                        </div>
                        <div class="plot-section">
                            {{ plot }}
                        </div>
                        {% if llm_insights and llm_insights.categorical_insights %}
                        <div class="insight-section">
                            <div class="insight-text">
                                {{ llm_insights.categorical_insights[loop.index0] }}
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}

                    <!-- Outlier Plots -->
                    {% for plot in plots.outliers %}
                    <div class="analysis-card">
                        <div class="section-header">
                            <h2>Outlier Analysis: {{ data_summary.columns.numeric[loop.index0] }}</h2>
                        </div>
                        <div class="plot-section">
                            {{ plot }}
                        </div>
                        {% if llm_insights and llm_insights.outlier_insights %}
                        <div class="insight-section">
                            <div class="insight-text">
                                {{ llm_insights.outlier_insights[loop.index0] }}
                            </div>
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                </div>

                <div class="timestamp">
                    Report generated at: {{ timestamp }}
                </div>
            </div>
        </body>
        </html>
        """)