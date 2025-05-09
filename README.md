# datapipe-quickstart

`datapipe-quickstart` is a sample Dagster project demonstrating a data pipeline for ingesting, processing, and analyzing sales data. It utilizes DuckDB as its local database.

## Overview

This project showcases how to build a data pipeline with Dagster, including:
- Defining assets for data ingestion, transformation, and analysis.
- Using partitions for incremental data processing.
- Setting up schedules for regular pipeline runs.
- Implementing sensors to trigger jobs based on external events (e.g., new request files).
- Performing data quality checks.

## Features

- **Data Ingestion**: Loads data from CSV files for products, sales representatives, and sales transactions.
- **Data Transformation**: Joins the ingested data to create a unified view.
- **Data Analysis**:
    - Calculates monthly sales performance.
    - Calculates product performance by category.
- **Ad-hoc Reporting**: Allows users to submit ad-hoc data requests via JSON files.
- **Scheduled Updates**: A weekly schedule keeps the core data up-to-date.
- **Data Quality**: Includes an asset check to identify missing dimensions in the joined data.
- **Local Data Warehouse**: Uses DuckDB for storing and querying data.

## Project Structure

```
datapipe-quickstart/
├── data/                     # Input CSV files, DuckDB database, and ad-hoc request files
│   ├── products.csv
│   ├── sales_data.csv
│   ├── sales_reps.csv
│   ├── mydb.duckdb           # DuckDB database file (created on first run)
│   └── requests/             # Directory for ad-hoc request JSON files
│       └── sample_request/
│           └── request.json  # Example ad-hoc request
├── datapipe_quickstart/      # Python package for the Dagster pipeline
│   ├── __init__.py
│   ├── assets.py             # Defines data assets and transformations
│   ├── definitions.py        # Main Dagster definitions (assets, schedules, sensors, resources)
│   ├── partitions.py         # Defines partitions used by assets
│   ├── schedules.py          # Defines pipeline schedules
│   └── sensors.py            # Defines sensors for triggering jobs
├── .gitignore
├── LICENSE                   # Apache License 2.0
├── py.typed                  # Marker for PEP 561 type information
├── pyproject.toml            # Build system and Dagster project configuration
├── requirements.txt          # Python dependencies
├── setup.cfg                 # Package metadata
└── setup.py                  # Setup script for the Python package
```

## Prerequisites

- Python 3.12
- pip

## Setup and Installation

1.  **Clone the repository or ensure you are in the project's root directory.**
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    pip install -e .  # Installs the project in editable mode
    ```
    The `requirements.txt` includes:
    - `dagster`: The core Dagster library.
    - `dagster-duckdb`: Integration for DuckDB.
    - `dagster-webserver`: For running Dagit, the Dagster UI.
    The `setup.py` also lists `dagster-cloud` and `pytest` (for development).

### Alternative Setup: Using Docker Compose

This method uses Docker Compose to set up and run the Dagster instance along with its dependencies (like PostgreSQL) in containers.

1.  **Ensure Docker and Docker Compose are installed.**
    Follow the official installation guides for [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/).
2.  **Clone the repository or ensure you are in the project's root directory.**
3.  **Copy the Docker Compose template file:**
    In the `datapipe-quickstart` directory, copy the template to create your local Docker Compose configuration:
    ```bash
    cp docker-compose.yml.tmpl docker-compose.yml
    ```
    You can review [`docker-compose.yml`](datapipe-quickstart/docker-compose.yml:0) and make any modifications if needed.
4.  **Build and run the services:**
    ```bash
    docker compose up --build -d
    ```
    This command will build the Docker images (if they don't exist) and start all the services defined in the `docker-compose.yml` file in detached mode (`-d`).
5.  **Access Dagit UI:**
    Once the services are up and running, the Dagit UI will be accessible at `http://localhost:3000`.
## Running the Pipeline

1.  **Start Dagit (Dagster UI):**
    From the `datapipe-quickstart` directory, run:
    ```bash
    dagster dev
    ```
    This will start the Dagit webserver, typically available at `http://localhost:3000`.

