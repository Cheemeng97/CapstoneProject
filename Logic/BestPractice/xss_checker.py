import requests

def xssChecker(url):
    # r = requests.get('https://www.healthcare.gov/api/articles.json')
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "Error", "Error"

    xss_protection = "not found"
    xss_result = "No X-XSS-Protection found in header."
    
    if 'X-XSS-Protection' not in r.headers:
       xss_result = "No X-XSS-Protection found in header."
    else:
        xss_protection = r.headers['X-XSS-Protection']

        if xss_protection == '0':
            xss_result = "X-XSS-Protection is not enabled. It is recommended to enable it."
        elif xss_protection == '1':
            xss_result = "X-XSS-Protection is enabled. but it is recommended to enable it with mode block."
        elif xss_protection == '1; mode=block':
            xss_result = "X-XSS-Protection is enabled with mode block. Good Practice!"

    return xss_protection, xss_result
