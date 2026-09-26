# hcnb-stock-data
Python library for retrieving, calculating and storing stock data.

Install lib

python -m pip install -e .


Run tests (offline, Yahoo and MongoDB are faked)

python -m pytest test

The integration test hits Yahoo and a local MongoDB; enable it with HCNB_INTEGRATION=1.
