#!/usr/bin/env python3
import requests

# Test URL analysis
response = requests.post('http://localhost:5000/analyze/url', data={'url': 'https://example.com'})
print(f"Status: {response.status_code}")
print("Response received (showing first 200 chars):")
print(response.text[:200])
