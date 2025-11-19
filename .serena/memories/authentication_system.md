# Authentication System Documentation

## Authentication Strategy

The application implements multiple authentication strategies:
1. **Traditional Email/Password** - JWT-based authentication
2. **Google OAuth 2.0** - Social login via Google
3. **Apple Sign-In** - Social login via Apple
4. **Token Refresh** - Refresh token rotation for security

## JWT Configuration

### Token Types
- **Access Token**: Short-lived (30 minutes default)
- **Refresh Token**: Long-lived (7 days default)

### JWT Service (`src/infrastructure/services/jwt_service.py`)
```python
class JWTService:
    def create_access_token(self, user_id: str) -> str:
        """Creates short-lived access token"""
        # Expiration: 30 minutes
        # Algorithm: HS256
        
    def create_refresh_token(self, user_id: str) -> str:
        """Creates long-lived refresh token"""
        # Expiration: 7 days
        # Algorithm: HS256
        
    def verify_token(self, token: str, token_type: str) -> dict:
        """Validates and decodes JWT token"""
        # Raises InvalidTokenError if invalid/expired
```

### Configuration (Environment Variables)
```env
JWT_SECRET_KEY=your-secret-key-here  # REQUIRED
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Password Security

### Password Service (`src/infrastructure/services/password_service.py`)
```python
class PasswordService:
    def hash(self, password: str) -> str:
        """Hashes password using bcrypt"""
        # Uses Passlib with bcrypt scheme
        # Cost factor: 12 (default)
        
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies password against hash"""
        # Constant-time comparison
```

### Password Requirements
- Minimum length: 8 characters (enforced in Pydantic schema)
- No maximum length
- No complexity requirements (can be added via validator)

### Best Practices
- Never log passwords
- Use HTTPS in production
- Implement rate limiting on login endpoints
- Consider adding password strength validation

## User Registration Flow

### Endpoint: `POST /api/v1/auth/register`

**Request Schema** (`RegisterRequest`):
```json
{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "securepassword123",
  "full_name": "John Doe"  // optional
}
```

**Response Schema** (`TokenResponse`):
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

**Process Flow**:
1. Validate request data (email format, username uniqueness)
2. Hash password using PasswordService
3. Create User entity with hashed password
4. Save to database via UserRepository
5. Generate JWT access and refresh tokens
6. Return tokens to client

**Use Case**: `RegisterUserUseCase`
- Dependencies: UserRepository, PasswordService, JWTService
- Business logic: User creation + password hashing + token generation

## Login Flow

### Endpoint: `POST /api/v1/auth/login`

**Request Schema** (`LoginRequest`):
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response**: Same as registration (`TokenResponse`)

**Process Flow**:
1. Find user by email
2. Verify password using PasswordService
3. If valid, generate new access and refresh tokens
4. Return tokens

**Error Handling**:
- User not found → 401 Unauthorized
- Invalid password → 401 Unauthorized
- Inactive user → 403 Forbidden (if implemented)

**Use Case**: `LoginUserUseCase`

## Token Refresh Flow

### Endpoint: `POST /api/v1/auth/refresh`

**Request Schema** (`RefreshTokenRequest`):
```json
{
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response**: New token pair (`TokenResponse`)

**Process Flow**:
1. Verify refresh token signature and expiration
2. Extract user_id from token payload
3. Validate user still exists and is active
4. Generate new access and refresh tokens
5. Return new tokens

**Security Notes**:
- Old refresh token should be invalidated (implement token blacklist)
- Detect refresh token reuse (potential security breach)
- Consider rotating refresh tokens on each use

**Use Case**: `RefreshTokenUseCase`

## OAuth Integration

### Google OAuth Flow

**Endpoint**: `POST /api/v1/auth/oauth/google`

**Request Schema** (`OAuthLoginRequest`):
```json
{
  "id_token": "google-id-token-from-client"
}
```

**Service**: `GoogleOAuthService`
- Verifies Google ID token
- Extracts user information (email, name, sub)
- Returns verified user data

**Process Flow**:
1. Client obtains ID token from Google (frontend)
2. Send ID token to backend
3. Verify token with Google's public keys
4. Extract user information
5. Find or create user in database
6. Generate JWT tokens
7. Return tokens

**Use Case**: `OAuthLoginUseCase`

### Apple OAuth Flow

**Endpoint**: `POST /api/v1/auth/oauth/apple`

**Request Schema**: Same as Google (`OAuthLoginRequest`)

**Service**: `AppleOAuthService`
- Verifies Apple ID token
- Handles Apple-specific claims
- Returns verified user data

**Process Flow**: Similar to Google OAuth

**Apple-Specific Considerations**:
- Apple may not always provide email
- Handle email privacy relay (@privaterelay.appleid.com)
- Apple only sends user info on first login

## Authentication Middleware

### JWT Authentication Dependency

**File**: `src/core/auth_dependencies.py`

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    jwt_service: JWTService = Depends(get_jwt_service),
    user_repo: UserRepository = Depends(get_user_repository)
) -> User:
    """
    Validates JWT token and returns current user
    Used as FastAPI dependency for protected routes
    """
```

**Usage in Protected Routes**:
```python
@router.get("/me")
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

### OAuth2 Password Bearer
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
```

## Database Schema (User Model)

### Authentication-Related Fields
```python
class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(CHAR(36), primary_key=True)  # UUID
    email = Column(String(255), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    
    # Authentication fields
    password_hash = Column(String(255), nullable=True)  # Null for OAuth users
    oauth_provider = Column(String(20), nullable=True)  # "google", "apple"
    oauth_id = Column(String(255), nullable=True)  # Provider user ID
    
    # Account status
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)
```

### Migration Files
- `001_add_uuid_primary_key_to_users.py` - Initial UUID setup
- `002_add_auth_fields_to_users.py` - OAuth and authentication fields

## Security Best Practices

### Current Implementations
✅ Password hashing with bcrypt
✅ JWT token expiration
✅ Secure token generation (HS256)
✅ OAuth token verification
✅ No password in responses

### Recommended Enhancements
⚠️ Add rate limiting on auth endpoints
⚠️ Implement token blacklist for logout
⚠️ Add CSRF protection for cookies
⚠️ Implement account lockout after failed attempts
⚠️ Add email verification flow
⚠️ Use HTTPS in production
⚠️ Add password strength requirements
⚠️ Implement refresh token rotation
⚠️ Add 2FA/MFA support
⚠️ Log authentication events

## Testing Authentication

### Unit Tests
- `tests/unit/test_jwt_service.py` - JWT creation and verification
- `tests/unit/test_password_service.py` - Password hashing and verification
- `tests/unit/test_user_entity.py` - User entity validation

### Integration Tests (Recommended)
- Registration flow end-to-end
- Login flow with valid/invalid credentials
- Token refresh flow
- OAuth login flow
- Protected route access

### Example Test
```python
@pytest.mark.asyncio
async def test_login_success():
    # Arrange
    repository = MockUserRepository()
    password_service = PasswordService()
    jwt_service = JWTService(settings)
    use_case = LoginUserUseCase(repository, password_service, jwt_service)
    
    # Act
    result = await use_case.execute("test@example.com", "password123")
    
    # Assert
    assert "access_token" in result
    assert "refresh_token" in result
```

## API Documentation

### Swagger UI
- URL: http://localhost:8000/docs
- Interactive API testing
- Authorization: "Authorize" button with Bearer token

### ReDoc
- URL: http://localhost:8000/redoc
- Alternative documentation format
