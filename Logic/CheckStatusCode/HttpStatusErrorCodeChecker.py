import json

input = 403

def httpStatusErrorCodeChecker(input):

    range_result = ""
    statusCode_result = ""

    # convert input to string
    inputStr = str(input)
    inputFirstDigit = inputStr[0]

    # check status code category
    if inputFirstDigit[0] == str(1):
        range_result = "100-199: Informational Response"
    elif inputFirstDigit[0] == str(2):
        range_result = "200-299: Successful Response"
    elif inputFirstDigit[0] == str(3):
        range_result = "300-399: Redirection Response"
    elif inputFirstDigit[0] == str(4):
        range_result = "400-499: Client Error Response"
    elif inputFirstDigit[0] == str(5):
        range_result = "500-599: Server Error Response"

    # Get list of HTTP Status Error Codes
    with open('./Logic/CheckStatusCode/HttpStatusErrorCodes.json') as HttpSECFile:
        httpStatusErrorCodeList = json.load(HttpSECFile)

    for code, meaning in httpStatusErrorCodeList.items():
        if code == inputStr:
            statusCode_result = meaning

    return range_result, statusCode_result

