

# ✈️ Airline Company Dashboard

This project is an interactive dashboard for an airline company, integrating a data pipeline orchestrated with Airflow to handle data ingestion, transformation, and visualization.

The data used in this project is available through this [link](https://edu.postgrespro.com/demo-big-en.zip).

## 📋 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Data Source](#2-data-source)
3. [Pipeline Architecture](#3-pipeline-architecture)
4. [Technologies Used](#4-technologies-used)
5. [How to Run the Project](#5-how-to-run-the-project)
6. [Makefile Commands](#6-makefile-commands)

---

## 1. 📊 Project Overview

The project consists of two main components:

1. **Data Pipeline**: Managed by Airflow, this pipeline extracts data from a PostgreSQL database, transforms it using DuckDB, and loads it into MongoDB Atlas for efficient storage.
2. **Streamlit Dashboard**: This application retrieves the data stored in MongoDB Atlas, processes it, and displays it in an interactive dashboard for real-time visualization.

## 2. 🗄️ Data Source

The data used for this project is sourced from a PostgreSQL database and can be downloaded from the following [link](https://edu.postgrespro.com/demo-big-en.zip). The data includes information about flights, passengers, and various operational aspects of the airline.

## 3. 🛠️ Pipeline Architecture

The data pipeline follows these steps:

1. **Data Extraction (PostgreSQL)**: Airflow orchestrates the extraction of data from the PostgreSQL database.
2. **Transformation (DuckDB)**: DuckDB is used to perform fast and efficient data transformations.
3. **Loading (MongoDB Atlas)**: The transformed data is loaded into MongoDB Atlas, ready for visualization.
4. **Visualization (Streamlit)**: The Streamlit app connects to MongoDB, retrieves the data, processes it, and displays it in an interactive dashboard.

## 4. 💻 Technologies Used

The following technologies are utilized in this project:

- **Airflow**: A workflow orchestrator used to automate the ETL pipeline.
- **DuckDB**: An OLAP engine used for efficient data processing.
- **PostgreSQL**: A relational database, the source of the data.
- **MongoDB Atlas**: A NoSQL database for storing the processed data.
- **Streamlit**: A web interface to display the data in an interactive dashboard.
- **Docker & Docker Compose**: Used to containerize the services and manage orchestration.

## 5. 🚀 How to Run the Project

### Prerequisites

Make sure you have the following tools installed on your machine:

- **Docker**
- **Docker Compose**
- **Make**

### Installation Steps

1. Clone the GitHub repository:
    ```bash
    git clone https://github.com/abrahamkoloboe27/Airflow-Pipeline-Dashboard-Compagnie-Aerienne
    cd Airflow-Pipeline-Dashboard-Compagnie-Aerienne
    ```

2. Configure Airflow connections:
    - After starting the services, navigate to the Airflow web interface.
    - Go to **Admin > Connections** in Airflow.
    - Add connections for PostgreSQL and MongoDB Atlas with the correct URI, login, and password.

### Launching the Services

- **Build Docker Images**:
    ```bash
    make build
    ```
    This command builds the necessary Docker images for the services.

- **Start the Services**:
    ```bash
    make up
    ```
    This command starts Airflow, PostgreSQL, MongoDB Atlas, and the Streamlit app.

- **Build and Start Services Simultaneously**:
    ```bash
    make up-build
    ```
    This command rebuilds the services if necessary and then starts them.

- **Stop the Services**:
    ```bash
    make down
    ```
    This command stops all running services.

## 6. 📜 Makefile Commands

The Makefile included in the project allows you to execute the following commands:

- **`make build`**: Builds the Docker images required for the project.
- **`make up`**: Starts the containerized services (Airflow, PostgreSQL, MongoDB, Streamlit).
- **`make up-build`**: Rebuilds the Docker images and starts the services.
- **`make down`**: Stops all the running services.

---

## 🎯 Conclusion

This project provides a comprehensive solution for data management and visualization for an airline company. It integrates a complete data pipeline that automates extraction, transformation, and loading (ETL) of data, while Streamlit provides an interactive environment for exploring and analyzing the data in real time.

---

