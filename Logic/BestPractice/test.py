import requests


# r = requests.get('https://www.healthcare.gov/api/articles.json')
r = requests.get('https://www.google.com')
# r = requests.get(url)

# result = r.headers['Referer']
print(r.cookies)
