import requests

def docTypeChecker(url):
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        return "Error", "Error"

    content_type_result = "No content-type found in header."
    content_type = r.headers['content-type'] 

    if content_type != 'application/json':
        content_type_result = "Use JSON as content type for API response are recommended"
    else:
        content_type_result = "JSON is used as content type for API response. Good Practice!"

    return content_type, content_type_result




