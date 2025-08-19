#!/usr/bin/env python3
"""
Setup script for Mastercard BIN Lookup application
This script helps set up the development environment
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e.stderr}")
        return False

def setup_environment():
    """Set up environment configuration"""
    print("\n⚙️ Setting up environment...")
    
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists():
        if env_example.exists():
            shutil.copy(env_example, env_file)
            print("✅ Created .env file from .env.example")
        else:
            # Create basic .env file
            env_content = """# Mastercard API Configuration
MASTERCARD_CONSUMER_KEY=your_consumer_key_here
MASTERCARD_KEYSTORE_PASSWORD=your_keystore_password_here
MASTERCARD_P12_FILE_PATH=./certs/your_certificate.p12
MASTERCARD_BASE_URL=https://sandbox.api.mastercard.com

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_SECRET_KEY=your-secret-key-here
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ Created .env file")
    else:
        print("✅ .env file already exists")
    
    # Create certs directory
    certs_dir = Path("certs")
    if not certs_dir.exists():
        certs_dir.mkdir()
        print("✅ Created certs directory")
        
        # Create placeholder for certificate
        placeholder_file = certs_dir / "README.txt"
        with open(placeholder_file, 'w') as f:
            f.write("""Place your Mastercard API P12 certificate file in this directory.

The certificate file should be obtained from:
https://developer.mastercard.com/

Update the MASTERCARD_P12_FILE_PATH in your .env file to point to your certificate.
""")
        print("✅ Created certificate placeholder")
    
    return True

def check_configuration():
    """Check if configuration is valid"""
    print("\n🔍 Checking configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        required_vars = [
            'MASTERCARD_CONSUMER_KEY',
            'MASTERCARD_KEYSTORE_PASSWORD', 
            'MASTERCARD_P12_FILE_PATH'
        ]
        
        missing_vars = []
        placeholder_vars = []
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                missing_vars.append(var)
            elif 'your_' in value.lower() or 'here' in value.lower():
                placeholder_vars.append(var)
        
        if missing_vars:
            print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
            return False
        
        if placeholder_vars:
            print(f"⚠️  Placeholder values detected in: {', '.join(placeholder_vars)}")
            print("   Please update these with your actual Mastercard API credentials")
            return False
        
        # Check if P12 file exists
        p12_file = os.getenv('MASTERCARD_P12_FILE_PATH')
        if p12_file and not os.path.exists(p12_file):
            print(f"❌ P12 certificate file not found: {p12_file}")
            return False
        
        print("✅ Configuration looks good")
        return True
        
    except ImportError:
        print("❌ python-dotenv not installed")
        return False
    except Exception as e:
        print(f"❌ Configuration check failed: {e}")
        return False

def run_tests():
    """Run basic functionality tests"""
    print("\n🧪 Running basic tests...")
    
    try:
        # Test imports
        from bin_lookup_client import BINValidator
        from mastercard_auth import MastercardAuth
        
        # Test BIN validation
        assert BINValidator.is_valid_bin("545454") == True
        assert BINValidator.is_valid_bin("12345") == False
        assert BINValidator.clean_bin("5454-5454") == "54545454"
        
        print("✅ Basic tests passed")
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except AssertionError:
        print("❌ Validation tests failed")
        return False
    except Exception as e:
        print(f"❌ Tests failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Get your Mastercard API credentials:")
    print("   - Visit https://developer.mastercard.com/")
    print("   - Create a project and add the BIN Lookup API")
    print("   - Download your P12 certificate file")
    print()
    print("2. Update your configuration:")
    print("   - Edit the .env file with your actual credentials")
    print("   - Place your P12 certificate in the certs/ directory")
    print("   - Update MASTERCARD_P12_FILE_PATH to point to your certificate")
    print()
    print("3. Test the application:")
    print("   - Run: python example_usage.py")
    print("   - Or start the web app: python app.py")
    print()
    print("4. Access the web interface:")
    print("   - Open http://localhost:5000 in your browser")

def main():
    """Main setup function"""
    print("🚀 Mastercard BIN Lookup Setup")
    print("=" * 50)
    
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies), 
        ("Setting up environment", setup_environment),
        ("Running basic tests", run_tests),
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            return 1
    
    # Optional configuration check
    print("\n" + "="*50)
    if check_configuration():
        print("\n🎉 Your application is ready to use!")
    else:
        print("\n⚠️  Application setup complete, but configuration needs attention.")
    
    print_next_steps()
    return 0

if __name__ == "__main__":
    sys.exit(main())