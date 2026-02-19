# User Service API - FastAPI Microservice

A production-ready FastAPI microservice for user authentication and management with JWT token-based security.

## Features

✅ **Authentication**
- POST `/login` - User authentication with JWT token generation
- Secure password hashing with bcrypt
- JWT token validation with expiration

✅ **Token Management**
- GET `/verify` - Validate and verify JWT tokens
- Automatic token expiration (30 minutes)
- Token payload inspection

✅ **User Management**
- GET `/users` - Retrieve all users (JWT protected)
- User data stored in SQLite database
- Sample user pre-populated on first run

✅ **Public Endpoints**
- GET `/health` - Health check (no authentication required)
- GET `/` - API information and endpoint listing

✅ **Security**
- bcrypt password hashing
- JWT token-based authentication
- Authorization header validation
- Secure token payload encoding

## Architecture

```
user-service/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── data/
│   └── users.db        # SQLite database (auto-created)
└── README.md           # This file
```

## Installation

### Prerequisites
- Python 3.9+
- pip package manager

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the service:**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Health Check (Public)
```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "User Service",
  "version": "1.0.0",
  "timestamp": "2026-02-19T11:30:00.000000"
}
```

### Login (Public)
```bash
POST /login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

### Verify Token (Public)
```bash
GET /verify?token=<jwt_token>
```

**Response:**
```json
{
  "valid": true,
  "username": "testuser",
  "exp": 1708346400
}
```

### Get Users (Protected - Requires JWT)
```bash
GET /users
Authorization: Bearer <jwt_token>
```

**Response:**
```json
{
  "users": [
    {
      "id": 1,
      "username": "testuser",
      "email": "testuser@example.com"
    }
  ],
  "count": 1
}
```

## Usage Examples

### Using cURL

**1. Health Check:**
```bash
curl -X GET http://localhost:8000/health
```

**2. Login:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```

**3. Save token and verify:**
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq -r '.access_token')

echo "Token: $TOKEN"

curl -X GET "http://localhost:8000/verify?token=${TOKEN}"
```

**4. Get users (with JWT authentication):**
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}' | jq -r '.access_token')

curl -X GET http://localhost:8000/users \
  -H "Authorization: Bearer ${TOKEN}"
```

### Using Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Login
login_response = requests.post(
    f"{BASE_URL}/login",
    json={"username": "testuser", "password": "password123"}
)
token = login_response.json()["access_token"]
print("Token:", token)

# Verify token
verify_response = requests.get(
    f"{BASE_URL}/verify",
    params={"token": token}
)
print("Verification:", verify_response.json())

# Get users
headers = {"Authorization": f"Bearer {token}"}
users_response = requests.get(f"{BASE_URL}/users", headers=headers)
print("Users:", users_response.json())
```

## Default Credentials

A sample user is automatically created on first run:

- **Username:** `testuser`
- **Password:** `password123`
- **Email:** `testuser@example.com`

## Environment Variables

You can customize the service with environment variables:

```bash
# Secret key for JWT encoding (change in production!)
export SECRET_KEY="your-secret-key-change-in-production"

# Database path
export DB_PATH="./data/users.db"

# Run the service
python main.py
```

## Database

The service uses SQLite for data storage. The database is automatically created in `./data/users.db` on first run.

### Users Table Schema
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## Interactive API Documentation

Once the service is running, access the interactive API documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## Security Features

✅ **Password Security**
- Passwords are hashed using bcrypt
- Never stored in plaintext
- Automatic salt generation

✅ **Token Security**
- JWT tokens with HS256 algorithm
- Automatic token expiration (30 minutes)
- Token signature validation

✅ **Request Validation**
- Pydantic models for input validation
- Type checking and serialization
- Automatic error responses

✅ **Error Handling**
- Detailed error messages for debugging
- Proper HTTP status codes
- Timestamp tracking for errors

## Logging

The application provides detailed logging:

```bash
# Run with debug logging
uvicorn main:app --host 0.0.0.0 --port 8000 --log-level debug
```

## Building with Docker

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV DB_PATH=/app/data/users.db
VOLUME ["/app/data"]

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run
```bash
docker build -t user-service .
docker run -p 8000:8000 -v $(pwd)/data:/app/data user-service
```

## Kubernetes Deployment

See the Kong gateway setup in the main README for instructions on deploying this service to Kubernetes using Kong API Gateway.

## Development

### Testing with pytest

Create `test_main.py`:
```python
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_login():
    response = client.post("/login", json={
        "username": "testuser",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_unauthorized_login():
    response = client.post("/login", json={
        "username": "testuser",
        "password": "wrong_password"
    })
    assert response.status_code == 401
```

Run tests:
```bash
pip install pytest
pytest test_main.py -v
```

## Troubleshooting

**Port already in use:**
```bash
# Use a different port
uvicorn main:app --port 8001
```

**Database lock error:**
```bash
# Remove the database file and restart
rm -rf data/
python main.py
```

**Import errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Production Deployment

For production deployments:

1. **Set a strong SECRET_KEY:**
```bash
export SECRET_KEY="your-extremely-secret-key-here"
```

2. **Use a production ASGI server:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

3. **Enable HTTPS/TLS**
4. **Store secrets securely** (use environment variables or secret management systems)
5. **Use an external database** (PostgreSQL recommended)
6. **Enable logging and monitoring**
7. **Implement rate limiting**
8. **Add health monitoring and alerting**

## License

MIT

## Support

For issues or questions, refer to the main project README.
