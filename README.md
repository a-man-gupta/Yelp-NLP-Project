# Yelp Dataset Database and NLP Application

This repository contains scripts to create and test SQLite databases from Yelp dataset JSON files, as well as a full-stack Yelp NLP application for predicting ratings and generating reviews based on user input.

## Prerequisites

- Python 3.8+
- `virtualenv` package
- Node.js 14+ and npm
- Unzipped `yelp_dataset.tar` file
- SQLite3 (included with Python)

## Setup

1. **Clone the repository**:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment**:

    ```sh
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. **Install Python dependencies**:

    ```sh
    pip install -r requirements.txt
    ```

## Creating Databases

The scripts in the `create-db-scripts` folder create SQLite databases from Yelp dataset JSON files:

- `create_business_db.py`: Creates the business database.
- `create_checkin_db.py`: Creates the checkin database.
- `create_review_db.py`: Creates the review database.
- `create_tip_db.py`: Creates the tip database.
- `create_user_db.py`: Creates the user database.
- `create_business_fts.py`: Creates a full-text search index for the business database.
- `create_user_fts.py`: Creates a full-text search index for the user database.

To run a script, use:

```sh
python create-db-scripts/<script_name>.py
```

Example:

```sh
python create-db-scripts/create_business_db.py
```

## Testing Databases

The scripts in the `test-db-scripts` folder test the created SQLite databases:

- `test_business_db.py`: Tests the business database.
- `test_checkin_db.py`: Tests the checkin database.
- `test_review_db.py`: Tests the review database.
- `test_tip_db.py`: Tests the tip database.
- `test_user_db.py`: Tests the user database.

To run a test script, use:

```sh
python test-db-scripts/<test_script_name>.py
```

Example:

```sh
python test-db-scripts/test_business_db.py
```

## Yelp NLP Application

The repository includes a full-stack Yelp NLP application with three components: a Python inference API, a Node.js backend, and a React frontend.

### 1. Inference API (`inference-api`)

The `inference-api` directory contains `predict_api.py`, which provides APIs for predicting ratings and generating reviews.

**Setup and Run**:

1. Navigate to the directory:

    ```sh
    cd inference-api
    ```

2. Ensure dependencies are installed (already done via `requirements.txt`).

3. Run the FastAPI server:

    ```sh
    uvicorn predict_api:app --host 0.0.0.0 --port 8000
    ```

The API will be available at `http://localhost:8000`.

### 2. Node.js Backend (`backend-yelp-nlp`)

The `backend-yelp-nlp` directory contains a Node.js server that proxies requests to the inference API and serves the frontend.

**Setup and Run**:

1. Navigate to the directory:

    ```sh
    cd backend-yelp-nlp
    ```

2. Initialize and install dependencies:

    ```sh
    npm install
    ```

3. Start the server:

    ```sh
    node index.js
    ```

The backend will typically run on `http://localhost:3000` (check `index.js` for the port).

### 3. React Frontend (`yelp-nlp-ui`)

The `yelp-nlp-ui` directory contains a React application for interacting with the Yelp NLP APIs. It allows users to search for businesses and users, submit review text for rating predictions, and generate reviews based on helpful text.

**Setup and Run**:

1. Navigate to the directory:

    ```sh
    cd yelp-nlp-ui
    ```

2. Install dependencies:

    ```sh
    npm install
    ```

3. Start the development server:

    ```sh
    npm start
    ```

The frontend will run on `http://localhost:3000` (or another port if specified) and open in your default browser.

### Running the Full Application

1. Start the inference API (`uvicorn predict_api:app --host 0.0.0.0 --port 8000`) in one terminal.
2. Start the Node.js backend (`node index.js`) in another terminal.
3. Start the React frontend (`npm start`) in a third terminal.
4. Access the application in your browser (typically `http://localhost:3000`).

The UI allows you to:
- Search for businesses and users.
- Submit review text to predict ratings (Funny, Useful, Cool), displayed as radial charts.
- Submit helpful text to generate a review, displayed as text.

## Requirements

The `requirements.txt` file includes all Python dependencies for the database scripts and inference API. Key dependencies include:

- `fastapi`: For the inference API server.
- `uvicorn`: For running the FastAPI server.
- `pydantic`: For request validation in the API.
- `requests`: For HTTP requests (if used in scripts).
- `sqlite3`: Included with Python for database operations.

Install them using:

```sh
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.