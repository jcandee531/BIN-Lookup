#!/usr/bin/env python3
"""
Example usage of Mastercard BIN Lookup API Client
This script demonstrates how to use the BIN lookup functionality
"""

import os
import sys
from dotenv import load_dotenv
from bin_lookup_client import create_bin_client, BINValidator

# Load environment variables
load_dotenv()

def main():
    """Main example function"""
    print("🔍 Mastercard BIN Lookup API Example")
    print("=" * 50)
    
    try:
        # Create BIN client
        print("📡 Initializing BIN lookup client...")
        client = create_bin_client()
        print("✅ Client initialized successfully!")
        
        # Example 1: Basic BIN lookup
        print("\n🔍 Example 1: Basic BIN Lookup")
        print("-" * 30)
        
        test_bins = ["545454", "515555", "555555"]
        
        for bin_number in test_bins:
            print(f"\n🔍 Looking up BIN: {bin_number}")
            
            # Validate BIN first
            if not BINValidator.is_valid_bin(bin_number):
                print(f"❌ Invalid BIN: {bin_number}")
                continue
            
            try:
                result = client.lookup_bin(bin_number)
                print(f"✅ BIN Lookup Result:")
                
                # Display key information
                if result:
                    for key, value in result.items():
                        if value:
                            print(f"   {key}: {value}")
                else:
                    print("   No data found for this BIN")
                    
            except ValueError as e:
                print(f"❌ Lookup failed: {e}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Example 2: Get account ranges
        print("\n\n📋 Example 2: Account Ranges")
        print("-" * 30)
        
        try:
            print("📡 Fetching account ranges...")
            ranges = client.get_account_ranges(page=1, size=5)
            
            if ranges and 'content' in ranges:
                print(f"✅ Found {len(ranges['content'])} account ranges:")
                
                for i, range_data in enumerate(ranges['content'][:3], 1):  # Show first 3
                    print(f"\n   Range {i}:")
                    print(f"     Low Range: {range_data.get('lowAccountRange', 'N/A')}")
                    print(f"     High Range: {range_data.get('highAccountRange', 'N/A')}")
                    print(f"     Issuer: {range_data.get('issuerName', 'N/A')}")
                    print(f"     Country: {range_data.get('countryCode', 'N/A')}")
                    print(f"     Product Type: {range_data.get('productType', 'N/A')}")
            else:
                print("   No account ranges found")
                
        except Exception as e:
            print(f"❌ Failed to fetch account ranges: {e}")
        
        # Example 3: Search BINs
        print("\n\n🔍 Example 3: Search BINs")
        print("-" * 30)
        
        search_criteria = [
            {"country_code": "US", "description": "US-based cards"},
            {"product_type": "CREDIT", "description": "Credit cards"},
        ]
        
        for criteria in search_criteria:
            description = criteria.pop('description')
            print(f"\n🔍 Searching for {description}...")
            
            try:
                results = client.search_bins(**criteria, size=3)
                
                if results and 'content' in results:
                    print(f"✅ Found {results.get('totalElements', 0)} results (showing first 3):")
                    
                    for i, result in enumerate(results['content'][:3], 1):
                        print(f"\n   Result {i}:")
                        print(f"     Issuer: {result.get('issuerName', 'N/A')}")
                        print(f"     Range: {result.get('lowAccountRange', 'N/A')} - {result.get('highAccountRange', 'N/A')}")
                        print(f"     Country: {result.get('countryCode', 'N/A')}")
                        print(f"     Type: {result.get('productType', 'N/A')}")
                else:
                    print("   No results found")
                    
            except Exception as e:
                print(f"❌ Search failed: {e}")
        
        # Example 4: BIN validation utilities
        print("\n\n✅ Example 4: BIN Validation")
        print("-" * 30)
        
        test_inputs = ["545454", "12345", "abcdef", "5454541234", ""]
        
        for test_input in test_inputs:
            is_valid = BINValidator.is_valid_bin(test_input)
            cleaned = BINValidator.clean_bin(test_input)
            
            print(f"Input: '{test_input}' -> Valid: {is_valid}, Cleaned: '{cleaned}'")
        
        print("\n🎉 Examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        print("\n💡 Make sure you have:")
        print("   1. Created a .env file with your Mastercard API credentials")
        print("   2. Placed your P12 certificate file in the correct location")
        print("   3. Installed all required dependencies: pip install -r requirements.txt")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())