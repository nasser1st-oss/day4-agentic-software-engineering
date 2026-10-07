# Maintenance Mini-App

## Overview
This is a FastAPI application for managing maintenance records of assets. It provides a CRUD API to create, read, update, and delete asset records.

## Requirements
- Python 3.7+
- FastAPI
- Uvicorn
- Pandas

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd maintenance_mini_app
   ```
2. Install the required packages:
   ```bash
   pip install fastapi uvicorn pandas
   ```

## Running the Application
1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```
2. Open your browser and navigate to `http://localhost:8000/docs` to access the API documentation.

## Running Tests
To run the tests, use:
```bash
pytest -q
```

## CSV Data
The application loads initial asset data from `maintenance_assets.csv` at startup. Ensure this file is present in the same directory as `main.py`.