2.  **Materialize Assets:**
    In Dagit, you can:
    - View the asset graph.
    - Manually materialize assets.
    - Observe scheduled runs and sensor activity.

    The first time you materialize assets that interact with DuckDB (e.g., `products`, `sales_data`), the `data/mydb.duckdb` file will be created.

## Data

### Input Data

The pipeline ingests data from the following CSV files located in the `data/` directory:
-   [`products.csv`](datapipe-quickstart/data/products.csv:0): Contains product information (product_id, product_name, category, price).
-   [`sales_reps.csv`](datapipe-quickstart/data/sales_reps.csv:0): Contains sales representative information (rep_id, rep_name, department, hire_date).
-   [`sales_data.csv`](datapipe-quickstart/data/sales_data.csv:0): Contains sales transaction records (order_id, date, product_id, rep_id, customer_name, quantity, dollar_amount).

### Database

The project uses DuckDB. The database file is stored at [`data/mydb.duckdb`](datapipe-quickstart/data/mydb.duckdb:0). Tables are created and populated by the assets.

## Key Components

### Assets

Defined in [`datapipe_quickstart/assets.py`](datapipe-quickstart/datapipe_quickstart/assets.py:0):
-   `products`: Loads product data from `products.csv` into DuckDB.
-   `sales_reps`: Loads sales representative data from `sales_reps.csv` into DuckDB.
-   `sales_data`: Loads sales transaction data from `sales_data.csv` into DuckDB.
-   `joined_data`: Creates a view in DuckDB by joining `sales_data`, `sales_reps`, and `products`.
-   `missing_dimension_check`: An asset check on `joined_data` to ensure `rep_name` and `product_name` are not null.
-   `monthly_sales_performance`: Calculates aggregated sales performance by month and representative. Partitioned by month.
-   `product_performance`: Calculates aggregated sales performance by product category. Partitioned by product category.
-   `adhoc_request`: Processes ad-hoc data requests based on configurations provided via JSON files.

### Schedules

Defined in [`datapipe_quickstart/schedules.py`](datapipe-quickstart/datapipe_quickstart/schedules.py:0):
-   `weekly_update_schedule` ([`analysis_update_job`](datapipe-quickstart/datapipe_quickstart/schedules.py:4)): Runs every Monday at midnight to materialize assets upstream of `joined_data`, effectively refreshing the core data tables.

### Sensors

Defined in [`datapipe_quickstart/sensors.py`](datapipe-quickstart/datapipe_quickstart/sensors.py:0):
-   `adhoc_request_sensor`: Monitors the `data/requests/` directory for new or modified `.json` files. When a change is detected, it triggers the `adhoc_request_job` with the configuration from the JSON file.

### Partitions

Defined in [`datapipe_quickstart/partitions.py`](datapipe-quickstart/datapipe_quickstart/partitions.py:0):
-   `monthly_partition`: A monthly partition definition starting from "2024-01-01", used by the `monthly_sales_performance` asset.
-   `product_category_partition`: A static partition definition for product categories (`Electronics`, `Books`, `Home and Garden`, `Clothing`), used by the `product_performance` asset.

## Ad-hoc Requests

To make an ad-hoc data request:
1.  Create a JSON file in the `datapipe-quickstart/data/requests/` directory.
2.  The JSON file should contain the configuration for the `adhoc_request` asset. See [`datapipe_quickstart/assets.py`](datapipe-quickstart/datapipe_quickstart/assets.py:247) for the `AdhocRequestConfig` structure:
    ```json
    {
        "department": "Electronics",
        "product": "Laptop",
        "start_date": "2024-03-01",
        "end_date": "2024-04-01"
    }
    ```
    An example is provided in [`data/sample_request/request.json`](datapipe-quickstart/data/sample_request/request.json:0).
3.  The `adhoc_request_sensor` will detect the new/modified file and trigger a run of the `adhoc_request` asset with the provided configuration. The results (a preview of the queried data) will be available in the Dagit UI for that run.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](datapipe-quickstart/LICENSE:0) file for details.