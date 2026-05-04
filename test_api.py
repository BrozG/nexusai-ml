"""
Test script for NexusAI API
Tests all endpoints with example requests
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
USER_API_KEY = "sk_ecommerce_amazon_abc123"
ADMIN_API_KEY = "sk_admin_master_xyz999"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_health():
    """Test health endpoint (no auth)"""
    print_section("Testing /api/health")
    
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    
    return response.status_code == 200

def test_chat():
    """Test chat endpoint"""
    print_section("Testing /api/chat")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": USER_API_KEY
    }
    
    payload = {
        "query": "What is your refund policy?",
        "top_k": 3,
        "max_tokens": 150,
        "temperature": 0.7
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    print("\nSending request...")
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        headers=headers,
        json=payload
    )
    
    print(f"\nStatus: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nQuery: {data['query']}")
        print(f"Domain: {data['domain']}")
        print(f"Company: {data['company']}")
        print(f"Sentiment: {data['sentiment']} (confidence: {data['sentiment_confidence']:.3f})")
        print(f"Response time: {data['response_time_ms']:.2f}ms")
        print(f"\nResponse: {data['response'][:200]}...")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_upload_file():
    """Test file upload endpoint (now available to all API keys)"""
    print_section("Testing /admin/upload-file")
    
    headers = {
        "X-API-Key": USER_API_KEY  # Changed from ADMIN_API_KEY
    }
    
    # Create a test text file
    test_content = b"This is a test document about refund policies. Customers can return items within 30 days."
    
    files = {
        'file': ('test_policy.txt', test_content, 'text/plain')
    }
    
    print("Uploading test file with user API key...")
    
    response = requests.post(
        f"{BASE_URL}/admin/upload-file",
        headers=headers,
        files=files
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nDomain: {data['domain']}")
        print(f"Company: {data['company']}")
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_add_url():
    """Test add URL endpoint (now available to all API keys)"""
    print_section("Testing /admin/add-url")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": USER_API_KEY  # Changed from ADMIN_API_KEY
    }
    
    payload = {
        "url": "https://example.com"
    }
    
    print(f"Request: {json.dumps(payload, indent=2)}")
    print("\nSending request with user API key...")
    
    response = requests.post(
        f"{BASE_URL}/admin/add-url",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nDomain: {data['domain']}")
        print(f"Company: {data['company']}")
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_logs():
    """Test logs endpoint"""
    print_section("Testing /admin/logs")
    
    headers = {
        "X-API-Key": ADMIN_API_KEY
    }
    
    response = requests.get(
        f"{BASE_URL}/admin/logs?lines=10",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nShowing last {data['count']} of {data['total_lines']} lines:\n")
        for line in data['lines']:
            print(f"  {line}")
    else:
        print(f"Error: {response.text}")
    
    return response.status_code == 200

def test_invalid_key():
    """Test with invalid API key (should fail)"""
    print_section("Testing Invalid API Key")
    
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": "invalid-key-12345"
    }
    
    payload = {
        "query": "Test query"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/chat",
        headers=headers,
        json=payload
    )
    
    print(f"Status: {response.status_code}")
    print(f"Expected: 401 (Unauthorized)")
    
    if response.status_code == 401:
        print("✓ Correctly rejected invalid API key")
        return True
    else:
        print("✗ Should have rejected invalid key")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  NexusAI API Test Suite")
    print("=" * 70)
    print(f"\nBase URL: {BASE_URL}")
    print(f"User API Key: {USER_API_KEY}")
    print(f"Admin API Key: {ADMIN_API_KEY}")
    
    # Check if server is running
    print("\nChecking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Server is running (status: {response.status_code})")
    except requests.ConnectionError:
        print("✗ Server is not running!")
        print("Start the server with: python main.py")
        return
    
    # Run tests
    results = {}
    
    # Give server time to fully initialize
    print("\nWaiting 2 seconds for server initialization...")
    time.sleep(2)
    
    results['health'] = test_health()
    results['invalid_key'] = test_invalid_key()
    results['logs'] = test_logs()
    
    # Optional: Comment out if you don't have vector stores ready
    # results['chat'] = test_chat()
    # results['upload'] = test_upload_file()
    # results['add_url'] = test_add_url()
    
    # Summary
    print_section("Test Summary")
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
