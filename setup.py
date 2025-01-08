from setuptools import setup, find_packages

setup(
    name="llm-auto-eda",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'plotly',
        'jinja2',
        'openai',
        'ipython',
        'markdown2',
        'scipy',
        'pathlib'
    ],
    author="Enes Fehmi Manan",
    author_email="enesmanan768@gmail.com",
    description="An intelligent automated exploratory data analysis tool powered by Large Language Models, providing in-depth insights and visualizations for your datasets",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/enesmanan/LLMAutoEDA",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)