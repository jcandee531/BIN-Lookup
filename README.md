# Mastercard BIN Lookup Application

A comprehensive web application for performing Bank Identification Number (BIN) lookups using the Mastercard BIN Lookup API. This application provides both a beautiful web interface and a programmatic API client for retrieving detailed card information.

## 🌟 Features

- **🔍 BIN Lookup**: Look up detailed information for any BIN number (6-8 digits)
- **📋 Account Ranges**: Browse and explore available account ranges
- **🔍 Advanced Search**: Search BINs by issuer, country, or product type
- **🌐 Web Interface**: Beautiful, responsive web UI with modern design
- **🔒 Secure Authentication**: OAuth 1.0a signing with RSA-SHA256
- **⚡ Fast & Reliable**: Built with Flask and optimized for performance
- **📱 Mobile Friendly**: Fully responsive design works on all devices

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Mastercard Developer Account and API credentials
- P12 certificate file from Mastercard

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd BIN-Lookup
   ```

2. **Run the setup script**
   ```bash
   python setup.py
   ```

3. **Configure your credentials**
   - Edit the `.env` file with your Mastercard API credentials
   - Place your P12 certificate in the `certs/` directory
   - Update the certificate path in `.env`

4. **Start the application**
   ```bash
   python app.py
   ```

5. **Access the web interface**
   - Open http://localhost:5000 in your browser

## 🔧 Configuration

Create a `.env` file with your Mastercard API credentials:

```env
# Mastercard API Configuration
MASTERCARD_CONSUMER_KEY=your_consumer_key_here
MASTERCARD_KEYSTORE_PASSWORD=your_keystore_password_here
MASTERCARD_P12_FILE_PATH=./certs/your_certificate.p12
MASTERCARD_BASE_URL=https://sandbox.api.mastercard.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY=your-secret-key-here
```

## 📖 API Usage

### Basic BIN Lookup

```python
from bin_lookup_client import create_bin_client

# Create client
client = create_bin_client()

# Look up a BIN
result = client.lookup_bin("545454")
print(result)
```

### Get Account Ranges

```python
# Get account ranges with pagination
ranges = client.get_account_ranges(page=1, size=25)
print(f"Found {ranges['totalElements']} ranges")
```

### Search BINs

```python
# Search by criteria
results = client.search_bins(
    country_code="US",
    product_type="CREDIT",
    size=10
)
```

## 🌐 Web API Endpoints

- `POST /lookup` - Look up BIN information
- `GET /ranges` - Get account ranges with pagination
- `GET /search` - Search BINs by criteria
- `GET /health` - Health check endpoint

## 🏗️ Project Structure

```
BIN-Lookup/
├── app.py                 # Flask web application
├── bin_lookup_client.py   # BIN lookup API client
├── mastercard_auth.py     # OAuth 1.0a authentication
├── example_usage.py       # Usage examples
├── setup.py              # Setup script
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── 404.html
│   └── 500.html
└── certs/               # Certificate storage directory
```

## 🔐 Security Features

- **OAuth 1.0a Authentication**: Secure API authentication with RSA-SHA256 signing
- **Input Validation**: Comprehensive validation of all user inputs
- **Error Handling**: Graceful error handling with user-friendly messages
- **Rate Limiting**: Built-in protection against API rate limits
- **Secure Configuration**: Environment-based configuration management

## 🎨 Web Interface Features

- **Modern Design**: Beautiful, responsive UI with Bootstrap 5
- **Real-time Validation**: Instant feedback on input validation
- **Loading Indicators**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Mobile Responsive**: Works perfectly on all device sizes
- **Accessibility**: WCAG compliant design

## 🧪 Testing

Run the example script to test functionality:

```bash
python example_usage.py
```

## 📚 API Documentation

### BIN Lookup Client Methods

#### `lookup_bin(bin_number: str) -> Dict`
Look up information for a specific BIN number.

**Parameters:**
- `bin_number`: 6-8 digit BIN number

**Returns:**
- Dictionary containing BIN information

#### `get_account_ranges(page: int = 1, size: int = 25, sort: str = "-lowAccountRange") -> Dict`
Retrieve account ranges with pagination.

**Parameters:**
- `page`: Page number (default: 1)
- `size`: Results per page (default: 25)
- `sort`: Sort order (default: "-lowAccountRange")

#### `search_bins(**kwargs) -> Dict`
Search BINs by various criteria.

**Parameters:**
- `issuer_name`: Issuer bank name
- `country_code`: ISO country code
- `product_type`: Card product type (CREDIT, DEBIT, PREPAID)
- `page`: Page number
- `size`: Results per page

## 🛠️ Development

### Prerequisites for Development

```bash
pip install -r requirements.txt
```

### Running in Development Mode

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Getting Mastercard API Credentials

1. Visit [Mastercard Developers Portal](https://developer.mastercard.com/)
2. Create an account and log in
3. Create a new project
4. Add the BIN Lookup API to your project
5. Download your P12 certificate file
6. Note your Consumer Key and Keystore Password

### Common Issues

**"Failed to load private key"**
- Ensure your P12 file path is correct
- Verify your keystore password
- Check file permissions

**"Unauthorized: Check your API credentials"**
- Verify your Consumer Key is correct
- Ensure your P12 certificate is valid
- Check that your project has the BIN Lookup API enabled

**"No module named 'cryptography'"**
- Run `pip install -r requirements.txt`
- Ensure you're using the correct Python environment

### Need Help?

- Check the [Mastercard Developers Documentation](https://developer.mastercard.com/bin-lookup/documentation/)
- Review the example usage in `example_usage.py`
- Run the setup script: `python setup.py`

## 🎉 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- Styled with [Bootstrap 5](https://getbootstrap.com/)
- Icons by [Font Awesome](https://fontawesome.com/)
- Powered by [Mastercard Developer APIs](https://developer.mastercard.com/)
