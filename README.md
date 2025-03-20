# Yelp Dataset Database Scripts

This repository contains scripts to create and test SQLite databases from Yelp dataset JSON files.

## Prerequisites

- Python 3.x
- `virtualenv` package
- unzip yelp_dataset.tar

## Setup

1. Clone the repository:

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a virtual environment:

    ```sh
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```sh
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```sh
        source venv/bin/activate
        ```

4. Install the required libraries:

    ```sh
    pip install -r requirements.txt
    ```

## Creating Databases

The following scripts are used to create SQLite databases from Yelp dataset JSON files:

- `create_business_db.py`
- `create_checkin_db.py`
- `create_review_db.py`
- `create_tip_db.py`
- `create_user_db.py`

To run a script, use the following command:

```sh
python <script_name>.py
```

For example, to create the business database:

```sh
python create_business_db.py
```

## Testing Databases

The following scripts are used to test the created SQLite databases:

- `test_business_db.py`
- `test_checkin_db.py`
- `test_review_db.py`
- `test_tip_db.py`
- `test_user_db.py`

To run a test script, use the following command:

```sh
python <test_script_name>.py
```

For example, to test the business database:

```sh
python test_business_db.py
```

## License

This project is licensed under the MIT License.