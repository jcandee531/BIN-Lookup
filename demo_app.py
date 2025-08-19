"""
Demo Flask Web Application for Mastercard BIN Lookup
This version provides mock data for demonstration purposes
"""

from flask import Flask, render_template, request, jsonify
import json
import time
import random

app = Flask(__name__)
app.secret_key = 'demo-secret-key'

# Mock BIN data for demonstration
MOCK_BIN_DATA = {
    "545454": {
        "issuerName": "Chase Bank",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "MASTERCARD",
        "lowAccountRange": "5454540000000000",
        "highAccountRange": "5454549999999999",
        "issuerCountry": "United States",
        "productSubType": "STANDARD"
    },
    "515555": {
        "issuerName": "Citibank",
        "countryCode": "US", 
        "productType": "CREDIT",
        "cardType": "MASTERCARD",
        "lowAccountRange": "5155550000000000",
        "highAccountRange": "5155559999999999",
        "issuerCountry": "United States",
        "productSubType": "WORLD"
    },
    "555555": {
        "issuerName": "Bank of America",
        "countryCode": "US",
        "productType": "CREDIT", 
        "cardType": "MASTERCARD",
        "lowAccountRange": "5555550000000000",
        "highAccountRange": "5555559999999999",
        "issuerCountry": "United States",
        "productSubType": "PLATINUM"
    },
    "424242": {
        "issuerName": "HSBC Bank",
        "countryCode": "GB",
        "productType": "DEBIT",
        "cardType": "VISA",
        "lowAccountRange": "4242420000000000", 
        "highAccountRange": "4242429999999999",
        "issuerCountry": "United Kingdom",
        "productSubType": "CLASSIC"
    },
    "411111": {
        "issuerName": "Wells Fargo",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "VISA",
        "lowAccountRange": "4111110000000000",
        "highAccountRange": "4111119999999999", 
        "issuerCountry": "United States",
        "productSubType": "SIGNATURE"
    },
    "378282": {
        "issuerName": "American Express",
        "countryCode": "US",
        "productType": "CREDIT",
        "cardType": "AMERICAN EXPRESS",
        "lowAccountRange": "378282000000000",
        "highAccountRange": "378282999999999",
        "issuerCountry": "United States",
        "productSubType": "GOLD"
    }
}

# Mock account ranges data
MOCK_ACCOUNT_RANGES = [
    {
        "lowAccountRange": "5454540000000000",
        "highAccountRange": "5454549999999999", 
        "issuerName": "Chase Bank",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5155550000000000",
        "highAccountRange": "5155559999999999",
        "issuerName": "Citibank", 
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5555550000000000",
        "highAccountRange": "5555559999999999",
        "issuerName": "Bank of America",
        "countryCode": "US", 
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "4242420000000000",
        "highAccountRange": "4242429999999999",
        "issuerName": "HSBC Bank",
        "countryCode": "GB",
        "productType": "DEBIT"
    },
    {
        "lowAccountRange": "4111110000000000", 
        "highAccountRange": "4111119999999999",
        "issuerName": "Wells Fargo",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "378282000000000",
        "highAccountRange": "378282999999999",
        "issuerName": "American Express",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "6011000000000000",
        "highAccountRange": "6011999999999999", 
        "issuerName": "Discover Bank",
        "countryCode": "US",
        "productType": "CREDIT"
    },
    {
        "lowAccountRange": "5432100000000000",
        "highAccountRange": "5432109999999999",
        "issuerName": "Capital One",
        "countryCode": "US",
        "productType": "CREDIT"
    }
]


@app.route('/')
def index():
    """Main page with BIN lookup form"""
    return render_template('index.html')


