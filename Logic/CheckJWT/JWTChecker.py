import requests

url = 'https://example.com/some_endpoint'

# Send HTTP request and get response
response = requests.get(url)

# Check response headers for Authorization or Bearer headers
auth_header = response.headers.get('Authorization')
bearer_header = response.headers.get('Bearer')

if auth_header or bearer_header:
    print('JWT token found in response headers')
else:
    print('No JWT token found in response headers')