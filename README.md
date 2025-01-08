# LLM Auto EDA

An intelligent automated exploratory data analysis tool powered by Large Language Models, providing in-depth insights and visualizations for your datasets.

## Installation

```bash
pip install llm-auto-eda
```



## Quick Start

```python
from llm_auto_eda import AutoEDA

# Initialize with your OpenAI API key (optional)
eda = AutoEDA(api_key='your-openai-api-key')

# Load and analyze your data
analysis = eda.analyze('your_data.csv')

# Generate interactive HTML report
analysis.save_report('analysis_report.html')
```

## Example Usage with Custom Parameters

```python
# Load data with specific configuration
analysis = eda.analyze(
    data_source='your_data.csv',
    domain='finance',  # Provide domain context for better insights
    exclude_columns=['id', 'timestamp']  # Exclude specific columns
)

# Access specific components
print(analysis.data_summary)  # Get data summary
print(analysis.correlations)  # Get correlation matrix
print(analysis.insights)      # Get LLM-generated insights
```


