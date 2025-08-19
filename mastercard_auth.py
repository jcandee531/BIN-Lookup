"""
Mastercard API Authentication Module
Handles OAuth 1.0a signing for Mastercard API requests
"""

import base64
import hashlib
import hmac
import time
import urllib.parse
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import secrets
import os


class MastercardAuth:
    """Handles Mastercard API OAuth 1.0a authentication"""
    
    def __init__(self, consumer_key, p12_file_path, keystore_password):
        self.consumer_key = consumer_key
        self.private_key = self._load_private_key(p12_file_path, keystore_password)
    
    def _load_private_key(self, p12_file_path, keystore_password):
        """Load private key from P12 certificate file"""
        try:
            with open(p12_file_path, 'rb') as f:
                p12_data = f.read()
            
            from cryptography.hazmat.primitives import serialization
            private_key, certificate, additional_certificates = serialization.pkcs12.load_key_and_certificates(
                p12_data, 
                keystore_password.encode('utf-8'),
                backend=default_backend()
            )
            return private_key
        except Exception as e:
            raise Exception(f"Failed to load private key: {str(e)}")
    
    def _generate_nonce(self):
        """Generate a random nonce for OAuth"""
        return secrets.token_hex(16)
    
    def _get_timestamp(self):
        """Get current timestamp for OAuth"""
        return str(int(time.time()))
    
    def _percent_encode(self, string):
        """Percent encode string according to OAuth spec"""
        return urllib.parse.quote(str(string), safe='')
    
    def _create_signature_base_string(self, method, url, params):
        """Create the signature base string for OAuth 1.0a"""
        # Sort parameters
        sorted_params = sorted(params.items())
        
        # Create parameter string
        param_string = '&'.join([f"{self._percent_encode(k)}={self._percent_encode(v)}" 
                                for k, v in sorted_params])
        
        # Create signature base string
        base_string = f"{method.upper()}&{self._percent_encode(url)}&{self._percent_encode(param_string)}"
        return base_string
    
    def _sign_request(self, signature_base_string):
        """Sign the request using RSA-SHA256"""
        try:
            signature = self.private_key.sign(
                signature_base_string.encode('utf-8'),
                padding.PKCS1v15(),
                hashes.SHA256()
            )
            return base64.b64encode(signature).decode('utf-8')
        except Exception as e:
            raise Exception(f"Failed to sign request: {str(e)}")
    
    def get_authorization_header(self, method, url, body=None):
        """Generate OAuth 1.0a authorization header"""
        # OAuth parameters
        oauth_params = {
            'oauth_consumer_key': self.consumer_key,
            'oauth_nonce': self._generate_nonce(),
            'oauth_signature_method': 'RSA-SHA256',
            'oauth_timestamp': self._get_timestamp(),
            'oauth_version': '1.0'
        }
        
        # Parse URL to get query parameters
        parsed_url = urllib.parse.urlparse(url)
        query_params = urllib.parse.parse_qsl(parsed_url.query)
        
        # Combine OAuth and query parameters
        all_params = oauth_params.copy()
        for key, value in query_params:
            all_params[key] = value
        
        # Add body hash for POST/PUT requests
        if body and method.upper() in ['POST', 'PUT']:
            body_hash = base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode('utf-8')
            all_params['oauth_body_hash'] = body_hash
        
        # Create signature base string
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        signature_base_string = self._create_signature_base_string(method, base_url, all_params)
        
        # Sign the request
        oauth_params['oauth_signature'] = self._sign_request(signature_base_string)
        
        # Create authorization header
        auth_header_params = []
        for key, value in oauth_params.items():
            auth_header_params.append(f'{key}="{self._percent_encode(value)}"')
        
        return f"OAuth {', '.join(auth_header_params)}"


def create_mastercard_auth():
    """Factory function to create MastercardAuth instance from environment variables"""
    consumer_key = os.getenv('MASTERCARD_CONSUMER_KEY')
    p12_file_path = os.getenv('MASTERCARD_P12_FILE_PATH')
    keystore_password = os.getenv('MASTERCARD_KEYSTORE_PASSWORD')
    
    if not all([consumer_key, p12_file_path, keystore_password]):
        raise ValueError("Missing required Mastercard API credentials in environment variables")
    
    return MastercardAuth(consumer_key, p12_file_path, keystore_password)