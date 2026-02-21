"""
FastAPI User Service Microservice
Provides authentication, user management, and JWT token validation
"""

from fastapi import FastAPI, HTTPException, Depends, status, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timedelta
from typing import Optional
import jwt
import sqlite3
import bcrypt
import os
from pathlib import Path

# ==================== Configuration ====================
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_PATH = os.getenv("DB_PATH", "./data/users.db")

# ==================== Pydantic Models ====================
class LoginRequest(BaseModel):
    """User login request model"""
    username: str = Field(..., min_length=1, description="Username")
    password: str = Field(..., min_length=1, description="Password")


class LoginResponse(BaseModel):
    """Login response with JWT token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class VerifyTokenRequest(BaseModel):
    """Token verification request"""
    token: str = Field(..., description="JWT token to verify")


class VerifyTokenResponse(BaseModel):
    """Token verification response"""
    valid: bool
    username: Optional[str] = None
    exp: Optional[int] = None


class UserResponse(BaseModel):
    """User response model"""
    id: int
    username: str
    email: str


class UserListResponse(BaseModel):
    """User list response"""
    users: list[UserResponse]
    count: int


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str = "User Service"
    version: str = "1.0.0"
    timestamp: str


# ==================== Database Setup ====================
def initialize_database():
    """Initialize SQLite database with schema and sample data"""
    db_dir = Path(DB_PATH).parent
    db_dir.mkdir(parents=True, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Check if sample user exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", ("testuser",))
    user_count = cursor.fetchone()[0]
    
    # Insert sample user if not exists
    if user_count == 0:
        sample_password = "password123"
        password_hash = hash_password(sample_password)
        cursor.execute("""
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        """, ("testuser", "testuser@example.com", password_hash))
        print("✓ Sample user created: username='testuser', password='password123'")
    
    conn.commit()
    conn.close()


# ==================== Password Hashing ====================
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))


# ==================== JWT Token Management ====================
def create_access_token(username: str, expires_delta: Optional[timedelta] = None) -> dict:
    """Create JWT access token"""
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    expire = datetime.utcnow() + expires_delta
    payload = {
        "sub": username,
        "iss": "user-client-key",
        "exp": expire,
        "iat": datetime.utcnow()
    }
    
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "expires_in": int(expires_delta.total_seconds())
    }


def verify_token(token: str) -> dict:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing username"
            )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(e)}"
        )


# ==================== Database Operations ====================
def get_user_by_username(username: str) -> Optional[dict]:
    """Retrieve user from database by username"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    
    return dict(user) if user else None


def get_all_users() -> list[dict]:
    """Retrieve all users from database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, username, email FROM users")
    users = [dict(row) for row in cursor.fetchall()]
    conn.close()
    
    return users


# ==================== Dependency: Token Validation ====================
async def get_current_user(authorization: Optional[str] = Header(None)) -> str:
    """Dependency to validate JWT token from Authorization header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing"
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format"
        )
    
    token = parts[1]
    payload = verify_token(token)
    return payload.get("sub")


# ==================== FastAPI Application ====================
app = FastAPI(
    title="User Service API",
    description="Microservice for user authentication and management",
    version="1.0.0"
)


# ==================== Startup Events ====================
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    initialize_database()
    print("✓ User Service started successfully")


# ==================== Public Endpoints ====================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint - public, no authentication required"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )


@app.post("/login", response_model=LoginResponse, tags=["Authentication"])
async def login(credentials: LoginRequest):
    """
    Login endpoint - authenticate user and return JWT token
    
    Request body:
    - username: str
    - password: str
    
    Returns:
    - access_token: JWT token
    - token_type: always "bearer"
    - expires_in: token expiration in seconds
    """
    user = get_user_by_username(credentials.username)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    if not verify_password(credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    token_data = create_access_token(credentials.username)
    return LoginResponse(**token_data)


@app.get("/verify", response_model=VerifyTokenResponse, tags=["Authentication"])
async def verify(token: str):
    """
    Verify JWT token endpoint
    
    Query parameters:
    - token: JWT token to verify
    
    Returns:
    - valid: boolean indicating if token is valid
    - username: username from token (if valid)
    - exp: token expiration timestamp (if valid)
    """
    payload = verify_token(token)
    return VerifyTokenResponse(
        valid=True,
        username=payload.get("sub"),
        exp=int(payload.get("exp", 0))
    )


# ==================== Protected Endpoints ====================

@app.get("/users", response_model=UserListResponse, tags=["Users"])
async def get_users(current_user: str = Depends(get_current_user)):
    """
    Get list of all users - requires JWT authentication
    
    Headers:
    - Authorization: Bearer <token>
    
    Returns:
    - users: list of user objects
    - count: total number of users
    """
    # Token is validated via dependency
    users = get_all_users()
    return UserListResponse(
        users=users,
        count=len(users)
    )


# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Generic exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# ==================== Application Info ====================

@app.get("/", tags=["Info"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "User Service API",
        "version": "1.0.0",
        "description": "Microservice for user authentication and management",
        "endpoints": {
            "health": "/health (GET - public)",
            "login": "/login (POST - public)",
            "verify": "/verify (GET - public)",
            "users": "/users (GET - protected)",
            "docs": "/docs (Swagger UI)",
            "redoc": "/redoc (ReDoc)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
