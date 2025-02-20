# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from jose import jwt, JWTError
# from typing import Optional, Dict, Any
# import time
# from pydantic import BaseModel
# from app.config import settings

# # OAuth2 scheme for token authentication
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# # User model
# class User(BaseModel):
#     username: str
#     email: Optional[str] = None
#     full_name: Optional[str] = None
#     disabled: Optional[bool] = None

# # Token payload model
# class TokenData(BaseModel):
#     username: Optional[str] = None

# # Simple user database for demonstration
# # In production, replace with actual database queries
# USERS_DB = {
#     "johndoe": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
#         "disabled": False,
#     }
# }

# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     """
#     Validate access token and return current user.
    
#     Args:
#         token: JWT token from Authorization header
        
#     Returns:
#         User object if token is valid
        
#     Raises:
#         HTTPException: If token is invalid or user not found
#     """
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
    
#     try:
#         # Decode JWT token
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
    
#     # Get user from database
#     user_dict = USERS_DB.get(token_data.username)
#     if user_dict is None:
#         raise credentials_exception
    
#     return User(**user_dict)

# class RateLimiter:
#     """
#     Rate limiter implementation to prevent API abuse.
    
#     Limits requests based on client IP or user ID within a specified time window.
#     """
    
#     def __init__(self, requests: int = 100, window: int = 60):
#         """
#         Initialize rate limiter.
        
#         Args:
#             requests: Maximum number of requests allowed in the window
#             window: Time window in seconds
#         """
#         self.requests = requests
#         self.window = window
#         self.clients: Dict[str, list] = {}
    
#     async def __call__(self, client_id: str = "default") -> None:
#         """
#         Check if client exceeds rate limit.
        
#         Args:
#             client_id: Unique identifier for the client (IP or user ID)
            
#         Raises:
#             HTTPException: If rate limit is exceeded
#         """
#         current_time = time.time()
        
#         # Initialize client record if not exists
#         if client_id not in self.clients:
#             self.clients[client_id] = []
        
#         # Filter out timestamps outside current window
#         self.clients[client_id] = [
#             timestamp for timestamp in self.clients[client_id]
#             if current_time - timestamp < self.window
#         ]
        
#         # Check if rate limit exceeded
#         if len(self.clients[client_id]) >= self.requests:
#             raise HTTPException(
#                 status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#                 detail=f"Rate limit exceeded: {self.requests} requests per {self.window} seconds"
#             )
        
#         # Add current request timestamp
#         self.clients[client_id].append(current_time)