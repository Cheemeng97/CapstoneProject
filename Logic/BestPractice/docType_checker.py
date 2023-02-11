import requests

r = requests.get('https://www.healthcare.gov/api/articles.json')

# print(r.headers)
print(r.headers['content-type'])

contect_type = r.headers['content-type'] 
if contect_type != 'application/json':
    print("Use JSON as content type for API response are recommended")
else:
    print("JSON is used as content type for API response. Good Practice!")


