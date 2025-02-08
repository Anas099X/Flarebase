# Flarebase Documentation

Flarebase is a lightweight Backend-as-a-Service (BaaS) solution built with Python and powered by the FastHTML Framework. It is designed to offer a simple user interface for managing your database with REST APIs for both tables and records.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Tables API](#tables-api)
  - [Records API](#records-api)
- [User Interface](#user-interface)
- [Contributing](#contributing)
- [Additional Documentation](#additional-documentation)

---

## Overview

Flarebase provides:
- A simple UI for database management.
- REST APIs that support creating, updating, and deleting tables and records.
- A flexible backend powered by [FastHTML](main.py) and [TinyDB](main.py).

---

## Features

- **Simple UI:** Easily navigate tables, view records, and perform CRUD operations.
- **Fast Setup:** Minimal configuration is required.
- **Extensible:** Built with Python; easily extend functionality.
- **RESTful Endpoints:** Interact with your database programmatically.

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `pip` package manager

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Anas099X/FlareBase.git
   cd flarebase
   ```
2. **Install Required Modules**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Application**
   ```bash
   python main.py
   ```
4. **Access the UI**

   Open your browser and navigate to [http://localhost:5001](http://localhost:5001).

For more details, refer to the [README.md](README.md).

---

## Project Structure

```
├── __pycache__/
├── .gitignore
├── .sesskey
├── docs/
│   ├── records.md
│   └── tables.md
├── flarebase.json
├── main.py
├── README.md
├── requirements.txt
├── routes/
│   ├── __pycache__/
│   └── REST.py
└── test.py
```

- **main.py:** Application setup, UI routes, and helper functions.
- **routes/REST.py:** REST API endpoints for tables and records.
- **docs/records.md:** Documentation related to records.
- **docs/tables.md:** Documentation related to tables.

---

## API Endpoints

### Tables API

- **Get All Tables**
  
  Endpoint: `GET /api/tables`
  
  Description: Returns a JSON list of all table names.
  
- **Get Table Content**
  
  Endpoint: `GET /api/tables/{table}`
  
  Description: Returns all documents (records) from the specified table.
  
- **Create Table**
  
  Endpoint: `POST /api/tables/create?name=table_name&fields=field1,field2,...`
  
  Description: Creates a new table with the specified name and fields.
  
- **Delete Table**
  
  Endpoint: `DELETE /api/tables/{table}`
  
  Description: Drops the specified table from the database.

- **Search Table**
  
  Endpoint: `GET /api/tables/search/{table}/{field}/{input}`
  
  Description: Searches for records in the specified table where the field matches the input.

For more details, you can review the implementation in [routes/REST.py](routes/REST.py).

### Records API

- **Create Record**
  
  Endpoint: `POST /api/record/create?table={table_name}&record={record_data}`
  
  Description: Inserts a new record into the specified table.
  
- **Delete Record**
  
  Endpoint: `DELETE /api/record/delete?table={table_name}&record-id={id}`
  
  Description: Removes a single record identified by its document ID.

See the record documentation in [docs/records.md](docs/records.md) and the REST implementation in [routes/REST.py](routes/REST.py).

---

## User Interface

The web interface is served via the root route (`/`) from [main.py](main.py). It provides:
- A dashboard listing all tables as clickable cards.
- A dynamic drawer for adding new tables and records.
- Interactive elements (using HTMX) to perform actions like updating or deleting records.

The UI also includes additional endpoints such as `/view_table/{selected_table}` to view and manage records in a specific table.

---

## Contributing

If you'd like to contribute:
1. Fork the repository.
2. Create a new branch (e.g., `git checkout -b feature/YourFeatureName`).
3. Commit your changes.
4. Push to your branch.
5. Open a pull request.

Follow guidelines in the [README.md](README.md).

---

## Additional Documentation

- **Records Documentation:** [docs/records.md](docs/records.md)
- **Tables Documentation:** [docs/tables.md](docs/tables.md)

---

Happy coding with Flarebase!
