## How to start
1. Run the command below in CLI to install required libraries
```
pip install -r requirements.txt
```
2. Run **app.py** 
3. Copy the url that is showing in the terminal and paste in browser. E.g. http://127.0.0.1:4949

## Functionality
You can see there are two box in the main page. Left one is for user to enter the url. Right one is to upload a file(currently not working).

### Analyse From URL
Below are the example URLs that I am using.

```
https://www.healthcare.gov/api/articles.json  # valid SSL with headers 
https://test-ev-rsa.ssl.com   #valid SSL
https://expired-rsa-dv.ssl.com   #expired SSL
```

There are currently two available tabs once user submit successfully. There are the TSL/SSL Certificate and API Endpoint Analysis.