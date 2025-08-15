"""
API client for making HTTP requests.
"""

import requests
from typing import Any, Dict, Optional
from .config import Config
from .utils import setup_logging


class APIClient:
    """HTTP API client with error handling and logging."""
    
    def __init__(self, base_url: Optional[str] = None, timeout: Optional[int] = None):
        """
        Initialize the API client.
        
        Args:
            base_url: Base URL for API requests
            timeout: Request timeout in seconds
        """
        self.base_url = base_url or Config.API_BASE_URL
        self.timeout = timeout or Config.API_TIMEOUT
        self.session = requests.Session()
        self.logger = setup_logging()
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': f'{Config.APP_NAME}/{Config.APP_VERSION}',
            'Content-Type': 'application/json',
        })
    
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request.
        
        Args:
            endpoint: API endpoint
            params: Query parameters
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            self.logger.info(f"Making GET request to: {url}")
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"GET request failed: {e}")
            raise
    
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a POST request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            self.logger.info(f"Making POST request to: {url}")
            response = self.session.post(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"POST request failed: {e}")
            raise
    
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a PUT request.
        
        Args:
            endpoint: API endpoint
            data: Request data
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            self.logger.info(f"Making PUT request to: {url}")
            response = self.session.put(url, json=data, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"PUT request failed: {e}")
            raise
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """
        Make a DELETE request.
        
        Args:
            endpoint: API endpoint
            
        Returns:
            Response data
            
        Raises:
            requests.RequestException: If the request fails
        """
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        try:
            self.logger.info(f"Making DELETE request to: {url}")
            response = self.session.delete(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            self.logger.error(f"DELETE request failed: {e}")
            raise
    
    def close(self) -> None:
        """Close the session."""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()