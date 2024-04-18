# Library Management System

The Library Management System is a web-based application built using Flask, SQLAlchemy, and Flask-WTF. It provides a platform for managing library resources, user accounts, book requests, and access control.

## Features

- **User Authentication:** Users can register and log in to the system with different roles (user, librarian).
- **Book Management:** Librarians can add new books, categorize them into sections, and view detailed book information.
- **User Interaction:** Users can search for books, provide feedback, and request access to specific titles.
- **Request Management:** Librarians can approve or reject access requests from users.
- **Access Control:** Once approved, users can access requested books, and librarians can revoke access if needed.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/library-management-system.git
   ```

2. Navigate to the project directory:

   ```bash
   cd library-management-system
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the project root directory.
   - Define the following variables in the `.env` file:
     ```
     SQLALCHEMY_DATABASE_URI=sqlite:///test.db
     SECRET_KEY=your_secret_key
     SQLALCHEMY_TRACK_MODIFICATIONS=False
     ```

5. Initialize the database:

   ```bash
   python model.py
   ```

6. Run the application:

   ```bash
   python app.py
   ```

   The application will be accessible at `http://localhost:5000`.

## Usage

- Register an account to access the system.
- Use the provided login credentials to log in.
- As a librarian, you can add new books, manage requests, and view access logs.
- As a user, you can search for books, provide feedback, and request access to titles.

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

