# Bitcoin Prices ETL

This project is an ETL (Extract, Transform, Load) pipeline that fetches Bitcoin prices from a Coingecko public API and stores them in a Postgres database on Aiven. The pipeline is automated using Apache Airflow and containerized with Docker.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup and Installation](#setup-and-installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Overview
The Bitcoin Prices ETL project is designed to automate the process of fetching, transforming, and storing Bitcoin price data. The data is fetched from coingecko , transformed for consistency, and loaded into a Postgres database hosted on Aiven.

## Features
- Fetch Bitcoin prices from Coingecko public API
- Data transformation and cleaning
- Load data into a Postgres database on Aiven
- Automated scheduling and monitoring using Apache Airflow
- Containerized deployment with Docker

## Technologies Used
- **Python** for scripting and data transformation
- **Apache Airflow** for automation and scheduling
- **Postgres** on Aiven for data storage
- **Docker** for containerization

## Setup and Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Aminkay95/Bitcoin-prices-ETL.git
    cd Bitcoin-prices-ETL
    ```

2. Build and run the Docker containers:
    ```bash
    docker-compose up --build
    ```

3. Access the Airflow web UI:
    ```
    http://localhost:8080
    ```
   Default credentials:
   - Username: `airflow`
   - Password: `airflow`

4. Configure the Postgres connection details in Airflow:
   - Host: Aiven Postgres endpoint
   - Port: 3306
   - Username, Password, and Database Name as configured in Aiven

## Usage
- The pipeline automatically fetches Bitcoin prices, transforms the data, and loads it into the database.
