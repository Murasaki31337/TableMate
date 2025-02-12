# TableMate

**TableMate** is a web application designed to streamline the process of reserving tables at various restaurants. Users can browse available restaurants, view table options, and make reservations seamlessly.

## Features

- **Restaurant Browsing**: Explore a list of available restaurants.
- **Table Reservations**: Select and reserve tables based on availability.
- **User Authentication**: Secure login and registration for users.
- **Profile Management**: Users can view and manage their reservations.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python**: Version 3.8 or higher.
- **MongoDB**: Ensure MongoDB is installed and running on your system.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Murasaki31337/TableMate.git
   cd TableMate
   ```

2. **Set Up Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Ensure MongoDB is running on its default port (`27017`). If MongoDB is running on a different port or requires authentication, update the connection settings in the application accordingly.

## Running the Application

To start the FastAPI application:

```bash
uvicorn tablemate_api.main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

## Project Structure

- `tablemate_api/`: Contains the FastAPI application code.
- `static/` and `templates/`: Directories for static files and HTML templates.

## Contributing

We welcome contributions! Please fork the repository and submit a pull request with your changes. Ensure that your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
