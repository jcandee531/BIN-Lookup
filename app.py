"""
Flask Web Application for Mastercard BIN Lookup
"""

from flask import Flask, render_template, request, jsonify, flash
import os
from dotenv import load_dotenv
from bin_lookup_client import create_bin_client, BINValidator
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize BIN client (will be created when needed)
bin_client = None

def get_bin_client():
    """Get or create BIN client instance"""
    global bin_client
    if bin_client is None:
        try:
            bin_client = create_bin_client()
        except Exception as e:
            logger.error(f"Failed to create BIN client: {e}")
            raise
    return bin_client


@app.route('/')
def index():
    """Main page with BIN lookup form"""
    return render_template('index.html')


@app.route('/lookup', methods=['POST'])
def lookup_bin():
    """Handle BIN lookup requests"""
    try:
        data = request.get_json()
        bin_number = data.get('bin_number', '').strip()
        
        if not bin_number:
            return jsonify({'error': 'BIN number is required'}), 400
        
        # Validate BIN number
        if not BINValidator.is_valid_bin(bin_number):
            return jsonify({'error': 'Invalid BIN number. Must be 6-8 digits.'}), 400
        
        # Clean BIN number
        clean_bin = BINValidator.clean_bin(bin_number)
        
        # Get BIN client and perform lookup
        client = get_bin_client()
        result = client.lookup_bin(clean_bin)
        
        return jsonify({
            'success': True,
            'data': result,
            'bin_number': clean_bin
        })
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"BIN lookup error: {e}")
        return jsonify({'error': 'An error occurred during BIN lookup'}), 500


@app.route('/ranges')
def get_ranges():
    """Get account ranges with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 25, type=int)
        sort_order = request.args.get('sort', '-lowAccountRange')
        
        # Validate parameters
        if page < 1:
            page = 1
        if size < 1 or size > 100:
            size = 25
        
        client = get_bin_client()
        result = client.get_account_ranges(page=page, size=size, sort=sort_order)
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"Account ranges error: {e}")
        return jsonify({'error': 'Failed to retrieve account ranges'}), 500


@app.route('/search')
def search_bins():
    """Search BINs based on criteria"""
    try:
        issuer_name = request.args.get('issuer_name')
        country_code = request.args.get('country_code')
        product_type = request.args.get('product_type')
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 25, type=int)
        
        client = get_bin_client()
        result = client.search_bins(
            issuer_name=issuer_name,
            country_code=country_code,
            product_type=product_type,
            page=page,
            size=size
        )
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        logger.error(f"BIN search error: {e}")
        return jsonify({'error': 'Failed to search BINs'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Test if we can create a client (validates configuration)
        get_bin_client()
        return jsonify({'status': 'healthy', 'message': 'API is ready'})
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    # Check if required environment variables are set
    required_vars = [
        'MASTERCARD_CONSUMER_KEY',
        'MASTERCARD_P12_FILE_PATH',
        'MASTERCARD_KEYSTORE_PASSWORD'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
        logger.error("Please copy .env.example to .env and fill in your credentials")
        exit(1)
    
    # Run the application
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.getenv('PORT', 5000))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)