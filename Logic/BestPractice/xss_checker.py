import requests

r = requests.get('https://www.healthcare.gov/api/articles.json')

# print(r.headers)
# print(r.headers['X-XSS-Protection'])
xss_result

xss_protection = r.headers['X-XSS-Protection']
if xss_protection == '0':
    print("X-XSS-Protection is not enabled. It is recommended to enable it.")
elif xss_protection == '1':
    print("X-XSS-Protection is enabled. but it is recommended to enable it with mode block.")
elif xss_protection == '1; mode=block':
    print("X-XSS-Protection is enabled with mode block. Good Practice!")
else:
    print("No X-XSS-Protection header is set.")