@app.route('/lookup', methods=['POST'])
def lookup_bin():
    """Handle BIN lookup requests with mock data"""
    try:
        # Add artificial delay to simulate API call
        time.sleep(random.uniform(0.5, 1.5))
        
        data = request.get_json()
        bin_number = data.get('bin_number', '').strip()
        
        if not bin_number:
            return jsonify({'error': 'BIN number is required'}), 400
        
        # Validate BIN number
        if not bin_number.isdigit() or len(bin_number) < 6 or len(bin_number) > 8:
            return jsonify({'error': 'Invalid BIN number. Must be 6-8 digits.'}), 400
        
        # Clean BIN number (take first 6 digits for lookup)
        clean_bin = bin_number[:6]
        
        # Check if we have mock data for this BIN
        if clean_bin in MOCK_BIN_DATA:
            result = MOCK_BIN_DATA[clean_bin].copy()
        else:
            # Generate mock data for unknown BINs
            result = {
                "issuerName": f"Demo Bank {clean_bin[:3]}",
                "countryCode": random.choice(["US", "GB", "CA", "DE", "FR"]),
                "productType": random.choice(["CREDIT", "DEBIT", "PREPAID"]),
                "cardType": random.choice(["MASTERCARD", "VISA"]),
                "lowAccountRange": f"{clean_bin}{'0' * (16 - len(clean_bin))}",
                "highAccountRange": f"{clean_bin}{'9' * (16 - len(clean_bin))}",
                "issuerCountry": "Demo Country",
                "productSubType": "STANDARD"
            }
        
        return jsonify({
            'success': True,
            'data': result,
            'bin_number': clean_bin,
            'demo_mode': True,
            'message': 'This is demo data for demonstration purposes'
        })
        
    except Exception as e:
        return jsonify({'error': f'An error occurred during BIN lookup: {str(e)}'}), 500


@app.route('/ranges')
def get_ranges():
    """Get account ranges with pagination - mock data"""
    try:
        # Add artificial delay
        time.sleep(random.uniform(0.3, 0.8))
        
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 25, type=int)
        sort_order = request.args.get('sort', '-lowAccountRange')
        
        # Validate parameters
        if page < 1:
            page = 1
        if size < 1 or size > 100:
            size = 25
        
        # Calculate pagination
        total_elements = len(MOCK_ACCOUNT_RANGES)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        
        content = MOCK_ACCOUNT_RANGES[start_idx:end_idx]
        
        result = {
            'content': content,
            'totalElements': total_elements,
            'totalPages': (total_elements + size - 1) // size,
            'number': page - 1,  # 0-based page number
            'numberOfElements': len(content),
            'first': page == 1,
            'last': end_idx >= total_elements,
            'demo_mode': True
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to retrieve account ranges: {str(e)}'}), 500


@app.route('/search')
def search_bins():
    """Search BINs based on criteria - mock data"""
    try:
        # Add artificial delay
        time.sleep(random.uniform(0.4, 1.0))
        
        issuer_name = request.args.get('issuer_name', '').lower()
        country_code = request.args.get('country_code', '').upper()
        product_type = request.args.get('product_type', '').upper()
        page = request.args.get('page', 1, type=int)
        size = request.args.get('size', 25, type=int)
        
        # Filter mock data based on criteria
        filtered_ranges = []
        
        for range_data in MOCK_ACCOUNT_RANGES:
            match = True
            
            if issuer_name and issuer_name not in range_data.get('issuerName', '').lower():
                match = False
            
            if country_code and country_code != range_data.get('countryCode', ''):
                match = False
                
            if product_type and product_type != range_data.get('productType', ''):
                match = False
            
            if match:
                filtered_ranges.append(range_data)
        
        # Calculate pagination
        total_elements = len(filtered_ranges)
        start_idx = (page - 1) * size
        end_idx = start_idx + size
        
        content = filtered_ranges[start_idx:end_idx]
        
        result = {
            'content': content,
            'totalElements': total_elements,
            'totalPages': (total_elements + size - 1) // size if total_elements > 0 else 0,
            'number': page - 1,
            'numberOfElements': len(content),
            'first': page == 1,
            'last': end_idx >= total_elements,
            'demo_mode': True
        }
        
        return jsonify({
            'success': True,
            'data': result
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to search BINs: {str(e)}'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'message': 'Demo API is ready',
        'demo_mode': True,
        'available_sample_bins': list(MOCK_BIN_DATA.keys())
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    print("🚀 Starting Mastercard BIN Lookup Demo Application")
    print("=" * 60)
    print("📡 Demo Mode: Using mock data for demonstration")
    print("🔍 Available sample BINs:")
    for bin_num, data in MOCK_BIN_DATA.items():
        print(f"   {bin_num} - {data['issuerName']} ({data['countryCode']})")
    print()
    print("🌐 Open your browser and go to: http://localhost:5000")
    print("=" * 60)
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)