# Planetarium API

This project is a Django REST API for managing a planetarium, including user registration, authentication, and management of various planetarium resources such as domes, shows, and reservations.

## Features

- **User Management:**
  - User registration and authentication using JWT.
  - View and update user profile.

- **Planetarium Management:**
  - CRUD operations for planetarium domes.
  - CRUD operations for show themes.
  - CRUD operations for astronomy shows with filtering capabilities.
  - CRUD operations for show sessions with filtering capabilities.
  - Create and list reservations with pagination.

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/planetarium-api.git
   cd planetarium-api

2. **Create a virtual environment and activate it:**
   ```sh
   python3 -m venv env
   source env/bin/activate

3. **Install the dependencies:**
   ```sh
   pip install -r requirements.txt
   
4. **Apply migrations:**
   ```sh
   python manage.py migrate
5. **Create a superuser:**
   ```sh
   python manage.py createsuperuser

6. **Run the development server:**
   ```sh
   python manage.py runserver

## API Endpoints

### User Endpoints

- **Register a new user:**
  - `POST /api/user/register/`

- **Obtain JWT token:**
  - `POST /api/user/token/`

- **Refresh JWT token:**
  - `POST /api/user/token/refresh/`

- **Verify JWT token:**
  - `POST /api/user/token/verify/`

- **Manage user profile:**
  - `GET /api/user/me/`
  - `PATCH /api/user/me/`

### Planetarium Endpoints

- **Planetarium Domes:**
  - `GET /api/planetarium/planetarium_domes/`
  - `POST /api/planetarium/planetarium_domes/`

- **Show Themes:**
  - `GET /api/planetarium/show_themes/`
  - `POST /api/planetarium/show_themes/`

- **Astronomy Shows:**
  - `GET /api/planetarium/astronomy_shows/`
  - `POST /api/planetarium/astronomy_shows/`
  - `GET /api/planetarium/astronomy_shows/{id}/`

- **Show Sessions:**
  - `GET /api/planetarium/show_sessions/`
  - `POST /api/planetarium/show_sessions/`
  - `GET /api/planetarium/show_sessions/{id}/`

- **Reservations:**
  - `GET /api/planetarium/reservations/`
  - `POST /api/planetarium/reservations/`

## API Documentation

Swagger and Redoc documentation are available for exploring the API endpoints.

- **Swagger UI:** `/api/doc/swagger/`
- **Redoc UI:** `/api/doc/redoc/`

## Authentication

This project uses JWT for authentication. Include the token in the `Authorization` header as follows:
   ```http
   Authorization: Bearer <your-token>
   ```
## License 

This project is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/MIT) file for details.

## Contact

If you have any questions or suggestions, feel free to contact me at [dimon1991@gmail.com](mailto:dimon1991@gmail.com).

