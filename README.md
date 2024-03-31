# TaskGuardian Backend

TaskGuardian is a backend service that manages tasks for users. It provides functionalities to create, update, delete, and retrieve tasks. Users can be assigned tasks, and administrators can manage user profiles and tasks.

## Features

- **Task Management**: Create, update, delete, and retrieve tasks.
- **User Management**: Administrators can manage user profiles, including updating user information.
- **Role-based Access Control**: Different levels of access for users,managers and administrators.
- **RESTful API**: API endpoints for seamless integration with frontend applications.

## Technologies Used

- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
- **MongoDB**: MongoDB is a document-oriented NoSQL database used for storing task and user data.
- **Pydantic**: Pydantic is a data validation and settings management using Python type annotations.


## API Documentation

For detailed information on available API endpoints and usage, refer to the [API Documentation](docs/API DOCUMENTATION.md).

## Configuration

Configuration settings such as database connection string, server port, and logging options can be modified in the `config.py` file.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.
