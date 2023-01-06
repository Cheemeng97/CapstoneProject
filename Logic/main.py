import requests
from CheckStatusCode.HttpStatusErrorCodeChecker import httpStatusErrorCodeChecker

# 503 - https://mockyard.herokuapp.com/products

response = requests.get("https://mockyard.herokuapp.com/products")
# print(response.status_code)

HttpStatusErrorCodeChecker_range_result, HttpStatusErrorCodeChecker_code_result = httpStatusErrorCodeChecker(response.status_code)
print(HttpStatusErrorCodeChecker_range_result)
print(HttpStatusErrorCodeChecker_code_result)