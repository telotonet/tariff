# Cargo Insurance Calculation API

This is a REST API service for calculating insurance costs based on cargo type, declared value, and effective date. The service loads tariff data from a JSON file into a database and calculates the insurance cost for requests using the most recent tariff.

## Features

- **Upload Tariffs**: Uploads tariff data in JSON format to the database.
- **Calculate Insurance**: Calculates the insurance cost based on cargo type, declared value, and date using the most recent tariff data.

## Technologies Used

- **FastAPI**: Web framework for building the API.
- **SQLAlchemy**: ORM for interacting with the database.
- **SQLite**: Database for storing tariff data.
- **Docker**: Containerization for the application and tests.
- **Docker-Compose**: To manage the multi-container setup (for PostgreSQL and the app).

## Endpoints

### 1. `POST /upload_tariffs/`
Uploads tariff data from a JSON file into the database.

**Request body** (multipart/form-data):
- `file`: The JSON file containing tariff data.

**Response**:
- `200 OK`: A success message indicating that the data was uploaded successfully.

### 2. `POST /calculate_insurance/`
Calculates the insurance cost for the provided cargo type, declared value, and date.

**Request body** (application/json):
```json
{
  "cargo_type": "Glass",
  "declared_value": 10000.0,
  "date": "2020-06-01"
}
```

**Response**:
```json
{
  "insurance_cost": 500.0,
  "cargo_type": "Glass",
  "rate": 0.05,
  "date": "2020-06-01"
}
```

**Errors**:
- `404 Not Found`: If no rate is found for the provided cargo type and date.

## Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/telotonet/tariff/
   cd your-repository-directory
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   Ensure PostgreSQL is running and update the `DATABASE_URL` in the `.env` file with the correct credentials.

5. Run database migrations using Alembic:
   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

The API will be available at [http://localhost:8000](http://localhost:8000).

## Docker Setup

### Run the Application

1. Build and start the application using Docker Compose:
   ```bash
   docker-compose up --build app
   ```

2. The FastAPI application will be available at [http://localhost:8000](http://localhost:8000).

### Run Tests

1. To run the tests using Docker Compose, you can build and run the test container:
   ```bash
   docker-compose up --build tests
   ```

2. This will start a separate container for running the tests without the application.

## Configuration

The application uses environment variables for configuration. You can set the following variables in the `.env` file:
- `DATABASE_URL`: The URL for your SQLite database (app/.env).
- `MODE`: Set to `TEST` when running tests (tests/.env).

## Dockerfile Explanation

- The `Dockerfile` defines the application image by setting up the environment, installing dependencies, and configuring the app to run using `uvicorn`.
- The `docker-compose.yml` file manages both the application and the PostgreSQL container, ensuring a seamless environment setup for both development and production.

## Running the Tests

The tests can be run separately from the server using the following command:

```bash
docker-compose up --build tests
```

This will spin up a container, run all the tests defined in the repository, and output the results.

## License

This project is licensed under the MIT License.
