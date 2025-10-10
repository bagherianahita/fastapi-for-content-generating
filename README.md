 A high-performance backend API built with **FastAPI** to manage user accounts, workout sessions, and custom routine planning. The application uses **SQLAlchemy** for efficient, object-relational database interactions.

## ✨ Features

  * **User Management:** Secure user registration and login with strong password hashing (bcrypt).
  * **JWT Authentication:** Token-based authentication (JSON Web Tokens) for securing all protected endpoints.
  * **Data Models:** ORM setup for Users, Workouts, and Routines using SQLAlchemy.
  * **Many-to-Many Relationships:** Connects Workouts and Routines, allowing for flexible program design.
  * **CORS Configuration:** Ready for integration with a frontend client (configured for `http://localhost:3000`).
  * **Clear Dependencies:** All dependencies managed via `requirements.txt`.

## ⚙️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Framework** | **FastAPI** | Modern, fast web framework for building Python APIs. |
| **Database ORM** | **SQLAlchemy** | SQL toolkit and Object-Relational Mapper (ORM) for data persistence. |
| **Database** | **SQLite** | Lightweight, file-based database used for development (`workout_app.db`). |
| **Security** | **JWT / Passlib / Bcrypt** | Token-based security and robust password hashing. |
| **Server** | **Uvicorn** | ASGI server for running FastAPI asynchronously. |

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1\. Prerequisites

Ensure you have **Python 3.9+** and **`pip`** installed.

### 2\. Setup the Environment

Create and activate a virtual environment to manage dependencies:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
.\venv\Scripts\activate
```

### 3\. Install Dependencies

Install all required Python packages using the provided `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4\. Configure Environment Variables

Create a file named **`.env`** in your project root and add the following configuration. **It is critical to change the `AUTH_SECRET_KEY` to a long, random, and secure string.**

```ini
# .env file

AUTH_SECRET_KEY="your-super-secret-key-change-this-for-production"
AUTH_ALGORITHM=HS256
API_URL=http://localhost:3000
```

### 5\. Run the Application

Start the FastAPI application using Uvicorn. The `--reload` flag enables live reloading during development.

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will now be running at `http://localhost:8000`.

## 🗺️ API Documentation

Once the server is running, you can view the automatic interactive API documentation:

  * **Swagger UI:** `http://localhost:8000/docs`
  * **ReDoc:** `http://localhost:8000/redoc`

## 📂 Project Structure (Core Files)

| File | Purpose |
| :--- | :--- |
| **`main.py`** | Application entry point, CORS configuration, and health check. |
| **`database.py`** | SQLAlchemy Engine and Session configuration (connects to `workout_app.db`). |
| **`models.py`** | SQLAlchemy ORM models (`User`, `Workout`, `Routine`) defining the database schema. |
| **`deps.py`** | FastAPI Dependency injection for database session and JWT authentication/user validation. |
| **`.env`** | Stores confidential configuration variables like the JWT secret. |
| **`requirements.txt`** | Lists all Python dependencies. |

## 🔑 Authentication Flow

This API uses **OAuth2** with **JWT Bearer Tokens**.

1.  **Login/Register:** A client sends user credentials to an authentication endpoint.
2.  **Token Generation:** The API validates the user, creates a JWT payload with the user ID and username, and signs it using the `AUTH_SECRET_KEY`.
3.  **Protected Endpoints:** For all protected routes (e.g., creating a workout), the client must include the token in the request header: `Authorization: Bearer <your_jwt_token>`.
4.  **Validation:** The `deps.get_current_user` dependency automatically intercepts the token, decodes it, and validates the user before allowing access to the route logic.
 
