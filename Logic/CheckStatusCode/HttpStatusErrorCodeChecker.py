import json

input = 403

# convert input to string
inputStr = str(input)
inputFirstDigit = inputStr[0]

# check status code category
if inputFirstDigit[0] == str(1):
    print("100-199: Informational Response")
elif inputFirstDigit[0] == str(2):
    print("200-299: Successful Response")
elif inputFirstDigit[0] == str(3):
    print("300-399: Redirection Response")
elif inputFirstDigit[0] == str(4):
    print("400-499: Client Error Response")
elif inputFirstDigit[0] == str(5):
    print("500-599: Server Error Response")

# Get list of HTTP Status Error Codes
with open('./Logic/CheckStatusCode/HttpStatusErrorCodes.json') as HttpSECFile:
    httpStatusErrorCodeList = json.load(HttpSECFile)

for code, meaning in httpStatusErrorCodeList.items():
    if code == inputStr:
        print(meaning)

