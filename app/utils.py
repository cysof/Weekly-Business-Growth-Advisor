# import logging
# import time
# import json
# from typing import Dict, Any, Optional, Union, List, Callable
# from datetime import datetime, timedelta
# import hashlib
# import asyncio
# import requests
# from fastapi import HTTPException, status
# from jose import jwt
# from passlib.context import CryptContext
# from app.config import settings

# # Set up logging
# logger = logging.getLogger(__name__)

# # Password hashing
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# # ---- Authentication Utilities ----

# def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
#     """Generate a JWT access token."""
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
#     return encoded_jwt

# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     """Verify a password against a hash."""
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password: str) -> str:
#     """Generate password hash."""
#     return pwd_context.hash(password)

# # ---- Rate Limiting ----

# class RateLimiter:
#     """Simple in-memory rate limiter."""
    
#     def __init__(self, requests: int = 100, window: int = 60):
#         self.requests = requests
#         self.window = window
#         self.clients: Dict[str, List[float]] = {}
    
#     async def __call__(self, client_id: str = "default") -> None:
#         """Check if client exceeds rate limit."""
#         current_time = time.time()
        
#         # Initialize client if not exists
#         if client_id not in self.clients:
#             self.clients[client_id] = []
        
#         # Remove timestamps outside the window
#         self.clients[client_id] = [
#             timestamp for timestamp in self.clients[client_id]
#             if current_time - timestamp < self.window
#         ]
        
#         # Check rate limit
#         if len(self.clients[client_id]) >= self.requests:
#             raise HTTPException(
#                 status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#                 detail=f"Rate limit exceeded: {self.requests} requests per {self.window} seconds"
#             )
        
#         # Add current timestamp
#         self.clients[client_id].append(current_time)

# # ---- HTTP Helpers ----

# def make_api_request(
#     url: str,
#     method: str = "GET",
#     params: Optional[Dict[str, Any]] = None,
#     headers: Optional[Dict[str, str]] = None,
#     json_data: Optional[Dict[str, Any]] = None,
#     max_retries: int = 3,
#     retry_delay: int = 1,
#     timeout: int = 10
# ) -> Dict[str, Any]:
#     """Make HTTP request with retry logic."""
#     method = method.upper()
    
#     if headers is None:
#         headers = {}
    
#     for attempt in range(max_retries):
#         try:
#             response = requests.request(
#                 method=method,
#                 url=url,
#                 params=params,
#                 headers=headers,
#                 json=json_data,
#                 timeout=timeout
#             )
#             response.raise_for_status()
#             return response.json()
            
#         except requests.exceptions.RequestException as e:
#             if attempt < max_retries - 1:
#                 wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
#                 logger.warning(f"API request attempt {attempt + 1} failed: {str(e)}. Retrying in {wait_time}s...")
#                 time.sleep(wait_time)
#             else:
#                 logger.error(f"API request failed after {max_retries} attempts: {str(e)}")
#                 raise HTTPException(
#                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                     detail="External API service unavailable"
#                 )

# # ---- Data Processing ----

# def calculate_percentage_change(current: float, previous: float) -> float:
#     """Calculate percentage change between two values."""
#     if previous == 0:
#         return 100.0 if current > 0 else 0.0
    
#     return ((current - previous) / previous) * 100.0

# def format_currency(amount: float, currency: str = "NGN") -> str:
#     """Format currency value."""
#     if currency == "NGN":
#         return f"₦{amount:,.2f}"
#     return f"{amount:,.2f} {currency}"

# # ---- Caching Utilities ----

# class SimpleCache:
#     """Simple in-memory cache with TTL."""
    
#     def __init__(self, ttl: int = 3600):
#         self.cache: Dict[str, Dict[str, Any]] = {}
#         self.ttl = ttl
    
#     def _generate_key(self, fn_name: str, args: tuple, kwargs: Dict[str, Any]) -> str:
#         """Generate a cache key based on function name and arguments."""
#         key_parts = [fn_name]
#         if args:
#             key_parts.append(str(args))
#         if kwargs:
#             key_parts.append(str(sorted(kwargs.items())))
        
#         key = hashlib.md5(json.dumps(key_parts).encode()).hexdigest()
#         return key
    
#     def cache_result(self, ttl: Optional[int] = None):
#         """Decorator to cache function results."""
#         def decorator(func: Callable):
#             def wrapper(*args, **kwargs):
#                 key = self._generate_key(func.__name__, args, kwargs)
                
#                 # Check if cached and not expired
#                 if key in self.cache:
#                     entry = self.cache[key]
#                     if time.time() - entry['timestamp'] < (ttl or self.ttl):
#                         logger.debug(f"Cache hit for {func.__name__}")
#                         return entry['data']
                
#                 # Call function and cache result
#                 result = func(*args, **kwargs)
#                 self.cache[key] = {
#                     'data': result,
#                     'timestamp': time.time()
#                 }
#                 logger.debug(f"Cache miss for {func.__name__}, stored result")
#                 return result
            
#             return wrapper
#         return decorator

# # Initialize global cache
# cache = SimpleCache()