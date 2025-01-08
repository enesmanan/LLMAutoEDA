from llm_auto_eda.main import AutoEDA
import pandas as pd

df = pd.read_csv("examples/titanic.csv")

eda = AutoEDA(api_key="your_api_key")

report = eda.analyze(
    df, 
    domain="passenger_data", 
    output_file="example_analysis.html"
)