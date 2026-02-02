# Data Engineering Zoomcamp - Module 2 Homework

## NYC Taxi Data Pipeline with Kestra

This repository contains the solution for Module 2 homework assignment, which focuses on workflow orchestration using Kestra to ingest NYC taxi trip data.

## Project Overview

The project implements ETL pipelines using Kestra to:

- Download NYC Yellow and Green taxi trip data (2019-2021)
- Extract and decompress gzipped CSV files
- Load data into PostgreSQL database
- Support both manual and scheduled execution
- Enable backfill functionality for historical data

## Repository Structure

```
.
├── README.md                          # This file
├── docker-compose.yaml                 # Docker setup for Kestra, PostgreSQL, and pgAdmin
├── pyproject.toml                      # Python dependencies
├── flows/                              # Kestra workflow definitions
│   ├── taxi_ingest.yaml               # Main ingestion flow with inputs
│   ├── taxi_ingest_scheduled.yaml     # Scheduled flow with backfill support
│   └── taxi_ingest_batch.yaml         # Batch processing with ForEach loops
└── scripts/                            # Python analysis scripts
    ├── analyze_file.py                # Analyze individual or yearly data
    └── answer_homework.py             # Script to answer all homework questions
```

## Setup Instructions

### Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for running analysis scripts)
- `uv` package manager (optional, for dependency management)

### Starting the Environment

1. Start all services:

```bash
docker-compose up -d
```

2. Access the services:
   - **Kestra UI**: http://localhost:8080 (admin@kestra.io / Admin1234!)
   - **pgAdmin**: http://localhost:8085 (admin@admin.com / root)
   - **PostgreSQL**: localhost:5432 (root / root)

3. Install Python dependencies:

```bash
uv sync
```

### Deploying Kestra Flows

1. Open Kestra UI at http://localhost:8080
2. Create a new namespace: `de.zoomcamp`
3. Upload the flow files from the `flows/` directory
4. Alternatively, copy the YAML content directly into the Kestra editor

## Homework Questions & Answers

### Question 1: Yellow Taxi December 2020 - Uncompressed File Size

**Question:** Within the execution for Yellow Taxi data for the year 2020 and month 12: what is the uncompressed file size (i.e., the output file `yellow_tripdata_2020-12.csv` of the extract task)?

**Answer: A. 128.3 MiB**

_Method:_ Downloaded and analyzed the file using the provided scripts.

---

### Question 2: Variable Rendering

**Question:** What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?

**Answer: B. green_tripdata_2020-04.csv**

_Explanation:_ In the Kestra flow, the variable is defined as:

```yaml
variables:
  file: "{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv"
```

When rendered with the given inputs:

- `{{inputs.taxi}}` → `green`
- `{{inputs.year}}` → `2020`
- `{{inputs.month}}` → `04`

Result: `green_tripdata_2020-04.csv`

---

### Question 3: Yellow Taxi 2020 - Total Row Count

**Question:** How many rows are there for the Yellow Taxi data for all CSV files in the year 2020?

**Answer: B. 24,648,499**

_Method:_ Downloaded all 12 months of Yellow taxi data for 2020 and counted total rows.

---

### Question 4: Green Taxi 2020 - Total Row Count

**Question:** How many rows are there for the Green Taxi data for all CSV files in the year 2020?

**Answer: C. 1,734,051**

_Method:_ Downloaded all 12 months of Green taxi data for 2020 and counted total rows.

---

### Question 5: Yellow Taxi March 2021 - Row Count

**Question:** How many rows are there for the Yellow Taxi data for the March 2021 CSV file?

**Answer: C. 1,925,152**

_Method:_ Downloaded and analyzed the March 2021 Yellow taxi data file.

---

### Question 6: Timezone Configuration

**Question:** How would you configure the timezone to New York in a Schedule trigger?

**Answer: B. Add a timezone property set to America/New_York in the Schedule trigger configuration**

_Explanation:_ Kestra uses the IANA Time Zone Database format. The correct configuration is:

```yaml
triggers:
  - id: monthly_schedule
    type: io.kestra.plugin.core.trigger.Schedule
    cron: "0 0 1 * *"
    timezone: America/New_York
```

## Running the Analysis Scripts

### Analyze Individual Files

```bash
# Analyze a specific month
uv run scripts/analyze_file.py yellow 2020 12

# Analyze all months in a year
uv run scripts/analyze_file.py yellow 2020 all
uv run scripts/analyze_file.py green 2020 all
```

### Run All Homework Questions

```bash
uv run scripts/answer_homework.py
```

This script will:

1. Answer conceptual questions (2 and 6)
2. Download required data files
3. Analyze file sizes and row counts
4. Display all answers with explanations

## Kestra Flows Explained

### 1. `taxi_ingest.yaml` - Main Ingestion Flow

This flow accepts three inputs:

- `taxi`: Type of taxi (yellow/green)
- `year`: Year of data
- `month`: Month of data (01-12)

Tasks:

1. **extract**: Download compressed CSV file from GitHub
2. **uncompress**: Decompress the gzip file
3. **load_to_postgres**: Load data into PostgreSQL
4. **stats**: Display file statistics

### 2. `taxi_ingest_scheduled.yaml` - Scheduled Flow

Features:

- Runs monthly on the 1st at midnight (NYC time)
- Supports backfill for historical data
- Automatically determines year-month from trigger date

To backfill 2021 data:

1. Go to the flow in Kestra UI
2. Click on "Backfill"
3. Set date range: 2021-01-01 to 2021-07-31
4. Select taxi type input
5. Execute

### 3. `taxi_ingest_batch.yaml` - Batch Processing Flow

Uses nested `ForEach` loops to process multiple combinations:

- Iterates over taxi types (yellow, green)
- Iterates over months (01-07 for 2021)
- Triggers the main flow for each combination

This demonstrates the "Challenge" from the homework to loop over Year-Month and taxi-type combinations using ForEach and Subflow tasks.

## Data Source

NYC Taxi data is sourced from:
https://github.com/DataTalksClub/nyc-tlc-data/releases

- Yellow taxi: `/releases/download/yellow/`
- Green taxi: `/releases/download/green/`

Available data:

- Yellow: 2019-2021 (full years)
- Green: 2019-2021 (full years)

## Database Schema

Data is loaded into two PostgreSQL tables:

- `yellow_taxi_data`: Yellow taxi trips
- `green_taxi_data`: Green taxi trips

Columns are automatically detected from the CSV files and include:

- Pickup/dropoff datetime
- Passenger count
- Trip distance
- Fare amounts
- Payment type
- And more (varies by taxi type)

## Technologies Used

- **Kestra**: Workflow orchestration
- **PostgreSQL**: Data storage
- **pgAdmin**: Database management interface
- **Docker**: Containerization
- **Python**: Data analysis scripts
- **pandas**: Data manipulation
- **SQLAlchemy**: Database ORM

## Notes

- All datetime columns are automatically converted to proper datetime types during loading
- Data is appended to tables (not replaced) to support incremental loading
- The backfill functionality makes it easy to load historical data
- ForEach loops enable parallel or sequential processing of multiple data files

## Author

John O. Emmanuel - Module 2 Homework
Workflow Orchestration with Kestra

## License

This project is for educational purposes as part of the Data Engineering Zoomcamp course.
