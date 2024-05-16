# Cafe API
A Flask based REST API serving detailed information about cafes within London.

### Methods

- `GET` - Retrieve information about all/random/specific cafe.
- `POST` - Add new cafe details to the database.
- `PATCH` - Update coffee price for a specific cafe.
- `DELETE` - Delete certain cafe details by using secret API key.

## Prerequisites

- Python 3.11 and up
- Poetry to use `poetry.lock`
- SQLite using SQLAlchemy

# Setup

- Clone the project files from the repository into your local device from the terminal.

  ```bash
  git clone https://github.com/SourasishBasu/Cafe-REST-API.git
  cd Cafe-Rest-API
  ```

- Initialize `venv` and install necessary libraries using `Poetry` or `pip`.

  ```bash
  python -m venv venv
  ./venv/Scripts/activate
  pip install -r requirements.txt
  # OR
  poetry install
  ```

- Run the app. Visit http://localhost:5000/ in your preferred browser to use various routes.
  
  ```bash
  python app.py
  ```

> [!TIP]
> Check out the API docs and try sending requests to the routes in [Postman](https://documenter.getpostman.com/view/32019277/2sA3JRafGo).
