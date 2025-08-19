"""
Mastercard BIN Lookup API Client
Provides methods to interact with Mastercard BIN Lookup APIs
"""

import requests
import json
import os
from typing import Dict, List, Optional, Union
from mastercard_auth import MastercardAuth, create_mastercard_auth


class BINLookupClient:
    """Client for Mastercard BIN Lookup API"""
    
    def __init__(self, auth: MastercardAuth, base_url: str = None):
        self.auth = auth
        self.base_url = base_url or os.getenv('MASTERCARD_BASE_URL', 'https://sandbox.api.mastercard.com')
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict:
        """Make authenticated request to Mastercard API"""
        url = f"{self.base_url}{endpoint}"
        
        # Prepare request body
        body = json.dumps(data) if data else None
        
        # Get authorization header
        auth_header = self.auth.get_authorization_header(method, url, body)
        
        # Set headers
        headers = {
            'Authorization': auth_header,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=body,
                timeout=30
            )
            
            # Handle response
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 400:
                error_data = response.json() if response.content else {}
                raise ValueError(f"Bad Request: {error_data.get('message', 'Invalid request parameters')}")
            elif response.status_code == 401:
                raise ValueError("Unauthorized: Check your API credentials")
            elif response.status_code == 403:
                raise ValueError("Forbidden: Access denied")
            elif response.status_code == 404:
                raise ValueError("Not Found: Endpoint or resource not found")
            elif response.status_code == 429:
                raise ValueError("Rate Limit Exceeded: Too many requests")
            else:
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_account_ranges(self, page: int = 1, size: int = 25, sort: str = "-lowAccountRange") -> Dict:
        """
        Retrieve account ranges information
        
        Args:
            page: Page number (default: 1)
            size: Number of results per page (default: 25)
            sort: Sort order (default: "-lowAccountRange")
        
        Returns:
            Dict containing account ranges data
        """
        params = {
            'page': page,
            'size': size,
            'sort': sort
        }
        
        return self._make_request('GET', '/bin-ranges', params=params)
    
    def lookup_bin(self, bin_number: str) -> Dict:
        """
        Lookup BIN information for a given BIN number
        
        Args:
            bin_number: Bank Identification Number (first 6-8 digits of card)
        
        Returns:
            Dict containing BIN information
        """
        # Validate BIN number
        if not bin_number or not bin_number.isdigit():
            raise ValueError("BIN number must be numeric")
        
        if len(bin_number) < 6 or len(bin_number) > 8:
            raise ValueError("BIN number must be 6-8 digits long")
        
        endpoint = f"/bin-ranges/{bin_number}"
        return self._make_request('GET', endpoint)
    
    def get_bin_details(self, account_range_low: str, account_range_high: str) -> Dict:
        """
        Get detailed information for a specific account range
        
        Args:
            account_range_low: Lower bound of account range
            account_range_high: Upper bound of account range
        
        Returns:
            Dict containing detailed BIN information
        """
        params = {
            'accountRangeLow': account_range_low,
            'accountRangeHigh': account_range_high
        }
        
        return self._make_request('GET', '/bin-ranges/details', params=params)
    
    def search_bins(self, 
                   issuer_name: str = None,
                   country_code: str = None,
                   product_type: str = None,
                   page: int = 1,
                   size: int = 25) -> Dict:
        """
        Search for BINs based on various criteria
        
        Args:
            issuer_name: Name of the issuing bank
            country_code: ISO country code
            product_type: Type of card product (e.g., CREDIT, DEBIT)
            page: Page number
            size: Number of results per page
        
        Returns:
            Dict containing search results
        """
        params = {
            'page': page,
            'size': size
        }
        
        if issuer_name:
            params['issuerName'] = issuer_name
        if country_code:
            params['countryCode'] = country_code
        if product_type:
            params['productType'] = product_type
        
        return self._make_request('GET', '/bin-ranges/search', params=params)


class BINValidator:
    """Utility class for BIN validation and formatting"""
    
    @staticmethod
    def is_valid_bin(bin_number: str) -> bool:
        """Check if BIN number is valid"""
        if not bin_number or not isinstance(bin_number, str):
            return False
        
        # Remove any non-digit characters
        clean_bin = ''.join(filter(str.isdigit, bin_number))
        
        # Check length (6-8 digits)
        return 6 <= len(clean_bin) <= 8
    
    @staticmethod
    def clean_bin(bin_number: str) -> str:
        """Clean and format BIN number"""
        if not bin_number:
            return ""
        
        # Remove any non-digit characters
        clean_bin = ''.join(filter(str.isdigit, str(bin_number)))
        
        # Take first 6-8 digits
        return clean_bin[:8] if len(clean_bin) >= 6 else clean_bin
    
    @staticmethod
    def format_card_number(card_number: str) -> str:
        """Format card number with spaces for display"""
        if not card_number:
            return ""
        
        clean_number = ''.join(filter(str.isdigit, card_number))
        
        # Format in groups of 4
        formatted = ""
        for i in range(0, len(clean_number), 4):
            if i > 0:
                formatted += " "
            formatted += clean_number[i:i+4]
        
        return formatted


def create_bin_client() -> BINLookupClient:
    """Factory function to create BINLookupClient with environment configuration"""
    auth = create_mastercard_auth()
    return BINLookupClient(auth)