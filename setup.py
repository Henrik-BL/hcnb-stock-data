from setuptools import setup, find_packages

setup(
    name="hcnb_stock_data",
    version="1.0.11",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pymongo",
        "requests",
        "pandas",
        "yfinance",
    ],
    python_requires=">=3.9",
)
